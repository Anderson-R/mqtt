import json
class Foo(object):
    def __init__(self, x=1, y=2, s="a"):
        self.x = x
        self.y = y
        self.s = s

foo = Foo(2,4,"b")
s = json.dumps(foo.__dict__)
print(s)

t = json.loads(s)
foo2 = Foo(**t)
print(foo2.x)
print(foo2.y)
print(foo2.s)