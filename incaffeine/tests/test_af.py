#!/usr/bin/env python3

import unittest
import sys
sys.path.append('../')

from incaffeine.af import AF


class TestAF(unittest.TestCase):

    def test_equality1(self):
        af1 = AF(3)
        af1.set_argument(0, AF.DEFINITE_ARGUMENT)
        af1.set_argument(1, AF.DEFINITE_ARGUMENT)
        af1.set_argument(2, AF.DEFINITE_ARGUMENT)
        af2 = AF(3)
        af2.set_argument(0, AF.DEFINITE_ARGUMENT)
        af2.set_argument(1, AF.DEFINITE_ARGUMENT)
        af2.set_argument(2, AF.DEFINITE_ARGUMENT)
        af1.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af2.set_attack(0, 1, AF.DEFINITE_ATTACK)

        self.assertTrue(af1 == af2)

    def test_equality2(self):
        af1 = AF(3)
        af1.set_argument(0, AF.DEFINITE_ARGUMENT)
        af1.set_argument(1, AF.DEFINITE_ARGUMENT)
        af1.set_argument(2, AF.DEFINITE_ARGUMENT)
        af2 = AF(3)
        af2.set_argument(0, AF.DEFINITE_ARGUMENT)
        af2.set_argument(1, AF.DEFINITE_ARGUMENT)
        af2.set_argument(2, AF.DEFINITE_ARGUMENT)
        af1.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af2.set_attack(0, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af1 == af2)

    def test_equality3(self):
        af1 = AF(3)
        af1.set_argument(0, AF.DEFINITE_ARGUMENT)
        af1.set_argument(1, AF.DEFINITE_ARGUMENT)
        af1.set_argument(2, AF.DEFINITE_ARGUMENT)
        af2 = AF(2)
        af2.set_argument(0, AF.DEFINITE_ARGUMENT)
        af2.set_argument(1, AF.DEFINITE_ARGUMENT)
        af1.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af2.set_attack(0, 1, AF.DEFINITE_ATTACK)

        self.assertFalse(af1 == af2)

    def test_restricted_extension(self):
        af = AF(2)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.NO_ARGUMENT)

        args = {0, 1}
        args_reference = {0}

        self.assertEqual(af.restricted_extension(args), args_reference)

    def test_grounded_extension1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        grounded_extension = {0, 2}

        self.assertEqual(set(af.grounded_extension()), grounded_extension)

    def test_grounded_extension2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        grounded_extension = set([])

        self.assertEqual(af.grounded_extension(), grounded_extension)

    def test_grounded_extension3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        grounded_extension = {0, 2}

        self.assertEqual(set(af.grounded_extension()), grounded_extension)

    def test_conflict_free1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_conflict_free({}))
        self.assertTrue(af.is_conflict_free({0}))
        self.assertTrue(af.is_conflict_free({1}))
        self.assertFalse(af.is_conflict_free({0, 1}))
        self.assertFalse(af.is_conflict_free({2}))
        self.assertFalse(af.is_conflict_free({0, 2}))
        self.assertFalse(af.is_conflict_free({1, 2}))
        self.assertFalse(af.is_conflict_free({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_CF))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_CF))
        self.assertTrue(af.verification({1}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_CF))

    def test_conflict_free2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_conflict_free({}))
        self.assertTrue(af.is_conflict_free({0}))
        self.assertTrue(af.is_conflict_free({1}))
        self.assertFalse(af.is_conflict_free({0, 1}))
        self.assertTrue(af.is_conflict_free({2}))
        self.assertFalse(af.is_conflict_free({0, 2}))
        self.assertFalse(af.is_conflict_free({1, 2}))
        self.assertFalse(af.is_conflict_free({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_CF))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_CF))
        self.assertTrue(af.verification({1}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_CF))
        self.assertTrue(af.verification({2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_CF))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_CF))

    def test_non_empty_conflict_free1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.verification({}, AF.SEMANTICS_NECF))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_NECF))
        self.assertTrue(af.verification({1}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_NECF))

    def test_non_empty_conflict_free2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertFalse(af.verification({}, AF.SEMANTICS_NECF))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_NECF))
        self.assertTrue(af.verification({1}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_NECF))
        self.assertTrue(af.verification({2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_NECF))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_NECF))

    def test_admissible1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_admissible({}))
        self.assertTrue(af.is_admissible({0}))
        self.assertFalse(af.is_admissible({1}))
        self.assertFalse(af.is_admissible({0, 1}))
        self.assertFalse(af.is_admissible({2}))
        self.assertFalse(af.is_admissible({0, 2}))
        self.assertFalse(af.is_admissible({1, 2}))
        self.assertFalse(af.is_admissible({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_AD))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_AD))

    def test_admissible2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_admissible({}))
        self.assertFalse(af.is_admissible({0}))
        self.assertFalse(af.is_admissible({1}))
        self.assertFalse(af.is_admissible({0, 1}))
        self.assertFalse(af.is_admissible({2}))
        self.assertFalse(af.is_admissible({0, 2}))
        self.assertFalse(af.is_admissible({1, 2}))
        self.assertFalse(af.is_admissible({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_AD))

    def test_admissible3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_admissible({}))
        self.assertTrue(af.is_admissible({0}))
        self.assertFalse(af.is_admissible({1}))
        self.assertFalse(af.is_admissible({0, 1}))
        self.assertFalse(af.is_admissible({2}))
        self.assertTrue(af.is_admissible({0, 2}))
        self.assertFalse(af.is_admissible({1, 2}))
        self.assertFalse(af.is_admissible({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_AD))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_AD))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_AD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_AD))

    def test_non_empty_admissible1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.verification({}, AF.SEMANTICS_NEAD))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_NEAD))

    def test_non_empty_admissible2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertFalse(af.verification({}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_NEAD))

    def test_non_empty_admissible3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.verification({}, AF.SEMANTICS_NEAD))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_NEAD))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_NEAD))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_NEAD))

    def test_complete1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_complete({}))
        self.assertTrue(af.is_complete({0}))
        self.assertFalse(af.is_complete({1}))
        self.assertFalse(af.is_complete({0, 1}))
        self.assertFalse(af.is_complete({2}))
        self.assertFalse(af.is_complete({0, 2}))
        self.assertFalse(af.is_complete({1, 2}))
        self.assertFalse(af.is_complete({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_CP))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_CP))

    def test_complete2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_complete({}))
        self.assertFalse(af.is_complete({0}))
        self.assertFalse(af.is_complete({1}))
        self.assertFalse(af.is_complete({0, 1}))
        self.assertFalse(af.is_complete({2}))
        self.assertFalse(af.is_complete({0, 2}))
        self.assertFalse(af.is_complete({1, 2}))
        self.assertFalse(af.is_complete({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_CP))

    def test_complete3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_complete({}))
        self.assertFalse(af.is_complete({0}))
        self.assertFalse(af.is_complete({1}))
        self.assertFalse(af.is_complete({0, 1}))
        self.assertFalse(af.is_complete({2}))
        self.assertTrue(af.is_complete({0, 2}))
        self.assertFalse(af.is_complete({1, 2}))
        self.assertFalse(af.is_complete({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_CP))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_CP))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_CP))

    def test_grounded1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_grounded({}))
        self.assertTrue(af.is_grounded({0}))
        self.assertFalse(af.is_grounded({1}))
        self.assertFalse(af.is_grounded({0, 1}))
        self.assertFalse(af.is_grounded({2}))
        self.assertFalse(af.is_grounded({0, 2}))
        self.assertFalse(af.is_grounded({1, 2}))
        self.assertFalse(af.is_grounded({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_GR))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_GR))

    def test_grounded2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_grounded({}))
        self.assertFalse(af.is_grounded({0}))
        self.assertFalse(af.is_grounded({1}))
        self.assertFalse(af.is_grounded({0, 1}))
        self.assertFalse(af.is_grounded({2}))
        self.assertFalse(af.is_grounded({0, 2}))
        self.assertFalse(af.is_grounded({1, 2}))
        self.assertFalse(af.is_grounded({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_GR))

    def test_grounded3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_grounded({}))
        self.assertFalse(af.is_grounded({0}))
        self.assertFalse(af.is_grounded({1}))
        self.assertFalse(af.is_grounded({0, 1}))
        self.assertFalse(af.is_grounded({2}))
        self.assertTrue(af.is_grounded({0, 2}))
        self.assertFalse(af.is_grounded({1, 2}))
        self.assertFalse(af.is_grounded({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_GR))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_GR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_GR))

    def test_preferred1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_preferred({}))
        self.assertTrue(af.is_preferred({0}))
        self.assertFalse(af.is_preferred({1}))
        self.assertFalse(af.is_preferred({0, 1}))
        self.assertFalse(af.is_preferred({2}))
        self.assertFalse(af.is_preferred({0, 2}))
        self.assertFalse(af.is_preferred({1, 2}))
        self.assertFalse(af.is_preferred({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_PR))
        self.assertTrue(af.verification({0}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_PR))

    def test_preferred2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_preferred({}))
        self.assertFalse(af.is_preferred({0}))
        self.assertFalse(af.is_preferred({1}))
        self.assertFalse(af.is_preferred({0, 1}))
        self.assertFalse(af.is_preferred({2}))
        self.assertFalse(af.is_preferred({0, 2}))
        self.assertFalse(af.is_preferred({1, 2}))
        self.assertFalse(af.is_preferred({0, 1, 2}))

        self.assertTrue(af.verification({}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_PR))

    def test_preferred3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_preferred({}))
        self.assertFalse(af.is_preferred({0}))
        self.assertFalse(af.is_preferred({1}))
        self.assertFalse(af.is_preferred({0, 1}))
        self.assertFalse(af.is_preferred({2}))
        self.assertTrue(af.is_preferred({0, 2}))
        self.assertFalse(af.is_preferred({1, 2}))
        self.assertFalse(af.is_preferred({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_PR))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_PR))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_PR))

    def test_stable1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_stable({}))
        self.assertFalse(af.is_stable({0}))
        self.assertFalse(af.is_stable({1}))
        self.assertFalse(af.is_stable({0, 1}))
        self.assertFalse(af.is_stable({2}))
        self.assertFalse(af.is_stable({0, 2}))
        self.assertFalse(af.is_stable({1, 2}))
        self.assertFalse(af.is_stable({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_ST))

    def test_stable2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_stable({}))
        self.assertFalse(af.is_stable({0}))
        self.assertFalse(af.is_stable({1}))
        self.assertFalse(af.is_stable({0, 1}))
        self.assertFalse(af.is_stable({2}))
        self.assertFalse(af.is_stable({0, 2}))
        self.assertFalse(af.is_stable({1, 2}))
        self.assertFalse(af.is_stable({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_ST))

    def test_stable3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_stable({}))
        self.assertFalse(af.is_stable({0}))
        self.assertFalse(af.is_stable({1}))
        self.assertFalse(af.is_stable({0, 1}))
        self.assertFalse(af.is_stable({2}))
        self.assertTrue(af.is_stable({0, 2}))
        self.assertFalse(af.is_stable({1, 2}))
        self.assertFalse(af.is_stable({0, 1, 2}))

        self.assertFalse(af.verification({}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({2}, AF.SEMANTICS_ST))
        self.assertTrue(af.verification({0, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({1, 2}, AF.SEMANTICS_ST))
        self.assertFalse(af.verification({0, 1, 2}, AF.SEMANTICS_ST))

    def test_credulous_acceptable_1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_CF))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_NECF))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_PR))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_ST))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_ST))

    def test_credulous_acceptable_2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_CF))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_AD))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_CP))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_GR))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_PR))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_ST))
        self.assertFalse(af.is_credulously_acceptable(2, AF.SEMANTICS_ST))

    def test_credulous_acceptable_3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_CF))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_NECF))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_AD))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_CP))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_GR))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_PR))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_PR))

        self.assertTrue(af.is_credulously_acceptable(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_credulously_acceptable(1, AF.SEMANTICS_ST))
        self.assertTrue(af.is_credulously_acceptable(2, AF.SEMANTICS_ST))

    def test_credulous_acceptable_4(self):
        af = AF(2)
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_CF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_CF))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_AD))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_AD))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_CP))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_CP))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_GR))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_GR))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_PR))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_PR))

        self.assertFalse(af.is_credulously_acceptable(0, AF.SEMANTICS_ST))
        self.assertTrue(af.is_credulously_acceptable(1, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_PR))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_CP))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_GR))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_PR))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CP))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_GR))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_PR))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_PR))

        self.assertTrue(af.is_skeptically_acceptable(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_4(self):
        af = AF(2)
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable(1, AF.SEMANTICS_AD))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_CP))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_CP))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_GR))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_GR))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_PR))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_PR))

        self.assertFalse(af.is_skeptically_acceptable(0, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable(1, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_and_extension_exists_1(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(2, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_PR))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_and_extension_exists_2(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)
        af.set_attack(2, 0, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_AD))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CP))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_GR))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_PR))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_and_extension_exists_3(self):
        af = AF(3)
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_argument(2, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 2, AF.DEFINITE_ATTACK)

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NECF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_AD))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NEAD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_NEAD))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CP))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CP))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_CP))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_GR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_GR))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_GR))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_PR))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_PR))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_PR))

        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_ST))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(2, AF.SEMANTICS_ST))

    def test_skeptical_acceptable_and_extension_exists_4(self):
        af = AF(2)
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CF))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NECF))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NECF))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_AD))
        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_AD))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_NEAD))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_NEAD))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_CP))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_CP))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_GR))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_GR))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_PR))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_PR))

        self.assertFalse(af.is_skeptically_acceptable_and_extension_exists(0, AF.SEMANTICS_ST))
        self.assertTrue(af.is_skeptically_acceptable_and_extension_exists(1, AF.SEMANTICS_ST))


if __name__ == "__main__":
    unittest.main()
