from fractions import Fraction
from dataclasses import dataclass,field
from typing import Optional, NewType, Mapping, List


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
class ListType:
    pass

@dataclass
class IntType:
    pass

@dataclass 
class FracType:
    pass


SimType = NumType | BoolType | StringType | ListType | IntType | FracType

@dataclass
class NumLiteral:
    value: Fraction
    type: SimType = NumType
    def __init__(self, *args):
        self.value = Fraction(*args)

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
class BoolLiteral:
    value: bool
    type: SimType =BoolType

@dataclass
class StringLiteral:
    value: str
    type: SimType=StringType
    

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'
    type: Optional[SimType] = None

@dataclass
class Variable:
    name: str

@dataclass
class UnOp:
    operator: str
    vari : int

@dataclass
class PrintOp:
    inp: 'AST'


@dataclass
class StringOp:
    operator:str
    left:'AST'
    right:Optional['AST']=None
    type:Optional[SimType]=StringType
    
@dataclass
class StringSlice(StringOp):
    start: Optional[int] = None
    stop: Optional[int] = None
    step: Optional[int] = None
    type: Optional[SimType] = StringType
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
class ListLiteral:
    list_val:list

@dataclass
class ListOp:
    operator:str
    left:'AST'
    right:Optional['AST']=None
    assign:Optional['AST']=None
    type:SimType=ListType

@dataclass
class Get:
    var: 'AST'

@dataclass
class Put:
    var: 'AST'
    e1: 'AST'

@dataclass
class LetMut:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class Seq:
    things: List['AST']

@dataclass
class Un_boolify:
    left:'AST'
    type:SimType=NumType|StringType

@dataclass
class Whilethen:
    condition: 'AST'
    then_body: 'AST'
    

@dataclass
class For:
    condition:'AST'
    update:'AST'
    body:'AST'

class Environment:
    envs: List

    def __init__(self):
        self.envs = [{}]

    def enter_scope(self):
        self.envs.append({})

    def exit_scope(self):
        assert self.envs
        self.envs.pop()

    def add(self, name, value):
        assert name not in self.envs[-1]
        self.envs[-1][name] = value

    def get(self, name):
        for env in reversed(self.envs):
            if name in env:
                return env[name]
        raise KeyError()

    def update(self, name, value):
        for env in reversed(self.envs):
            if name in env:
                env[name] = value
                return
        raise KeyError()

AST = NumLiteral | BoolLiteral | BinOp | IfElse | StringLiteral | StringOp|ListLiteral|IntLiteral|FracLiteral|ListOp| Get | Put |Let | LetMut |Seq | Whilethen |For

Value = Fraction

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
            
            if tleft.type != NumType or tright.type != NumType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            return BinOp(op, left, right, NumType)
        
        case BinOp(op, left, right) if op in ["/"]:
            tleft = typecheck(left)
            tright = typecheck(right)
            
            if tleft.type != IntType or tright.type != IntType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            elif tleft.type != FracType or tright.type != FracType:
                print(f"left: {tleft}.type")
                print(f"right: {tright}.type")
                raise TypeError()
            return BinOp(op, left, right, tleft.type)

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
        
        case UnOp('-',vari):
            tvari=typecheck(vari)
            if tvari.type != NumType:
                raise TypeError() 
            return UnOp("++",vari,NumType)
            
        case UnOp('++',vari):
            tvari=typecheck(vari)
            if tvari.type != NumType:
                raise TypeError()
            return UnOp("++",vari,NumType)
            
        case UnOp('--',vari):
            tvari=typecheck(vari)
            if tvari.type != NumType:
                raise TypeError()
            return UnOp("++",vari,NumType)

        case PrintOp(inp):
            if inp==None:
                raise TypeError()
        case IfElse(c, t, f): # We have to typecheck both branches.
            tc = typecheck(c)
            if tc.type != BoolType:
                raise TypeError()
            tt = typecheck(t)
            tf = typecheck(f)
            if tt.type != tf.type: # Both branches must have the same type.
                raise TypeError()
            return IfElse(tc, tt, tf, tt.type) # The common type becomes the type of the if-else.
        case StringSlice("slice",left,start, stop, step):
            tleft = typecheck(left)
            if tleft.type != StringType:
                raise TypeError()
            return StringSlice("slice", left, start, stop, step, StringType)
        
        case StringOp('add',left,right):
            tleft=typecheck(left)
            tright=typecheck(right)
            if tleft.type!=StringType or tright.type!=StringType:
                raise TypeError()
            return StringOp("add",left,right)
        
        case StringOp('compare',left,right):
            tleft=typecheck(left)
            tright=typecheck(right)
            if tleft.type!=StringType or tright.type!=StringType:
                raise TypeError()
            return StringOp("compare",left,right,BoolType)


        case StringOp('length',left):
            tleft=typecheck(left)
            if tleft.type!=StringType:
                raise TypeError()
            return StringOp("length",left,type=NumType)

        case Un_boolify(left):
            tleft=typecheck(left)
            if tleft.type!=NumType or StringType:
                raise TypeError()
            return Un_boolify(left)
         
        
    raise TypeError()


