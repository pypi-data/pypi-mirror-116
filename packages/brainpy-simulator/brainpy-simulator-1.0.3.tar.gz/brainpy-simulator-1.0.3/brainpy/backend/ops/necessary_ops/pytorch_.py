# -*- coding: utf-8 -*-

"""
The PyTorch with the version of xx is needed.
"""

from brainpy import errors

try:
    import torch
except ModuleNotFoundError:
    raise errors.BackendNotInstalled('pytorch')

from brainpy.backend.ops.more_unified_ops import pytorch_

__all__ = [
    'normal',
    'exp',
    'sum',
    'shape',
    'as_tensor',
    'zeros',
    'ones',
    'arange',
    'concatenate',
    'where',
    'reshape',
    'bool',
    'int',
    'int32',
    'int64',
    'float',
    'float32',
    'float64'
]

# necessary ops for integrators

normal = torch.normal
exp = torch.exp
sum = torch.sum


def shape(x):
    if isinstance(x, torch.Tensor):
        return x.size()
    else:
        return ()


# necessary ops for dynamics simulation

as_tensor = torch.as_tensor
zeros = torch.zeros
ones = torch.ones
arange = torch.arange
concatenate = torch.cat
reshape = torch.reshape


def where(tensor, x, y):
    if not isinstance(x, torch.Tensor):
        x = torch.full_like(tensor, x)
    if not isinstance(y, torch.Tensor):
        y = torch.full_like(tensor, y)
    return torch.where(tensor, x, y)


# necessary ops for dtypes

bool = torch.bool
int = torch.int
int32 = torch.int32
int64 = torch.int64
float = torch.float
float32 = torch.float32
float64 = torch.float64

if __name__ == '__main__':
    pytorch_
