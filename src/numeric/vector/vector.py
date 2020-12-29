from copy import deepcopy



class Vector:
    def __init__(self, data, shape=None, requires_grad=True, _creator=None, grad=None, name='Unknown'):
        if not shape:
            shape = _inference_shape(data)
        else:
            shape = deepcopy(shape)
        if len(shape) > 1:
            self.array = [elem if isinstance(elem, Vector) else Vector(elem, shape=shape[1:]) for elem in data]
        else:
            _array = []
            for elem in data:
                if isinstance(elem, int):
                    elem = Int(elem)
                elif isinstance(elem, float):
                    elem = Float(elem)
                elif isinstance(elem, BaseType):
                    pass
                _array.append(elem)
            self.array = _array

        self.shape = shape
        self._creator = _creator
        self.requires_grad = requires_grad
        self.grad = grad
        self.name = name

    def __getitem__(self, index):
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

            res_array = recursive_getitem(self, index)

        else:
            raise Exception()
        if isinstance(res_array, list):
            return Vector(res_array)
        else:
            return res_array

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if isinstance(value, BaseType):
                self.array[key] = value
            elif isinstance(value, int):
                self.array[key] = Int(value)
            elif isinstance(value, float):
                self.array[key] = Float(value)
            else:
                self.array[key] = value
        elif isinstance(key, list) or isinstance(key, tuple):
            vector = self
            for k in key[:-1]:
                vector = vector[k]
            if isinstance(value, BaseType):
                vector[key[-1]] = value
            elif isinstance(value, int):
                vector[key[-1]] = Int(value)
            elif isinstance(value, float):
                vector[key[-1]] = Float(value)
            else:
                vector[key[-1]] = value

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
    return Vector(array, shape=shape, _creator=_creator)


def ones(shape, _creator=None):
    array = create_array_by_shape(shape, 1)
    return Vector(array, shape=shape, _creator=_creator)


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