class InvalidProgram(Exception):
    pass


def eval(program: AST, environment: Environment = None) -> Value:
    if environment is None:
        environment =Environment()
    
    # Pass environment to all explicitally
    def eval2(program):
        return eval(program, environment)
    
    # always call eval2 for enviornment passing instead of eval(program, envi)
    match program:
        case NumLiteral(value):
            return value
        case StringLiteral(value):
            return value
        case IntLiteral(value):
            return value
        case FracLiteral(value):
            return value
        case Variable(name):
            return environment.get(name)
        case ListLiteral(value):
            # print(f'values: {value}')
            return value
        case BoolLiteral(value):
            return value
        case Let(Variable(name), e1, e2):
            v1 = eval2(e1)
            environment.enter_scope()
            environment.add(name,v1)
           
            v2 = eval2(e2)
            environment.exit_scope()
            return v2
         
        case LetMut(Variable(name),e1,e2):
            v1 = eval2(e1)
            environment.enter_scope()
            environment.add(name,v1)
            v2 = eval2(e2)
            environment.exit_scope()
            return v2
        case Put(Variable(name),e):
            environment.update(name,eval2(e))
            return environment.get(name)
        case Get(Variable(name)):
            return environment.get(name)
        case Seq(things):
            v = None
            for thing in things:
                v = eval2(thing)
            return v
        case BinOp("+", left, right):
            return eval2(left) + eval2(right)
        case BinOp("-", left, right):
            return eval2(left) - eval2(right)
        case BinOp("*", left, right):
            return eval2(left,) * eval2(right )
        case BinOp("/", left, right):
            if(right==0):
                raise InvalidProgram()
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if (left_type==NumType and right_type== NumType):
                return  eval2(left ) /  eval2(right )
            elif(left_type==IntType and right_type== IntType):
                return int(int(eval2(left )) /  int(eval2(right )))
            elif(left_type==FracType and right_type== FracType):
                return  Fraction(Fraction(eval2(left )) /  Fraction(eval2(right )))
            else:
                # print(left_type)
                # print(right_type)
                raise TypeError()
        case BinOp("//", left, right):
            if(right==0):
                raise InvalidProgram()
            return  eval2(left ) //  eval2(right )
        case BinOp("%", left, right):
            if(right==0):
                raise InvalidProgram()
            return  eval2(left ) %  eval2(right )
        case BinOp("**", left, right):
            return  eval2(left ) **  eval2(right )
        case BinOp("==",left,right):
            return  eval2(left ) ==  eval2(right )
        case BinOp("<",left,right):
            return  eval2(left ) <  eval2(right )
        case BinOp(">",left,right):
            return  eval2(left ) >  eval2(right )
        case BinOp(">=",left,right):
            return  eval2(left ) >=  eval2(right )
        case BinOp("<=",left,right):
            return  eval2(left ) <=  eval2(right )
        case BinOp("!=",left,right):
            return  eval2(left ) !=  eval2(right )
    
        # Bitwise Operators With type checking
        case BinOp("&",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                # print(left_type)
                # print(right_type)
                raise InvalidProgram()
            return int( eval2(left )) & int( eval2(right ))
        case BinOp("|",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise InvalidProgram()
            return int( eval2(left )) | int( eval2(right ))
        case BinOp("^",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type) 
                print(right_type)
                raise InvalidProgram()
            return int( eval2(left )) ^ int( eval2(right ))
        case BinOp(">>",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise InvalidProgram()
            return int( eval2(left )) >> int( eval2(right ))
        case BinOp("<<",left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            
            if(left_type!=NumType or right_type!=NumType):
                print(left_type)
                print(right_type)
                raise InvalidProgram()
            return int( eval2(left )) << int( eval2(right ))

        case PrintOp(inp):
            print(eval2(inp))
            return 
  
        # String Operations
        # implement string typecheck for this
        case StringOp('add',left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if(left_type!=StringType or right_type!=StringType):
                raise InvalidProgram()
            return  eval2(left )+ eval2(right )
        
        case StringOp('compare',left,right):
            left_type=typecheck(left).type
            right_type=typecheck(right).type
            if(left_type!=StringType or right_type!=StringType):
                raise InvalidProgram()
            return eval2(BoolLiteral(eval2(left)==eval2(right)))

        case StringOp('length',left):
            left_type=typecheck(left).type
            if(left_type!=StringType):
                raise InvalidProgram()
            return len(eval2(left))        

        


        case StringSlice("slice", left,start, stop,step):
            left_value =  eval2(left )
            return left_value[start:stop:step]
        

        #unary Operations
        case UnOp('-',vari):
            un= eval2(vari )
            un=-un
            return  eval2(NumLiteral(un) )
        case UnOp('++',vari):
            un= eval2(vari )
            un=un+1
            return  eval2(NumLiteral(un) )
        case UnOp('--',vari):
            un= eval2(vari )
            un=un-1
            return  eval2(NumLiteral(un) )

        # IfElse
        case IfElse(c,l,r):
            # if(typecheck(l)!=typecheck(r)):
            #     return InvalidProgram()
            condition_eval= eval2(c)
            # print(typech(c))

            if(condition_eval==True):
                return  eval2(l)
                
            else:
                return  eval2(r)
        
        # List Operations
        case ListOp("append",left,right):
            
            # if(right.type!=left.type):
            #     raise InvalidProgram
            l= eval2(left)
            r= eval2(right)
            if(type(r)==Fraction):
                l.append(int(r))
            else:
                l.append(r)
            return l
            

        case ListOp('length',left):
            return len( eval2(left))

        case ListOp('assign',array,index,assign):
            if(typecheck(assign).type!=array.type or typecheck(index).type!=NumType):
                raise InvalidProgram
            arr= eval2(array)
            
            arr[int( eval2(index))]=int( eval2(assign))
            return arr
        
        case ListOp('remove',array):
            arr= eval2(array)
            arr.pop()
            return arr


        case ListOp('remove',array,index):
            if(index!=NumType):
                raise InvalidProgram
            arr= eval2(arr)

        case ListOp('pop',array,index):
            if(index!=NumType):
                raise InvalidProgram
            arr= eval2(array)
            arr.remove(index)
            return arr
        
        case Un_boolify(left):
            left_var=eval(left,environment)
            if left_var==0:
                return bool(left_var)
            elif left_var:
                return bool(left_var)
            elif len(left_var)==0:
                return bool(left_var)
            return bool(left_var)
        
        case For(condition,update,body):
            eval_cond=eval2(condition)
            while(eval_cond):
                eval2(body)
                eval2(Put(update.vari,update))
                cond=eval2(condition)
                if(cond==False):
                    break
            return
    raise InvalidProgram()


