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
        return find_instances(ast.ext[0], set(argv), ID)

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

    #####################################################################################
    #   _____ ____  _   _ _____ _____ _______ _____ ____  _   _          _       _____  #
    #  / ____/ __ \| \ | |  __ \_   _|__   __|_   _/ __ \| \ | |   /\   | |     / ____| #
    # | |   | |  | |  \| | |  | || |    | |    | || |  | |  \| |  /  \  | |    | (___   #
    # | |   | |  | | . ` | |  | || |    | |    | || |  | | . ` | / /\ \ | |     \___ \  #
    # | |___| |__| | |\  | |__| || |_   | |   _| || |__| | |\  |/ ____ \| |____ ____) | #
    #  \_____\____/|_| \_|_____/_____|  |_|  |_____\____/|_| \_/_/    \_\______|_____/  #
    #####################################################################################

    def test_conditional_host_condition(self):
        src = '''void provide_a(){ int a; }
        void foo() { if (a) { _; } }'''
        d = self.src2d(src, ['a'])
        print(d)




if __name__ == "__main__":
    unittest.main()
