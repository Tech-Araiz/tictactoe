import unittest
from tictactoe import TicTacToe


class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = TicTacToe()
        self.game.root.withdraw()
    
    def tearDown(self):
        """Clean up after each test method."""
        if self.game.root:
            self.game.root.destroy()
    
    def test_initial_game_state(self):
        """Test that the game initializes with correct default values."""
        self.assertEqual(self.game.current_player, "O")
        self.assertFalse(self.game.game_over)
        expected_board = [["" for _ in range(3)] for _ in range(3)]
        self.assertEqual(self.game.board, expected_board)
    
    def test_check_winner_horizontal_rows(self):
        """Test winner detection for horizontal wins."""
        test_cases = [
            ([["O", "O", "O"], ["", "", ""], ["", "", ""]], "O"),
            ([["", "", ""], ["X", "X", "X"], ["", "", ""]], "X"),
            ([["", "", ""], ["", "", ""], ["O", "O", "O"]], "O"),
        ]
        
        for board, player in test_cases:
            with self.subTest(board=board, player=player):
                self.game.board = board
                self.game.current_player = player
                self.assertTrue(self.game.check_winner())
    
    def test_check_winner_vertical_columns(self):
        """Test winner detection for vertical wins."""
        test_cases = [
            ([["O", "", ""], ["O", "", ""], ["O", "", ""]], "O"),
            ([["", "X", ""], ["", "X", ""], ["", "X", ""]], "X"),
            ([["", "", "O"], ["", "", "O"], ["", "", "O"]], "O"),
        ]
        
        for board, player in test_cases:
            with self.subTest(board=board, player=player):
                self.game.board = board
                self.game.current_player = player
                self.assertTrue(self.game.check_winner())
    
    def test_check_winner_diagonals(self):
        """Test winner detection for diagonal wins."""
        test_cases = [
            ([["O", "", ""], ["", "O", ""], ["", "", "O"]], "O"),
            ([["", "", "X"], ["", "X", ""], ["X", "", ""]], "X"),
        ]
        
        for board, player in test_cases:
            with self.subTest(board=board, player=player):
                self.game.board = board
                self.game.current_player = player
                self.assertTrue(self.game.check_winner())
    
    def test_check_winner_no_win(self):
        """Test that check_winner returns False when there's no winner."""
        test_boards = [
            [["", "", ""], ["", "", ""], ["", "", ""]],
            [["O", "X", "O"], ["X", "O", "X"], ["X", "O", "X"]],
            [["O", "O", "X"], ["X", "X", "O"], ["", "", ""]],
        ]
        
        for board in test_boards:
            with self.subTest(board=board):
                self.game.board = board
                self.game.current_player = "O"
                self.assertFalse(self.game.check_winner())
    
    def test_winning_game_flow(self):
        """Test complete game flow when a player wins."""
        self.game.player_o_id = 1
        self.game.player_x_id = 2
        self.game.board = [["O", "O", ""], ["", "", ""], ["", "", ""]]
        self.game.current_player = "O"
        
        self.game.make_move(0, 2)
        
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.board[0][2], "O")
    
    def test_draw_game_flow(self):
        """Test complete game flow when the game ends in a draw."""
        self.game.player_o_id = 1
        self.game.player_x_id = 2
        self.game.board = [["O", "X", "O"], ["X", "X", "O"], ["X", "O", ""]]
        self.game.current_player = "X"
        
        self.game.make_move(2, 2)
        
        self.assertTrue(self.game.game_over)
    
    def test_all_winning_combinations(self):
        """Test all possible winning combinations."""
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        
        for combination in winning_combinations:
            with self.subTest(combination=combination):
                self.game.board = [["" for _ in range(3)] for _ in range(3)]
                
                for row, col in combination:
                    self.game.board[row][col] = "O"
                
                self.game.current_player = "O"
                self.assertTrue(self.game.check_winner(), f"Failed for combination: {combination}")


if __name__ == '__main__':
    unittest.main(verbosity=2)