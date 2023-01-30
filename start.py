from fractions import Fraction
from dataclasses import dataclass,field
from typing import Optional, NewType, Mapping

# A minimal example to illustrate typechecking.

@dataclass
class NumType:
    pass

@dataclass
class BoolType:
    pass

@dataclass
class StringType:
    pass

@dataclass
class IntType:
    pass

@dataclass 
class FracType:
    pass

SimType = NumType | BoolType | StringType | IntType | FracType

@dataclass
class NumLiteral:
    value: Fraction
    type: SimType = NumType
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BoolLiteral:
    value: bool
    type: SimType =BoolType
@dataclass
class StringLiteral:
    value: str
    type: SimType=StringType
    
@dataclass 
class IntLiteral:
    value: int
    type: SimType=IntType
    def __init__(self, *args):
        self.value = int(*args)

@dataclass 
class FracLiteral:
    value: Fraction
    type: SimType=FracType
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'
    type: SimType = NumType | BoolType | StringType | IntType | FracType

@dataclass
class Variable:
    name: str

@dataclass
class UnOp:
    operator: str
    vari : int

@dataclass
class StringOp:
    operator:str
    left:'AST'
    right:Optional['AST']=None
    # type:StringLiteral

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class IfElse:
    condition: 'AST'
    iftrue: 'AST'
    iffalse: 'AST'
    type: Optional[SimType] = None

@dataclass
class PrintOp:
    inp: 'AST'

AST = NumLiteral | BoolLiteral | BinOp | IfElse | StringLiteral | IntLiteral | FracLiteral


TypedAST = NewType('TypedAST', AST)

class TypeError(Exception):
    pass

# Since we don't have variables, environment is not needed.
def typecheck(program: AST, env = None) -> TypedAST:
    match program:
        case NumLiteral() as t: # already typed.
            return t
        case BoolLiteral() as t: # already typed.
            return t
        case StringLiteral() as t:
            return t
        case IntLiteral() as t:
            return t
        case FracLiteral() as t:
            return t
    
        case BinOp(op, left, right) if op in ["+", "*"]:
            tleft = typecheck(left)
            tright = typecheck(right)
            
            if tleft.type != tright.type :
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            return BinOp(op, left, right,tleft)
        
        case BinOp(op, left, right) if op in ["/"]:
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != NumType or tright.type != NumType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            if tleft.type != IntType or tright.type != IntType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            elif tleft.type != FracType or tright.type != FracType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            return BinOp(op, left, right)

        case BinOp("<", left, right):
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != NumType or tright.type != NumType:
                raise TypeError()
            return BinOp("<", left, right, BoolType)
        case BinOp("=", left, right):
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != tright.type:
                raise TypeError()
            return BinOp("=", left, right, BoolType)
        case IfElse(c, t, f): # We have to typecheck both branches.
            tc = typecheck(c)
            if tc.type != BoolType:
                raise TypeError()
            tt = typecheck(t)
            tf = typecheck(f)
            if tt.type != tf.type: # Both branches must have the same type.
                raise TypeError()
            return IfElse(tc, tt, tf, tt.type) # The common type becomes the type of the if-else.
        case PrintOp(inp):
            if inp==None:
                raise TypeError()
    raise TypeError()
Value = Fraction

class InvalidProgram(Exception):
    pass


    

def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
        case StringLiteral(value):
            return value
        case IntLiteral(value):
            return int(value)
        case FracLiteral(value):
            return Fraction(value)
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Variable(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | { name: v1 })
        case BinOp("+", left, right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if (left_type==NumType and right_type== NumType):
                return eval(left, environment) + eval(right, environment)
            elif(left_type==IntType and right_type== IntType):
                return int(eval(left, environment) + eval(right, environment))
            elif(left_type==FracType and right_type== FracType):
                return Fraction(Fraction(eval(left, environment)) + Fraction(eval(right, environment)))
            else:
                # print(left_type)
                # print(right_type)
                raise TypeError()

        case BinOp("-", left, right):
            return eval(left, environment) - eval(right, environment)
        case BinOp("*", left, right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if (left_type==NumType and right_type== NumType):
                return eval(left, environment) * eval(right, environment)
            elif(left_type==IntType and right_type== IntType):
                return int(eval(left, environment) * eval(right, environment))
            elif(left_type==FracType and right_type== FracType):
                return Fraction(Fraction(eval(left, environment)) * Fraction(eval(right, environment)))
            else:
                # print(left_type)
                # print(right_type)
                raise TypeError()

        case BinOp("/", left, right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if (left_type==NumType and right_type== NumType):
                return eval(left, environment) / eval(right, environment)
            elif(left_type==IntType and right_type== IntType):
                return int(eval(left, environment) / eval(right, environment))
            elif(left_type==FracType and right_type== FracType):
                return Fraction(Fraction(eval(left, environment)) / Fraction(eval(right, environment)))
            else:
                # print(left_type)
                # print(right_type)
                raise TypeError()

            

        # Bitwise Operators With type checking
        case BinOp("&",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                # print(left_type)
                # print(right_type)
                raise TypeError()
            return int(eval(left,environment)) & int(eval(right,environment))
        case BinOp("|",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise TypeError()
            return int(eval(left,environment)) | int(eval(right,environment))
        case BinOp("^",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise TypeError()
            return int(eval(left,environment)) ^ int(eval(right,environment))
        case BinOp(">>",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise TypeError()
            return int(eval(left,environment)) >> int(eval(right,environment))
        case BinOp("<<",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise TypeError()
            return int(eval(left,environment)) << int(eval(right,environment))

        #unary Operations
        case UnOp('-',vari):
            un=eval(vari)
            un=-un
            return eval(NumLiteral(un))
        case UnOp('++',vari):
            un=eval(vari)
            un=un+1
            return eval(NumLiteral(un))
        case UnOp('--',vari):
            un=eval(vari)
            un=un-1
            return eval(NumLiteral(un))

        
        # String Operations
        # implement string typecheck for this
        case StringOp('add',left,right):
            return eval(left)+eval(right)
        case StringOp('length',left):
            return len(eval(left))
        
        #print Operation
        case PrintOp(inp):
            print(inp)
            return inp
        
    raise InvalidProgram()

def test_division():
    # a=FracLiteral(2)
    # b=FracLiteral(4)
    # c=BinOp("/",a,b)
    # print(c)
    # assert eval(c)== 1/2

    a=IntLiteral(5)
    print(type(a))
    b=IntLiteral(2)
    print(type(b))
    c=BinOp("+",a,b)
    print(type(eval(c)))
    
    # d=IntLiteral(9)
    # print(type(d))
    # c=BinOp("/",BinOp("+",a,d),b)
    # print(type(c))
    # print(eval(c))
    # assert eval(c)== 7

    # a=NumLiteral(5)                 #Using Numliteral We can get float values
    # b=NumLiteral(2)
    # c=BinOp("/",a,b)
    # print(c)
    # assert eval(c)== 2.5

    # a=IntLiteral(5)               #//If the opreands hav different type Like Int and Fraction 
    # b=FracLiteral(2)
    # c=BinOp("/",a,b)
    # print(c)
    # assert eval(c)== 2.5

test_division()












    


