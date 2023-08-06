# -*- coding: utf-8 -*-

from brainpy import errors
from brainpy.simulation import utils
from .dynamic_system import DynamicSystem

__all__ = [
    'NeuGroup',
]

_NeuGroup_NO = 0


class NeuGroup(DynamicSystem):
    """Neuron Group.

    Parameters
    ----------
    size : int, tuple
        The neuron group geometry.
    monitors : list, tuple
        Variables to monitor.
    name : str
        The name of the neuron group.
    """

    def __init__(self, size, monitors=None, name=None, show_code=False, steps=None):
        # name
        # -----

        if name is None:
            global _NeuGroup_NO
            _NeuGroup_NO += 1
            name = f'NG{_NeuGroup_NO}'
        else:
            assert name.isidentifier()

        # size
        # ----
        if isinstance(size, (list, tuple)):
            if len(size) <= 0:
                raise errors.ModelDefError('size must be int, or a tuple/list of int.')
            if not isinstance(size[0], int):
                raise errors.ModelDefError('size must be int, or a tuple/list of int.')
            size = tuple(size)
        elif isinstance(size, int):
            size = (size,)
        else:
            raise errors.ModelDefError('size must be int, or a tuple/list of int.')
        self.size = size
        self.num = utils.size2len(size)

        # initialize
        # ----------
        if steps is None:
            steps = {'update': self.update}
        super(NeuGroup, self).__init__(steps=steps,
                                       monitors=monitors,
                                       name=name,
                                       show_code=show_code)

    def update(self, _t, _i, _dt):
        raise NotImplementedError



