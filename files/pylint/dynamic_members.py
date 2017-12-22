# Copy somewhere in PYTHONPATH (sys.path)

# pylint: disable=missing-docstring
from astroid import MANAGER
from astroid import node_classes
from astroid import scoped_nodes

def transform_classdef(node):
    # Make sure it's part of a module
    if not hasattr(node, "parent") or\
            not isinstance(node.parent, scoped_nodes.Module):
        return None
    # Make sure it's not part of the main python installation
    if node.parent.file is None or node.parent.file == "<?>" or\
            "python27" in node.parent.file.lower():
        return None
    # Find the CONFIG node of the class node
    config_node = None
    for subnode in node.body:
        if isinstance(subnode, node_classes.Assign) and\
                subnode.targets[0].name == "CONFIG":
            config_node = subnode
            break
    # Make sure there is a config node
    if config_node is None:
        return None
    # Get the init function
    init_func = None
    for subnode in node.body:
        if isinstance(subnode, scoped_nodes.FunctionDef) and\
                subnode.name == "__init__":
            init_func = subnode
            break
    # Create a fake init method
    if init_func is None:
        init_func = scoped_nodes.FunctionDef("__init__", parent=node)
    # Add config options as local parameters inside __init__
    for config_item in config_node.value.items:
        key = config_item[0].value
        value = config_item[1]
        assign = node_classes.Assign(lineno=value.lineno, parent=init_func)
        attr = node_classes.AssignAttr(key, parent=assign)
        attr.postinit(node_classes.Name("self", parent=attr))
        assign.postinit([attr], value)
        node.instance_attrs[key] = [attr]
        init_func.body.insert(0, assign)
    return node

def register(linter):
    # pylint: disable=unused-argument
    MANAGER.register_transform(scoped_nodes.ClassDef, transform_classdef)
