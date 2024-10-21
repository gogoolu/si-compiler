from lark import Lark, tree, Tree
from lark.visitors import Interpreter
import sys


class siuudInterpreter(Interpreter):

    def __init__(self) -> Interpreter:
        super().__init__()
        self.numberSpace = {}
        self.vars = {}

    # ------------ type ----------------

    def boolean(self, tree: Tree) -> bool:
        if tree.children[0].value == "true":
            return True
        else: 
            return False

    def number(self, tree: Tree) -> float:
        return (float)(tree.children[0].value)

    def var(self, tree: Tree):
        return self.vars[tree.children[0].value]

    # -------------- declare stmt -------------
    def number_declare(self, tree: Tree) -> None:
        if not tree.children[0].value in self.vars:
            self.vars[tree.children[0].value] = None
            if tree.children[1]:
                self.vars[tree.children[0].value] = self.visit(tree.children[1])
        else:
            # raise "variable redefine"
            print("variable redefine")

    # -------------- assign ------------------
    def assign(self, tree: Tree) -> None:
        varName = tree.children[0].value
        if varName in self.vars:
            varValue = self.visit(tree.children[1]) 
            self.vars[varName] = varValue
        else:
            print(f"ERROR: variable {varName} not define")

    def add_assign(self, tree: Tree) -> None:
        varName = tree.children[0].value
        if varName in self.vars:
            addValue = self.visit(tree.children[1])
            self.vars[varName] = self.vars[varName] + addValue
        else:
            print(f"ERROR: variable {varName} not define")

    def sub_assign(self, tree: Tree) -> None:
        varName = tree.children[0].value
        if varName in self.vars:
            subValue = self.visit(tree.children[1])
            self.vars[varName] = self.vars[varName] - subValue
        else:
            print(f"ERROR: variable {varName} not define")

    def mul_assign(self, tree: Tree) -> None:
        varName = tree.children[0].value
        if varName in self.vars:
            mulValue = self.visit(tree.children[1])
            self.vars[varName] = self.vars[varName] * mulValue
        else:
            print(f"ERROR: variable {varName} not define")

    def div_assign(self, tree: Tree) -> None:
        varName = tree.children[0].value
        if varName in self.vars:
            divValue = self.visit(tree.children[1])
            self.vars[varName] = self.vars[varName] / divValue
        else:
            print(f"ERROR: variable {varName} not define")

    # ------------- branch and loop------------
    def if_stmt(self, tree: Tree) -> None:
        if self.visit(tree.children[0]):
            self.visit(tree.children[1])
        else: 
            if (tree.children[2]):
                self.visit(tree.children[2])
    
    def while_stmt(self, tree: Tree) -> None:
        while self.visit(tree.children[0]):
            self.visit(tree.children[1])

    # ---------------- compare operator ------------------
    def gt(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) > self.visit(tree.children[1])
    
    def ge(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) >= self.visit(tree.children[1])
    
    def lt(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) < self.visit(tree.children[1])
    
    def le(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) <= self.visit(tree.children[1])
    
    def eq(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) == self.visit(tree.children[1])
    
    def ne(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) != self.visit(tree.children[1])
    
    # ---------------- logical operator ------------------
    def s_not(self, tree: Tree) -> bool:
        return not self.visit(tree.children[0])

    def s_or_(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) or self.visit(tree.children[1])
    
    def s_and(self, tree: Tree) -> bool:
        return self.visit(tree.children[0]) and self.visit(tree.children[1])
    
    # ---------------- arithmetic operator -----------------
    def add(self, tree: Tree) -> float:
        return self.visit(tree.children[0]) + self.visit(tree.children[1])
    
    def sub(self, tree: Tree) -> float:
        return self.visit(tree.children[0]) - self.visit(tree.children[1])
    
    def mul(self, tree: Tree) -> float:
        return self.visit(tree.children[0]) * self.visit(tree.children[1])

    def div(self, tree: Tree) -> float:
        return self.visit(tree.children[0]) / self.visit(tree.children[1])
    
    # --------------- api -------------------
    def print_stmt(self, tree: Tree) -> None:
        print(self.visit(tree.children[0]))


if __name__ == "__main__":
    grammar = ""
    srcCode = ""

    with open("./grammar.lark", "r") as file:
        grammar = file.read()
    with open(sys.argv[1], "r") as file:
        srcCode = file.read()
    
    parser = Lark(grammar, parser="lalr")
    grammarTree = parser.parse(srcCode)

    siuudInterpreter().visit(grammarTree)

    tree.pydot__tree_to_png(grammarTree, "./grammar-tree.png")