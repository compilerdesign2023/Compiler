from start import *
import pytest

# Test For Eval

def test_div_operator():
    a  = Variable("a")
    n1= NumLiteral(5)
    e2 = BinOp("/", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == 1

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("/", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == 2

    """
    should show error if divided by zero. 
    """
    # c = Variable("c")
    # n0 = NumLiteral(0)
    # e2 = BinOp("/", b, c)
    # e  = Let(c, n0, Let(b, n2,e2 ))
    # assert eval(e) == InvalidProgram

def test_modulus_operator():
    a  = Variable("a")
    n1= NumLiteral(5)
    e2 = BinOp("%", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == 0

    b = Variable("b")
    n2 = NumLiteral(11)
    e2 = BinOp("%", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == 1

def test_floor_div_operator():
    a  = Variable("a")
    n1= NumLiteral(5)
    e2 = BinOp("//", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == 1

    b = Variable("b")
    n2 = NumLiteral(15)
    e2 = BinOp("//", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == 3

def test_power_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp("**", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == 27

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("**", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == 1000

    """ Show an error of Invalid program from line 136"""
    # c = Variable("c")
    # n3 = NumLiteral(0)
    # e2 = BinOp("**", a, c)
    # e  = Let(a, n1, Let(b, n2,e2 ))
    # assert eval(e) == 0

def test_equal_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp("==", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == True

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("==", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == False

def test_not_equal_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp("!=", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == False

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("!=", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == True

def test_greter_than_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp(">", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == False

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp(">", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == True

def test_greter_than_equal_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp(">=", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == True

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp(">=", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == True

    c = Variable("c")
    n3 = NumLiteral(9)
    e2 = BinOp(">=", c, b)
    e  = Let(c, n3, Let(b, n2,e2 ))
    assert eval(e) == False

def test_less_than_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp("<", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == False

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("<", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == False

    c = Variable("c")
    n3 = NumLiteral(9)
    e2 = BinOp("<", c, b)
    e  = Let(c, n3, Let(b, n2,e2 ))
    assert eval(e) == True

def test_less_than_equal_operator():
    a  = Variable("a")
    n1= NumLiteral(3)
    e2 = BinOp("<=", a, a)
    e  = Let(a, n1, e2)
    assert eval(e) == True

    b = Variable("b")
    n2 = NumLiteral(10)
    e2 = BinOp("<=", b, a)
    e  = Let(a, n1, Let(b, n2,e2 ))
    assert eval(e) == False

    c = Variable("c")
    n3 = NumLiteral(9)
    e2 = BinOp("<=", c, b)
    e  = Let(c, n3, Let(b, n2,e2 ))
    assert eval(e) == True

def test_string():

    a=StringLiteral("hello ")
    b=StringLiteral("world! ")
    c=StringOp("add",a,b)
    print(eval(c))
    print(eval(StringOp('length',StringLiteral(eval(c)))))

    #print(eval(StringOp('slice',)))

    
    #concatenation of 3 words
    d=StringLiteral("This ")
    e=StringLiteral("is ")
    f=StringOp("add",d,e)
    g=StringLiteral("string")
    h=StringOp("add",f,g)
    print(eval(h))
    print(eval(StringOp('length',h)))

    #concatenation using Numliteral and Let should show error
    # a1=StringLiteral("dsdsd")
    # b1=NumLiteral(2)
    # c1=StringOp("add",a1,b1)
    # d1=Let(a1,b1,c1)
    # print(eval(d1))
    # print(eval(StringOp('length',d1)))

    #concatenation of a string with a empty string 
    a2=StringLiteral("Hello")
    b2=StringLiteral("")
    x=StringOp("add",a2,b2)
    print(eval(x))
    print(eval(StringOp('length',x)))

    y=StringLiteral("Welcome")
    slice = StringSlice("slice",y,1,5)
    print(eval(slice))
    assert eval(slice)=="elco"

    z=StringLiteral("HelloWorld")
    slice1=StringSlice("slice",z,3,8)
    print(eval(slice1))
    assert eval(slice1)=="loWor"

    y1=StringLiteral("Hello World")
    slice2=StringSlice("slice",y1,5,6)
    print(eval(slice2))
    assert(eval(slice2))==" "

    y2=StringLiteral("Rishi123")
    slice3=StringSlice("slice",y2,5,8)
    print(eval(slice3))
    assert(eval(slice3))=="123"

    #It gives error
    # y2=NumLiteral(2)
    # slice3=StringSlice("slice",y1,2,5)
    # print(eval(slice2))

    #test for compare

    d=StringLiteral("This world")
    e=StringLiteral("This ")
    f=StringOp("add",e,StringLiteral('world'))
    assert eval(f)==eval(d)

def test_UnBoolify():
    
    z=NumLiteral()
    s=Un_boolify(z)
    print(eval(s))
    assert eval(s)==False

    x=NumLiteral(0)
    a=Un_boolify(x)
    print(eval(a))
    assert eval(a)==False
    
    y=NumLiteral(3)
    w=Un_boolify(y)
    print(eval(w))
    assert eval(w)==True

    z=StringLiteral("")
    s=Un_boolify(z)
    print(eval(s))
    assert eval(s)==False

    z=StringLiteral("swfwr")
    s=Un_boolify(z)
    print(eval(s))
    assert eval(s)==True

def test_if_Else():

    a=NumLiteral(3)
    b=NumLiteral(4)
    condition=BinOp("<",a,b)
    conditonalBlock=IfElse(condition,NumLiteral(30),NumLiteral(12))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)==30

    a1=NumLiteral(10)
    b1=NumLiteral(6)
    condition1=BinOp("<",a1,b1)
    conditonalBlock=IfElse(condition1,StringLiteral("Ten is greater"),StringLiteral("Six is greater"))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)=="Six is greater"

    a=NumLiteral(0)
    b=NumLiteral(0)
    condition=BinOp("==",a,b)
    conditonalBlock=IfElse(condition,StringLiteral("Equal"),StringLiteral("Not Equal"))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)=="Equal"

    a=NumLiteral(10)
    b=NumLiteral(35)
    condition=BinOp("!=",a,b)
    conditonalBlock=IfElse(condition,StringLiteral("Not Equal"),StringLiteral("Equal"))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)=="Not Equal"

    a=NumLiteral(2)
    b=NumLiteral(3)
    e=BinOp("+",UnOp("-",a),BinOp("*",UnOp("++",a),b))
    condition=BinOp("==",e,NumLiteral(7))
    conditonalBlock=IfElse(condition,StringLiteral("Equal"),StringLiteral("Not Equal"))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)=="Equal"

    a=NumLiteral(4)
    b=NumLiteral(6)
    e1=BinOp("*",b,UnOp("++",BinOp("+", a,b)))
    condition1=BinOp("==",e1,NumLiteral(66))
    e2=BinOp("*",b,BinOp("-",UnOp("++",a),UnOp("--",b)))
    condition2=BinOp("==",e2,NumLiteral(0))
    conditonalBlock=IfElse(condition1,IfElse(condition2,StringLiteral("Equal To Zero"),StringLiteral("Not Equal To Zero")),StringLiteral("Not Equal to 66"))
    print(eval(conditonalBlock))
    assert eval(conditonalBlock)=="Equal To Zero"

def test_list():
    
    my_list=ListLiteral([1,3,5,7,9])
    e1=ListOp("append",my_list,NumLiteral(10)) #append
    print(eval(e1))
    #assert eval(e1)==[1, 3, 5, 7, 9, 10]

    e2=ListOp("length",my_list) #length
    print(eval(e2))
    #assert eval(e2)==6

    e3=ListOp("remove",my_list) #pop
    print(eval(e3))
    #assert eval(e3)==[1, 3, 5, 7, 9]
    
    my_list1=ListLiteral([11,13,15])
    e4=ListOp("append",my_list,my_list1) #appending list into another list
    print(eval(e4))
    #assert eval(e4)==[1, 3, 5, 7, 9, [11, 13, 15]]

    e5=ListOp("length",my_list1)
    print(eval(e5))
    #assert eval(e5)==3

    e6=ListOp("length",my_list)
    print(eval(e6))
    #assert eval(e6)==6

    e7=ListOp("append",my_list,ListOp("remove",my_list1))
    print(eval(e7))
    #assert eval(e7)==[1, 3, 5, 7, 9, [11, 13], [11, 13]]

    e8=ListOp("remove",my_list)
    print(eval(e8))
    #assert eval(e7)==[1, 3, 5, 7, 9, [11, 13]]

def test_unop():
    
    a=Variable("a")
    e1=NumLiteral(1) 
    e2=UnOp("++",e1)
    e3=UnOp("-",e1)
    e4=UnOp("--",e1)
    assert eval(e3)== -1
    assert eval(e2)==2
    assert eval(e4)== 0

    a=Variable("a")
    e1=NumLiteral(2)
    b=NumLiteral(1)
    e2=BinOp("+",b,BinOp("*",UnOp("--",e1),e1))     #1+((2--)*2) = 3
    assert eval(e2)==3
    
    
    e1=NumLiteral(10)
    b=NumLiteral(5)
    c=NumLiteral(2)
    e2=BinOp("+",UnOp("++",e1),BinOp("*",UnOp("-",c),b))     #(10++) + ((-2)*5) = 1
    assert eval(e2)==1

    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e3 = UnOp("++",Let(a, e1, BinOp("+", a, Let(a, e2, e2))))
    assert eval(e3)==26

def test_bit():
    # "Bitwise AND"
    a=NumLiteral(15)
    b=NumLiteral(4)
    c=BinOp("&",a,b)   
    assert eval(c)==4

    # "Bitwise OR"
    a=NumLiteral(12)
    b=NumLiteral(20)
    c=BinOp("|",a,b)
    assert eval(c)==28

    # "Bitwise XOR"
    a=NumLiteral(34)
    b=NumLiteral(41)
    c=BinOp("^",a,b)
    assert eval(c)==11

def test_ls_rs():
    
    # "Bitwise Right Shift"
    a=NumLiteral(10)
    b=NumLiteral(1)
    c=BinOp(">>",a,b)
    assert eval(c)==5

    # "Bitwise Left Shift"
    a=NumLiteral(8)
    b=NumLiteral(3)
    c=BinOp("<<",a,b)
    assert eval(c)==64

def test_cases_list_literal():
    # test for length using Variables
    l=ListLiteral([1,3,4])
    l.type=NumType
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = ListOp("length",l)
    e=Let(a,l,e2)
    assert eval(e)==3
    

    # test case for append operations
    e3 = ListOp("append",l,e1)
    d=Let(a,l,e3)
    
    assert eval(d)==[1,3,4,5]
    print(l.list_val)
    f=eval(d)
    assert f==[1,3,4,5,5]
    assert eval(d)==[1,3,4,5,5,5]

    l1=ListLiteral([23,45,12])
    l1.type=NumType
    l2=ListLiteral([89,93])
    l2.type=NumType
    a  = Variable("a")
    e2=ListOp('append',l1,l2)
    inp=Let(a,l1,e2)
    assert eval(inp)==[23,45,12,[89,93]]

    l1=ListLiteral([23,45,12])
    l1.type=NumType
    l2=ListLiteral([89,93])
    l2.type=NumType
    a1  = Variable("a")
    e2=ListOp('append',l1,l2)
    inp1=Let(a1,l1,ListOp('append',e2,NumLiteral(2000)))
    assert eval(inp1)==[23,45,12,[89,93],2000]

    # assign test
    l1=ListLiteral([23,45,12])
    l1.type=NumType
    e2=ListOp('assign',l1,NumLiteral(0),NumLiteral(90))
    assert eval(e2)==[90,45,12]

    # remove test
    l1=ListLiteral([23,45,12])
    l1.type=NumType
    c=ListOp('remove',l1)
    assert eval(c)==[23,45]

def test_unOp():
    v=Variable('v')
    e1=NumLiteral(5)
    e2=UnOp('--',v)
    c=Let(v,e1,BinOp('*',v,Let(v,e2,e2)))
    assert eval(c)==15

def test_LetConst():
    a = Variable("a")
    b = Variable("b")
    e1 = LetConst(b, NumLiteral(2), Put(a, BinOp("+", Get(a), Get(b))))
    e2 = LetConst(a, NumLiteral(1), Seq([e1, Get(a)]))
    # print(eval(e2))
    assert eval(e2) == 3

    # a = Variable("a")
    # b = Variable("b")
    # e1 = LetConst(b, NumLiteral(2), Put(a, BinOp("+", Get(a), Get(b))))
    # e2 = LetConst(b, NumLiteral(1), Seq([e1, Get(a)]))
    # print(eval(e2))

    #  Outpout of the above program is error msg Variable name exists.


def test_let_eval():
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, e2)
    assert eval(e) == 10
    e  = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert eval(e) == 22

def test_bit():
    # "Bitwise AND"
    a=NumLiteral(15)
    b=NumLiteral(4)
    c=BinOp("&",a,b)   
    assert eval(c)==4

    # "Bitwise OR"
    a=NumLiteral(12)
    b=NumLiteral(20)
    c=BinOp("|",a,b)
    assert eval(c)==28

    # "Bitwise XOR"
    a=NumLiteral(34)
    b=NumLiteral(41)
    c=BinOp("^",a,b)
    assert eval(c)==11

def test_ls_rs():
    
    # "Bitwise Right Shift"
    a=NumLiteral(10)
    b=NumLiteral(1)
    c=BinOp(">>",a,b)
    assert eval(c)==5

    # "Bitwise Left Shift"
    a=NumLiteral(8)
    b=NumLiteral(3)
    c=BinOp("<<",a,b)
    assert eval(c)==64

def test_for_iteration():
    v=Variable('v')
    n1=NumLiteral(0)
    s=NumLiteral(5)
    condition=BinOp("<",v,s)
    update=UnOp('++',v)
    # l=ListLiteral([1,2,4,5,6])
    # let=Let(v,s,BinOp('+',v,v))
    # print(eval(let))
    body=PrintOp(UnOp("++",v))

    # body=PrintOp()

    # array=ListLiteral([20,43,54,23340,3291])
    # body_array=PrintOp(ListOp("get",array,v))
    x=Variable('x')
    
    body = BinOp("+",x,v) 
    n2 = NumLiteral(0)
    f=Let(x,n2 ,Let(v,n1,For(condition,update,body)))
    eval(f)

def test_while():
    v=Variable('v')
    n1=NumLiteral(0)
    s=NumLiteral(9)
    condition=BinOp("<",v,s)

    body = PrintOp(UnOp("++", v))
    w = Whilethen(condition, body)
    l = Let(v,n1, w)
    eval(l)

#  Test Typechek
# test_let_eval()
# test_div_operator()
# test_modulus_operator()
# test_power_operator()
# test_floor_div_operator()
# test_equal_operator()
# test_not_equal_operator()
# test_greter_than_operator()
# test_less_than_operator()
# test_less_than_equal_operator()

def test_typecheck_BinOp():
    import pytest
    te = typecheck(BinOp("+", NumLiteral(2), NumLiteral(3)))
    assert te.type == NumType
    te = typecheck(BinOp("*", NumLiteral(2), NumLiteral(3)))
    assert te.type == NumType
    te = typecheck(BinOp("*", NumLiteral(2),BinOp("*", NumLiteral(2), NumLiteral(3)) ))
    assert te.type == NumType
    te = typecheck(BinOp("<", NumLiteral(2), NumLiteral(3)))
    assert te.type == BoolType
    te = typecheck(BinOp("==", NumLiteral(2), NumLiteral(2)))
    assert te.type == BoolType
    te = typecheck(BinOp("==", StringLiteral("a"), StringLiteral("a")))
    assert te.type == BoolType
    te = typecheck(BinOp(">", StringLiteral("a"), StringLiteral("b")))
    assert te.type == BoolType
    te = typecheck(BinOp(">", NumLiteral(1), StringLiteral("b")))
    assert te.type == BoolType

def test_typecheck_string():
    #add method
    tc=typecheck(StringOp('add',StringLiteral("hello"),StringLiteral("World")))
    assert tc.type==StringType

    #comparision method
    tc=typecheck(StringOp('compare',StringLiteral("hello"),StringLiteral("World")))
    assert tc.type==BoolType

    #numtype
    tc=typecheck(StringOp('length',StringOp('add',StringLiteral("hello"),StringLiteral("World"))))
    print(f"type: {tc.type}")
    assert tc.type==NumType




# test_let_eval()
# test_div_operator()
# test_modulus_operator()
# test_power_operator()
# test_floor_div_operator()
# test_equal_operator()
# test_not_equal_operator()
# test_greter_than_operator()
# test_less_than_operator()
# test_less_than_equal_operator()

# test_div_operator()
# test_modulus_operator()
# test_power_operator()
# test_floor_div_operator()
# test_equal_operator()
# test_not_equal_operator()
# test_greter_than_operator()
# test_less_than_operator()
# test_less_than_equal_operator()
# test_string()
# test_UnBoolify()
# test_if_Else()
# test_list()
# test_unop()
# test_ls_rs()
# test_bit()
# test_typecheck_BinOp()
