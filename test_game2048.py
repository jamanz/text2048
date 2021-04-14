import unittest as unit
from main import Game2048, Direction
import sys


class TestGameField(unit.TestCase):

    def test_line_is_reducible(self):
        g = Game2048()
        self.cases = ('0 0 0 0', '2 4 0 0', '0 4 0 0', '2 2 0 0', '4 4 2 2', '2 0 0 2')
        for c in self.cases:
            with self.subTest(case=c):
                case = c.split()
                self.assertTrue(g.line_is_reducible(case), msg=f'Line {c} should be reducibe one')

        self.cases = ('2 4 16 2', '2 4 2 16',)
        for c in self.cases:
            with self.subTest(case=c):
                case = c.split()
                self.assertFalse(g.line_is_reducible(case), msg=f'Line {c} should NOT be reducibe one')

    def test_table_is_reducible(self):
        g = Game2048()
        self.cases = (
            [['4', '2', '4', '2'],
             ['16', '4', '2', '4'],
             ['4', '2', '16', '2'],
             ['2', '4', '2', '8']]
        )
        for c in self.cases:
            with self.subTest(case=c):
                case = c
                self.assertFalse(g.table_is_reducible(case), msg=f'Game over')

    def test_merge_numbers_in_line(self):
        g = Game2048()
        self.cases = ('2 2 4 4', '2 2 2 2', '2 4 2 2', '8 4 2 2', '2 0 0 2')
        excepted = ('4 8', '4 4', '2 4 4', '8 4 4', '4')
        for i, c in enumerate(self.cases):
            with self.subTest(case=c):
                case = c.split()
                self.assertEqual(g.merge_numbers_in_line(case, Direction.Right), excepted[i].split(),
                                 msg=f'Line {c} should be merged to {excepted[i]}')

    def test_one_move_in_line(self):
        g = Game2048()
        self.cases = (
            ('2 2 4 4', 'R'),
            ('2 2 2 2', 'L'),
            ('2 4 2 2', 'L'),
            ('8 4 2 2', 'R'),
            ('0 2 2 4', 'L')
        )
        excepted = ('0 0 4 8', '4 4 0 0', '2 4 4 0', '0 8 4 4', '4 4 0 0')
        for i, c in enumerate(self.cases):
            with self.subTest(case=c):
                case = c[0].split()  # '2 0 2 0' -> ['2', '0', '2', '0']
                direct = c[1]
                exp = excepted[i].split()
                self.assertEqual(g.one_move_in_line(case, direct), exp,
                                 msg=f'Line {c} should be reduced to {excepted[i]}')

    def test_one_move_in_table(self):
        g = Game2048()
        self.cases = (
            (
                [['4', '4', '2', '2'],
                 ['4', '4', '2', '2'],
                 ['4', '4', '2', '2'],
                 ['4', '4', '2', '2']], 'R'),
            (
                [['4', '4', '0', '2'],
                 ['4', '8', '4', '2'],
                 ['4', '2', '2', '4'],
                 ['4', '8', '8', '8']], 'U')
        )

        expected = (
            [['0', '0', '8', '4'],
             ['0', '0', '8', '4'],
             ['0', '0', '8', '4'],
             ['0', '0', '8', '4']],

            [['8', '4', '4', '4'],
             ['8', '8', '2', '4'],
             ['0', '2', '8', '8'],
             ['0', '8', '0', '0']]
        )

        for i, c in enumerate(self.cases):
            with self.subTest(case=c):
                case = c[0]
                direct = c[1]
                msg = f'Table should be {expected}'
                self.assertEqual(g.one_move_in_table(case, direct), expected[i], msg=msg)


def test_suite():
    suite = unit.TestSuite()
    suite.addTest(TestGameField('test_line_is_reducible'))
    suite.addTest(TestGameField('test_table_is_reducible'))
    suite.addTest(TestGameField('test_merge_numbers_in_line'))
    suite.addTest(TestGameField('one_move_in_line'))
    suite.addTest(TestGameField('test_move_in_table'))
    return suite


if __name__ == '__main__':
    runner = unit.TextTestRunner(stream=sys.stdout, verbosity=2)
    test_suite = test_suite()
    runner.run(test_suite)
