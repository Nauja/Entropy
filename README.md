# Entropy - Coding Standard

Language agnostic coding standard and static code analysis tool.

## Introduction

**There must exist universal coding guidelines reflecting how nature works.**

Entropy is a coding standard aimed to help you writing code easier to understand, maintain and unit test.

It works by defining a set of simple rules that encourage you to write code that tend to mimic how
nature works. They emerged from the main idea that our code can be easier to understand when it reflects the
fact that nature is
composed of a multitude of independent systems each having little responsibilities rather than
a single one system with a lot. Thus it can be seen as the [single responsibility principle](https://en.wikipedia.org/wiki/Single_responsibility_principle).

Of course we don't fully understand how nature works, but this is a k-approximation; and examples
will prove that code written this way tend to be clearer.
Ultimately it provides a way to measure entropy in your code and use it as a metric to identify and
improve parts of your code that can be.

Feedback is most welcome !

## Documents

* [Draft.md](Draft.md): Unstable version of the standard (markdown)
* [Draft.pdf](pdf/Draft.pdf): Unstable version of the standard (pdf)

## Tools

* [PyRabbit](https://github.com/Nauja/pyrabbit): Static code source analysis for Python

## Rules format

Rules are written as follow:
<html>
<blockquote>
<h3>Rule's name</h3>
<hr/>
<i>Short description.</i><br/><br/>
Hints can be:<br/>
<ul><li><i>list of tips to detect this case</i></li></ul>
  
Yes:
```python
# Something to do
```

No:
```python
# Something to avoid
```

Measure:
```
# How to measure entropy
```

Notes:<br/>
<ul><li><i>special notes</i></li></ul>

</blockquote>
</html>
