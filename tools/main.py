import ast
from functools import reduce

MAX_CALLS = 10


def func_entropy(n_calls, max_calls):
	return max(min(1 - (n_calls / max_calls), 1), 0)

def percent(v):
	return int(v * 100.0)


class Stack:
	def __init__(self):
		self.__inner = []
		self.__depth = -1

	def push(self, e):
		self.__inner.append(e)
		self.__depth += 1

	def pop(self):
		e = self.__inner[self.__depth]
		del self.__inner[self.__depth]
		self.__depth -= 1
		return e

	@property
	def peek(self):
		return self.__inner[self.__depth]

	def __len__(self):
		return len(self.__inner)


class Analyzer(ast.NodeVisitor):
	def __init__(self):
		self.stack = Stack()

	def visit_ClassDef(self, node):
		self.stack.push({
			"type": "class",
			"functions": []
		})
		self.generic_visit(node)
		infos = self.stack.pop()
		entropy = reduce(lambda x, y: x * y, infos["functions"])
		print("class", node.name)
		print(len(infos["functions"]), "functions")
		print("{}% entropy".format(percent(entropy)))
		print()

	def visit_FunctionDef(self, node):
		self.stack.push({
			"type": "func",
			"calls": 0
		})
		self.generic_visit(node)
		infos = self.stack.pop()
		entropy = func_entropy(infos["calls"], MAX_CALLS)
		print("function", node.name)
		print(infos["calls"], "calls")
		print("{}% entropy".format(percent(entropy)))
		print()

		if len(self.stack) and self.stack.peek["type"] == "class":
			self.stack.peek["functions"].append(entropy)


	def visit_Call(self, node):
		if self.stack:
			self.stack.peek["calls"] += 1
		self.generic_visit(node)

def main():
	def wrap():
		pass

	with open("sample.py", "r") as f:
		content = f.read()

	tree = ast.parse(content)
	analyzer = Analyzer()
	analyzer.visit(tree)

if __name__ == '__main__':
	main()