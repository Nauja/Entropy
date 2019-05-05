---
title: "Entropy Guidelines"
document: Draft 0.1
date: 2019-04-07
author:
  - name: Jérémy Morosi
    email: <jeremymorosi@hotmail.fr>
---

# Introduction

**There must exist universal coding guidelines reflecting how nature works.**

Entropy is a coding standard aimed to help you writing code easier to understand, maintain and unit test.

It works by defining a set of simple rules that encourage you to write code that tend to mimic how nature works. They emerged from the main idea that our code can be easier to understand when it reflects the fact that nature is composed of a multitude of independent systems each having little responsibilities rather than a single one system with a lot. Thus it can be seen as the single responsibility principle.

Of course we don't fully understand how nature works, but this is a k-approximation; and examples will prove that code written this way tend to be clearer. Ultimately it provides a way to measure entropy in your code and use it as a metric to identify and improve parts of your code that can be.

# Motivation and Scope

These guidelines emerged from the fact that we often tend to
write big monolithic codebase that we can hardly maintain and
we can't remember/explain how it works days later. The goal
is to prevent such things to happen by providing coding guidelines
that - when applied correctly - help us to write code that mimic
how nature works; thus producing a high amount of entropy.

But why entropy ? Think about the efforts required to keep
a house clean. It naturally tend to be in disorder because
this is simply how entropy works. Cleaning a house is like lowering
the amount of entropy by reorganizing everything. Such process
requires a lot of energy and it goes the same for your
code.

If you are afraid of your code becoming obsolete or
afraid of having someone else working on it because you
know it's too complex for him to understand, it's because you
are trying to maintain a codebase with too much functionalities,
responsibilities or organization; which is equivalent to
trying to keep it's amount of entropy low by spending a lot
of efforts and energy.

Now, what would a codebase with a hight amount of entropy
be like ? Functionalities would be written as separate and
independent subprojects. Understanding how a functionality
works and is written would require little effort and it would
be easy to write unit tests covering as much code as possible.
The best is that you wouldn't be afraid of having to rewrite
your code if it became obsolete or broken.

This is what these guidelines are about. Not how writing
high performance code in a specific language, but how
organizing it to result into a high amount of entropy, requiring
less efforts to maintain.

# Whole principle explained with one simple example

This example is going to be overkill but will help us concentrate on
what interest us here: how to make up our mind to write code that is
easily documentable, readable, testable and maintainable.

Let's take the case of a simple function such as `sum`:

```python
def sum(a:int, b:int) -> int:
    return a + b
```

## Responsibilities beyond its scope

The most important when writing code is to keep in mind what its
added value is. We are writing something that transforms some inputs
to generate some outputs and one common pitfall is to write it according to
the way we think its users are going to use it instead of its added value,
ending up with something like this:

```python
def sum(filename:str) -> int:
    v = 0
    with open(filename, "r") as f:
        v += int(f.readline())
```

Here we have a function that sum numbers written on each line of a file.
Why ? Because we think this is the most common way it's going to be used.
Let's be clear, this shouldn't be the responsibility of this function
to read numbers from a file or to even know what a file is.

First principle to keep in mind is that it becomes way too complex
to document, read, test or maintain something when it has responsibilities
beyond its scope, thus it should be avoided as much as possible by limiting
its scope to its added value.

## No added value

Now, talking about added value, does our `sum` function even have one ?
Let's try to document it:

```python
def sum(a:int, b:int) -> int:
    """Sum two numbers.
    
    :param a: first number
    :param b: second number
    :returns: a + b
    """
    return a + b
```

It's straightforward. This is what you would answer to someone asking what
the function does: "well, it's called sum, it sum two numbers". That person
would look at you and ask why you didn't simply write `a + b` and he would
be right. The problem here is that this function doesn't have enough added
value to exist on its own.

So, let's try to add some added value to it:

```python
def calc(a:int, b:int, *, op:Optional[Callable[[int,int],int]] = None) -> int:
    """Perform an operation on two numbers.
    
    >>> calc(1, 2)
    3
    >>> calc(1, 2, operator.add)
    3
    >>> calc(1, 2, operator.mul)
    2
    
    :param a: first number
    :param b: second number
    :param op: operation or operator.add by default
    :returns: result of op applied to a and b
    """
    op = op or operator.add
    return op(a, b)
```

