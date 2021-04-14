import copy


class Direction:
    Up = 'U'
    Down = 'D'
    Left = 'L'
    Right = 'R'


class Game2048:
    FieldSize = 4

    def read_file(self, path='inp') -> tuple[list[list[str]], list[str]]:
        with open(path, 'r') as f:
            table = [f.readline().strip().split(' ') for line in range(4)]
            controls = f.readline().split()
        return table, controls

    def write_table_to_file(self, table: list[list[str]], path='output.txt'):
        with open(path, 'w') as f:
            for line in table:
                f.write(' '.join(line) + '\n')

    def print_table(self, table: list[list[str]]):
        print('\n')
        print(*table, sep='\n')
        print('\n')

    def line_is_reducible(self, line: list[str]) -> bool:
        if '0' in line:
            return True
        for i in range(len(line) - 1):
            if line[i] == line[i + 1] and line != '0':
                return True
        return False

    def table_is_reducible(self, table: list[list[str]]) -> bool:
        all_possible_lines = table + self.rotate_table(table)
        return any(self.line_is_reducible(line) for line in all_possible_lines)

    def rotate_table(self, table: list[list[str]]) -> list[list[str]]:
        return [list(row) for row in zip(*table)]

    def merge_numbers_in_line(self, line: list[str], direction: str) -> list[str]:
        merged = copy.deepcopy(line)
        if '0' in merged:
            merged = list(filter(lambda el: el != '0', merged))
        i = 0
        if direction is Direction.Right: merged.reverse()
        while i < len(merged) - 1:
            current_tile = merged[i]
            next_neighbor = merged[i + 1]
            if current_tile == next_neighbor:
                merged[i] = str(int(current_tile) + int(next_neighbor))
                merged.pop(i + 1)
            i += 1
        if direction is Direction.Right: merged.reverse()
        return merged

    def one_move_in_line(self, line: list[str], direction: str):
        # manages Left/Right sides to insert zeros into merged list
        reduced = self.merge_numbers_in_line(line, direction)
        if direction == Direction.Right:
            side = 0
        else:
            side = len(reduced)
        while len(reduced) < self.FieldSize:
            reduced.insert(side, '0')
        return reduced

    def one_move_in_table(self, table, direction: str) -> list[list[str]]:
        new_table = copy.deepcopy(table)
        if direction in ('L', 'R'):
            for i, line in enumerate(table):
                new_table[i] = self.one_move_in_line(line, direction)
        elif direction in ('U', 'D'):
            rotated_table = copy.deepcopy(self.rotate_table(table))
            # Up/Down -> Left/Right in transposed table
            if direction == Direction.Up:
                direction = Direction.Left
            else:
                direction = Direction.Right
            for i, line in enumerate(rotated_table):
                rotated_table[i] = self.one_move_in_line(line, direction)
            self.print_table(rotated_table)
            new_table = self.rotate_table(rotated_table)
        return new_table

    def run_file(self, path='inp'):
        inp_table, moves = self.read_file(path)
        for move in moves:
            inp_table = self.one_move_in_table(inp_table, move)
        self.write_table_to_file(inp_table)


if __name__ == '__main__':
    g = Game2048()
    g.run_file('inp')
