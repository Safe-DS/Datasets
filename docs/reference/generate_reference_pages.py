"""
Automatically generate reference pages for all public classes and functions in the package.

Inspired by https://mkdocstrings.github.io/recipes/#bind-pages-to-sections-themselves.
"""

import sys
from importlib import import_module
from inspect import getmembers, isclass, isfunction
from pathlib import Path

import mkdocs_gen_files

root = "src"
package = "safeds_datasets"


def list_class_and_function_names_in_module(module_name: str) -> list[str]:
    """Return a list with the names of all classes and function names in the given module."""
    import_module(module_name)
    module = sys.modules[module_name]

    return [name for name, obj in getmembers(module) if isclass(obj) or isfunction(obj)]


nav = mkdocs_gen_files.Nav()

for path in sorted(Path(root).rglob("__init__.py")):
    module_path = path.relative_to(root).with_suffix("")
    doc_path = path.relative_to(root).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    # Skip demos, tests, etc.
    parts = tuple(module_path.parts)
    if parts[0] != package:
        continue

    # Remove the final "__init__" part
    parts = parts[:-1]

    # Skip private modules
    if any(part.startswith("_") for part in parts):
        continue

    qualified_name = ".".join(parts)

    for name in list_class_and_function_names_in_module(qualified_name):
        doc_path = doc_path.with_name(f"{name}.md")
        full_doc_path = full_doc_path.with_name(f"{name}.md")

        nav[(*parts, name)] = doc_path.as_posix()

        # Create one file containing the documentation for the current class or function
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = qualified_name + "." + name
            fd.write(f"::: {ident}")

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
