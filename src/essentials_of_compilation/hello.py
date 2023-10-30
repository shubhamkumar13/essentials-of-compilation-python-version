def main():
    print("hello world!")

class Constant:
    def __init__(self, value):
        self.value = value

# instance of [Constant] class
eight = Constant(8)

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class USub:
    def __init__(self):
        return None

neg_eight = UnaryOp(USub(), eight)

class Call:
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Name:
    def __init__(self, id):
        self.id = id

read = Call(Name('input_int'), [])

class BinOp:
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right

class Add:
    def __init__(self):
        return None
class Sub:
    def __init__(self):
        return None

ast1_1 = BinOp(read, Add(), neg_eight)
class Module:
    def __init__(self, body):
        self.body = body

class Expr:
    def __init__(self, )

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
    
print(leaf(Call(Name('input_int'), [])))
print(leaf(UnaryOp(USub(), eight)), eight)
print(leaf(Constant(8)))

def is_exp(e):
    match e:
        case Constant(n):
            return True
        case Call(Name('input_int'), []):
            return True
        case UnaryOp(USub(), e1):
            return is_exp(e1)
        case BinOp(e1, Add(), e2):
            return is_exp(e1) and is_exp(e2)
        case BinOp(e1, Sub(), e2):
            return is_exp(e1) and is_exp(e2)
        case _:
            return False

def is_stmt(s):
    match s:
        case Expr(Call(Name('print'), [e])):
            return is_exp(e)
        case Expr(e):
            return is_exp(e)
        case _:
            return False