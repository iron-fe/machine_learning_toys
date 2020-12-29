class BaseType:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return self.val != other.val

    def __gt__(self, other):
        return self.val > other.val

    def __lt__(self, other):
        return self.val < other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __le__(self, other):
        return self.val <= other.val


class Int(BaseType):
    def __init__(self, val):
        if isinstance(val, int):
            pass
        elif isinstance(val, float):
            val = int(val)
        elif isinstance(val, Float):
            val = int(val.val)
        else:
            raise ValueError
        super().__init__(val)

    def __add__(self, other):
        return Int(self.val + other.val)

    def __sub__(self, other):
        return Int(self.val - other.val)

    def __mul__(self, other):
        return Int(self.val * other.val)

    def __truediv__(self, other):
        return Int(self.val / other.val)

    def __floordiv__(self, other):
        return Int(self.val // other.val)

    def __and__(self, other):
        return Int(self.val & other.val)

    def __or__(self, other):
        return Int(self.val | other.val)

    def __xor__(self, other):
        return Int(self.val ^ other.val)

    def __divmod__(self, other):
        return Int(self.val % other.val)


class Float(BaseType):
    def __init__(self, val):
        if isinstance(val, float):
            pass
        elif isinstance(val, int):
            val = float(val)
        elif isinstance(val, Int):
            val = float(val.val)
        else:
            raise TypeError
        super().__init__(val)

    def __add__(self, other):
        return Float(self.val + other.val)

    def __sub__(self, other):
        return Float(self.val - other.val)

    def __mul__(self, other):
        return Float(self.val * other.val)

    def __truediv__(self, other):
        return Float(self.val / other.val)

    def __floordiv__(self, other):
        return Float(self.val // other.val)

    def __and__(self, other):
        return Float(self.val & other.val)

    def __or__(self, other):
        return Float(self.val | other.val)

    def __xor__(self, other):
        return Float(self.val ^ other.val)

    def __divmod__(self, other):
        return Float(self.val % other.val)