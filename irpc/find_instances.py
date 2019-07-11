from pycparser.c_ast import Compound
from collections import defaultdict
from .node_extract import node_extract

def find_instances(astnode, l_ent, _type_, old_compound = None, idx_old_compound = 0):
    """
    Recursively search through AST to locate all instances of ID nodes

    Args:
        param1: Node to be analyzed (ie. FuncDef, Compound, etc)
        param2: Placeholder for current compounds parent (None by default)
        param3: Cached index to maintain integrity of value across recurses (Default 0: ie. No cache)

    Returns:
        Returns a dict of all Compounds containing instances of entity w/ provider
    """
    # d holds all compounds with appropriate index values based on entity occurences
    d = defaultdict(list)
    # Recurses through elements in body of head node

    for i, node in enumerate(node_extract(astnode)):

        if isinstance(node, Compound):
            old_compound = node

        if isinstance(astnode, Compound):
            idx_old_compound = i
        # Append any entries of ID node names to d so long as it is a function with a provider
        if isinstance(node, _type_):
            if node.name in l_ent:
                if d[node.name] == [] or ( d[node.name][-1] != (old_compound, idx_old_compound) ):
                    d[node.name].append( (old_compound, idx_old_compound) )
        # If anything but instance of ID -> recurse
        else:
            # Recursive call followed by updating the dictionary
            for k,v in find_instances(node, l_ent, _type_, old_compound, idx_old_compound).items():
                d[k] += v
    return d
