# (WIP) Python Function Prototypes
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) This project is currently WIP, APIs are very much subject to change.

This library currently provides a `Prototype` class which can check names of inpt functions
and their associated types (optional). It also provides a fixture system inspired by pytest, which allows you to defined default values for the input function based on other functions. You can also nest the fixtures like pytest.

The goal is to also provide a "class" prototype which allows you to bind a protocol to a class
and their properties.

# Examples
## Names and types
Here is an example of current functionality
```python
from pyprototypes.prototype import Prototype


@Prototype
def proto(income: int, tax: int, penalities: int):
	pass


def inpt_function(incm: int, tx: int, penalities: float): ...


proto.check(inpt_function)
# From here we can assume that the function is correct
```
Here the following error is thrown
```python
pyprototypes.exceptions.UnsupportedParameters: 
Error in the signature of 'inpt_function' in <path-to-file>
* Parameter 'incm' is not supported, did you mean:
        - income
* Parameter 'tx' is not supported, did you mean:
        - tax
* Wrong Type - Parameter 'penalities'
         it is 'float' it should be 'int'
```
## Fixtures
```python
from pyprototypes.prototype import Prototype


@Prototype
def proto(foo: int, bar: str):
	pass


@proto.fixture
def qar():
	return 60


@proto.fixture
def foo():
	return "Hello world"


@proto.fixture
def bar(qar):
	return qar + 2


def testfunc(bar: int, foo: str):
	print(str(bar) + " " + foo)


wrapped = proto.check(testfunc)
wrapped()
```
This will print:
```shell
$ 62 Hello world
```