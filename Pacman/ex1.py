import search
import math
import utils
from collections import deque

""" Rules """
SQUARE = 10
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77
WALL = 99
LOSS = 88


def check_movement(state, move, element):
    bottom = len(state) - 1
    right = len(state[0]) - 1
    for row in range(bottom + 1):
        for column in range(right + 1):
            rc = state[row][column]
            if rc == element:
                if move == "R" and column != right and state[row][column + 1] not in [RED, RED + 1, BLUE, BLUE + 1,
                                                                                      YELLOW,
                                                                                      YELLOW + 1, GREEN, GREEN + 1,
                                                                                      WALL]:
                    return True
                if move == "D" and row != bottom and state[row + 1][column] not in [RED, RED + 1, BLUE, BLUE + 1,
                                                                                    YELLOW,
                                                                                    YELLOW + 1, GREEN, GREEN + 1, WALL]:
                    return True
                if move == "L" and column != 0 and state[row][column - 1] not in [RED, RED + 1, BLUE, BLUE + 1, YELLOW,
                                                                                  YELLOW + 1, GREEN, GREEN + 1, WALL]:
                    return True
                if move == "U" and row != 0 and state[row - 1][column] not in [RED, RED + 1, BLUE, BLUE + 1, YELLOW,
                                                                               YELLOW + 1, GREEN, GREEN + 1, WALL]:
                    return True
    return False


def move_ghost(state, row, column, value):
    if state[row][column] == PACMAN:
        return None
    elif state[row][column] == SQUARE + 1:
        state[row][column] = value + 1
    else:
        state[row][column] = value
    return state


def manhattan(x1, x2, y1, y2):
    if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
        return float('inf')
    return abs(x1 - x2) + abs(y1 - y2)


def convert_to_list(state):
    return [list(row) for row in state]


def convert_to_tuple(state):
    if state is not None:
        return tuple(tuple(row) for row in state)
    return None


def find_nearest_pill(state, start):
    rows, cols = len(state), len(state[0])
    visited = set()  # Track of visited positions
    queue = deque([(start, 0)])  # Stores tuples representing positions and their distances from the starting position,
    # The Pacman distance from itself is zero.
    while queue:
        current_position, distance = queue.popleft()
        x, y = current_position
        if state[x][y] in [SQUARE + 1, RED + 1, BLUE + 1, YELLOW + 1, GREEN + 1]:
            return current_position  # Found the nearest pill
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # The possible moves (right, down, left, up)
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), distance + 1))
    return None  # No pill found


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for ghosts and Pacman:
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Pacman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        successors = []
        moves = ["R", "D", "L", "U"]
        for move in moves:
            new_state = self.result(state, move)
            if new_state is not None:  # Check if the move is valid
                successors.append((move, new_state))
        return tuple(successors)

    def result(self, state, move):
        """given state and an action and return a new state"""
        converted_state = convert_to_list(state)
        bottom = len(converted_state)
        right = len(converted_state[0])
        pacman_row = -1
        pacman_column = -1
        pacman_moved = 0
        ghost_moved = 0
        if not check_movement(state, move, PACMAN):  # This condition handles the Pacman movement
            return None
        for row in range(bottom):
            if pacman_moved == 1:
                break
            for column in range(right):
                element = converted_state[row][column]
                if element == PACMAN:
                    converted_state[row][column] = SQUARE  # clear the Pacman former square
                    if move == "R":
                        converted_state[row][column + 1] = PACMAN
                        pacman_row = row
                        pacman_column = column + 1
                    elif move == "D":
                        converted_state[row + 1][column] = PACMAN
                        pacman_row = row + 1
                        pacman_column = column
                    elif move == "L":
                        converted_state[row][column - 1] = PACMAN
                        pacman_row = row
                        pacman_column = column - 1
                    elif move == "U":
                        converted_state[row - 1][column] = PACMAN
                        pacman_row = row - 1
                        pacman_column = column
                    pacman_moved = 1
                    break
        ghost_set = [RED, BLUE, YELLOW, GREEN]
        for ghost_type in ghost_set.copy():  # handles the ghosts movement
            for row in range(bottom):
                for column in range(right):
                    element = converted_state[row][column]
                    if (element == ghost_type or element == ghost_type + 1) and ghost_type in ghost_set:
                        results = (("R", manhattan(pacman_row, row, pacman_column, column + 1)),
                                   ("D", manhattan(pacman_row, row + 1, pacman_column, column)),
                                   ("L", manhattan(pacman_row, row, pacman_column, column - 1)),
                                   ("U", manhattan(pacman_row, row - 1, pacman_column, column)))
                        sorted_results = sorted(results, key=lambda x: x[1])
                        # sorting the optional directions according to the minimum Manhattan distance
                        for direction in sorted_results:
                            if check_movement(converted_state, direction[0],
                                              element):  # This condition handles the ghost movement
                                ghost_set.remove(ghost_type)
                                if element == ghost_type:
                                    converted_state[row][column] = SQUARE
                                else:
                                    converted_state[row][column] = SQUARE + 1
                                if direction[0] == "R":
                                    converted_state = move_ghost(converted_state, row, column + 1, ghost_type)
                                elif direction[0] == "D":
                                    converted_state = move_ghost(converted_state, row + 1, column, ghost_type)
                                elif direction[0] == "L":
                                    converted_state = move_ghost(converted_state, row, column - 1, ghost_type)
                                elif direction[0] == "U":
                                    converted_state = move_ghost(converted_state, row - 1, column, ghost_type)
                                if converted_state is None:
                                    return None
                                break
        return convert_to_tuple(converted_state)

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        for row in state:
            for element in row:
                if element in [SQUARE + 1, RED + 1, BLUE + 1, YELLOW + 1, GREEN + 1]:
                    return False
        return True

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        num_of_pills = 0
        pacman_position_x = -1
        pacman_position_y = -1
        for row in node.state:
            for element in row:
                if element in [SQUARE + 1, RED + 1, BLUE + 1, YELLOW + 1, GREEN + 1]:
                    num_of_pills += 1
                if element == PACMAN:
                    pacman_position_x = node.state.index(row)
                    pacman_position_y = row.index(element)
        nearest_pill = find_nearest_pill(node.state, (pacman_position_x, pacman_position_y))  # Finding the nearest pill
        if nearest_pill is None:  # Won
            return 0
        distance_nearest_pill = manhattan(pacman_position_x, nearest_pill[0], pacman_position_y,
                                          nearest_pill[1])  # Finding the distance to the nearest pill
        return num_of_pills + distance_nearest_pill - 1  # -1 because in both will do at least 1 step


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
