# (WIP) Python Function Prototypes
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) This project is currently WIP, so this readme is more to illustrate the goal of the project.


This library provides a way to define an prototype interface for problems that require a function parameter. It checks the parameter names, types and return types to ensure
that the input is correct. In case the functions does not match, it raises an exception with recommendations for what you were meant to type.
## Example
Lets start by defining an prototype interface
```python
import pyprototypes as ppt

@ppt.ParamChecker
def my_proto_type(income, tax, penalities):
	pass
```
This here will define a prototype with the name `my_proto_type`.  

Then to check weather or not a function follows the prototype
```python
def inpt_function(incm, tx, penaltis):
	...

my_proto_type.check(inpt_function)
# From here we can assume that the function is correct
```
Here the following error is thrown
```
Error in the signature of 'inpt_function' in <File of inpt function>   
* Parameter 'incm' is not supported, did you mean:
        - income
* Parameter 'penaltis' is not supported, did you mean:
        - penalities
* Parameter 'tx' is not supported, did you mean:
        - tax
```

The checker will ear tag the function, such that when it encounters it again, it will just skip it.
