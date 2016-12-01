# Poker practice

Just a simple poker hand Class.

## How to use

```python
from poker import Hand

three_of_a_kind = Hand.from_string('4D 4S 4H 7H 8D')
one_pair = Hand.from_string('4D 3D 3H 7H AD')

three_of_a_kind > one_pair
>>> True

str(three_of_a_kind)
>>> "<hand [4D, 4S, 4H, 7H, 8D], 'Tree of a Kind'>"

str(one_pair)
>>> "<hand [4D, 3D, 3H, 7H, AD], 'One Pair'>"

```

Run tests with ``python tests.py``
