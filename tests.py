import unittest

import main


class BattleTests(unittest.TestCase):
    def test_create_fighter(self):
        test_fighter = main.Combatant('Rob', 10, 300)
        self.assertEqual(test_fighter.__str__(), '{}\t[HP: {}, AC: {}]'.format('Rob', 10, 300))


if __name__ == "__main__":
    unittest.main()
