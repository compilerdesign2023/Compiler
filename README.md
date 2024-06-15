# **Thorium Documentation**


```
Language Description :Thorium is under development,a high-level, general-purpose
programming language created as part of the CS 327 course at IITGN.Thorium emphasis on expressiveness.
```
## DataTypes
```
**1. Numeric**
    NumType->Integer|Fraction
    IntType->Integer
    Fractype->Fraction
**2. String**
    StringType->str
**3. List**
    ListType->list
**4. Boolean**
    BoolType->bool
**5. Variable**
    VarType->var
```

## Operators:

**1. BinaryOperators:**
    **Input** - BinOp(“Operator”,left,right)
    **Operators-** + - * /// ** %
    **Operand(left,right)-** NumType|IntType|FracType|Vartype


```
(+):sumsupleftandright
return eval(left)+ eval(right)
(-): differenceofleftandright
return eval(left)- eval(right)
(*):productofleftandright
return eval(left)* eval(right)
(/):dividesofleftwithright
return eval(left)/ eval(right)
(//):floordivision
return eval(left)// eval(right)
(%):modulooperator
return eval(left)+ eval(right)
(**):poweroperator,lefttothepowerright
return eval(left)** eval(right)
```
( **Note:** The return type of the result is the same as types of left and right both, it is int if the      resultant value is integer and float if result contains decimal. 
IntType operand only allows operations to be executed with IntType operand for division, same goes for FracType
)

**2. ComparisonOperators:**
    **Input** - BinOp(“Operator”,left,right)
    **Operators-** == != < > >= <=
    **Operand(left,right)-** NumType|Vartype
    **ReturnType-** BoolType

```
(==): Checks if two values are equal
(!=): Checks if two values are not equal
(<): Checks if the value on the left is less than right
(>): Checks if the value on the left is greater than right
(<=) : Checks if the value on the left is less than or equal to the right
(>=): Checks if the value on the left is greater than or equal to the rig

```

**3. BitwiseOperators** :& |^ >> <<
    **Input** - BinOp(“Operator”,left,right)
    **Operators-** & |^ >> <<
    **Operand(left,right)-** NumType|Vartype


**4. UnaryOperators**

Input - UnOp(“Operator”,“Operand”)
Operators- “-”,”++”,“--”
Operand- NumType

```
(-):Unarynegation,negatesvalue
return “-Operand”
(++):Incrementsthevaluebyone
return “Operand+1”
(--):Decrementsthevaluebyone
return “Operand-1”
```
**5. PrintOperation**
    **Input-** PrintOp(‘AST’)
    return print(eval(‘AST’))

```
(Note:fornowPrintOPonlytakeoneASTasinput)
```
**6. AssignmentOperators** :+=
    **Input** - BinOp(“+=”,left,right)
    **Operandtype:** left-VarType
       right-NumType|VarType

## Variables:

1. **Mutable:** aredefinedwithlet
2. **Immutable:** aredefinedwithletconst.

**List Methods:**

1. **Append**

Append elements into the list.
```
i)
**Example-** i)ListOp(“append”,ListLiteral([1,2,3,4,5]),NumLiteral(10)
ii)
ListOp(“append”,ListLiteral([1,2,3,4,5]),ListLiteral([5,6,7,7]))
```
2. **Length**

Returns the length ofthe list. 
**Example-**
```
ListOp(“length”,ListLiteral([1,2,3]))
```
3. **Remove**

Removes the last element ofthe list. 
**Example-** 
```ListOp(“remove”,my\_list)```

4. **Assign**

Assign elements to the index ofthe array.
```
**Structure:**ListOp(“assign”,array,index,assign\_value)

**Example-** ListOp(“assign”,ListLiteral([1,2,3,4]),NumLiteral(1),NumLiteral (10))
```
5. **Get**

Returns element ofa particular index.
```
**Structure:**ListOp(“get”,array,index) **Example**-ListOp(“get”,ListLiteral([1,2,3]),NumLiteral(1))
```

**String Methods:**

1. **Length**

Returns String Length.

Example-
```
StringOp(‘length’,StringLiteral(“Hello World”))
```

2. **Add**

Concatenates two strings.

Example- 
```StringOp(“add”,StringLiteral(“Hello”),StringLiteral(“World”))```


3. **Compare**

Compare two strings. Example-

StringOp(“compare”,StringLiteral(“Hello”),StringLiteral(“World”

))

4. **Slicing**

Return the sliced strings. Structure:StringSlice(“slice”,String,start,stop,step)

**Control Statements:**

1. **If-Else statement**

**Input-** IfElse(BinOp(“<”,NumLiteral(1),NumLiteral(89)),NumLiteral(30),N umLiteral(12))

**Input Type:**

i)condition- ‘AST’ ii)then -’AST’ iii)else -’AST’

2. **While loop**

**Input-** Let(Variable(“v”),NumLiteral(0),Whilethen(BinOp(“<”,v,NumLitera l(10)), PrintOp(UnOp(“++”,v))))

**Input Type:**

i)condition- ‘AST’ ii)body - ‘AST’

3. **Forloop**

**Input-** Let(Variable(“v”),NumLiteral(0),For(condition,update,body))

**Input Type:**

i)condition: ‘AST’ ii)update: ‘AST’ iii)body: ‘AST’

**Functions :**

1) **LetFun**

**Input- LetFun(Variable(‘f’),[Variable(‘a’),Variable(‘b’)],BinOp(‘+’,a,b),FunC all(f,[NumLiteral(10),NumLiteral(4)]))**

**Input Type:**

i)Function Name : ‘Variable’ ii)parameters: List[‘AST’] iii)body: ‘AST’ iv)Expression: ‘AST’

2) **FunCall Input-FunCall(f,[NumLiteral(10),NumLiteral(4)])**

**Input Type:**

i)Function Name : ‘Variable’ ii)arguments: List[‘AST’]

**Scoping:**

**1. Let Statement**

**Precedence:**

Assign Bitwise Unary

Multi div Add sub Comparison

**TypeChecking**

1. This verifies that the defined value for each data type matches the type that was initially specified.

NumLiteral() as NumType BoolLiteral() as BoolType String Literal() as StringType ListLiteral() as ListType IntLiteral() as IntType FractLiteral() as FracType Variable() as VarType

2. The same goes for the operations (BinOp, UnOp, StringOp) performed by these defined values, which have the same datatype as the specified.

BinOp(“+”,NumLiteral(1),NumLiteral(2))

#this BinOp operation will have type NumType

3. The return type of if-else statements is consistent and matches the type of the returned value.

if (cond) then (body) else (body)

#evaluated value of body is assigned as the type

4. Typecheck on Multiple Number types like IntLiteral and FracLiteral is done for Division Operation (to be done for each BinOp)
4. Types ofWhilethen,For,PrintOp are not specified.
4. Typecheck on Variables (VarType)is yet to be done
