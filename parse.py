from start import *
import ast
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str)
args = parser.parse_args()

class EndOfStream(Exception):
    pass

# Stream processes the sequence of characters
@dataclass
class Stream:
    source: str
    pos: int

    def from_file(file):
        return Stream(file.read(), 0)
    
    def from_string(s):
        return Stream(s, 0)

    def next_char(self):
        if self.pos >= len(self.source):
            raise EndOfStream()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def unget(self):
        assert self.pos > 0
        self.pos = self.pos - 1

# Defining  the token types.
@dataclass
class Num:
    n: int

@dataclass
class Bool:
    b: bool

@dataclass
class Keyword:
    word: str

@dataclass
class Identifier:
    word: str

@dataclass
class Operator:
    op: str

@dataclass
class List:
    b:ListLiteral
@dataclass
class String:
    s:str

@dataclass
class Method:
    method_name:str
    identifier:Identifier

@dataclass
class BitwiseOperator:
    op:str
@dataclass
class EndStatement:
    op:str
@dataclass
class ContinueOuterLoopException(Exception):
    pass
# Markers are for defining the braces,punctuations used
@dataclass
class Markers:
    punctuation:str

Token = Num | Bool | Keyword | Identifier | Operator | BitwiseOperator | List| String| Method | Markers


class EndOfTokens(Exception):
    pass

# Defining the keywords, operators and markers for our language

keywords = "if then else endfor while done letfun let in list String  assign len length append do get for up print seq endseq end".split()
symbolic_operators = "! + - * ** / < > <= >= = ++ %".split()
unary_operators="!= ++ -- += ** //".split()
double_operators='!= == >= <= << >>'.split()
word_operators = "and or not quot rem".split()
braces=' ( )  , { }'.split()
starting_braces='['
ending_braces=']'
list_braces='[]'.split()
quotes='"'
comma=","
end_of_statement=";"

whitespace = " \t\n"

Bitwise_Operators="& | ^".split()

# converts word to token from lexer

def word_to_token(word): 
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
        return Operator(word)
    if word in Bitwise_Operators:
        return BitwiseOperator(word)
    if word == "True":
        return Bool(True)
    if word == "False":
        return Bool(False)
    if word.startswith('[') and word.endswith(']'):
        return List(ast.literal_eval(word))
    if word.startswith('"') and word.endswith('"'):
        return String(word)
    
    if "." in word:
        word=word.split('.')
        return Method(word[1],Identifier(word[0]))
    if word.startswith('len(') and word.endswith(')'):
        return Method('len',Identifier(word[4:-1]))

    return Identifier(word)

class TokenError(Exception):
    pass

# Lexer for getting Tokens from sequence of characters
@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        
        try:
            
            match self.stream.next_char():
                case c if c in Bitwise_Operators: return BitwiseOperator(c)
                case c if c in end_of_statement: 
                    return EndStatement(c)
                case c if c in braces:
                    return Markers(c)
                
                case c if c in symbolic_operators:
                    
                    n=c
                    l=self.stream.next_char()
                    n+=l
                    if(n in symbolic_operators or n in unary_operators or n in double_operators):
                        return Operator(n)
                    else:
                        self.stream.unget()
                        return Operator(c)
                case c if c.isdigit():
                    
                    n = int(c)
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n*10 + int(c)
                            else:
                                self.stream.unget()
                                return Num(n)
                        except EndOfStream:
                            return Num(n)
                
                 
                
                case c if c.isalpha():
                    
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if (c=='.'):
                                s=s+c

                                while True:
                                    try:
                                        nc=self.stream.next_char()
                                        if nc.isalpha():
                                            s=s+nc
                                        else:
                                            return word_to_token(s)
                                    except EndOfStream:

                                        return word_to_token(s)


                            elif c.isalpha() or c in list_braces:
                                s = s + c


                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)
                        
                case c if c in whitespace:
                    
                    return self.next_token()
                case c if c in starting_braces:
                    s=c
                    while True:
                        try:
                            c=self.stream.next_char()
                            s=s+c
                            if c in ending_braces:
                                return word_to_token(s)

                        except EndOfStream:
                            return word_to_token(s)

                case c if c in quotes:
                    s=c
                    while True:
                        try:
                            c=self.stream.next_char()
                            s+=c
                            if c in quotes:
                                return word_to_token(s)

                        except EndOfStream:
                            return word_to_token(s)

                        
        except EndOfStream:
            raise EndOfTokens

    def peek_token(self) -> Token:
        if self.save is not None:
           
            return self.save
        self.save = self.next_token()
        
        return self.save

    def advance(self):
        assert self.save is not None
        self.save = None

    def match(self, expected):
        
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration

