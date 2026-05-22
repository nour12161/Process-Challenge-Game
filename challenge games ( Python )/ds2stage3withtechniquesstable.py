import tkinter as tk
import random
from PIL import Image, ImageTk

class ZombieConfrontationGUI:
    def __init__(self, master, num_zombies):
        self.master = master
        self.master.title("Zombie Confrontation Game")
        self.num_zombies = num_zombies
        self.player1_zombies = self.generate_zombies()
        self.player2_zombies = self.generate_zombies()
        self.player1_power = 100
        self.player2_power = 100
        self.player1_treasures = []
        self.player2_treasures = []
        self.selected_technique1 = None
        self.selected_technique2 = None
        self.create_widgets()

    def generate_zombies(self):
        # Generate zombies with random treasure values and combat powers
        zombies = [{"treasure_value": random.randint(1, 10), "combat_power": random.randint(1, 10), "defeated": False} for _ in range(self.num_zombies)]
        return zombies

    def create_widgets(self):
        self.master.configure(bg="#2c3e50")
        
        # Custom fonts
        title_font = ("Helvetica", 24, "bold")
        text_font = ("Helvetica", 14)
        result_font = ("Helvetica", 16, "bold")

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="#34495e")
        self.canvas.pack()

        # Draw cart
        self.canvas.create_rectangle(50, 50, 550, 350, fill="#95a5a6", outline="#7f8c8d")
        self.canvas.create_text(300, 25, text="Zombie Cart", font=title_font, fill="#ecf0f1")

        # Draw zombies for player 1
        self.player1_zombie_images = []
        self.player1_zombie_rectangles = []
        for i, zombie in enumerate(self.player1_zombies):
            x = 100 + i * 100
            y = 100
            zombie_image = Image.open("C:/Users/LENOVO/OneDrive/Bureau/zombie.gif")
            zombie_image = zombie_image.resize((100, 100), Image.BILINEAR)
            zombie_image = ImageTk.PhotoImage(zombie_image)
            self.player1_zombie_images.append(zombie_image)
            zombie_id = self.canvas.create_image(x, y, image=zombie_image)
            self.player1_zombie_rectangles.append((x - 40, y - 40, x + 40, y + 40))

        # Draw zombies for player 2
        self.player2_zombie_images = []
        self.player2_zombie_rectangles = []
        for i, zombie in enumerate(self.player2_zombies):
            x = 100 + i * 100
            y = 250
            zombie_image = Image.open("C:/Users/LENOVO/OneDrive/Bureau/zombie.gif")
            zombie_image = zombie_image.resize((100, 100), Image.BILINEAR)
            zombie_image = ImageTk.PhotoImage(zombie_image)
            self.player2_zombie_images.append(zombie_image)
            zombie_id = self.canvas.create_image(x, y, image=zombie_image)
            self.player2_zombie_rectangles.append((x - 40, y - 40, x + 40, y + 40))

        # Player 1's technique selection
        self.player1_technique_label = tk.Label(self.master, text="Player 1, select a technique:", font=text_font, fg="#ecf0f1", bg="#2c3e50")
        self.player1_technique_label.pack()

        self.player1_techniques = ["Dynamic Programming", "Backtracking", "Branch and Bound"]
        self.selected_technique1 = tk.StringVar()
        self.selected_technique1.set(self.player1_techniques[0])  
        for technique in self.player1_techniques:
            tk.Radiobutton(self.master, text=technique, variable=self.selected_technique1, value=technique, font=text_font, fg="#ecf0f1", bg="#2c3e50", selectcolor="#2c3e50").pack(anchor=tk.W)

        # Player 2's technique selection
        self.player2_technique_label = tk.Label(self.master, text="Player 2, select a technique:", font=text_font, fg="#ecf0f1", bg="#2c3e50")
        self.player2_technique_label.pack()

        self.player2_techniques = ["Dynamic Programming", "Backtracking", "Branch and Bound"]
        self.selected_technique2 = tk.StringVar()
        self.selected_technique2.set(self.player2_techniques[0])  
        for technique in self.player2_techniques:
            tk.Radiobutton(self.master, text=technique, variable=self.selected_technique2, value=technique, font=text_font, fg="#ecf0f1", bg="#2c3e50", selectcolor="#2c3e50").pack(anchor=tk.W)

        # Start button
        self.start_button = tk.Button(self.master, text="Start", command=self.start_game, font=text_font, fg="#ecf0f1", bg="#3498db")
        self.start_button.pack(pady=(20, 10))

        self.result_label = tk.Label(self.master, text="", font=result_font, fg="#27ae60", bg="#2c3e50")
        self.result_label.pack(pady=(20, 10))

        # Player's attack power labels
        self.player1_power_label = tk.Label(self.master, text=f"", font=text_font, fg="#ecf0f1", bg="#2c3e50")#Player 1 Power: {self.player1_power}
        self.player1_power_label.pack()
        
        self.player2_power_label = tk.Label(self.master, text=f"", font=text_font, fg="#ecf0f1", bg="#2c3e50")#Player 2 Power: {self.player2_power}
        self.player2_power_label.pack()

    def start_game(self):
        # Reset treasures
        self.player1_treasures = []
        self.player2_treasures = []

        # Reset player powers
        self.player1_power = 100
        self.player2_power = 100

        # Get selected techniques for both players
        selected_technique1 = self.selected_technique1.get()
        selected_technique2 = self.selected_technique2.get()

        # Initialize indices for both players
        player1_index = 0
        player2_index = 0

        # Confront zombies until one of the players runs out of power or there are no unbeaten zombies left
        while self.player1_power > 0 and self.player2_power > 0 and (player1_index < len(self.player1_zombies) or player2_index < len(self.player2_zombies)):
            # Player 1 confronts a zombie if available
            if player1_index < len(self.player1_zombies) and not self.player1_zombies[player1_index]["defeated"]:
                self.confront_zombie(1, selected_technique1, player1_index)
                player1_index += 1

            # Player 2 confronts a zombie if available
            if player2_index < len(self.player2_zombies) and not self.player2_zombies[player2_index]["defeated"]:
                self.confront_zombie(2, selected_technique2, player2_index)
                player2_index += 1

        # Update power labels
        self.player1_power_label.config(text=f"") #Player 1 Power: {self.player1_power} didn't work
        self.player2_power_label.config(text=f"") #Player 2 Power: {self.player2_power}

        # Determine winner after both players have confronted zombies
        self.determine_winner()


    def confront_zombie(self, player, selected_technique, zombie_index):
        # Get player's treasures and power
        if player == 1:
            player_treasures = self.player1_treasures
            player_power = self.player1_power
            power_label = self.player1_power_label
            zombies = self.player1_zombies
        else:
            player_treasures = self.player2_treasures
            player_power = self.player2_power
            power_label = self.player2_power_label
            zombies = self.player2_zombies

        # Get the zombie at the specified index
        zombie = zombies[zombie_index]

        # Check if the zombie is defeated and the player has enough power to defeat it
        if not zombie["defeated"] and player_power >= zombie["combat_power"]:
            # Defeat the zombie
            player_treasures.append(zombie["treasure_value"])
            player_power -= zombie["combat_power"]  # Decrease player's power
            power_label.config(text=f"Player {player} Power: {player_power}")
            zombie["defeated"] = True  # Mark the zombie as defeated
            
    def get_nearest_zombie(self, selected_technique, player_power):
        available_zombies = [zombie for zombie in self.zombies if not zombie["defeated"] and player_power >= zombie["combat_power"]]
        print("Available zombies:", available_zombies)
        
        if not available_zombies:
            return None
        
        if selected_technique == "Dynamic Programming":
            nearest_zombie = min(available_zombies, key=lambda z: abs(player_power - z["combat_power"]))
            print("Nearest zombie (Dynamic Programming):", nearest_zombie)
            return nearest_zombie

        elif selected_technique == "Backtracking":
            nearest_zombie = min(available_zombies, key=lambda z: z["combat_power"])
            print("Nearest zombie (Backtracking):", nearest_zombie)
            return nearest_zombie

        elif selected_technique == "Branch and Bound":
            nearest_zombie = min(available_zombies, key=lambda z: abs(player_power - z["combat_power"]))
            print("Nearest zombie (Branch and Bound):", nearest_zombie)
            return nearest_zombie

        else:
            raise ValueError("Invalid technique")

    def dynamic_programming_nearest_zombie(self, zombies, player_power):
        dp = [None] * (player_power + 1)
        dp[0] = []
        
        for zombie in zombies:
            for j in range(player_power, zombie["combat_power"] - 1, -1):
                if dp[j - zombie["combat_power"]] is not None:
                    if dp[j] is None or len(dp[j]) > len(dp[j - zombie["combat_power"]]) + 1:
                        dp[j] = dp[j - zombie["combat_power"]] + [zombie]
        
        nearest_zombies = [zombie for zombie in dp if zombie is not None]
        return min(nearest_zombies, key=lambda x: sum(z["combat_power"] for z in x))

    def backtracking_nearest_zombie(self, zombies, player_power):
        min_distance = float('inf')
        nearest_zombie = None

        def backtrack(index, remaining_power, path):
            nonlocal min_distance, nearest_zombie

            if index == len(zombies):
                return

            zombie = zombies[index]
            if zombie["defeated"] or remaining_power < zombie["combat_power"]:
                backtrack(index + 1, remaining_power, path)
            else:
                remaining_power -= zombie["combat_power"]
                path.append(zombie)
                if remaining_power < min_distance:
                    min_distance = remaining_power
                    nearest_zombie = path[:]
                backtrack(index + 1, remaining_power, path)
                path.pop()
        
        backtrack(0, player_power, [])
        return nearest_zombie

    def branch_and_bound_nearest_zombie(self, zombies, player_power):
        min_distance = float('inf')
        nearest_zombie = None

        def branch_and_bound(index, remaining_power, path):
            nonlocal min_distance, nearest_zombie

            if index == len(zombies):
                return

            zombie = zombies[index]
            if zombie["defeated"] or remaining_power < zombie["combat_power"]:
                branch_and_bound(index + 1, remaining_power, path)
            else:
                remaining_power -= zombie["combat_power"]
                path.append(zombie)
                if remaining_power < min_distance:
                    min_distance = remaining_power
                    nearest_zombie = path[:]
                branch_and_bound(index + 1, remaining_power, path)
                path.pop()
                branch_and_bound(index + 1, remaining_power + zombie["combat_power"], path)

        branch_and_bound(0, player_power, [])
        return nearest_zombie

    def determine_winner(self):
        # Determine winner based on collected treasures
        player1_score = sum(self.player1_treasures)
        player2_score = sum(self.player2_treasures)

        if player1_score > player2_score:
            winner = "Player 1"
        elif player1_score < player2_score:
            winner = "Player 2"
        else:
            winner = "It's a tie"

        self.result_label.config(text=f"Game Over! {winner} wins with Player 1: {player1_score} treasures, Player 2: {player2_score} treasures.", fg="#2980b9")

def main():
    root = tk.Tk()
    app = ZombieConfrontationGUI(root, 5)  # Initialize the game with 5 zombies
    root.mainloop()

if __name__ == "__main__":
    main()
