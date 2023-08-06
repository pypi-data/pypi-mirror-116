# -*- coding: utf-8 -*-

from brainpy import errors
from brainpy.backend import ops

from . import utils

__all__ = [
    'Monitor'
]


class Monitor(object):
    """The basic Monitor class to store the past variable trajectories.

    Currently, :py:class:`brainpy.simulation.Monitor` support to specify:

    - variable key by `strings`.
    - variable index by `None`, `int`, `list`, `tuple`, `1D array/tensor`
      (==> all will be transformed into a 1D array/tensor)
    - variable monitor interval by `None`, `int`, `float`

    Users can instance a monitor object by multiple ways:

    1. list of strings.

    >>> Monitor(target=..., variables=['a', 'b', 'c'])

    1.1. list of strings and list of intervals

    >>> Monitor(target=..., variables=['a', 'b', 'c'],
    >>>         every=[None, 1, 2] # ms
    >>>        )

    2. list of strings and string + indices

    >>> Monitor(target=..., variables=['a', ('b', ops.as_tensor([1,2,3])), 'c'])

    2.1. list of string (+ indices) and list of intervals

    >>> Monitor(target=..., variables=['a', ('b', ops.as_tensor([1,2,3])), 'c'],
    >>>         every=[None, 2, 3])

    3. a dictionary with the format of {key: indices}

    >>> Monitor(target=..., variables={'a': None, 'b': ops.as_tensor([1,2,3])})

    3.1. a dictionaly of variable and indexes, and a dictionary of time intervals

    >>> Monitor(target=..., variables={'a': None, 'b': ops.as_tensor([1,2,3])},
    >>>         every={'b': 2.})

    .. note::
        :py:class:`brainpy.simulation.Monitor` records any target variable with an
        two-dimensional array/tensor with the shape of `(num_time_step, variable_size)`.
        This means for any variable, no matter what's the shape of the data
        (int, float, vector, matrix, 3D array/tensor), will be reshaped into a
        one-dimensional vector.

    """

    _KEYWORDS = ['_KEYWORDS', 'target', 'vars', 'every', 'ts', 'num_item',
                 'item_names', 'item_indices', 'item_intervals', 'item_contents', ]

    def __init__(self, variables, every=None, target=None):
        if isinstance(variables, (list, tuple)):
            if every is not None:
                if not isinstance(every, (list, tuple)):
                    raise errors.ModelUseError(f'"vars" and "every" must be the same type. '
                                               f'While we got type(vars)={type(variables)}, '
                                               f'type(every)={type(every)}.')
                if len(variables) != len(every):
                    raise errors.ModelUseError(f'The length of "vars" and "every" are not equal.')

        elif isinstance(variables, dict):
            if every is not None:
                if not isinstance(every, dict):
                    raise errors.ModelUseError(f'"vars" and "every" must be the same type. '
                                               f'While we got type(vars)={type(variables)}, '
                                               f'type(every)={type(every)}.')
                for key in every.keys():
                    if key not in variables:
                        raise errors.ModelUseError(f'"{key}" is not in "vars": {list(variables.keys())}')

        else:
            raise errors.ModelUseError(f'We only supports a format of list/tuple/dict of '
                                       f'"vars", while we got {type(variables)}.')

        self.ts = None
        self.vars = variables
        self.every = every
        self.target = target
        self.item_names = []
        self.item_indices = []
        self.item_intervals = []
        self.item_contents = dict()
        self.num_item = len(variables)

    def check(self, mon_key):
        if mon_key in self._KEYWORDS:
            raise ValueError(f'"{mon_key}" is a keyword in Monitor class. '
                             f'Please change to another name.')
        if not hasattr(self.target, mon_key):
            raise errors.ModelDefError(f"Item \"{mon_key}\" isn't defined in model "
                                       f"{self.target}, so it can not be monitored.")

    def build(self):
        item_names = []
        item_indices = []
        item_intervals = []
        item_content = {}

        if isinstance(self.vars, (list, tuple)):
            if self.every is None:
                item_intervals = [None] * len(self.vars)
            else:
                item_intervals = list(self.every)
            for mon_var in self.vars:
                # users monitor a variable by a string
                if isinstance(mon_var, str):
                    var_data = getattr(self.target, mon_var)
                    mon_key = mon_var
                    mon_idx = None
                    mon_shape = (utils.size2len(ops.shape(var_data)),)
                # users monitor a variable by a tuple: `('b', ops.as_tensor([1,2,3]))`
                elif isinstance(mon_var, (tuple, list)):
                    mon_key = mon_var[0]
                    var_data = getattr(self.target, mon_key)
                    mon_idx = mon_var[1]
                    if mon_idx is None:
                        mon_shape = (utils.size2len(ops.shape(var_data)),)
                    else:
                        mon_idx = self.check_mon_idx(mon_idx)
                        mon_shape = ops.shape(mon_idx)
                else:
                    raise errors.ModelUseError(f'Unknown monitor item: {str(mon_var)}')

                self.check(mon_key)
                item_names.append(mon_key)
                item_indices.append(mon_idx)
                dtype = var_data.dtype if hasattr(var_data, 'dtype') else None
                item_content[mon_key] = ops.zeros((1,) + mon_shape, dtype=dtype)
                item_content[f'{mon_key}_t'] = ops.zeros((1,))
        elif isinstance(self.vars, dict):
            # users monitor a variable by a dict: `{'a': None, 'b': ops.as_tensor([1,2,3])}`
            for mon_key, mon_idx in self.vars.items():
                item_names.append(mon_key)
                if mon_idx is None:
                    shape = ops.shape(getattr(self.target, mon_key))
                else:
                    mon_idx = self.check_mon_idx(mon_idx)
                    shape = ops.shape(mon_idx)
                item_indices.append(mon_idx)
                shape = (utils.size2len(shape),)
                val_data = getattr(self.target, mon_key)
                dtype = val_data.dtype if hasattr(val_data, 'dtype') else None
                item_content[mon_key] = ops.zeros((1,) + shape, dtype=dtype)
                item_content[f'{mon_key}_t'] = ops.zeros((1,))
                if self.every is None:
                    item_intervals.append(None)
                else:
                    if mon_key in self.every:
                        item_intervals.append(self.every[mon_key])
        else:
            raise errors.ModelUseError(f'Unknown monitors type: {type(self.vars)}')

        self.item_names = item_names
        self.item_indices = item_indices
        self.item_contents = item_content
        self.item_intervals = item_intervals
        self.num_item = len(item_content)

    @staticmethod
    def check_mon_idx(mon_idx):
        if isinstance(mon_idx, int):
            mon_idx = ops.as_tensor([mon_idx])
        else:
            mon_idx = ops.as_tensor(mon_idx)
            if len(ops.shape(mon_idx)) != 1:
                raise errors.ModelUseError(f'Monitor item index only supports '
                                           f'an int or a one-dimensional vector, '
                                           f'not {str(mon_idx)}')
        return mon_idx

    def __getattr__(self, item):
        item_contents = super(Monitor, self).__getattribute__('item_contents')
        if item in item_contents:
            return item_contents[item]
        else:
            super(Monitor, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in self._KEYWORDS:
            object.__setattr__(self, key, value)
        elif key in self.item_contents:
            self.item_contents[key] = value
        else:
            object.__setattr__(self, key, value)