Here we wrote a more generalized version of our `sum` function by simply moving `+` operator - previously
implicit because of function's name - to an optional parameter defaulting
to the builtin `operator.add` function. As a side effect, we now have a useful documentation
with examples of usage because it becames easy to explain what the added value is and how it
can be used.

Second principle to keep in mind is that having difficulties to write useful documentation
or unit test for your code can be a hint that it doesn't have enough added value
to exist on its own and should be removed or generalized to something else.

## Too much assumptions

What we can say about the `calc` function is that it takes two numbers and apply a lambda to it.
But why only two numbers ? And why does `type hints` indicate it should be `int` ?
Making too much assumptions about functions parameters is another pitfall as it make your
code closed to extension.

Let's see how it can be improved:

```python
def calc(*numbers:List[Any], op:Optional[Callable[[Any,Any],Any]] = None, initial:Any = None) -> Any:
    """Perform an operation on numbers.
    
    >>> calc()
    0
    >>> calc(1, 2, 3)
    6
    >>> calc(1, 2, 3, initial=1)
    7
    >>> calc(1, 2, 3, operator.add)
    6
    >>> calc(1, 2, 3, operator.mul)
    6
    
    :param numbers: list of numbers
    :param op: operation or operator.add by default
    :param initial: initial sequence value
    :returns: result of op applied to numbers
    """
    op = op or operator.add
    initial = initial if initial is not None else 0
    for n in numbers:
        initial = op(initial, n)
    return initial
```

As you can see by `type hints` and documentation, our `calc` function became
generic enough to handle an arbitrary amount of numbers of any type and apply
the lambda on them. We also added a new parameter `initial` because this is
not the responsibility of `calc` to know what the initial value will be (first principle)
and we don't want to close our code to extension by making assumptions on it (this principle).

This open your code to extension and allow others to use it in cases you didn't
even expect they would:

```python
>>> calc("hello", " ", "world", " !", initial="")
hello world !
>>> calc(*"hello world !", op=lambda a, b: a + ord(b))
1181
```

Third principle to keep in mind is that simplicity, readability and extensibility
of your code can be greatly improved by making the less assumptions possible
about inputs and allowing users to override these assumptions by providing
optional parameters.

## Good naming is as important as good coding

At this stage you should notice that the added value of our function changed from
`applying an operator to two numbers` to `applying a lambda to pair of elements in a sequence` as
shown by the `"hello world !"` example.

Name of the function is no more related to its added value so we are going to change it:

```python
def reduce(fun:Callable[[Any,Any],Any], *sequence:List[Any], initial:Any = None) -> Any:
    """Apply a function on pair of elements of a sequence.
    
    >>> reduce(operator.add, 1, 2, 3)
    6
    >>> reduce(operator.add, 1, 2, 3, initial=1)
    7
    >>> reduce(operator.add, " ", "world", " !", initial="hello")
    hello world !
    
    :param fun: function to apply
    :param sequence: sequence of elements
    :param initial: initial sequence value
    :returns: result of fun applied to pair of elements
    """
    it = iter(sequence)
    initial = initial if initial is not None else next(it)
    for _ in it:
        initial = fun(initial, _)
    return initial
```

We renamed the `calc` function to `reduce` which is a more suitable name for such function.
As a side effect, the `op` parameter has been renamed to `fun` and is now mandatory because
there is no way our function can guess what the default value would be and we don't want to
make such assumption.

Fourth principle to keep in mind is that having difficulties to determine the added value or
scope of a function or to write documentation, unit tests for it may indicate that it is poorly
named. As a programmer, finding the right name for something is as important as writing good code because
a name can totally change the way you look at it or the responsibilities you would give
to it.

## Conclusion

# Readability

## Mixed coding conventions

You shouldn't mix multiple coding conventions together.

Yes:
```python
def first_function():
    pass

def second_function():
    pass
```

No:
```python
def firstFunction():
    pass

def second_function():
    pass
```

Measure:
```python
'''
max entropy is the number of symbols in parent.
value is the number of symbols following the coding convention.
'''
def entropy(parent, conventions):
    symbols = find_symbols(parent)
    default = matching_convention(symbols[0], conventions)
    return {
        "max": len(symbols),
	"value": count_matching(symbols, default)
    }
```

