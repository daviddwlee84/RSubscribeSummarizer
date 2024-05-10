from typing import Optional, Dict, Type
from types import TracebackType
import logging
import os
import sys
from functools import partial
from rich.logging import RichHandler


def handle_exception(
    logger: logging.Logger,
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[TracebackType],
    by_pass_keyboard_interrupt: bool = True,
) -> None:
    """
    This function handles uncaught exceptions and logs them.

    https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
    """
    if issubclass(exc_type, KeyboardInterrupt):
        if by_pass_keyboard_interrupt:
            # Do not capture interrupt signals sent from the keyboard or kill commands.
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            logger.warning(
                "User Keyboard Interrupt", exc_info=(exc_type, exc_value, exc_traceback)
            )
        else:
            logger.error(
                "User Keyboard Interrupt", exc_info=(exc_type, exc_value, exc_traceback)
            )
    else:
        logger.error(
            "Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback)
        )


loggers: Dict[str, logging.Logger] = {}


def get_logger(
    logger_name: Optional[str] = None,
    log_file_path: Optional[str] = None,
    stdout: bool = True,
    level: int = logging.INFO,
    use_rich: bool = True,
    by_pass_keyboard_interrupt: bool = True,
) -> logging.Logger:
    # https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
    global loggers
    if logger_name in loggers:
        return loggers[logger_name]

    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Set formatter
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s - %(message)s"
    )

    # Create stdout handler
    if stdout:
        if use_rich:
            stdout_handler = RichHandler(
                rich_tracebacks=True, tracebacks_show_locals=True
            )
            stdout_handler.setFormatter(logging.Formatter("%(name)s - %(message)s"))
            logger.addHandler(stdout_handler)
        else:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)

    # Create file handler
    if log_file_path is not None:
        log_dir = os.path.dirname(log_file_path)
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Register the exception handler with the logging system
    sys.excepthook = partial(
        handle_exception, logger, by_pass_keyboard_interrupt=by_pass_keyboard_interrupt
    )

    loggers[logger_name] = logger

    # https://stackoverflow.com/questions/67269916/how-to-avoid-root-handler-being-called-from-the-custom-logger-in-python
    # This will stop the root handler's output
    logger.propagate = False

    return logger


if __name__ == "__main__":
    # python -m utils.logger
    import os

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    logger = get_logger("logger_test", stdout=True)
    logger.info("test")
    logger.error("error test")

    logger = get_logger(log_file_path=os.path.join(curr_dir, "test.log"))
    logger.info("test")
    logger.error("error test")

    raise Exception("Should be catch in the file")
