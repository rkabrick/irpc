#!/usr/bin/env python3

import sys, copy
from pycparser.c_ast import *
#FuncCall, ID, Decl, TypeDecl, IdentifierType, If

from irpc.irpctyping import *
from irpc.bindingEntity import entity2Compound

# Function can:
#   - use entity
#   - be a provider
#
# A provider:
#    - provide an entity
#    - is identified by is name

# 1/ Generate the list of entity
# 2/ Inside function body, insert a call to the provider before any usage of an entity.
# 3/ Inside provider body, hoist the entity declaration

def is_provider(funcdef: FuncDef):
    return funcdef.decl.name.startswith('provide_')

def provider_name(provdef: ProvDef):
    return provdef.decl.name.split('provide_').pop()

def hoist_declaration(main: FuncDef,
                      provdef: ProvDef):

    entname = provider_name(provdef)
    l_node = provdef.body.block_items
    for i, node in enumerate(l_node):
             if isinstance(node,Decl) and node.type.declname == entname:
                    node = l_node.pop(i)
                    main.insert(0, node)
                    break

def hoist_prov_memo(main: FuncDef,
                    provdef: ProvDef):

    _name_ = f"{e}_provided"
    memo_node = Decl(name=_name_,
        quals=[], storage=[],funcspec=[],
        type=TypeDecl(declname=_name_, quals=[],
                    type=IdentifierType(names=['bool'])),
        init=ID(name='False'),
        bitsize=None
        )
    main.insert(1, memo_node)

def add_provider_call(funcdef: FuncDef,
                      entnames: Set[Entity]):

    if is_provider(funcdef):
        entnames = entnames - set([provider_name(funcdef)])

    # Insert the provider call
    for e, l_compound in entity2Compound(funcdef.body, entnames).items():
          for compound in l_compound:
                prov_if = If(cond=UnaryOp(op='!', expr=ID(name=f'{e}_provided')), iftrue=Compound(block_items=(FuncCall(name=ID(name=f'provide_{e}'), args=None), Assignment(op='=',lvalue=ID(name=f'{e}_provided'), rvalue=Constant(type='bool', value='true')))), iffalse=None)
                compound.block_items.insert(0, prov_if)
                

if __name__ == "__main__":

    from pycparser import parse_file, c_parser, c_generator

    filename = sys.argv[1]
    ast = parse_file(filename,
                     use_cpp=True,
                     cpp_path='gcc',
                     cpp_args=['-E'])

    l_func = { f for f in ast.ext if isinstance(f, FuncDef) }
    l_provider = { f for f in l_func if is_provider(f) }
    l_ent  = { provider_name(e) for e in l_provider }

    for f in l_func:
        add_provider_call(f, l_ent)

        

    for p in l_provider:
        hoist_declaration(ast.ext, p)

    for e in l_ent:
        hoist_prov_memo(ast.ext, e)

    print(ast.ext) 
    generator = c_generator.CGenerator()
    print(generator.visit(ast))
