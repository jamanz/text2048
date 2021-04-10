import sys, copy


class Direction:
    Up = 'U'
    Down = 'D'
    Left = 'L'
    Right = 'R'


class GameField:

    FieldSize = 4

    def read_file(self, path):
        with open(path, 'r') as f:
            grid = [f.readline().strip().split(' ') for line in range(4)]
            control_flow = f.readline().split()
        return grid, control_flow

    def line_is_reducible(self, line: list[str]):
        if '0' in line:
            return True
        for i in range(len(line) - 1):
            if line[i] == line[i+1] and line != '0':
                return True
        return False

    def table_is_reducible(self, table):
        all_posible_lines = table + self.rotate_table(table)
        return any(self.line_is_reducible(line) for line in all_posible_lines)

    def rotate_table(self, table: list[list[str]]):
        res = [row for row in zip(*table)]
        return res

    def print_table(self, table):
        print('\n')
        print(*table, sep='\n')
        print('\n')

    def merge_tiles_in_line(self, line: list[str], direction: str):
        merged = copy.deepcopy(line)
        i = 0
        if direction is Direction.Right: merged.reverse()
        while i < len(merged) - 1:
            current_tile = merged[i]
            next_neighbor = merged[i+1]
            if current_tile == next_neighbor:
                merged[i] = str(int(current_tile) + int(next_neighbor))
                merged.pop(i+1)
            i += 1
        if direction is Direction.Right: merged.reverse()
        return merged

    def reduce_line(self, line: list[str], direction: str):
        not_zero_tiles = [el for el in line if el != '0']
        reduced = self.merge_tiles_in_line(not_zero_tiles, direction)
        if direction == Direction.Right:
            side = 0
        else:
            side = len(reduced)
        while len(reduced) < self.FieldSize:
            reduced.insert(side, '0')
        print(f'REDUCED IS {reduced}')
        return reduced

    def move_in_table(self, table, direction: 'str'):
        new_table = copy.deepcopy(table)
        if direction in ('L', 'R'):
            for i, line in enumerate(table):
                new_table[i] = self.reduce_line(line, direction)
        else:
            rotated_table = self.rotate_table(table)
            # in Rotated Up == Left, Down == Right
            if direction == Direction.Up:
                direction = Direction.Left
            else:
                direction = Direction.Right
            for i, line in enumerate(rotated_table):
                rotated_table[i] = self.reduce_line(line, direction)
            new_table = self.rotate_table(rotated_table)
        return new_table


import unittest as unit

class TestGameField(unit.TestCase):

    def test_line_is_reducible(self):
        g = GameField()
        self.cases = ('0 0 0 0', '2 4 0 0', '0 4 0 0', '2 2 0 0', '4 4 2 2', '2 0 0 2')
        for c in self.cases:
            with self.subTest(case=c):
                case = c.split()
                self.assertTrue(g.line_is_reducible(case), msg=f'Line {c} should be reducibe one')

        self.cases = ('2 4 16 2', '2 4 2 16', )
        for c in self.cases:
            with self.subTest(case=c):
                case = c.split()
                self.assertFalse(g.line_is_reducible(case), msg=f'Line {c} should NOT be reducibe one')

    def test_table_is_reducible(self):
        g = GameField()
        self.cases = (
            [['4', '2', '4', '2'],
             ['16', '4', '2', '4'],
             ['4', '2', '16', '2'],
             ['2', '4', '2', '8']]
        )
        for c in self.cases:
            with self.subTest(case=c):
                case = c
                self.assertFalse(g.table_is_reducible(case), msg=f'Table cannot be reduced')

    def test_merge_tiles_in_line(self):
        g = GameField()
        self.cases = ('2 2 4 4', '2 2 2 2', '2 4 2 2', '8 4 2 2')
        excepted = ('4 8', '4 4', '2 4 4', '8 4 4')
        for i, c in enumerate(self.cases):
            with self.subTest(case=c):
                case = c.split()
                self.assertEqual(g.merge_tiles_in_line(case, Direction.Right), excepted[i].split(), msg=f'Line {c} should be merged to {excepted[i]}')

    def test_reduce_line(self):
        g = GameField()
        self.cases = (('2 2 4 4', 'R'), ('2 2 2 2', 'L'), ('2 4 2 2', 'L'), ('8 4 2 2', 'R'))
        excepted = ('0 0 4 8', '4 4 0 0', '2 4 4 0', '0 8 4 4')
        for i, c in enumerate(self.cases):
            with self.subTest(case=c):
                case = c[0].split()
                direct = c[1]
                self.assertEqual(g.reduce_line(case, direct), excepted[i].split(),
                                 msg=f'Line {c} should be reduced to {excepted[i]}')

    def test_move_in_table(self):
        g = GameField()
        self.cases = (
            ([['4', '4', '2', '2'],
             ['4', '4', '2', '2'],
             ['4', '4', '2', '2'],
             ['4', '4', '2', '2']], 'R')
        )

        expected = (
             [['0', '0', '8', '4'],
              ['0', '0', '8', '4'],
              ['0', '0', '8', '4'],
              ['0', '0', '8', '4']]
        )
        for c in self.cases:
            with self.subTest(case=c):
                case = c[0]
                direct = c[1]
                msg = f'Table should be {expected[0]}'
                self.assertEqual(g.move_in_table(case, direct), expected[0], msg=msg)


def test_suite():
    suite = unit.TestSuite()
    suite.addTest(TestGameField('test_line_is_reducible'))
    suite.addTest(TestGameField('test_table_is_reducible'))
    suite.addTest(TestGameField('test_merge_tiles_in_line'))
    suite.addTest(TestGameField('test_reduce_line'))
    suite.addTest(TestGameField('test_move_in_table'))
    return suite


if __name__ == '__main__':
    runner = unit.TextTestRunner(stream=sys.stdout, verbosity=2)
    test_suite = test_suite()
    runner.run(test_suite)
    g = GameField()
    print()
    g.print_table(g.rotate_table(g.read_file('inp')[0]))
