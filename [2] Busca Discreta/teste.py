from collections import deque
from enum import IntEnum
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
            self.volume -= self.volume

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
        # Gallons start with random information in order
        # to simulate uninitialized variables (garbage)
        self.g3 = Gallon(3, random.randint(0, 3))
        self.g5 = Gallon(5, random.randint(0, 5))

    def run(self, code: VMC):
        match code:
            case VMC.G3_EMPTY:
                self.g3.empty()
            case VMC.G3_FILL:
                self.g3.FILL()
            case VMC.G3_TRANSFER_G5:
                self.g3.transferTo(self.g5)
            case VMC.G5_EMPTY:
                self.g5.empty()
            case VMC.G5_FILL:
                self.g5.fill()
            case VMC.G5_TRANSFER_G3:
                self.g5.transferTo(self.g3)
            case _:
                print("ERROR: UNKNOWN INSTRUCTION ", code)

    def get_state(self):
        return (self.g3.volume, self.g5.volume)

    def set_state(self, state):
        self.g3.volume, self.g5.volume = state

    def printMemory(self):
        print("g3: {} | g5: {}".format(self.g3.volume, self.g5.volume))

    # The objective of the problem is to find 4L of liquid in a jug
    # Die Hard 3 - Jugs Problem
    # https://www.youtube.com/watch?v=BVtQNK_ZUJg
    def success(self):
        return self.g5.volume == 4


class Node:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


def bfs():
    commands = [
        VMC.G3_EMPTY,
        VMC.G5_EMPTY,
        VMC.G5_FILL,
        VMC.G5_TRANSFER_G3,
        VMC.G3_EMPTY,
        VMC.G5_TRANSFER_G3,
        VMC.G5_FILL,
        VMC.G5_TRANSFER_G3,
    ]

    vm = VirtualMachine()  # Virtual machine instance, gallons start with random values

    if (
        vm.g5.volume == 4
    ):  # If the initial state already give me the final asnwer, it's not necessary a search
        print("The gallon g5 already started with 4l, no search necessary :D\n")
        exit()
    else:
        initial_state = (vm.g3.volume, vm.g5.volume)  # initial state of gallons
        queue = deque()  # Instancing a queue
        queue.append(initial_state)  # Put the initial State in the Queue
        visitedNodes = []  # Initializing a List of Visited Nodes
        path = []

        while queue:
            currentNode = queue.popleft()
            visitedNodes.append(currentNode)
            for command in commands:
                vm.run(command)
                vm.set_state(currentNode)
                vm.run(command)
                new_state = vm.get_state()
                if new_state not in visitedNodes:
                    if vm.success():
                        return path + [command]
                    queue.append(new_state)
                    visitedNodes.append(new_state)
        return visitedNodes


def main():
    """
    vm = VirtualMachine()
    commands = [
        VMC.G3_EMPTY,
        VMC.G5_EMPTY,
        VMC.G5_FILL,
        VMC.G5_TRANSFER_G3,
        VMC.G3_EMPTY,
        VMC.G5_TRANSFER_G3,
        VMC.G5_FILL,
        VMC.G5_TRANSFER_G3,
    ]
    for code in commands:
        vm.printMemory()
        vm.run(code)
    vm.printMemory()
    print("Reached goal: ", vm.success())
    """
    result = bfs()
    print(result)


if __name__ == "__main__":
    main()
