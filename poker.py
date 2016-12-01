# -*- coding: utf-8 -*-


class Card(object):
    """
    A Card class.
    """
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    SUITS = ['C', 'D', 'H', 'S']

    NAMES = {
        '1': 'One',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine',
        'T': 'Ten',
        'J': 'Jack',
        'Q': 'Queen',
        'K': 'King',
        'A': 'Ace',
        'C': 'Clubs',
        'D': 'Diamonds',
        'H': 'Hearts',
        'S': 'Spades',
    }

    def __init__(self, string):
        assert string[0] in self.VALUES, "Invalid Card value '%s'" % string[0]
        assert string[1] in self.SUITS, "Invalid Card suit '%s'" % string[1]
        self.value = string[0]
        self.suit = string[1]

    def __str__(self):
        return '%s of %s' % (self.NAMES[self.value], self.NAMES[self.suit])

    @property
    def value_as_int(self):
        return self.VALUES.index(self.value)


class Hand(object):
    """
    A Hand class.

    Can be initialized from a string like so:

    ``three_of_a_kind = Hand.from_string('4D 4S 4H 7H 8D')``
    ``one_pair = Hand.from_string('4D 3D 3H 7H AD')``
    """
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    TREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    HANDS = [
        (HIGH_CARD, 'High Card'),
        (ONE_PAIR, 'One Pair'),
        (TWO_PAIR, 'Two Pair'),
        (TREE_OF_A_KIND, 'Tree of a Kind'),
        (STRAIGHT, 'Straight'),
        (FLUSH, 'Flush'),
        (FULL_HOUSE, 'Full House'),
        (FOUR_OF_A_KIND, 'Four of a Kind'),
        (STRAIGHT_FLUSH, 'Straight Flush'),
        (ROYAL_FLUSH, 'Royal Flush'),
    ]

    def __init__(self, cards=None):
        self.cards = cards

    def __str__(self):
        cards = ', '.join(['%s%s' % (x.value, x.suit) for x in self.cards])
        return "<hand [%s], '%s'>" % (cards, dict(self.HANDS)[self.value])

    def __cmp__(self, other):
        """
        Return if hand is better than other, if hand value is the same as
        other, sum individual cards ranks together and use that value as rank.
        """
        if self.value == other.value:
            values = sum([x.value_as_int for x in self.cards])
            other_values = sum([x.value_as_int for x in other.cards])
            return -1 if values < other_values else 1 if values > other_values else 0
        return -1 if self.value < other.value else 1

    @classmethod
    def from_string(cls, string):
        """Initialize Hand from string"""
        card_strings = [x for x in string.split(' ')]
        assert len(set(card_strings)) == 5, '5 unique card combinations are needed, %s given' % len(set(card_strings))
        return cls([Card(x) for x in card_strings])

    @property
    def value(self):
        """Returns the best rank matching the rules of a hand, cache value"""
        if not hasattr(self, '_value'):
            for rank, name in reversed(self.HANDS):
                if getattr(self, 'is_%s' % name.lower().replace(' ', '_'))():
                    setattr(self, '_value', rank)
                    break
        return getattr(self, '_value')

    def is_royal_flush(self):
        """Combination of ten, jack, queen, king, ace, all of the same suit"""
        values = [x.value for x in self.cards]
        suits = [x.suit for x in self.cards]
        return len(set(suits)) == 1 and set(values).issubset(set(['T', 'J', 'Q', 'K', 'A']))

    def is_straight_flush(self):
        """Five cards of the same suit in sequential order"""
        values = sorted([x.value_as_int for x in self.cards])
        suits = [x.suit for x in self.cards]
        # If Ace needs to be 1, make it so.
        if values[0] == 0 and values[-1] == 12:
            values.pop()
            values.insert(0, -1)
        return len(set(suits)) == 1 and values == range(values[0], values[-1] + 1)

    def is_four_of_a_kind(self):
        """Any four numerically matching cards"""
        values = [x.value for x in self.cards]
        value = max(set(values), key=values.count)
        return values.count(value) == 4

    def is_full_house(self):
        """Combination of three of a kind and a pair in the same hand"""
        values = [x.value for x in self.cards]
        value3 = max(set(values), key=values.count)
        value2 = min(set(values), key=values.count)
        return values.count(value3) == 3 and values.count(value2) == 2

    def is_flush(self):
        """Five cards of the same suit, in any order"""
        suits = [x.suit for x in self.cards]
        return len(set(suits)) == 1

    def is_straight(self):
        """Five cards of any suit, in sequential order"""
        values = sorted([x.value_as_int for x in self.cards])
        # If Ace needs to be 1, make it so.
        if values[0] == 0 and values[-1] == 12:
            values.pop()
            values.insert(0, -1)
        return values == range(values[0], values[-1] + 1)

    def is_tree_of_a_kind(self):
        """Any three numerically matching cards"""
        values = [x.value for x in self.cards]
        value = max(set(values), key=values.count)
        return values.count(value) >= 3

    def is_two_pair(self):
        """Two different pairs in the same hand"""
        values = [x.value for x in self.cards]
        value1 = max(set(values), key=values.count)
        value2 = max(set([x for x in values if x != value1]), key=values.count)
        return values.count(value1) == 2 and values.count(value2) == 2

    def is_one_pair(self):
        """Any two numerically matching cards"""
        values = [x.value for x in self.cards]
        value = max(set(values), key=values.count)
        return values.count(value) == 2

    def is_high_card(self):
        """The highest ranked card in your hand, always True if cards exist"""
        return self.cards is not None
