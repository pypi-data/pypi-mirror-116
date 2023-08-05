from typing import Any, Dict, Tuple

from collections.abc import Hashable


class Comparable:
    def __lt__(self, other: Any) -> bool:
        raise NotImplementedError


class PriorityMap:
    def __init__(self):
        self.arr = []
        self.key_to_i: Dict[Hashable, int] = {}
        self.key_to_priority: Dict[Hashable, Comparable] = {}

    # Get priority of key in O(1)
    def __getitem__(self, key: Hashable):
        if key not in self:
            raise ValueError(f"{key} not in heap")
        return self.key_to_priority[key]

    # Set priority of key in O(log n)
    def __setitem__(self, key: Hashable, priority: Comparable) -> None:
        if key in self:
            self._update_priority(key, priority)
        else:
            self._push(key, priority)

    # Remove a key in O(log n)
    def __delitem__(self, key: Hashable) -> None:
        if key not in self:
            raise ValueError(f"{key} not in heap")

        i = self.key_to_i[key]

        # Move key to end
        self._swap(i, len(self.arr) - 1)
        # Remove end
        del self.key_to_i[key]
        del self.key_to_priority[key]
        self.arr.pop()

        if i < len(self.arr):
            self._sink_down(self._bubble_up(i))  # Reposition key now at i

    # Check whether a key is contained in O(1)
    def __contains__(self, key: Hashable) -> bool:
        return key in self.key_to_i

    # Return the number of keys contained in O(1)
    def __len__(self) -> int:
        return len(self.arr)

    # Get lowest-priority key and its priority in O(1)
    def peek(self) -> Tuple[Hashable, Comparable]:
        if not self.arr:
            raise ValueError("PriorityMap is empty")
        return self.arr[0], self.key_to_priority[self.arr[0]]

    # Get and remove lowest-priority key and its priority in O(log n)
    def pop(self) -> Tuple[Hashable, Comparable]:
        if not self.arr:
            raise ValueError("PriorityMap is empty")
        key = self.arr[0]
        priority = self.key_to_priority[key]
        del self[key]
        return key, priority

    # Adds a key (assumes it doesn't exist) with a priority in O(log n)
    def _push(self, key: Hashable, priority: Comparable) -> None:
        i = len(self.arr)
        self.key_to_i[key] = i
        self.key_to_priority[key] = priority
        self.arr.append(key)
        self._bubble_up(i)

    # Updates priority of a key (assumes it exists) in O(log n)
    def _update_priority(self, key: Hashable, priority: Comparable) -> None:
        self.key_to_priority[key] = priority
        self._sink_down(self._bubble_up(self.key_to_i[key]))

    def _bubble_up(self, i: int) -> int:
        while (
            i > 0
            and self.key_to_priority[self.arr[i]]
            < self.key_to_priority[self.arr[(i - 1) // 2]]
        ):
            self._swap(i, (i - 1) // 2)
            i = (i - 1) // 2
        return i

    def _sink_down(self, i: int) -> int:
        while 2 * i + 1 < len(self.arr):
            gt_left = (
                self.key_to_priority[self.arr[2 * i + 1]]
                < self.key_to_priority[self.arr[i]]
            )
            gt_right = (
                2 * i + 2 < len(self.arr)
                and self.key_to_priority[self.arr[2 * i + 2]]
                < self.key_to_priority[self.arr[i]]
            )
            if gt_left and gt_right:
                if (
                    self.key_to_priority[self.arr[2 * i + 1]]
                    < self.key_to_priority[self.arr[2 * i + 2]]
                ):
                    self._swap(i, i * 2 + 1)
                    i = i * 2 + 1
                else:
                    self._swap(i, i * 2 + 2)
                    i = i * 2 + 2
            elif gt_left:
                self._swap(i, i * 2 + 1)
                i = i * 2 + 1
            elif gt_right:
                self._swap(i, i * 2 + 2)
                i = i * 2 + 2
            else:
                break
        return i

    def _swap(self, i1: int, i2: int) -> None:
        x1, x2 = self.arr[i1], self.arr[i2]
        self.key_to_i[x1] = i2
        self.key_to_i[x2] = i1
        self.arr[i1] = x2
        self.arr[i2] = x1
