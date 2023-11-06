from dataclasses import dataclass
from sys import stdin
from pprint import pprint
from typing import Any

@dataclass
class Expr:
    exp : 'Any'

@dataclass
class Constant:
    value : int

@dataclass
class UnaryOp:
    op : 'Any'
    operand : 'Any'

@dataclass
class Call:
    func : 'Any'
    args : 'Any'

@dataclass
class Name:
    id : str

@dataclass
class BinOp:
    left : 'Any'
    op : 'Any'
    right : 'Any'

class USub:
    def __init__(self):
        pass

    def __repr__(self):
        return "USub()"

class Add:
    def __init__(self):
        pass

    def __repr__(self):
        return "Add()"

class Sub:
    def __init__(self):
        pass

    def __repr__(self):
        return "Sub()"

@dataclass
class Module:
    body : list

def leaf(arith):
    match arith:
        case Constant(n):
            return True
        case Call(Name('input_int'), []):
            return True
        case UnaryOp(USub(), e1):
            return False
        case BinOp(e1, Add(), e2):
            return False
        case BinOp(e1, Sub(), e2):
            return False

def add64(left : int, right : int) -> int:
    return left + right

def sub64(left : int, right : int) -> int:
    return left - right

def neg64(value : int) -> int:
    return -1 * value

def input_int() -> int:
    return int(stdin.readline())

class CheckEvaluator:
    def is_exp(self, e):
        match e:
            case Constant(n):
                return True
            case Call(Name('input_int'), []):
                return True
            case UnaryOp(USub(), e1):
                return self.is_exp(e1)
            case BinOp(e1, Add(), e2):
                return (self.is_exp(e1) and self.is_exp(e2))
            case BinOp(e1, Sub(), e2):
                return (self.is_exp(e1) and self.is_exp(e2))
            case _:
                return False

    def is_stmt(self, s):
        match s:
            case Expr(Call(Name('print'), [e])):
                return self.is_exp(e)
            case Expr(e):
                return self.is_exp(e)
            case _:
                return False

    def is_Lint(self, p):
        match p:
            case Module(body):
                return all([self.is_stmt(s) for s in body])
            case _:
                return False

class InterpLint:
    def interp_exp(self, e, env):
        match e:
            case BinOp(left, Add(), right):
                left  = self.interp_exp(left, env)
                right = self.interp_exp(right, env)
                return add64(left, right)
            case BinOp(left, Sub(), right):
                left = self.interp_exp(left)
                right = self.interp_exp(right)
                return sub64(left, right)
            case UnaryOp(USub(), v):
                return neg64(self.interp_exp(v))
            case Constant(value):
                return value
            case Call(Name('input_int'), []):
                return input_int()

    def interp_stmt(self, s, env, cont):
        match s:
            case Expr(Call(Name('print'), [arg])):
                val = self.interp_exp(arg, env)
                print(val, end='')
                return self.interp_stmts(cont, env)
            case Expr(value):
                self.interp_exp(value, env)
                return self.interp_stmts(cont, env)
            case _:
                raise Exception('error in interp_stmt, unexpected' + repr(s))
    
    def interp_stmts(self, ss, env):
        match ss:
            case []:
                return 0
            case [s, *ss]:
                return self.interp_stmt(s, env, ss)
    
    def interp(self, p):
        match p:
            case Module(body):
                self.interp_stmts(body, {})


def interp_Lint(p):
    return InterpLint().interp(p)

# def check_Lint():
#     read = Call(Name('input_int'), [])
#     eight = Constant(8)
#     neg_eight = UnaryOp(USub(), eight)
#     ast1_1 = BinOp(read, Add(), neg_eight)
#     s = Module([Expr(ast1_1)])
#     # this is Lint
#     print(is_Lint(s))
#     # this is not Lint
#     print(is_Lint(Module([Expr(BinOp(read, Sub(), UnaryOp(Add(), Constant(8))))])))

# def check_42():
#     ten = Constant(10)
#     thirty_two = Constant(32)
#     ten_plus_thirty_two = BinOp(Constant(10), Add(), Constant(32))
#     ast1_2 = Call(Name('print'), [ten_plus_thirty_two])
#     s = Module([Expr(ast1_2)])
#     # this is Lint
#     print(is_Lint(s))

# def interp_minus_twenty_two():
#     ten = Constant(10)
#     twenty = Constant(20)
#     twelve = Constant(12)
#     thirty_two = BinOp(twelve, Add(), twenty)
#     minus_thirty_two = UnaryOp(USub(), thirty_two)
#     ast1_1 = BinOp(ten, Add(), minus_thirty_two)
#     s = Module([Expr(Call(Name('print'), [ast1_1]))])
#     interp_Lint(s)

# def interp_input_plus_minus_eight():
#     three = Constant(3)
#     five = Constant(5)
#     neg_eight = UnaryOp(USub(), BinOp(three, Add(), five))
#     ast = BinOp(Call(Name('input_int'), []), Add(), neg_eight)
#     s = Module([Expr(Call(Name('print'), [ast]))])
#     interp_Lint(s)

class PartialEvaluator:
    def pe_neg(self, r):
        match r:
            case Constant(n):
                return Constant(neg64(n))
            case _:
                return UnaryOp(USub(), r)
    
    def pe_add(self, r1, r2):
        match (r1, r2):
            case (Constant(n1), Constant(n2)):
                return Constant(add64(n1, n2))
            case _:
                return BinOp(r1, Add(), r2)
    
    def pe_sub(self, r1, r2):
        match (r1, r2):
            case (Constant(n1), Constant(n2)):
                return Constant(sub64(n1, n2))
            case _:
                return BinOp(r1, Sub(), r2)
    
    def pe_exp(self, e):
        match e:
            case BinOp(left, Add(), right):
                left = self.pe_exp(left)
                right = self.pe_exp(right)
                return self.pe_add(left, right)
            
            case BinOp(left, Sub(), right):
                left = self.pe_exp(left)
                right = self.pe_exp(right)
                return self.pe_sub(left, right)
            
            case UnaryOp(USub(), v):
                v = self.pe_exp(v)
                return self.pe_neg(v)
            
            case Constant(value):
                return e
            
            case Call(Name('input_int'), []):
                return e           
    
    def pe_stmt(self, s):
        match s:
            case Expr(Call(Name('print'), [args])):
                args = self.pe_exp(args)
                return Expr(Call(Name('print'), [args]))
            case Expr(value):
                value = self.pe_exp(value)
                return Expr(value)
    
    def pe_partial_Lint(self, p : list):
        match p:
            case Module(body):
                new_body = [self.pe_stmt(s) for s in body]
                return Module(new_body)

def partial_ast1():
    five = Constant(5)
    three = Constant(3)
    input_int = Call(Name('input_int'), [])
    five_plus_three = BinOp(five, Add(), three)
    expr = BinOp(input_int, Add(), five_plus_three)
    print_expr = Expr(Call(Name('print'), [expr]))
    eval = PartialEvaluator()
    p = eval.pe_partial_Lint(Module([print_expr]))
    pprint(p)

def main():
    # check_Lint()
    # check_42()
    # interp_minus_twenty_two()
    # interp_input_plus_minus_eight()
    partial_ast1()