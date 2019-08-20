#!/usr/bin/env python3

import unittest
import sys
sys.path.append('../')

from incaffeine.incaf import IncAF


class TestIncAF(unittest.TestCase):

    def test_equality1(self):
        af1 = IncAF(3)
        af2 = IncAF(3)
        af1.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af2.set_attack(0, 1, IncAF.DEFINITE_ATTACK)

        self.assertTrue(af1 == af2)

    def test_equality2(self):
        af1 = IncAF(3)
        af2 = IncAF(3)
        af1.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af1.set_attack(0, 2, IncAF.POSSIBLE_ATTACK)
        af2.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af2.set_attack(0, 2, IncAF.POSSIBLE_ATTACK)

        self.assertTrue(af1 == af2)

    def test_equality3(self):
        af1 = IncAF(3)
        af2 = IncAF(3)
        af1.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af2.set_attack(0, 1, IncAF.POSSIBLE_ATTACK)

        self.assertFalse(af1 == af2)

    def test_restricted_extension(self):
        af = IncAF(3)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.NO_ARGUMENT)
        af.set_argument(2, IncAF.POSSIBLE_ARGUMENT)

        args = {0, 1, 2}
        args_reference = {0}

        self.assertEqual(af.restricted_extension(args), args_reference)

    def test_maximal_completion(self):
        af = IncAF(3)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.NO_ARGUMENT)
        af.set_argument(2, IncAF.POSSIBLE_ARGUMENT)

        maximal_completion = IncAF(3)
        maximal_completion.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        maximal_completion.set_argument(1, IncAF.NO_ARGUMENT)
        maximal_completion.set_argument(2, IncAF.DEFINITE_ARGUMENT)

        self.assertEqual(af.maximal_completion(), maximal_completion)

    def test_minimal_completion(self):
        af = IncAF(3)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.NO_ARGUMENT)
        af.set_argument(2, IncAF.POSSIBLE_ARGUMENT)

        minimal_completion = IncAF(3)
        minimal_completion.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        minimal_completion.set_argument(1, IncAF.NO_ARGUMENT)
        minimal_completion.set_argument(2, IncAF.NO_ARGUMENT)

        self.assertEqual(af.minimal_completion(), minimal_completion)

    def test_possibly_attacks(self):
        af = IncAF(9)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_argument(4, IncAF.NO_ARGUMENT)
        af.set_argument(5, IncAF.NO_ARGUMENT)
        af.set_argument(6, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(7, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(8, IncAF.POSSIBLE_ARGUMENT)
        af.set_attack(0, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(0, 1, IncAF.NO_ATTACK)
        af.set_attack(0, 2, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 3, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 4, IncAF.NO_ATTACK)
        af.set_attack(3, 5, IncAF.POSSIBLE_ATTACK)
        af.set_attack(6, 6, IncAF.DEFINITE_ATTACK)
        af.set_attack(6, 7, IncAF.NO_ATTACK)
        af.set_attack(6, 8, IncAF.POSSIBLE_ATTACK)

        self.assertTrue(af.possibly_attacks(0, 0))
        self.assertFalse(af.possibly_attacks(0, 1))
        self.assertTrue(af.possibly_attacks(0, 2))
        self.assertFalse(af.possibly_attacks(3, 3))
        self.assertFalse(af.possibly_attacks(3, 4))
        self.assertFalse(af.possibly_attacks(3, 5))
        self.assertTrue(af.possibly_attacks(6, 6))
        self.assertFalse(af.possibly_attacks(6, 7))
        self.assertTrue(af.possibly_attacks(6, 8))

    def test_necessarily_attacks(self):
        af = IncAF(9)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_argument(4, IncAF.NO_ARGUMENT)
        af.set_argument(5, IncAF.NO_ARGUMENT)
        af.set_argument(6, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(7, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(8, IncAF.POSSIBLE_ARGUMENT)
        af.set_attack(0, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(0, 1, IncAF.NO_ATTACK)
        af.set_attack(0, 2, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 3, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 4, IncAF.NO_ATTACK)
        af.set_attack(3, 5, IncAF.POSSIBLE_ATTACK)
        af.set_attack(6, 6, IncAF.DEFINITE_ATTACK)
        af.set_attack(6, 7, IncAF.NO_ATTACK)
        af.set_attack(6, 8, IncAF.POSSIBLE_ATTACK)

        self.assertTrue(af.necessarily_attacks(0, 0))
        self.assertFalse(af.necessarily_attacks(0, 1))
        self.assertFalse(af.necessarily_attacks(0, 2))
        self.assertFalse(af.necessarily_attacks(3, 3))
        self.assertFalse(af.necessarily_attacks(3, 4))
        self.assertFalse(af.necessarily_attacks(3, 5))
        self.assertFalse(af.necessarily_attacks(6, 6))
        self.assertFalse(af.necessarily_attacks(6, 7))
        self.assertFalse(af.necessarily_attacks(6, 8))

    def test_possibly_conflict_free(self):
        af = IncAF(12)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(4, IncAF.NO_ARGUMENT)
        af.set_argument(5, IncAF.NO_ARGUMENT)
        af.set_argument(6, IncAF.NO_ARGUMENT)
        af.set_argument(7, IncAF.NO_ARGUMENT)
        af.set_argument(8, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(9, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(10, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(11, IncAF.POSSIBLE_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(0, 2, IncAF.NO_ATTACK)
        af.set_attack(0, 3, IncAF.POSSIBLE_ATTACK)
        af.set_attack(4, 5, IncAF.DEFINITE_ATTACK)
        af.set_attack(4, 6, IncAF.NO_ATTACK)
        af.set_attack(4, 7, IncAF.POSSIBLE_ATTACK)
        af.set_attack(8, 9, IncAF.DEFINITE_ATTACK)
        af.set_attack(8, 10, IncAF.NO_ATTACK)
        af.set_attack(8, 11, IncAF.POSSIBLE_ATTACK)

        self.assertFalse(af.is_possibly_conflict_free({0, 1}))
        self.assertTrue(af.is_possibly_conflict_free({0, 2}))
        self.assertTrue(af.is_possibly_conflict_free({0, 3}))
        self.assertTrue(af.is_possibly_conflict_free({4, 5}))
        self.assertTrue(af.is_possibly_conflict_free({4, 6}))
        self.assertTrue(af.is_possibly_conflict_free({4, 7}))
        self.assertTrue(af.is_possibly_conflict_free({8, 9}))
        self.assertTrue(af.is_possibly_conflict_free({8, 10}))
        self.assertTrue(af.is_possibly_conflict_free({8, 11}))

    def test_necessarily_conflict_free(self):
        af = IncAF(12)
        af.set_argument(0, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(4, IncAF.NO_ARGUMENT)
        af.set_argument(5, IncAF.NO_ARGUMENT)
        af.set_argument(6, IncAF.NO_ARGUMENT)
        af.set_argument(7, IncAF.NO_ARGUMENT)
        af.set_argument(8, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(9, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(10, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(11, IncAF.POSSIBLE_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(0, 2, IncAF.NO_ATTACK)
        af.set_attack(0, 3, IncAF.POSSIBLE_ATTACK)
        af.set_attack(4, 5, IncAF.DEFINITE_ATTACK)
        af.set_attack(4, 6, IncAF.NO_ATTACK)
        af.set_attack(4, 7, IncAF.POSSIBLE_ATTACK)
        af.set_attack(8, 9, IncAF.DEFINITE_ATTACK)
        af.set_attack(8, 10, IncAF.NO_ATTACK)
        af.set_attack(8, 11, IncAF.POSSIBLE_ATTACK)

        self.assertFalse(af.is_necessarily_conflict_free({0, 1}))
        self.assertTrue(af.is_necessarily_conflict_free({0, 2}))
        self.assertFalse(af.is_necessarily_conflict_free({0, 3}))
        self.assertTrue(af.is_necessarily_conflict_free({4, 5}))
        self.assertTrue(af.is_necessarily_conflict_free({4, 6}))
        self.assertTrue(af.is_necessarily_conflict_free({4, 7}))
        self.assertFalse(af.is_necessarily_conflict_free({8, 9}))
        self.assertTrue(af.is_necessarily_conflict_free({8, 10}))
        self.assertFalse(af.is_necessarily_conflict_free({8, 11}))

    def test_possible_verification(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertTrue(af.possible_verification(set([]), IncAF.SEMANTICS_CF))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_CF))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_CF))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_CF))

        self.assertTrue(af.possible_verification(set([]), IncAF.SEMANTICS_AD))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_AD))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_AD))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_AD))

        self.assertTrue(af.possible_verification(set([]), IncAF.SEMANTICS_CP))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_CP))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_CP))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_CP))

        self.assertTrue(af.possible_verification(set([]), IncAF.SEMANTICS_GR))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_GR))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_GR))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_GR))

        self.assertTrue(af.possible_verification(set([]), IncAF.SEMANTICS_PR))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_PR))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_PR))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_PR))

        self.assertFalse(af.possible_verification(set([]), IncAF.SEMANTICS_ST))
        self.assertTrue(af.possible_verification({0, 1}, IncAF.SEMANTICS_ST))
        self.assertTrue(af.possible_verification({0, 2}, IncAF.SEMANTICS_ST))
        self.assertFalse(af.possible_verification({1, 2}, IncAF.SEMANTICS_ST))

    def test_necessary_verification(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_CF))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_CF))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_CF))

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_AD))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_AD))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_AD))

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_CP))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_CP))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_CP))

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_GR))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_GR))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_GR))

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_PR))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_PR))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_PR))

        self.assertFalse(af.necessary_verification({0, 1}, IncAF.SEMANTICS_ST))
        self.assertFalse(af.necessary_verification({0, 2}, IncAF.SEMANTICS_ST))
        self.assertFalse(af.necessary_verification({1, 2}, IncAF.SEMANTICS_ST))

    def test_possible_credulous_acceptance(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_CF))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_CF))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_CF))

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_AD))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_AD))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_AD))

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_CP))

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_GR))

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_PR))

        self.assertTrue(af.is_possibly_credulously_acceptable(0, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_credulously_acceptable(1, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_credulously_acceptable(2, IncAF.SEMANTICS_ST))

    def test_possible_skeptical_acceptance(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_CF))

        self.assertFalse(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_AD))

        self.assertTrue(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_CP))

        self.assertTrue(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_GR))

        self.assertTrue(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_PR))

        self.assertTrue(af.is_possibly_skeptically_acceptable(0, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_skeptically_acceptable(1, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_skeptically_acceptable(2, IncAF.SEMANTICS_ST))

    def test_possible_skeptical_acceptance_and_extension_exists(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_CF))

        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_AD))

        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_CP))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_CP))

        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_GR))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_GR))

        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_PR))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_PR))

        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_ST))
        self.assertTrue(af.is_possibly_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_ST))

    def test_necessary_credulous_acceptance(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_CF))
        self.assertTrue(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_CF))
        self.assertTrue(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_CF))

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_AD))

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_CP))

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_GR))

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_PR))

        self.assertFalse(af.is_necessarily_credulously_acceptable(0, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_credulously_acceptable(1, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_credulously_acceptable(2, IncAF.SEMANTICS_ST))

    def test_necessary_skeptical_acceptance(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_CF))

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_AD))

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_CP))

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_GR))

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_PR))

        self.assertFalse(af.is_necessarily_skeptically_acceptable(0, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(1, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_skeptically_acceptable(2, IncAF.SEMANTICS_ST))

    def test_necessary_skeptical_acceptance_and_extension_exists(self):
        af = IncAF(4)
        af.set_argument(0, IncAF.POSSIBLE_ARGUMENT)
        af.set_argument(1, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(2, IncAF.DEFINITE_ARGUMENT)
        af.set_argument(3, IncAF.NO_ARGUMENT)
        af.set_attack(0, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(1, 2, IncAF.DEFINITE_ATTACK)
        af.set_attack(2, 0, IncAF.POSSIBLE_ATTACK)
        af.set_attack(3, 0, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 1, IncAF.DEFINITE_ATTACK)
        af.set_attack(3, 2, IncAF.DEFINITE_ATTACK)

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_CF))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_CF))

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_AD))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_AD))

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_CP))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_CP))

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_GR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_GR))

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_PR))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_PR))

        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(0, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(1, IncAF.SEMANTICS_ST))
        self.assertFalse(af.is_necessarily_skeptically_acceptable_and_extension_exists(2, IncAF.SEMANTICS_ST))


if __name__ == "__main__":
    unittest.main()
