from pycparser.c_ast import Compound, If, While, For, FuncDef, Switch, Case, BinaryOp, Assignment, ID, ExprList, FuncCall, Return, Decl, Constant, UnaryOp

def node_extract(node):
    if isinstance(node, Compound):
        return node.block_items
    elif isinstance(node, If):
        return [node.iftrue, node.iffalse]
    elif isinstance(node, (While, For) ):
        return [ node.cond, node.stmt ]
    elif isinstance(node, FuncDef):
        return [ node.body ]
    elif isinstance(node, ( Switch, Case ) ):
        return [node.stmts]
    elif isinstance(node, BinaryOp):
        return [node.left, node.right]
    elif isinstance(node, Assignment):
        return [node.lvalue, node.rvalue]
    elif isinstance(node, ID):
        return [node.name]
    elif isinstance(node, ExprList):
        return node.exprs
    elif isinstance(node, FuncCall) and node.args:
        return node.args
    elif  isinstance(node, (Return, Decl, Constant)):
        return []
    elif isinstance(node, UnaryOp):
        return [ node.expr ]
    else:
        return []
