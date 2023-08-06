# Better Range

A range which automatically deals with either direction.


### Installation
```
pip install brange
```

### Usage

Start is always inclusive and end is always exclusive. Step must be a positive integer, as it always steps toward the end. A negative value will result in an empty range.

#### Regular

```py
from brange import brange

# This will create a list between 10 (inclusive) and -40 (exclusive)
# [10, 11, 12, ... -37, -38, -39]
[i for i in brange(10, -40)]
```

#### N-dimensional

```py
from brange import nbrange

dimensions = [
    (1, 10, 2), # X
    (3, -2, 1), # Y
    (-2, 5, 1), # Z
]

[xyz for xyz in nbrange(*dimensions)]

# This will result in a list as below:
# [
#     (1, 3, -2),
#     (1, 3, -1),
#     ...
#     (9, -1, 2),
#     (9, -1, 3),
#     (9, -1, 4),
# ]
```