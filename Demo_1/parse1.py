from start import *
import ast
class EndOfStream(Exception):
    pass

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

# Define the token types.

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

Token = Num | Bool | Keyword | Identifier | Operator | BitwiseOperator | List| String| Method


class EndOfTokens(Exception):
    pass

keywords = "if then else end while done let in list String len length do  for up print".split()
symbolic_operators = "+ - * / < > <= >= = ≠ ++ ==".split()
unary_operators="++ -- +=".split()
double_operators='>= <= << >>'.split()
word_operators = "and or not quot rem".split()
starting_braces='[ ('.split()
ending_braces='] )'.split()
quotes='"'
end_of_statement=";"

whitespace = " \t\n"

Bitwise_Operators="& | ^".split()

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
                case c if c in symbolic_operators: 
                    n=c
                    l=self.stream.next_char()
                    n+=l
                    if(n in unary_operators or n in double_operators):
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


                            elif c.isalpha() or c in starting_braces or c in ending_braces:
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

    def parse_let(self):
        self.lexer.match(Keyword('let'))
        c=self.parse_atom()
        self.lexer.match(Operator("="))
        b=self.parse_expr()
        self.lexer.match(Keyword("in"))
        a=self.parse_expr()
        return Let(c,b,a)
    
    def parse_print(self):
        self.lexer.match(Keyword('print'))
        p=self.parse_expr()
        self.lexer.advance()
        return PrintOp(p)
    

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
        return For(c,u,b)
    
    def parse_assign(self):
        left=self.parse_atom()
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
                case Operator(op) if op in "*/":
                    self.lexer.advance()
                    m = self.parse_atom()
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
    
    def parse_length(self,m):
        self.lexer.match(Method('length',Identifier(m.identifier.word)))
        return ListOp('length',Variable(m.identifier.word))

    def parse_cmp(self):
        left = self.parse_add()
        match self.lexer.peek_token():
            case Operator(op) if op in "<>" or op in "<= >= << >>".split():
                self.lexer.advance()
                right = self.parse_add()
                return BinOp(op, left, right)
        return left

    def parse_bitwise(self):
        left = self.parse_cmp()
        while True:
            match self.lexer.peek_token():
                case BitwiseOperator(op) if op in "& | ^":
                    self.lexer.advance()
                    right = self.parse_cmp()
                    left = BinOp(op, left, right) 
                case _:
                    break
        return left

    def parse_simple(self):
        return self.parse_bitwise()

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
            case Keyword("String"):
                return self.parse_string()
            case Method('length',Identifier(name)):
                return self.parse_length(Method('length',Identifier(name)))
            case Method("len",Identifier(name)):
                return self.parse_len(Method("len",Identifier(name)))
            case Keyword("print"):
                return self.parse_print()

            case _:
                return self.parse_simple()

def test_parse():
    def parse(string):

        return Parser.parse_expr (
            Parser.from_lexer(Lexer.from_stream(Stream.from_string(string)))
        )
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    # print(parse("if a+b > c*d then a*b + c + d else e*f/g end"))
    # print(parse('let a=3 in a*a end'))
    # print(parse('let a=list [1,2,3]  in a end')) #working fine
    # print(eval(parse('let a=list [1,2,3,4,5]  in len(a) end')))
    # print(parse('String "this is a string"'))
    # print(eval(parse('let abc= String "have a nice day sir" in len(abc) end')))
    # print(parse('list [1,2,3] end'))
    # print(eval(parse('let a=3 in a*a end')))
    # print(parse('if 3+4 >2 then 3 else 5 end'))
    # print(parse('let a =2 in a+4 end'))
    # print(eval(parse('if 3+4 > 8 then 3 else 5 end')))
    # print(eval(parse('let abc=list [1,2,3,4,5] in abc.length end')))
    # print(parse("let a=1 in for a<10 up a++ do print a end"))

def test_for():
    def parse(string):
    
        return Parser.parse_expr (
            Parser.from_lexer(Lexer.from_stream(Stream.from_string(string)))
        )
    
    # print(parse("let a=1 in let b=1 in for a<10 up a++ do print a+b end"))
    # eval(parse("let a=121 in let b=10 in a+1 in print b+a end"))
    # eval(parse('let a=1 in let b=1 in for a<10 up a++ do print b+=b*a end'))
    # (eval(parse('let a=4 in let b=9 in let c=1 in print c += b*a end')))
    # (eval(parse('let a=1 in let b=1 in for a<10 up a++ do print a+b end')))
    # Sum 10 digit
    eval(parse('let a = 1 in let b=0 in for a<=10 up a++ do print b+=a  end'))
    # print(parse('let a=1 in for a<2 up a++ do print a+2 in let b=1 in print b end'))
    # (eval(parse(' let b= String "Hello World" in let c= b.length in print c end')))
    # eval(parse('let b= String "hello world" in print b end '))
    

test_for()

with open("myfile.txt") as f:
    stream = Stream.from_file(f)
    lexer = Lexer(stream)
    parser = Parser.from_lexer(lexer)
    ast = Parser.parse_expr(parser)
    #print(ast)
    print(eval(ast))
    f.close()

