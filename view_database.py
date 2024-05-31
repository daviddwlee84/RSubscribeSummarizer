from sqlalchemy_schemadisplay import create_schema_graph
from app import engine, SQLModel

# from sqlalchemy import MetaData

# Install Graphviz first
# https://www.graphviz.org/download/

graph = create_schema_graph(engine=engine, metadata=SQLModel.metadata)
graph.write_png("database_schema.png")
