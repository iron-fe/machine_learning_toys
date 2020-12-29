from copy import deepcopy
from .math.basic_type import Int, Float, BaseType


class Vector:
    def __init__(self, data, shape=None, name='Unknown'):
        self.min_num = float("inf")
        self.max_num = float("-inf")
        self.name = name
        if not shape:
            self.shape = _inference_shape(data)
        else:
            self.shape = deepcopy(shape)

        if self.ndim > 1:
            _array = []
            for elem in data:
                if isinstance(elem, Vector):
                    _array.append(elem)
                else:
                    nv = Vector(elem, shape=self.shape[1:])
                    if nv.max_num > self.max_num:
                        self.max_num = nv.max_num
                    if nv.min_num < self.min_num:
                        self.min_num = nv.min_num
                    _array.append(nv)
            self.array = _array
        else:
            _array = []
            for elem in data:
                if isinstance(elem, int):
                    elem = Int(elem)
                elif isinstance(elem, float):
                    elem = Float(elem)
                elif isinstance(elem, BaseType):
                    pass
                else:
                    raise TypeError
                if elem.val > self.max_num:
                    self.max_num = elem.val
                if elem.val < self.min_num:
                    self.min_num = elem.val
                _array.append(elem)
            self.array = _array


    def __getitem__(self, index):
        def recursive_getitem(vector, index_):
            if len(index_) > 0:
                res_array_ = []
                if isinstance(index_[0], slice):
                    for elem in vector.array[index_[0]]:
                        res_array_.append(recursive_getitem(elem, index_[1:]))
                else:
                    res_array_ = recursive_getitem(vector.array[index_[0]], index_[1:])
            else:
                return vector
            return res_array_

        if isinstance(index, int):
            return self.array[index]

        elif isinstance(index, slice):
            start = index.start if index.start else 0
            end = index.stop if index.stop else self.shape[0]
            step = index.step if index.step else 1
            res_array = [self[i].array if isinstance(self[i], Vector) else self[i] for i in range(start, end, step)]

        elif isinstance(index, tuple) or isinstance(index, list):
            if len(index) < self.ndim:
                index = list(index)
                index.extend([slice(None, None, None)] * (self.ndim - len(index)))
            res_array = recursive_getitem(self, index)
        else:
            raise Exception()
        if isinstance(res_array, list):
            return Vector(res_array)
        else:
            return res_array

    def __setitem__(self, key, value):
        def cast(value):
            if isinstance(value, int):
                return Int(value)
            elif isinstance(value, float):
                return Float(value)
            else:
                return value

        def recursive_setitem():


        if isinstance(key, int):
            self.array[key] = cast(value)
        elif isinstance(key, slice):
            start = key.start if key.start else 0
            end = key.stop if key.stop else self.shape[0]
            step = key.step if key.step else 1
            for i in range(start, end, step):
                self.array[i] = cast(value[i])
        elif isinstance(key, list) or isinstance(key, tuple):
            if len(key) < self.ndim:
                key = list(key)
                key.extend([slice(None, None, None)] * (self.ndim - len(key)))
            recursive_setitem(self, key, value)


    def __str__(self):
        max_l = len(str(self.max_num))
        def recursive_print_vector(vector):
            if isinstance(vector, Vector):
                res = []
                for i, elem in enumerate(vector.array):
                    s = recursive_print_vector(elem)
                    if isinstance(vector.array[0], Vector):
                        if i == len(vector.array) - 1:
                            res.append(str(s))
                        else:
                            res.append('%s\n' % s)
                    else:
                        offset = max_l - len(s)
                        prefix = ' ' * offset
                        res.append('%s%s' % (prefix, s))
                return '[' + ' '.join(res) + ']'
            else:
                return str(vector)
        return recursive_print_vector(self)

    @property
    def ndim(self):
        return len(self.shape)

    def transpose(self, axises=None):
        new_shape = [self.shape[axises[i]] for i in range(self.ndim)]
        new_vec = zeros(new_shape)
        curr_index = [0 for _ in range(self.ndim)]
        target_idx = [0 for _ in range(new_vec.ndim)]
        while 1:
            for axis in range(self.ndim - 1):
                if curr_index[axis] == self.shape[axis]:
                    curr_index[axis] = 0
                    curr_index[axis + 1] += 1
            if curr_index[-1] >= self.shape[-1]:
                break
            for i, j in enumerate(axises):
                target_idx[i] = curr_index[j]
            new_vec[target_idx] = self[curr_index]
            curr_index[0] += 1
        return new_vec


def zeros(shape, _creator=None):
    array = create_array_by_shape(shape, 0)
    return Vector(array, shape=shape)


def ones(shape, _creator=None):
    array = create_array_by_shape(shape, 1)
    return Vector(array, shape=shape)


def _inference_shape(data):
    shape = []
    while isinstance(data, list):
        shape.append(len(data))
        data = data[0]
    return shape


def create_array_by_shape(shape, val):
    if isinstance(shape, int):
        return val
    else:
        new_shape = shape[1:] if len(shape) > 1 else shape[0]
        return [create_array_by_shape(new_shape, val) for _ in range(shape[0])]
