# Copy somewhere in PYTHONPATH (sys.path)

# pylint: disable=missing-docstring
import imp
from astroid import MANAGER
from astroid import node_classes
from astroid import scoped_nodes

def transform(class_node):
    # Make sure it's part of a module
    if not hasattr(class_node, "parent") or\
            not isinstance(class_node.parent, scoped_nodes.Module):
        return
    # Get the module name
    name = class_node.parent.name
    if name.rfind(".") >= 0:
        name = name[name.rfind(".") + 1:]
    # Load the module from the file
    module = imp.load_source(name, class_node.parent.file)
    # Make sure the class is part of the module
    if not hasattr(module, class_node.name):
        return
    # Get the class
    cls = getattr(module, class_node.name)
    # Make sure there is a CONFIG
    if not hasattr(cls, "CONFIG"):
        return
    # Add config options as local parameters
    for param in cls.CONFIG:
        class_node.locals[param] = [node_classes.Attribute(attrname=param,
                                                           parent=class_node)]

def register(linter):
    # pylint: disable=unused-argument
    MANAGER.register_transform(scoped_nodes.ClassDef, transform)
