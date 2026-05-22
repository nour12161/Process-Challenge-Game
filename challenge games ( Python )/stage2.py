import tkinter as tk
import random
import time
from collections import deque
from PIL import Image, ImageTk
import heapq


class ForestNavigationGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Forest Navigation Game")

        # Game parameters
        obstacles_player1 = 0 #score du joueur 1
        obstacles_player2 = 0 #score du joueur 2q
        self.board_size = 10  # Taille de la grille de la forêt
        self.start_point = (0, 0)
        self.end_point = (self.board_size - 1, self.board_size - 1)
        self.obstacle_density = 0.2  # Densité des obstacles dans la forêt
        self.algorithms = ["Breadth-First Search", "Depth-First Search", "Dijkstra's Algorithm"]

        # Create GUI elements
        self.canvas_player1 = tk.Canvas(self.master, width=400, height=400, bg="forest green")
        self.canvas_player1.pack(side=tk.LEFT, padx=20, pady=20)

        self.canvas_player2 = tk.Canvas(self.master, width=400, height=400, bg="forest green")
        self.canvas_player2.pack(side=tk.RIGHT, padx=20, pady=20)

        self.algorithm_label = tk.Label(self.master, text="Sélectionnez l'algorithme de navigation pour chaque joueur:")
        self.algorithm_label.pack(pady=10)

        self.player1_label = tk.Label(self.master, text="Joueur 1:")
        self.player1_label.pack()
        self.player1_var = tk.StringVar(self.master)
        self.player1_var.set(self.algorithms[0])  # Algorithme par défaut pour le joueur 1
        self.player1_menu = tk.OptionMenu(self.master, self.player1_var, *self.algorithms)
        self.player1_menu.pack(pady=5)

        self.player2_label = tk.Label(self.master, text="Joueur 2:")
        self.player2_label.pack()
        self.player2_var = tk.StringVar(self.master)
        self.player2_var.set(self.algorithms[1])  # Algorithme par défaut pour le joueur 2
        self.player2_menu = tk.OptionMenu(self.master, self.player2_var, *self.algorithms)
        self.player2_menu.pack(pady=5)

        self.start_button = tk.Button(self.master, text="Commencer la navigation", command=self.start_navigation)
        self.start_button.pack(pady=20)

        # Générer la disposition initiale de la forêt pour chaque joueur
        self.forest_player1 = [[0] * self.board_size for _ in range(self.board_size)]
        self.forest_player2 = [[0] * self.board_size for _ in range(self.board_size)]
        self.generate_obstacles(self.forest_player1)
        self.generate_obstacles(self.forest_player2)

        # Load forest background image
        self.forest_image = tk.PhotoImage(file="C:/Users/LENOVO/OneDrive/Bureau/orest.png")
        self.forest_image = self.forest_image.subsample(4, 4)

        # Dessiner les forêts initiales pour chaque joueur
        self.draw_forest(self.forest_player1, self.canvas_player1)
        self.draw_forest(self.forest_player2, self.canvas_player2)
        

    def generate_obstacles(self, forest):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if random.random() < self.obstacle_density and (r, c) != self.start_point and (r, c) != self.end_point:
                    forest[r][c] = 1  # Marquer l'obstacle

    def draw_forest(self, forest, canvas):
        cell_size = 40
        for r in range(self.board_size):
            for c in range(self.board_size):
                cell_color = "#006400" if forest[r][c] == 0 else "#8B4513"  # Chemin vert, obstacle marron
                x0, y0 = c * cell_size, r * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                canvas.create_rectangle(x0, y0, x1, y1, fill=cell_color, outline="black")
                canvas.create_image(0, 0, image=self.forest_image, anchor=tk.NW)


        # Marquer les points de départ et d'arrivée
        x0, y0 = self.start_point[1] * cell_size, self.start_point[0] * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="deep sky blue")

        x0, y0 = self.end_point[1] * cell_size, self.end_point[0] * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red")

        # Set forest background image
        
        #canvas.create_image(200, 200, image=self.forest_image)
    def start_navigation(self):
        selected_algorithm_player1 = self.player1_var.get()
        selected_algorithm_player2 = self.player2_var.get()

        start_time = time.perf_counter()
        path_player1 = self.navigate_forest(selected_algorithm_player1, self.forest_player1)
        end_time = time.perf_counter()
        execution_time_player1 = (end_time - start_time)*1000

        start_time = time.perf_counter()
        path_player2 = self.navigate_forest(selected_algorithm_player2, self.forest_player2)
        end_time = time.perf_counter()
        execution_time_player2 = (end_time - start_time)*1000
        
        obstacles_player1 = self.calculate_obstacles(path_player1, self.forest_player1)
        obstacles_player2 = self.calculate_obstacles(path_player2, self.forest_player2)

        if path_player1:
            print(f"Joueur 1 a trouvé un chemin en utilisant {selected_algorithm_player1}: {path_player1}")
            self.draw_path(path_player1, self.canvas_player1, "yellow")
        else:
            print(f"Joueur 1 n'a pas trouvé de chemin en utilisant {selected_algorithm_player1}.")

        if path_player2:
            print(f"Joueur 2 a trouvé un chemin en utilisant {selected_algorithm_player2}: {path_player2}")
            self.draw_path(path_player2, self.canvas_player2, "cyan")
        else:
            print(f"Joueur 2 n'a pas trouvé de chemin en utilisant {selected_algorithm_player2}.")

        # Déterminer le gagnant en fonction du temps et du succès de la navigation
        if path_player1 and path_player2:
            if execution_time_player1 < execution_time_player2:
                winner_message = "Joueur 1 a navigué plus rapidement avec succès !"
            elif execution_time_player2 < execution_time_player1:
                winner_message = "Joueur 2 a navigué plus rapidement avec succès !"
            else:
                winner_message = "Égalité ! Les joueurs ont terminé en même temps."
        else:
            winner_message = "Aucun joueur n'a réussi à atteindre l'objectif."

        if obstacles_player1 > obstacles_player2:
            obstacles_message = "Le joueur 1 a confronté plus d'obstacles que le joueur 2."
        elif obstacles_player2 > obstacles_player1:
            obstacles_message = "Le joueur 2 a confronté plus d'obstacles que le joueur 1."
        else:
            obstacles_message = "Les joueurs ont confronté le même nombre d'obstacles."

        self.display_result(winner_message, execution_time_player1, execution_time_player2)
        self.display_obstacles(obstacles_player1, obstacles_player2)
        print(obstacles_message)
        obstacles_label_message = tk.Label(self.master, text=obstacles_message)
        obstacles_label_message.pack()

    def calculate_obstacles(self, path, forest):
        obstacles = 0
        for node in path:
            x, y = node
            neighbors = self.get_neighbors(node)
            for neighbor in neighbors:
                nx, ny = neighbor
                if forest[nx][ny] == 1:
                    obstacles += 1
        return obstacles

    def display_obstacles(self, obstacles_player1, obstacles_player2):
        obstacles_label_player1 = tk.Label(self.master, text=f"Obstacles Joueur 1: {obstacles_player1}")
        obstacles_label_player1.pack()

        obstacles_label_player2 = tk.Label(self.master, text=f"Obstacles Joueur 2: {obstacles_player2}")
        obstacles_label_player2.pack()

    def navigate_forest(self, algorithm, forest):
        if algorithm == "Breadth-First Search":
            return self.breadth_first_search(forest)
        elif algorithm == "Depth-First Search":
            return self.depth_first_search(forest)
        elif algorithm == "Dijkstra's Algorithm":
            return self.dijkstra_algorithm(forest)
        else:
            return None

    def breadth_first_search(self, forest):
        # Implementation de Breadth-First Search
        queue = deque([(self.start_point, [])])
        visited = set()

        while queue:
            current_node, path = queue.popleft()
            if current_node == self.end_point:
                return path + [current_node]

            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.get_neighbors(current_node)
                for neighbor in neighbors:
                    # Check if the neighbor is not an obstacle
                    if forest[neighbor[0]][neighbor[1]] != 1:
                        queue.append((neighbor, path + [current_node]))

        return []

    def depth_first_search(self, forest):
        # Implementation de Depth-First Search
        stack = [(self.start_point, [])]
        visited = set()

        while stack:
            current_node, path = stack.pop()
            if current_node == self.end_point:
                return path + [current_node]

            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.get_neighbors(current_node)
                for neighbor in neighbors:
                    # Check if the neighbor is not an obstacle
                    if forest[neighbor[0]][neighbor[1]] != 1:
                        stack.append((neighbor, path + [current_node]))

        return []

    def dijkstra_algorithm(self, forest):
        # Implementation de Dijkstra's Algorithm
        queue = [(0, self.start_point, [])]
        visited = set()

        while queue:
            distance, current_node, path = heapq.heappop(queue)
            if current_node == self.end_point:
                return path + [current_node]

            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.get_neighbors(current_node)
                for neighbor in neighbors:
                    # Check if the neighbor is not an obstacle
                    if forest[neighbor[0]][neighbor[1]] != 1:
                        heapq.heappush(queue, (distance + 1, neighbor, path + [current_node]))

        return []

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.board_size - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.board_size - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def reconstruct_path(self, current_node, came_from):
        path = []
        while current_node is not None:
            path.append(current_node)
            if current_node in came_from:
                current_node = came_from[current_node]
            else:
                print(f"Key {current_node} not found in came_from dictionary.")
                break
        path.reverse()
        return path

    def draw_path(self, path, canvas, color):
        cell_size = 40
        for r, c in path:
            x0, y0 = c * cell_size, r * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=color)

    def display_result(self, message, execution_time_player1, execution_time_player2):
        result_label = tk.Label(self.master, text=message, fg="blue")
        result_label.pack(pady=10)

        time_label_player1 = tk.Label(self.master, text=f"Temps d'exécution Joueur 1: {execution_time_player1:.2f} secondes")
        time_label_player1.pack()

        time_label_player2 = tk.Label(self.master, text=f"Temps d'exécution Joueur 2: {execution_time_player2:.2f} secondes")
        time_label_player2.pack()

def main():
    root = tk.Tk()
    app = ForestNavigationGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
