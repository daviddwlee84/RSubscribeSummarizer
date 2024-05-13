import re

dummy_html_video_code_re = re.compile(
    r"\[!--begin:htmlVideoCode--\].*?\[!--end:htmlVideoCode--\]", re.DOTALL
)

from markdownify import MarkdownConverter


class ModifiedMarkdownConverter(MarkdownConverter):
    def convert_td(self, el, text, convert_as_inline):
        colspan = 1
        if "colspan" in el.attrs:
            try:
                colspan = int(el["colspan"])
            except ValueError:
                colspan = 1  # Default to 1 if conversion fails
        return " " + text.strip().replace("\n", " ") + " |" * colspan

    def convert_th(self, el, text, convert_as_inline):
        colspan = 1
        if "colspan" in el.attrs:
            try:
                colspan = int(el["colspan"])
            except ValueError:
                colspan = 1  # Default to 1 if conversion fails
        return " " + text.strip().replace("\n", " ") + " |" * colspan


# BUG: sometimes might get content as a URL link
# MarkupResemblesLocatorWarning: The input looks more like a URL than markup. You may want to use an HTTP client like requests to get the document behind the URL, and feed that document to Beautiful Soup.
#  soup = BeautifulSoup(html, 'html.parser')
def markdownify(
    html: str, re_to_remove: list[re.Pattern] = [dummy_html_video_code_re], **options
) -> str:
    md = ModifiedMarkdownConverter(**options).convert(html)
    for pattern in re_to_remove:
        md = pattern.sub("", md)
    return md
