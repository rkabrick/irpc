import sys
sys.path.append('../')
from irpc.find_instances import find_instances
from pycparser.c_ast import Compound, ID, If, For, UnaryOp, BinaryOp, Assignment, FuncCall, ExprList, FuncDef, Decl, Constant, While

from collections import defaultdict
import unittest

class TestFind(unittest.TestCase):
    from pycparser import c_parser
    parser = c_parser.CParser()

    def src2d(self, src, argv):
        ast = self.parser.parse(src)
        return find_instances(ast.ext[0], list(l_ent), ID)

#  __
# (_  o ._ _  ._  |  _
# __) | | | | |_) | (/_
#             |

    def test_simple(self):
        src = 'void foo(){ _ = a;}' ''
        d = self.src2d(src, ['a'])

        assert(d["a"][0][0].block_items[0].rvalue.name == "a")
        assert(d["a"][0][1] == 0)

    def test_multiple_entity(self):
        src = 'void foo(){ _ = a + a ;}' ''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].rvalue.right.name == "a")
        assert(d["a"][0][0].block_items[0].rvalue.left.name == "a")
        assert(d["a"][0][1] == 0)

    def test_simple_fuction(self):
        src = 'void foo(){ _ = f(a) ;}' ''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].rvalue.args.exprs[0].name == "a")
        assert(d["a"][0][1] == 0)

    def test_fuction_expression(self):
        src = 'void foo(){ _ = f(a + 1) ;}' ''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].rvalue.args.exprs[0].left.name == "a")
        assert(d["a"][0][1] == 0)

    #################
    #  _____  ____  #
    # |_   _|/ ___| #
    #   | | | |__   #
    #   | | |  __|  #
    #  _| |_| |     #
    # |_____|_|     #
    #################

    def test_if_host_condition(self):
        src = '''void foo() { if (a) { _; } }'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].cond.name == 'a')

    def test_if_iftrue(self):
        src = '''void foo() { if (_){ x = a; } }'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].rvalue.name == 'a')

    def test_if_else(self):
        src = '''void foo() { if (_){ a = 10; } else { a = 0; }}'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].lvalue.name == 'a')
        assert(d["a"][1][0].block_items[0].lvalue.name == 'a')

    def test_nested_if(self):
        src = '''
void foo() {
    if (_){
        if(_) {a = 10; }
        else { x = a; }
        }
    else {
        if (a) {a = 100 ; }
        }}'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].lvalue.name == 'a')
        assert(d["a"][1][0].block_items[0].rvalue.name == 'a')
        assert(d["a"][2][0].block_items[0].cond.name == 'a')
        assert(d["a"][2][0].block_items[0].iftrue.block_items[0].lvalue.name == 'a')

    def test_after_if_else(self):
        src = '''
void foo() {
    if (_){ x = 10; }
    else { x = 0; }
    { a = 10; }}'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].lvalue.name == 'a')

        #################################
        #  _                            #
        # | |                           #
        # | |     ___   ___  _ __  ___  #
        # | |    / _ \ / _ \| '_ \/ __| #
        # | |___| (_) | (_) | |_) \__ \ #
        # |______\___/ \___/| .__/|___/ #
        #                   | |         #
        #                   |_|         #
        #################################
    def test_for_loop(self):
        src = '''
void foo() {
    for (a = 0; a < 10; a++){
         x = 10;
        }
        }'''
        d = self.src2d(src, ['a'])
        print(d["a"][0][0])
        assert(d["a"][0][0].block_items[0].init.lvalue.name == 'a')
        assert(d["a"][0][0].block_items[0].cond.left.name == 'a')
        assert(d["a"][0][0].block_items[0].next.expr.name == 'a')

    def test_while_loop(self):
        src = '''
void foo() {
    while (a < 10){
        x = 10;
        a++;
    }
}'''
        d = self.src2d(src, ['a'])
        assert(d["a"][0][0].block_items[0].cond.left.name == 'a')
        assert(d["a"][0][0].block_items[0].stmt.block_items[1].expr.name == 'a')

        ####################################
        #   _____         _ _       _      #
        #  / ____|       (_) |     | |     #
        # | (_____      ___| |_ ___| |__   #
        #  \___ \ \ /\ / / | __/ __| '_ \  #
        #  ____) \ V  V /| | || (__| | | | #
        # |_____/ \_/\_/ |_|\__\___|_| |_| #
        ####################################




if __name__ == "__main__":
    unittest.main()
