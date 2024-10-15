import os
from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library

# Initialize BuildingMOTIF
bm = BuildingMOTIF("sqlite://")

# Load the library
lib = Library.load(directory="basic-building")

# Directory to store the generated .rst files
output_dir = "docs/source/templates"
os.makedirs(output_dir, exist_ok=True)

# Template for the .rst file
rst_template = """
{name}
{'=' * len(name)}

Parameters
----------

{parameters}

Dependencies
------------

{dependencies}
"""

# Generate .rst files for each template
for templ in lib.get_templates():
    name = templ.name
    parameters = "\n".join(f"- {param}" for param in templ.parameters)
    dependencies = "\n".join(f"- {dep.template.name}" for dep in templ.get_dependencies())

    # Create the .rst content
    rst_content = rst_template.format(name=name, parameters=parameters, dependencies=dependencies)

    # Write to a .rst file
    with open(os.path.join(output_dir, f"{name}.rst"), "w") as f:
        f.write(rst_content)
