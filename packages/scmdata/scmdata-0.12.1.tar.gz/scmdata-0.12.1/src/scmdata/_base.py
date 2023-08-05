import operator

import numpy as np


class OpsMixin:
    """
    Mixin for common binary operators
    """

    def _binary_op(self, other, f, reflexive=False):
        raise NotImplementedError

    def __add__(self, other):
        return self._binary_op(other, operator.add)

    def __sub__(self, other):
        return self._binary_op(other, operator.sub)

    def __mul__(self, other):
        return self._binary_op(other, operator.mul)

    def __pow__(self, other):
        return self._binary_op(other, operator.pow)

    def __truediv__(self, other):
        return self._binary_op(other, operator.truediv)

    def __floordiv__(self, other):
        return self._binary_op(other, operator.floordiv)

    def __mod__(self, other):
        return self._binary_op(other, operator.mod)

    def __lt__(self, other):
        return self._binary_op(other, operator.lt)

    def __le__(self, other):
        return self._binary_op(other, operator.le)

    def __gt__(self, other):
        return self._binary_op(other, operator.gt)

    def __ge__(self, other):
        return self._binary_op(other, operator.ge)

    def __eq__(self, other):
        return self._binary_op(other, np.equal)

    def __ne__(self, other):
        # TODO: check xarray implementation
        return self._binary_op(other, np.not_equal)

    def __radd__(self, other):
        return self._binary_op(other, operator.add, reflexive=True)

    def __rsub__(self, other):
        return self._binary_op(other, operator.sub, reflexive=True)

    def __rmul__(self, other):
        return self._binary_op(other, operator.mul, reflexive=True)

    def __rpow__(self, other):
        return self._binary_op(other, operator.pow, reflexive=True)

    def __rtruediv__(self, other):
        return self._binary_op(other, operator.truediv, reflexive=True)

    def __rfloordiv__(self, other):
        return self._binary_op(other, operator.floordiv, reflexive=True)

    def __rmod__(self, other):
        return self._binary_op(other, operator.mod, reflexive=True)

    def _unary_op(self, f, *args, **kwargs):
        raise NotImplementedError

    def __neg__(self):
        return self._unary_op(operator.neg)

    def __pos__(self):
        return self._unary_op(operator.pos)

    def __abs__(self):
        return self._unary_op(operator.abs)

    __add__.__doc__ = operator.add.__doc__
    __sub__.__doc__ = operator.sub.__doc__
    __mul__.__doc__ = operator.mul.__doc__
    __pow__.__doc__ = operator.pow.__doc__
    __truediv__.__doc__ = operator.truediv.__doc__
    __floordiv__.__doc__ = operator.floordiv.__doc__
    __mod__.__doc__ = operator.mod.__doc__
    __lt__.__doc__ = operator.lt.__doc__
    __le__.__doc__ = operator.le.__doc__
    __gt__.__doc__ = operator.gt.__doc__
    __ge__.__doc__ = operator.ge.__doc__
    __eq__.__doc__ = np.equal.__doc__
    __ne__.__doc__ = np.not_equal.__doc__
    __radd__.__doc__ = operator.add.__doc__
    __rsub__.__doc__ = operator.sub.__doc__
    __rmul__.__doc__ = operator.mul.__doc__
    __rpow__.__doc__ = operator.pow.__doc__
    __rtruediv__.__doc__ = operator.truediv.__doc__
    __rfloordiv__.__doc__ = operator.floordiv.__doc__
    __rmod__.__doc__ = operator.mod.__doc__
    __neg__.__doc__ = operator.neg.__doc__
    __pos__.__doc__ = operator.pos.__doc__
    __abs__.__doc__ = operator.abs.__doc__