Notes:

* Default convention may be the one of first encountered symbol
* This should only take locally defined symbols into account
* Multiple coding conventions can be used but shouldn't be
mixed together inside of one function, or class, ...

# Functions

Function related rules.

## Function has too many calls

A function shouldn't have responsibilities beyond its scope.

Hints can be:

* A name stating `x_or_y`
* Too many calls to other functions
* Difficulty to explain how it works

Yes:
```python
def get_user(login, password):
    return db.find_user(login, password)

def create_user(login, password):
    user = User(login, password)
    db.insert_user(user)
    return user

check_login(login)
check_password(password)
user = get_user(login, password)
if not user:
    user = create_user(login, password)
```

No:
```python
def get_or_create_user(login, password):
    check_login(login)
    check_password(password)
    user = db.find_user(login, password)
    if not user:
        user = User(login, password)
        db.insert_user(user)
    return user
```

Measure:
```python
'''
1 when n <= eps
0 when n >= threshold
'''
def entropy(fun, threshold):
    n = count_calls_from(fun)
    return {
        "max": 1,
	"value": 1 - clamp(threshold / n, 0, 1)
    }
```

Notes:

* Calls to lambda functions passed as arguments shouldn't
be considered because they are expected to be called

## Function has too many signatures

A function shouldn't have responsibilities beyond its scope.

Hints can be:

* Too many signatures
* Too many parameters to achieve same result

Yes:
```python
def parse(source):
    ...

with open(filename, "r") as f:
    r = parse(f.read())
```

No:
```python
def parse(source):
    ...

def parse_file(filename):
    with open(filename, "r") as f:
    	return parse(f.read())

r = parse_file("...")
```

Measure:
```python
'''
# todo
```

Notes:

* Is it your responsibility of your code to handle all possible cases
or the one of calling function
* Prefer one variant with a common interface as parameter rather than
multiple variants

## Function parameters could be packed

Multiple parameters that are always passed together
should be packed together.

Hints can be:

* Too many parameters in the signature
* Passing most of them from one function to another

Yes:
```python
class Rect:
    def __init__(x, y, width, height):
        ...
        
def area(rect):
    return rect.width * rect.height

def compare(rect1, rect2):
    return compare(area(rect1), area(rect2))
```

No:
```python
def area(w, h):
    return w * h

def compare(w1, h1, w2, h2):
    return compare(area(w1, h1), area(w2, h2))
```

Measure:
```python
'''
1 when n <= eps
0 when n >= max
'''
def compute(fun, threshold):
    n = eps
    for call in get_calls_from(fun):
        n = max(n, count_same_args(call, fun))
    return {
        "max": 1,
	"value": 1 - clamp(threshold / n, 0, 1)
    }
```

Note:

* This is in no way an indicator of functions having too many
parameters

## Function makes too many assumptions

A function should make the less assumptions possible about its parameters.

Hints:

* Too restrictive parameters
* Code closed to outside

Yes:
```python
def default_load(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def default_parse(input: Any, *, load: Callable[[Any], str] = None) -> str:
    load = load or default_load
    content = load(input)
    # do something
    return result

def run(inputs: List[Any], *, parse: Callable[[List[Any]], str] = None) -> List[str]:
    parse = parse of default_parse
    return [parse(input) for input in inputs]

# Custom parse function for str inputs
def parse_string(input: str) -> str:
    return default_parse(input, load=lambda _: _)
    
run(["/some/path"])
run(["/some/path"], parse=default_parse)
run(["hello world !"], parse=parse_string)
```

No:
```python
def parse(input: str) -> str:
    with open(input, "r") as f:
        content = f.read()
        # do something
        return result

def run(inputs: List[str]) -> List[str]:
    return [parse(input) for input in inputs]

run(["/some/path"])
```

In `No` example, `run` is expecting to be called with a list of
filenames and let `parse` read them. This is wrong because users
wan't to use `parse` for the functionality it provides and there is
no reason here to restrict it to files. In `Yes` example, `run` and
`parse` are taking optional callables so that users can customize how
inputs are converted to string for being parsed, thus providing the
exact same functionality, but for any inputs.
