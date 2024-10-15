import os
from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library

# Initialize BuildingMOTIF
bm = BuildingMOTIF("sqlite://")

brick = Library.load(ontology_graph="https://brickschema.org/schema/1.4/Brick.ttl")

# Load the library
lib = Library.load(directory="basic-building")

# Directory to store the generated .rst files
output_dir = "source/templates"
os.makedirs(output_dir, exist_ok=True)

# Template for the .rst file
rst_template = """
{name}
{padding}

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
    dependencies = "\n".join(f"- :doc:`{dep.template.name}`" for dep in templ.get_dependencies())
    padding = "-" * len(name)

    # Create the .rst content
    rst_content = rst_template.format(name=name, padding=padding, parameters=parameters, dependencies=dependencies)

    # Write to a .rst file
    with open(os.path.join(output_dir, f"{name}.rst"), "w") as f:
        f.write(rst_content)
# Create index.rst content
index_content = """.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Template Documentation

"""

index_content += "\n".join(f"   {name}" for name in template_names)

# Write the index.rst file
with open(os.path.join(output_dir, "index.rst"), "w") as f:
    f.write(index_content)
