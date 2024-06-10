import time
import random
import pacman
import math


class Controller:
    "This class is a controller for a Pacman game."

    def __init__(self, N, M, init_locations, init_pellets, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout.
        N - board size along the coordinate y (number of rows)
        M - board size along the coordinate x (number of columns)
        init_locations - the locations of ghosts and Pacman in the initial state
        init_pellets - the locations of pellets in the initial state
        steps - number of steps the controller will perform
        """

        self.N = N
        self.M = M
        self.init_locations = init_locations
        self.init_pellets = init_pellets
        self.steps = steps
        self.q_table = [[0 for j in range(4)] for i in range(N * M)]
        self.episodes = 5000
        self.gamma = 0.95
        self.alpha = 0.8
        self.epsilon = 1
        self.p = 0.7
        self.board = [[10] * self.M for _ in range(self.N)]  # Initialize the board with empty slots (value 10)
        self.construct_board()
        self.game = pacman.Game(steps, self.board)  # Create a game instance
        self.q_learning()

    def construct_board(self):
        # Add monsters and Pacman to the board
        for entity, position in self.init_locations.items():
            if position is not None:
                x, y = position
                self.board[x][y] = entity * 10

        # Add pellets to the board
        for pellet_position in self.init_pellets:
            x, y = pellet_position
            if self.board[x][y] != 10:
                self.board[x][y] += 1
            else:
                self.board[x][y] = 11

    def run_epsilon_greedy(self, state, episode):
        self.epsilon = max(0.01, math.exp(-0.01 * episode))  # Reduce epsilon over episodes
        if random.random() < self.epsilon:
            return random.choice(['U', 'D', 'L', 'R'])  # Explore randomly
        return self.get_best_action(state)  # Exploit best action from Q-table

    def get_best_action(self, state):
        """Get the index of the best action for the given state from the Q-table."""
        actions = dict(zip((0, 1, 2, 3), ('R', 'D', 'L', 'U')))
        action_index = self.q_table[state].index(max(self.q_table[state]))
        return actions[action_index]

    def get_state(self):
        """Convert current state to a unique state index."""
        pacman_position = None
        for i in range(self.N):  # Find Pacman position
            for j in range(self.M):
                if self.game.board[i][j] == 70:
                    pacman_position = (i, j)
                    break
            if pacman_position is not None:
                break
        if pacman_position is not None:
            x, y = pacman_position
            state_index = x * self.M + y
            return state_index
        return None

    def q_learning(self):
        actions = dict(zip(('R', 'D', 'L', 'U'), (0, 1, 2, 3)))

        for episode in range(self.episodes):
            self.game.reset()  # Reset the game and get initial state
            episode_reward = 0
            step = 0

            while step < self.steps:
                state = self.get_state()
                action = self.run_epsilon_greedy(state, episode)
                if random.random() < self.p:
                    move = self.game.actions[action]
                else:
                    moves = ['U', 'R', 'D', 'L']
                    moves.remove(action)  # Remove the chosen action from the list of available actions
                    action = random.choice(moves)  # Choose a random action from the remaining valid actions
                    move = self.game.actions[action]

                # Execute the action and observe the reward and next state
                reward = self.game.update_board(move)
                next_state = self.get_state()

                # Update Q-value for the current state and action
                prev_q_value = self.q_table[state][actions[action]]
                next_max_q_value = max(self.q_table[next_state])
                new_q_value = prev_q_value + self.alpha * (reward + self.gamma * next_max_q_value - prev_q_value)
                self.q_table[state][actions[action]] = new_q_value

                episode_reward += reward

                if self.game.done:
                    break
                step += 1

    def choose_next_move(self, locations, pellets):
        "Choose next action for Pacman given the current state of the board."
        state_index = self.get_state()  # Get the current state index
        if state_index is not None:
            action = self.get_best_action(state_index)  # Get the best action index from the Q-table
            return action  # Return the corresponding action
        else:
            # Handle the case where the state index is None (e.g., Pacman not found on the board)
            return random.choice(['U', 'R', 'D', 'L'])
