"""
Autores: Gabriel Tomazini Marani 2266083
         Paulo Victor Nogueira Rodrigues 2265125
"""

from enum import IntEnum
from collections import deque
import random


class Gallon:
    def __init__(self, maxVolume, volume):
        self.maxVolume = maxVolume
        self.volume = volume

    def limit(self):
        if self.volume < 0:
            self.volume = 0
        elif self.volume > self.maxVolume:
            self.volume = self.maxVolume

    def empty(self):
        self.volume = 0

    def fill(self):
        self.volume = self.maxVolume

    def transferTo(self, other):
        destinationCapacity = other.maxVolume - other.volume

        if self.volume > destinationCapacity:
            other.volume += destinationCapacity
            self.volume -= destinationCapacity
        else:
            other.volume += self.volume
            self.volume = 0

        self.limit()
        other.limit()


class VMC(IntEnum):
    G3_EMPTY = 0
    G3_FILL = 1
    G3_TRANSFER_G5 = 2
    G5_EMPTY = 3
    G5_FILL = 4
    G5_TRANSFER_G3 = 5


class VirtualMachine:
    def __init__(self):
        self.g3 = Gallon(3, random.randint(0, 3))
        self.g5 = Gallon(5, random.randint(0, 5))

    def run(self, code: VMC):
        match code:
            case VMC.G3_EMPTY:
                self.g3.empty()
            case VMC.G3_FILL:
                self.g3.fill()
            case VMC.G3_TRANSFER_G5:
                self.g3.transferTo(self.g5)
            case VMC.G5_EMPTY:
                self.g5.empty()
            case VMC.G5_FILL:
                self.g5.fill()
            case VMC.G5_TRANSFER_G3:
                self.g5.transferTo(self.g3)
            case _:
                print("ERROR: UNKNOWN INSTRUCTION", code)

    def get_state(self):
        return (self.g3.volume, self.g5.volume)

    def set_state(self, state):
        self.g3.volume, self.g5.volume = state

    def printMemory(self):
        print("g3: {} | g5: {} \n".format(self.g3.volume, self.g5.volume))

    def success(self):
        return self.g5.volume == 4


def bfs():
    vm = VirtualMachine()  # Instância da máquina virtual
    initial_state = (vm.g3.volume, vm.g5.volume)

    print("Estado inicial foi: \n")

    vm.printMemory()

    if (
        vm.g5.volume == 4
    ):  # Se o estado inicial já for a solução, não é necessário busca
        print("Galão g5 já começou com 4l, não é necessário busca :D\n")
        exit()

    queue = deque(
        [(initial_state, [])]
    )  # Fila vai consistir de nodos, cada nodo vai ter um estado e o caminho
    visited = set(
        [initial_state]
    )  # Marco o estado inicial como visitado, pois iremos começar dele
    solutions = []  # Lista onde as soluções serão armazenadas

    commands = [
        VMC.G3_EMPTY,
        VMC.G5_EMPTY,
        VMC.G5_FILL,
        VMC.G3_FILL,
        VMC.G3_TRANSFER_G5,
        VMC.G5_TRANSFER_G3,
    ]

    # Aqui começa o BFS, vizinhos são tuplas compostas por estados e o caminho de comandos que levou até ali
    while queue:  # Algoritmo executa enquanto houverem nodos na fila
        (
            current_state,
            path,
        ) = (
            queue.popleft()
        )  # Tira o primeiro item da fila, armazena o estado atual e o caminho
        for command in commands:
            vm.set_state(current_state)
            vm.run(command)
            new_state = vm.get_state()
            if new_state not in visited:
                if vm.success():
                    solutions.append(path + [command])
                else:
                    queue.append((new_state, path + [command]))
                visited.add(new_state)

    return solutions


def main():
    menor = 999
    solutions = bfs()

    # Caso haja mais de uma solução, verifica qual é a solução com menor número de passos
    for solution in solutions:
        if len(solution) < menor:
            menor = len(solution)

    # Só mostra soluções com o menor número de passos, mesmo que haja uma solução com maior número de passos
    for solution in solutions:
        if len(solution) == menor:
            print("Solução encontrada:")
            for command in solution:
                print(command.name)
            print(" ")


if __name__ == "__main__":
    main()
