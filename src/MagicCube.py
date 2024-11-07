import numpy as np
import random
import time
import matplotlib.pyplot as plt

class MagicCube:
    def __init__(self, n):
        self.n = n
        self.magic_number = 315
        self.total_elements = 117 # Jumlah elemen pada magic cube (baris, kolom, tiang, diagonal bidang, diagonal ruang)
        self.target_value = self.magic_number * self.total_elements
        self.cube = self.generate_random_cube()
    
    def generate_random_cube(self):
        numbers = np.arange(1, self.n ** 3 + 1)
        np.random.shuffle(numbers)
        random_cube = numbers.reshape((self.n, self.n, self.n))
        return random_cube

    def calculate_totals(self):
        Sbarisx, Skolomx, Stiangx, Sdiagonal_bidangx, Sdiagonal_ruangx = 0, 0, 0, 0, 0

        # Sbarisx: total penjumlahan baris dari semua sisi
        for layer in range(self.n):
            for row in range(self.n):
                Sbarisx += np.sum(self.cube[layer, row, :])

        # Skolomx: total penjumlahan kolom dari semua sisi
        for layer in range(self.n):
            for col in range(self.n):
                Skolomx += np.sum(self.cube[layer, :, col])

        # Stiangx: total penjumlahan tiang dari diagonal magic cube
        for row in range(self.n):
            for col in range(self.n):
                Stiangx += np.sum(self.cube[:, row, col])

        # Sdiagonal_bidangx: total penjumlahan diagonal bidang dari semua sisi
        for layer in range(self.n):
            diag1 = np.sum([self.cube[layer, i, i] for i in range(self.n)])
            diag2 = np.sum([self.cube[layer, i, self.n - i - 1] for i in range(self.n)])
            Sdiagonal_bidangx += (diag1 + diag2)

        # Sdiagonal_ruangx: total penjumlahan diagonal ruang pada diagonal magic cube
        diag_space_1 = np.sum([self.cube[i, i, i] for i in range(self.n)])
        diag_space_2 = np.sum([self.cube[i, i, self.n - i - 1] for i in range(self.n)])
        diag_space_3 = np.sum([self.cube[i, self.n - i - 1, i] for i in range(self.n)])
        diag_space_4 = np.sum([self.cube[i, self.n - i - 1, self.n - i - 1] for i in range(self.n)])
        Sdiagonal_ruangx = diag_space_1 + diag_space_2 + diag_space_3 + diag_space_4

        return Sbarisx, Skolomx, Stiangx, Sdiagonal_bidangx, Sdiagonal_ruangx

    def objective_function(self):
        Sbarisx, Skolomx, Stiangx, Sdiagonal_bidangx, Sdiagonal_ruangx = self.calculate_totals()
        total_sum = Sbarisx + Skolomx + Stiangx + Sdiagonal_bidangx + Sdiagonal_ruangx
        fx = self.target_value - total_sum
        return fx

    def swap_elements(self, pos1, pos2):
        self.cube[pos1], self.cube[pos2] = self.cube[pos2], self.cube[pos1]
    
    def is_valid_magic_cube(self):
        return self.objective_function() == 0
        
    def next_states(self):
        next_states = []
        for _ in range(10):
            pos1 = (random.randint(0, self.n - 1), random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            pos2 = (random.randint(0, self.n - 1), random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            new_cube = MagicCube(self.n)
            new_cube.cube = np.copy(self.cube)
            new_cube.swap_elements(pos1, pos2)
            next_states.append(new_cube)
        return next_states

    def visualize(self):
        fig, axes = plt.subplots(1, self.n, figsize=(15, 5))
        fig.suptitle('Visualisasi Magic Cube', fontsize=16, color='black')

        for layer in range(self.n):
            ax = axes[layer]
            
            ax.imshow(np.full((self.n, self.n), np.nan), cmap='pink', interpolation='nearest')
            
            mat = ax.imshow(self.cube[layer], cmap='viridis', interpolation='nearest', alpha=0.7)
            
            for i in range(self.n):
                for j in range(self.n):
                    ax.text(j, i, str(self.cube[layer][i, j]), ha='center', va='center', color='black')
            
            ax.set_title(f'Layer {layer + 1}', color='black')
            ax.axis('off')

        plt.show()