import numpy as np
import random
import time
import matplotlib.pyplot as plt

class MagicCube:
    def __init__(self, n):
        self.n = n
        self.magicnumber = 315
        self.totalelements = 109 # Jumlah elemen pada magic cube (baris, kolom, tiang, diagonal bidang, diagonal ruang)
        self.targetvalue = self.magicnumber * self.totalelements # Buat rumus objective valuesnya nanti
        self.cube = self.generateRandomStates()
    
    def generateRandomStates(self):
        # Bikin cube dengan angka random dan ngga magic cube
        numbers = np.arange(1, self.n ** 3 + 1)
        np.random.shuffle(numbers)
        randomCube = numbers.reshape((self.n, self.n, self.n))
        return randomCube

    def calculateElements(self):
        # Buat ngitung total baris, kolom, tiang, diagonal bidang, sama diagonal ruang cube
        Sbarisx = []
        Skolomx = []
        Stiangx = []
        Sdiagonalbidangx = []
        Sdiagonalruangx = []
        
        # Sbarisx: total penjumlahan baris dari semua sisi
        for layer in range(self.n):
            for row in range(self.n):
                Sbarisx.append(np.sum(self.cube[layer, row, :]))
        
        # Skolomx: total penjumlahan kolom dari semua sisi
        for layer in range(self.n):
            for col in range(self.n):
                Skolomx.append(np.sum(self.cube[layer, :, col]))
        
        # Stiangx: total penjumlahan tiang dari diagonal magic cube
        for row in range(self.n):
            for col in range(self.n):
                Stiangx.append(np.sum(self.cube[:, row, col]))
        
        # Sdiagonal_bidangx: total penjumlahan diagonal bidang dari semua sisi
        for layer in range(self.n):
            diag1 = np.sum([self.cube[layer, i, i] for i in range(self.n)])
            diag2 = np.sum([self.cube[layer, i, self.n - i - 1] for i in range(self.n)])
            Sdiagonalbidangx.extend([diag1, diag2])

        # Sdiagonal_ruangx: total penjumlahan diagonal ruang pada diagonal magic cube
        Sdiagonalruangx.extend([
            np.sum([self.cube[i, i, i] for i in range(self.n)]),
            np.sum([self.cube[i, i, self.n - i - 1] for i in range(self.n)]),
            np.sum([self.cube[i, self.n - i - 1, i] for i in range(self.n)]),
            np.sum([self.cube[i, self.n - i - 1, self.n - i - 1] for i in range(self.n)])
        ])
        
        # Ngembaliin hasil dari semua masing masing elemen (bentuknya list)
        return Sbarisx + Skolomx + Stiangx + Sdiagonalbidangx + Sdiagonalruangx 

    def objectiveFunction(self):
        # Rumus objective function
        totalSums = self.calculateElements()
        fx = sum(abs(sums - self.magicnumber) for sums in totalSums)
        print("Objective function:", fx)
        return fx

    def swapElements(self, pos1, pos2):
        # Buat ngeswap angka dan mastiin 2 angka doang yang di swap
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        self.cube[x1, y1, z1], self.cube[x2, y2, z2] = self.cube[x2, y2, z2], self.cube[x1, y1, z1]
    
    def isValid(self):
        # Buat cek dia magic cube apa ngga (objective function = 0)
        return self.objectiveFunction() == 0

    def nextStates(self):
        # Cek next state yang ada (succesor) dengan cara nge swap
        nextstates = []
        for x1 in range(self.n):
            for y1 in range(self.n):
                for z1 in range(self.n):
                    for x2 in range(self.n):
                        for y2 in range(self.n):
                            for z2 in range(self.n):
                                if (x1, y1, z1) != (x2, y2, z2):  # Ini buat mastiin kita ga nuker elemen yang sama
                                    newCube = MagicCube(self.n)
                                    newCube.cube = np.copy(self.cube)
                                    newCube.swapElements((x1, y1, z1), (x2, y2, z2))
                                    nextstates.append(newCube)
        return nextstates

    def visualize(self):
        # Buat visualisasi layer magic cube 
        fig, axes = plt.subplots(1, self.n, figsize=(3 * self.n, 3))
        fig.suptitle('Visualisasi Diagonal Magic Cube', fontsize=16)

        for layer in range(self.n):
            ax = axes[layer] # pake axes biar bisa nyamping
            ax.imshow(self.cube[layer], cmap='Pastel1', interpolation='nearest') # warna pastel biar imut
            ax.set_title(f'Layer {layer + 1}')
            ax.axis('off') # biar lebih rapih
            
            for i in range(self.n):
                for j in range(self.n):
                    ax.text(j, i, str(self.cube[layer][i, j]), ha='center', va='center', color='black')

        plt.tight_layout()
        plt.show()