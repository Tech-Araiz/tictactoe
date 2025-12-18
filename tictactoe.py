import tkinter as tk
import pyodbc

DEFAULT_CONN = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-RR0LU1O;Database=TicTacToe;Trusted_Connection=yes;"
)

class DatabaseManager:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string or DEFAULT_CONN
        self.conn = pyodbc.connect(self.connection_string, autocommit=True)
        self.ensure_schema()

    def ensure_schema(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.users', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(255) NOT NULL UNIQUE,
                    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
                );
            END
            """
        )
        cursor.execute(
            """
            IF OBJECT_ID('dbo.matches', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.matches (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    player_o_id INT NOT NULL,
                    player_x_id INT NOT NULL,
                    winner_id INT NULL,
                    is_draw BIT NOT NULL DEFAULT 0,
                    played_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                    CONSTRAINT FK_matches_o FOREIGN KEY (player_o_id) REFERENCES dbo.users(id),
                    CONSTRAINT FK_matches_x FOREIGN KEY (player_x_id) REFERENCES dbo.users(id),
                    CONSTRAINT FK_matches_w FOREIGN KEY (winner_id) REFERENCES dbo.users(id)
                );
            END
            """
        )
        cursor.close()

    def get_or_create_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM dbo.users WHERE username = ?", username)
        row = cursor.fetchone()
        if row:
            cursor.close()
            return int(row[0])
        cursor.execute("INSERT INTO dbo.users (username) VALUES (?)", username)
        cursor.execute("SELECT @@IDENTITY")
        new_id = int(cursor.fetchone()[0])
        cursor.close()
        return new_id

    def record_match(self, player_o_id, player_x_id, winner_id):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO dbo.matches (player_o_id, player_x_id, winner_id, is_draw)
            VALUES (?, ?, ?, ?)
            """,
            player_o_id,
            player_x_id,
            winner_id,
            1 if winner_id is None else 0,
        )
        cursor.close()

    def fetch_leaderboard(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 10
                u.username,
                SUM(CASE WHEN m.winner_id = u.id THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN m.winner_id IS NULL AND m.id IS NOT NULL 
                         AND (m.player_o_id = u.id OR m.player_x_id = u.id)
                    THEN 1 ELSE 0 END) AS draws
            FROM dbo.users u
            LEFT JOIN dbo.matches m ON m.player_o_id = u.id OR m.player_x_id = u.id
            GROUP BY u.id, u.username
            ORDER BY wins DESC, draws DESC, u.username ASC
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return [{"username": r[0], "wins": int(r[1] or 0), "draws": int(r[2] or 0)} for r in rows]


class TicTacToe:
    def __init__(self):
        self.db = DatabaseManager()
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("750x680")
        self.root.configure(bg="#2c3e50")
        
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "O"
        self.game_over = False
        self.player_o_name = "Player 1"
        self.player_x_name = "Player 2"
        self.player_o_id = None
        self.player_x_id = None
        
        self.player_o_var = tk.StringVar(value=self.player_o_name)
        self.player_x_var = tk.StringVar(value=self.player_x_name)
        
        self.create_widgets()
        self.refresh_leaderboard()
    
    def create_widgets(self):
        # Main container with two columns
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Game
        left_frame = tk.Frame(main_frame, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Title
        tk.Label(
            left_frame,
            text="TIC TAC TOE",
            font=("Arial", 24, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(pady=(0, 15))
        
        # Player names
        players_frame = tk.Frame(left_frame, bg="#2c3e50")
        players_frame.pack(pady=10)
        
        tk.Label(players_frame, text="Player O:", fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=0, padx=5)
        tk.Entry(players_frame, textvariable=self.player_o_var, width=15).grid(row=0, column=1, padx=5)
        tk.Label(players_frame, text="Player X:", fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=0, padx=5)
        tk.Entry(players_frame, textvariable=self.player_x_var, width=15).grid(row=1, column=1, padx=5)
        
        tk.Button(
            players_frame,
            text="Start Match",
            bg="#2980b9",
            fg="white",
            command=self.start_match
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Turn indicator
        self.turn_label = tk.Label(
            left_frame,
            text="Enter names and start match",
            font=("Arial", 14),
            fg="#3498db",
            bg="#2c3e50"
        )
        self.turn_label.pack(pady=10)
        
        # Game board
        board_frame = tk.Frame(left_frame, bg="#2c3e50")
        board_frame.pack(pady=15)
        
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=5,
                    height=2,
                    bg="#34495e",
                    fg="#ecf0f1",
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # New Game button
        tk.Button(
            left_frame,
            text="New Game",
            font=("Arial", 12),
            bg="#27ae60",
            fg="white",
            command=self.new_game
        ).pack(pady=15)
        
        # Right side - Leaderboard
        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            right_frame,
            text="LEADERBOARD",
            font=("Arial", 16, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(pady=(0, 10))
        
        # Leaderboard frame with scrollbar
        leaderboard_frame = tk.Frame(right_frame, bg="#2c3e50")
        leaderboard_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(leaderboard_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.leaderboard_text = tk.Text(
            leaderboard_frame,
            font=("Consolas", 10),
            fg="#ecf0f1",
            bg="#2c3e50",
            width=30,
            yscrollcommand=scrollbar.set,
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.leaderboard_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.leaderboard_text.yview)
    
    def start_match(self):
        self.player_o_name = self.player_o_var.get() or "Player 1"
        self.player_x_name = self.player_x_var.get() or "Player 2"
        self.player_o_id = self.db.get_or_create_user(self.player_o_name)
        self.player_x_id = self.db.get_or_create_user(self.player_x_name)
        self.new_game()
        self.refresh_leaderboard()
    
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] or not self.player_o_id or not self.player_x_id:
            return
        
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            state="disabled",
            bg="#95a5a6"
        )
        
        if self.check_winner():
            self.game_over = True
            winner_name = self.player_o_name if self.current_player == "O" else self.player_x_name
            self.turn_label.config(text=f"{winner_name} Wins!", fg="#27ae60")
            self.highlight_winner()
            winner_id = self.player_o_id if self.current_player == "O" else self.player_x_id
            self.db.record_match(self.player_o_id, self.player_x_id, winner_id)
            self.refresh_leaderboard()
            return
        
        if all(self.board[i][j] for i in range(3) for j in range(3)):
            self.game_over = True
            self.turn_label.config(text="It's a Draw!", fg="#e74c3c")
            self.db.record_match(self.player_o_id, self.player_x_id, None)
            self.refresh_leaderboard()
            return
        
        self.current_player = "X" if self.current_player == "O" else "O"
        next_name = self.player_o_name if self.current_player == "O" else self.player_x_name
        color = "#e74c3c" if self.current_player == "O" else "#3498db"
        self.turn_label.config(text=f"{next_name}'s Turn ({self.current_player})", fg=color)
    
    def check_winner(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] == self.current_player or
                self.board[0][i] == self.board[1][i] == self.board[2][i] == self.current_player):
                return True
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player):
            return True
        return False
    
    def highlight_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == self.current_player:
                for j in range(3):
                    self.buttons[i][j].config(bg="#27ae60")
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == self.current_player:
                for j in range(3):
                    self.buttons[j][i].config(bg="#27ae60")
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            for i in range(3):
                self.buttons[i][i].config(bg="#27ae60")
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
            for i in range(3):
                self.buttons[i][2-i].config(bg="#27ae60")
    
    def refresh_leaderboard(self):
        rows = self.db.fetch_leaderboard()
        self.leaderboard_text.config(state=tk.NORMAL)
        self.leaderboard_text.delete(1.0, tk.END)
        if not rows:
            self.leaderboard_text.insert(1.0, "No matches yet!")
        else:
            lines = ["Player              Wins  Draws\n"]
            for row in rows:
                lines.append(f"{row['username']:<18}  {row['wins']:<4}  {row['draws']}\n")
            self.leaderboard_text.insert(1.0, "".join(lines))
        self.leaderboard_text.config(state=tk.DISABLED)
    
    def new_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "O"
        self.game_over = False
        
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state="normal", bg="#34495e")
        
        self.turn_label.config(text=f"{self.player_o_name}'s Turn (O)", fg="#e74c3c")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()