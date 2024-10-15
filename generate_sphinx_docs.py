import os
import rdflib
from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library

def build_dependencies_string(template):
    dependencies = ""
    for dep in template.get_dependencies():
        # if the template is from the brick library, link to the brick documentation
        if str(dep.template.defining_library.name) == "https://brickschema.org/schema/1.4/Brick":
            # get the qname
            ns, _, value = dep.template.body.compute_qname(dep.template.name)
            # link externally to ontology.brickschema.org/qname
            link = f"https://ontology.brickschema.org/{ns}/{value}.html"
            # generate a sphinx link to external documentation
            dependencies += f"- `{dep.template.name} <{link}>`_\n"
        else:
            dependencies += f"- :doc:`{dep.template.name}`\n"
    return dependencies

def build_graphviz(g: rdflib.Graph):
    # create a graphviz representation of the graph
    from rdflib.tools.rdf2dot import rdf2dot
    import pydot
    import io
    buf = io.StringIO()
    rdf2dot(g, buf)
    dot = pydot.graph_from_dot_data(buf.getvalue())
    # put tab before each line in dot[0]
    dot = "\n".join(f"    {line}" for line in dot[0].to_string().split("\n"))
    sphinx_string = f"""
.. graphviz::

    {dot}
    """
    return sphinx_string

# Initialize BuildingMOTIF
bm = BuildingMOTIF("sqlite://")

brick = Library.load(ontology_graph="https://brickschema.org/schema/1.4/Brick.ttl")

# Load the library
lib = Library.load(directory="basic-building")

# Directory to store the generated .rst files
output_dir = "source"
os.makedirs(output_dir, exist_ok=True)

# Template for the .rst file
rst_template = """
{name}
{padding}

{turtle}

{graphviz}

Parameters
----------

{parameters}

Dependencies
------------

{dependencies}
"""

# List to store template names for index.rst
template_names = []

# Generate .rst files for each template
for templ in lib.get_templates():
    name = templ.name
    template_names.append(name)
    parameters = "\n".join(f"- {param}" for param in templ.parameters)

    dependencies = build_dependencies_string(templ)
    padding = "-" * len(name)
    
    serialized_body = templ.body.serialize(format="turtle")
    # add a tab to each line
    serialized_body = "\n".join(f"    {line}" for line in serialized_body.split("\n"))

    turtle = f"""
.. code-block:: turtle

{serialized_body}
    """

    graphviz = build_graphviz(templ.inline_dependencies().body)

    # Create the .rst content
    rst_content = rst_template.format(name=name, padding=padding, turtle=turtle, graphviz=graphviz, parameters=parameters, dependencies=dependencies)

    # Write to a .rst file
    with open(os.path.join(output_dir, f"{name}.rst"), "w") as f:
        f.write(rst_content)
# Create index.rst content
index_content = """.. toctree::
   :maxdepth: 1
   :caption: Template Documentation

"""

index_content += "\n".join(f"   {name}" for name in template_names)

# Write the index.rst file
with open(os.path.join(output_dir, "index.rst"), "w") as f:
    f.write(index_content)
