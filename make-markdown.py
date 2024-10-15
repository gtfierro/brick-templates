from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library, Template

template_markdown_entry = """
## {name}

### Parameters
{parameters}
"""

bm = BuildingMOTIF("sqlite://")
brick = Library.load(ontology_graph="https://brickschema.org/schema/1.4/Brick.ttl")
lib = Library.load(directory="basic-building")
for templ in lib.get_templates():
    name = templ.name
    parameters = templ.parameters
    dependencies = {t.template.name for t in templ.get_dependencies()}
    print(template_markdown_entry.format(name=name, parameters=parameters))
