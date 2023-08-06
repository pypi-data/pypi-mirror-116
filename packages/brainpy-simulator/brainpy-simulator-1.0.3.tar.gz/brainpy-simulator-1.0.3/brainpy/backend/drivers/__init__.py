# -*- coding: utf-8 -*-

from brainpy.backend.drivers.tensor import TensorDiffIntDriver
from brainpy.backend.drivers.tensor import TensorNetDriver
from brainpy.backend.drivers.tensor import TensorNodeDriver
from brainpy.simulation.drivers import BaseDiffIntDriver
from brainpy.simulation.drivers import BaseNetDriver
from brainpy.simulation.drivers import BaseNodeDriver

__all__ = [
    'switch_to',
    'set_buffer',
    'get_buffer',
    'get_node_driver',
    'get_net_driver',
    'get_diffint_driver',

    'BUFFER',
]

DIFFINT_DRIVER = TensorDiffIntDriver
NODE_DRIVER = TensorNodeDriver
NET_DRIVER = TensorNetDriver
BUFFER = {}


def switch_to(backend):
    buffer = get_buffer(backend)

    global NODE_DRIVER, NET_DRIVER, DIFFINT_DRIVER
    if backend in ['numpy', 'pytorch', 'tensorflow']:
        from . import tensor
        NODE_DRIVER = buffer.get('node', None) or TensorNodeDriver
        NET_DRIVER = buffer.get('net', None) or TensorNetDriver
        DIFFINT_DRIVER = buffer.get('intg', None) or TensorDiffIntDriver

    elif backend in ['numba', 'numba-parallel']:
        from . import numba

        if backend == 'numba':
            numba.set_numba_profile(nogil=False, parallel=False)
        else:
            numba.set_numba_profile(nogil=True, parallel=True)

        NET_DRIVER = buffer.get('net', None) or TensorNetDriver
        NODE_DRIVER = buffer.get('node', None) or numba.NumbaNodeDriver
        DIFFINT_DRIVER = buffer.get('intg', None) or numba.NumbaDiffIntDriver

    else:
        if 'node' not in buffer:
            raise ValueError(f'"{backend}" is an unknown backend, should set node buffer '
                             f'by "brainpy.drivers.set_buffer(backend, node_driver=SomeNodeDriver)"')
        if 'net' not in buffer:
            raise ValueError(f'"{backend}" is an unknown backend, should set node buffer '
                             f'by "brainpy.drivers.set_buffer(backend, net_driver=SomeNetDriver)"')
        if 'diffint' not in buffer:
            raise ValueError(f'"{backend}" is an unknown backend, should set integrator wrapper '
                             f'by "brainpy.drivers.set_buffer(backend, diffint_driver=SomeDriver)"')
        NODE_DRIVER = buffer.get('node')
        NET_DRIVER = buffer.get('net')
        DIFFINT_DRIVER = buffer.get('diffint')


def set_buffer(backend, node_driver=None, net_driver=None, diffint_driver=None):
    global BUFFER
    if backend not in BUFFER:
        BUFFER[backend] = dict()

    if node_driver is not None:
        assert BaseNodeDriver in node_driver.__bases__
        BUFFER[backend]['node'] = node_driver
    if net_driver is not None:
        assert BaseNetDriver in net_driver.__bases__
        BUFFER[backend]['net'] = net_driver
    if diffint_driver is not None:
        assert BaseDiffIntDriver in diffint_driver.__bases__
        BUFFER[backend]['diffint'] = diffint_driver


def get_buffer(backend):
    return BUFFER.get(backend, dict())


def get_node_driver():
    """Get the current node driver.

    Returns
    -------
    node_driver
        The node driver.
    """
    return NODE_DRIVER


def get_net_driver():
    """Get the current network driver.

    Returns
    -------
    net_driver
        The network driver.
    """
    return NET_DRIVER


def get_diffint_driver():
    """Get the current integration driver for differential equations.

    Returns
    -------
    diffint_driver
        The integration driver.
    """
    return DIFFINT_DRIVER
