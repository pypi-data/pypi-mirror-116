# Tree Containers

Asymptotically-efficient tree-based containers in pure Python. Licensed under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Priority Map

A combination between a heap and a map that stores key:priority mappings.

### Operations
| Operation | Description | Runtime Complexity |
|---|---|---|
| `__getitem__(key)` | Get priority of key | O(1) |
| `__setitem__(key, priority)` | Set priority of key | O(log n) |
| `__delitem__(key)` | Remove a key | O(log n) |
| `__contains__(key)` | Check whether a key is contained | O(1) |
| `__len__()` | Return the number of keys contained | O(1) |
| `peek()` | Get lowest-priority key and its priority | O(1) |
| `pop()` | Get and remove lowest-priority key and its priority | O(log n) |

### Example Console Output
```py
>>> from prioritymap import PriorityMap
>>> pm = PriorityMap()
>>> pm["first"] = 1
>>> pm["second"] = 2
>>> pm["underdog"] = 5
>>> pm.peek()
('first', 1)
>>> pm["underdog"] = 0
>>> len(pm)
3
>>> pm.pop()
('underdog', 0)
>>> pm.pop()
('first', 1)
>>> pm.pop()
('second', 2)
>>> len(pm)
0
```

## PrioritySet

To be implemented.

## TreeMap

To be implemented.