@dataclass
class Parser:
    lexer: Lexer

    def from_lexer(lexer):
        return Parser(lexer)

    def parse_if(self):
        self.lexer.match(Keyword("if"))
        c = self.parse_expr()
        self.lexer.match(Keyword("then"))
        t = self.parse_expr()
        self.lexer.match(Keyword("else"))
        f = self.parse_expr()
        self.lexer.match(Keyword("end"))
        return IfElse(c, t, f)
    
    def parse_if(self):
        self.lexer.match(Keyword('if'))
        c=self.parse_expr()
        self.lexer.match(Keyword('then'))
        b=self.parse_expr()
        x=True
        while x:
            match self.lexer.peek_token():
                case Keyword(ky) if ky=="else":
                    self.lexer.advance()
                    r=self.parse_expr()
                    x=False
                    self.lexer.match(Keyword('end'))
                    return IfElse(c,b,r) 
                case _:
                    x=False
                    self.lexer.match(Keyword('end'))
                    return If(c,b)

    def parse_let(self):
        self.lexer.match(Keyword('let'))
        c=self.parse_atom()
        self.lexer.match(Operator("="))
        b=self.parse_expr()
        self.lexer.match(Keyword("in"))
        a=self.parse_expr()

        return Let(c,b,a)
    
    def parse_while(self):
        self.lexer.match(Keyword("while"))
        c = self.parse_expr()
        self.lexer.match(Keyword("do"))
        t = self.parse_expr()
        return Whilethen(c, t)
    
    def parse_print(self):
        self.lexer.match(Keyword('print'))
        p=self.parse_expr()
        self.lexer.advance()
        return PrintOp(p)
    
    # Parsing sequence using braces(Markers('{) etc)
    # For inner sequence processing ';' is used.
    
    def parse_seq(self):
        self.lexer.match(Markers('{'))
        list=[]
        while True:
            match self.lexer.peek_token():
                case EndStatement():
                    self.lexer.advance()
                    continue
                
                case Markers('}'):
                    
                    if self.lexer.next_token()==EndStatement(";"):
                        self.lexer.advance()
                        return Seq(list)
                        
                    else: 
                        return Seq(list)
                            
                case Identifier(var):
                    self.lexer.match(Identifier(var))
                    val=0
                    
                    match self.lexer.peek_token():
                        case Operator(op) if op in symbolic_operators or op in unary_operators:
                            self.lexer.advance()
                            val=self.parse_expr()
                            self.lexer.advance()
                            list.append(Put(Variable(var),val))
                            continue
                            
                case _:
                    list.append(self.parse_expr())  
                    continue              


    # parsing functions in the same way as defined in start1.py
    # defining the function in this also allows for recursive
    # functions as well as passing evaluated functions as arguments
    # to other functions.
    def parse_func(self):
        self.lexer.match(Keyword('letfun'))
        func_name=self.parse_atom()
        parameters=[]
        self.lexer.match(Markers('('))
        while True:
            match self.lexer.peek_token():
                case Markers(')'):
                    self.lexer.advance()
                    break
                case _:
                    while True:
                        match self.lexer.peek_token():
                            case Identifier(I):
                                self.lexer.advance()
                                parameters.append(Variable(I))
                            case Markers(','):
                                self.lexer.advance()
                            
                            case _:
                                self.lexer.advance()
                                break
                    break
               
        self.lexer.match(Operator("="))
        body=self.parse_expr()
        self.lexer.match(Keyword("in"))
        rest_code=self.parse_expr()
        return LetFun(func_name,parameters,body,rest_code)
                
                

    def parse_list(self):
        
        self.lexer.match(Keyword('list'))
        
        match self.lexer.peek_token():
            case List(name):
                self.lexer.advance()
                return ListLiteral(name)
            
    def parse_string(self):
        self.lexer.match(Keyword('String'))
        match self.lexer.peek_token():
            case String(name):
                self.lexer.advance()
                return StringLiteral(name)
            
    def parse_length(self,m):
        self.lexer.match(Method('length',Identifier(m.identifier.word)))
        return ListOp('length',Variable(m.identifier.word))
    
    def parse_append(self,m):
        self.lexer.match(Method('append',Identifier(m.identifier.word)))
        val= self.parse_atom()
        return ListOp('append',Variable(m.identifier.word),val)
    
    def parse_get(self,m):
        self.lexer.match(Method('get',Identifier(m.identifier.word)))
        idx= self.parse_atom()
        return ListOp('get',Variable(m.identifier.word),idx)
    
    def parse_assignment(self,m):
        self.lexer.match(Method('assign',Identifier(m.identifier.word)))
        idx= self.parse_atom()
        val=self.parse_atom()
        return ListOp('assign',Variable(m.identifier.word),idx,val)
    
    def parse_concat(self,m):
        self.lexer.match(Method('concat',Identifier(m.identifier.word)))
        next_str=self.parse_atom()
        return StringOp('add',Variable(m.identifier.word),next_str)
    
    def parse_slice(self,m):
        self.lexer.match(Method('slice',Identifier(m.identifier.word)))
        start=self.parse_atom()
        stop=self.parse_atom()
        step=self.parse_atom()

        return StringSlice('slice',Variable(m.identifier.word),start,stop,step)



    def parse_len(self,m):

        self.lexer.match(Method('len',Identifier(m.identifier.word)))


        return ListOp('length',Variable(m.identifier.word))

    def parse_atom(self):
        match self.lexer.peek_token():
            case Operator(value):
                self.lexer.advance()
                return Operator(value)
            case Identifier(name):
                self.lexer.advance()
                return Variable(name)
            case Num(value):
                self.lexer.advance()
                return NumLiteral(value)
            case Bool(value):
                self.lexer.advance()
                return BoolLiteral(value)
    def parse_for(self):
        self.lexer.match(Keyword('for'))
        c=self.parse_expr()
        self.lexer.match(Keyword('up'))
        u=self.parse_expr()
        self.lexer.match(Keyword('do'))
        b=self.parse_expr()
        # self.lexer.match(Keyword('endfor'))
        return For(c,u,b)
    
    
    def parse_call(self):
        fn=self.parse_atom()
        
        match self.lexer.peek_token():
            case Markers('('):
                self.lexer.advance()
                args=[]
                while True:
                    match self.lexer.peek_token():
                        case Markers(")"):
                            self.lexer.advance()
                            break
                        case _:
                            while True:
                                args.append(self.parse_expr())
                                match self.lexer.peek_token():
                                    case Markers(','):
                                        self.lexer.advance()
                                    case _:
                                        break
                return FunCall(fn,args)
            case _:
                return fn


    def parse_power(self):
        left=self.parse_call()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op =="**":
                    self.lexer.advance()
                    m=self.parse_atom()
                    left=BinOp(op, left, m)
                case _:
                    break

        return left
    
    def parse_assign(self):
        left=self.parse_power()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op=="+=":
                    self.lexer.advance()
                    m=self.parse_atom()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left


            
    def parse_unary(self):
        left=self.parse_assign()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "++ --".split():
                    
                    self.lexer.advance()
                    left = UnOp(op, left)
                case _:
                    break
        return left

    def parse_mult(self):
        left = self.parse_unary()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "*/%" or op =="//":
                    self.lexer.advance()
                    m = self.parse_unary()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left

    def parse_add(self):
        left = self.parse_mult()
        
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "+-":
                    self.lexer.advance()
                    m = self.parse_mult()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left
    
    def parse_shift(self):
        left = self.parse_add()
        match self.lexer.peek_token():
            case Operator(op) if op in "<>" or op in "<< >>".split():
                self.lexer.advance()
                right = self.parse_add()
                return BinOp(op, left, right)
        return left

    def parse_bitwise(self):
        left = self.parse_shift()
        while True:
            match self.lexer.peek_token():
                case BitwiseOperator(op) if op in "& | ^":
                    self.lexer.advance()
                    right = self.parse_shift()
                    left = BinOp(op, left, right) 
                case _:
                    break
        return left
    
    def parse_cmp(self):
        left = self.parse_bitwise()
        match self.lexer.peek_token():
            case Operator(op) if op in "<= >= == != < >".split():
                self.lexer.advance()
                right = self.parse_bitwise()
                return BinOp(op, left, right)
        return left
    
    def parse_log(self):
        left = self.parse_cmp()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "and or":
                    self.lexer.advance()
                    right = self.parse_cmp()
                    left = LogOp(op, left, right) 
                case Operator(op) if op in "not":
                    self.lexer.advance()
                    left= LogOp(op, left) 
                case _:
                    break
        return left

    def parse_simple(self):
        return self.parse_log()
    
    


        

    def parse_expr(self):
        match self.lexer.peek_token():
            case Keyword("let"):
                return self.parse_let()
            case Keyword("if"):
                return self.parse_if()
            case Keyword("list"):
                return self.parse_list()
            case Keyword("for"):
                return self.parse_for()
            case Keyword("while"):
                return self.parse_while()
           
            case Keyword("String"):
                return self.parse_string()
            
            # List Methods
            case Method('length',Identifier(name)):
                return self.parse_length(Method('length',Identifier(name)))
            case Method('append',Identifier(name)):
                return self.parse_append(Method('append',Identifier(name)))
            case Method('get',Identifier(name)):
                return self.parse_get(Method('get',Identifier(name)))
            
            case Method('assign',Identifier(name)):
                return self.parse_assignment(Method('assign',Identifier(name)))
            
            case Method("len",Identifier(name)):
                return self.parse_len(Method("len",Identifier(name)))
            
            # String Methods

            case Method("concat",Identifier(name)):
                return self.parse_concat(Method("concat",Identifier(name)))
            
            case Method("slice",Identifier(name)):
                return self.parse_slice(Method("slice",Identifier(name)))

            # --------------
            
            case Keyword("print"):
                return self.parse_print()
            case Markers("{"):
                return self.parse_seq()
            case Keyword("letfun"):
                return self.parse_func()
            
            case _:
                return self.parse_simple()

with open(args.filename) as f:
    stream = Stream.from_file(f)
    lexer = Lexer(stream)
    parser = Parser.from_lexer(lexer)
    ast = Parser.parse_expr(parser)
    eval(ast)
    f.close()
