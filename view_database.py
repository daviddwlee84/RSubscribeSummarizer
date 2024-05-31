from sqlalchemy_schemadisplay import create_schema_graph
from app import engine, SQLModel

# from sqlalchemy import MetaData

# Install Graphviz first
# https://www.graphviz.org/download/

graph = create_schema_graph(engine=engine, metadata=SQLModel.metadata)
graph.write_png("database_schema.png")

from RSubscribeSummarizer.data import model
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy.orm import class_mapper

# lets find all the mappers in our model
mappers = []
for attr in dir(model):
    if attr[0] == "_":
        continue
    try:
        cls = getattr(model, attr)
        mappers.append(class_mapper(cls))
    except Exception:
        pass

# pass them to the function and set some formatting options
graph = create_uml_graph(
    mappers,
    # show_operations=False,  # not necessary in this case
    # show_multiplicity_one=False,  # some people like to see the ones, some don't
)
graph.write_png("uml_class_diagram.png")  # write out the file
