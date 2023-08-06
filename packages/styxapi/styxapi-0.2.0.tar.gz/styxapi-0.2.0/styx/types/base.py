
class Type:
    def visit(self, visitor, *args):
        func = getattr(visitor, f'visit_{ type(self).__name__.lower() }')
        return func(self, *args)

    def __str__(self):
        return type(self).__name__


class String(Type):
    pass


class Integer(Type):
    pass


class Boolean(Type):
    pass


class Null(Type):
    pass


class Object(Type):
    def __init__(self, fields):
        self.fields = fields


class List(Type):
    def __init__(self, type_):
        self.type = type_


class Any(Type):
    pass


class Const(Type):
    def __init__(self, value):
        self.value = value


class Reference(Type):
    def __init__(self, name):
        self.name = name


class OneOf(Type):
    def __init__(self, *types):
        self.types = types


class Unset(Type):
    class UNSET:
        pass


def optional(type_):
    return OneOf(type_, Unset())
