"""
The pocket dimension contains an infinite 4-dimensional grid.
At every integer 4-dimensional coordinate (x,y,z,w),
there exists a single hypercube which is either active (#) or inactive (.).
"""
import copy
from collections import defaultdict
from itertools import product


class Cube:
    def __init__(self, initial_state):
        self.cycle = 0
        self.cube_states = defaultdict(lambda: False)
        for y, row in enumerate(initial_state.splitlines()):
            for x, state in enumerate(row.strip()):
                self.cube_states[(x, y, 0, 0)] = state == '#'

    def count_total_active(self):
        return sum([active for active in self.cube_states.values()])

    def get_neighbors(self, position):
        """
        Any of the 80 other cubes where any of their
        coordinates differ by at most 1.
        """
        x, y, z, w = position
        n_x = [x - 1, x, x + 1]
        n_y = [y - 1, y, y + 1]
        n_z = [z - 1, z, z + 1]
        n_w = [w - 1, w, w + 1]
        neighbors = list(product(*[n_x, n_y, n_z, n_w]))
        neighbors.remove(position)  # remove current position from neighbors
        return neighbors

    def run_cycle(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active
        the cube remains active. Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active,
        the cube becomes active. Otherwise, the cube remains inactive.
        """
        updated_states = copy.deepcopy(self.cube_states)
        i = self.cycle + 10  # dynamically grow range of grid space to search
        for position in product(range(-i, i), repeat=4):
            active = self.cube_states[position]
            neighbors = self.get_neighbors(position)
            neighbors_count = sum([self.cube_states[n_pos]
                                   for n_pos in neighbors])
            if active and (neighbors_count not in [2, 3]):
                updated_states[position] = False
            elif not active and neighbors_count == 3:
                updated_states[position] = True
        self.cube_states = updated_states
        self.cycle += 1


def main(puzzle_input, turns):
    cube = Cube(puzzle_input)
    for t in range(turns):
        cube.run_cycle()
    return cube.count_total_active()


TEST_INPUT = """\
.#.
..#
###"""

PUZZLE_INPUT = """\
##..####
.###....
#.###.##
#....#..
...#..#.
#.#...##
..#.#.#.
.##...#."""

assert main(TEST_INPUT, 6) == 848

cubes = main(PUZZLE_INPUT, 6)
print("solution:", cubes)
