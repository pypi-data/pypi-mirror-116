# Better Range

A range which automatically deals with either direction.


### Installation
```
pip install brange
```

### Usage

Start is always inclusive and end is always exclusive. Step must be a positive integer, as it always steps toward the end. A negative value will result in an empty range.

```py
from brange import brange

# This will create a list between 10 (inclusive) and -40 (exclusive)
# [10, 11, 12, ... -37, -38, -39]
[i for i in brange(10, -40)]
```