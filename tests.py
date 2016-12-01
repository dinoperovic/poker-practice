# -*- coding: utf-8 -*-

import unittest

from poker import Card, Hand


class CardTest(unittest.TestCase):
    def test__str__(self):
        self.assertEquals(str(Card('QH')), 'Queen of Hearts')
        self.assertEquals(str(Card('AS')), 'Ace of Spades')
        self.assertEquals(str(Card('3D')), 'Three of Diamonds')

    def test_value_as_int(self):
        self.assertEquals(Card('AH').value_as_int, 12)
        self.assertEquals(Card('2H').value_as_int, 0)


class HandTest(unittest.TestCase):
    def test__str__(self):
        self.assertEquals(str(Hand.from_string('2H 2D QS QD QC')), "<hand [2H, 2D, QS, QD, QC], 'Full House'>")
        self.assertEquals(str(Hand.from_string('AS 2S 3S 4S 5S')), "<hand [AS, 2S, 3S, 4S, 5S], 'Straight Flush'>")
        self.assertEquals(str(Hand.from_string('QS QC KD KH 3C')), "<hand [QS, QC, KD, KH, 3C], 'Two Pair'>")

    def test__cmp__(self):
        full_house = Hand.from_string('2H 2D QS QD QC')
        royal_flush = Hand.from_string('TD JD QD AD KD')
        self.assertTrue(full_house < royal_flush)
        two_pair = Hand.from_string('2D 2C 3D 3C 5D')
        two_pair2 = Hand.from_string('2D 2C 3D 3C 6D')
        self.assertTrue(two_pair < two_pair2)
        flush_hearts = Hand.from_string('AH QH 4H 5H TH')
        flush_diamonds = Hand.from_string('AD QD 4D 5D TD')
        self.assertTrue(flush_hearts == flush_diamonds)

    def test_from_string(self):
        hand = Hand.from_string('2D 2C 2S 3C 5D')
        self.assertIsInstance(hand, Hand)
        self.assertEquals(len(hand.cards), 5)

    def test_value(self):
        self.assertEqual(Hand.from_string('QC AC KC TC JC').value, Hand.ROYAL_FLUSH)
        self.assertEqual(Hand.from_string('AD 2D 3D 4D 5D').value, Hand.STRAIGHT_FLUSH)
        self.assertEqual(Hand.from_string('3H 2H 2S 2D 2C').value, Hand.FOUR_OF_A_KIND)
        self.assertEqual(Hand.from_string('3H 4H 4D 4C 3C').value, Hand.FULL_HOUSE)
        self.assertEqual(Hand.from_string('AS QS 4S 5S TS').value, Hand.FLUSH)
        self.assertEqual(Hand.from_string('4H 5C 3D 2H AC').value, Hand.STRAIGHT)
        self.assertEqual(Hand.from_string('4H 4C 5D 3C 4D').value, Hand.TREE_OF_A_KIND)
        self.assertEqual(Hand.from_string('AH 4C 4D 3H 3C').value, Hand.TWO_PAIR)
        self.assertEqual(Hand.from_string('AH 4C 4D 5H 3C').value, Hand.ONE_PAIR)
        self.assertEqual(Hand.from_string('AH 5C 4D 3H 7C').value, Hand.HIGH_CARD)

    def test_is_royal_flush(self):
        self.assertFalse(Hand.from_string('TD JD QD AD KS').is_royal_flush())
        self.assertTrue(Hand.from_string('TD JD QD AD KD').is_royal_flush())
        self.assertTrue(Hand.from_string('QH AH KH TH JH').is_royal_flush())

    def test_is_straight_flush(self):
        self.assertFalse(Hand.from_string('5H 6H 7H AH 9H').is_straight_flush())
        self.assertTrue(Hand.from_string('5H 6H 7H 8H 9H').is_straight_flush())
        self.assertTrue(Hand.from_string('AS 2S 3S 4S 5S').is_straight_flush())

    def test_is_four_of_a_kind(self):
        self.assertFalse(Hand.from_string('2H 2D QS QD QC').is_four_of_a_kind())
        self.assertTrue(Hand.from_string('3H 2H 2S 2D 2C').is_four_of_a_kind())
        self.assertTrue(Hand.from_string('8H 7D 8S 8D 8C').is_four_of_a_kind())

    def test_is_full_house(self):
        self.assertFalse(Hand.from_string('3H 4H 4D 4C 2C').is_full_house())
        self.assertTrue(Hand.from_string('3H 4H 4D 4C 3C').is_full_house())
        self.assertTrue(Hand.from_string('AH AD AC QC QD').is_full_house())

    def test_is_flush(self):
        self.assertFalse(Hand.from_string('2H 3H 4D 5H 6H').is_flush())
        self.assertTrue(Hand.from_string('AH QH 4H 5H TH').is_flush())
        self.assertTrue(Hand.from_string('3D 9D 4D 5D TD').is_flush())

    def test_is_straight(self):
        self.assertFalse(Hand.from_string('4H 5C 3D 2H 2C').is_straight())
        self.assertTrue(Hand.from_string('4H 5C 3D 2H AC').is_straight())
        self.assertTrue(Hand.from_string('9H TC JD QH KC').is_straight())

    def test_is_tree_of_a_kind(self):
        self.assertFalse(Hand.from_string('AH 5C 3D 2H 3C').is_tree_of_a_kind())
        self.assertTrue(Hand.from_string('4H 4C 3D 3C 4D').is_tree_of_a_kind())
        self.assertTrue(Hand.from_string('8H 7D 8S 8D 8C').is_tree_of_a_kind())

    def test_is_two_pair(self):
        self.assertFalse(Hand.from_string('4H 4C 4D 3H 3C').is_two_pair())
        self.assertTrue(Hand.from_string('AH 4C 4D 3H 3C').is_two_pair())
        self.assertTrue(Hand.from_string('QS QC KD KH 3C').is_two_pair())

    def test_is_one_pair(self):
        self.assertFalse(Hand.from_string('4H 4C 4D 3H 3C').is_one_pair())
        self.assertTrue(Hand.from_string('AH 5C 4D 3H 3C').is_one_pair())
        self.assertTrue(Hand.from_string('TS QC KD KH 3C').is_one_pair())

    def test_is_high_card(self):
        self.assertFalse(Hand().is_high_card())
        self.assertTrue(Hand.from_string('AH 5C 4D 3H 3C').is_high_card())


if __name__ == '__main__':
    unittest.main()
