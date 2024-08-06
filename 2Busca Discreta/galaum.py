from enum import IntEnum
import random


class gallon:
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


# Virtual Machine Commands
class VMC(IntEnum):
    G3_EMPTY = 0
    G3_FILL = 1
    G3_TRANSFER_G5 = 2
    G5_EMPTY = 3
    G5_FILL = 4
    G5_TRANSFER_G3 = 5


class VirtualMachine:
    def __init__(self):
        # gallons start with random information in order
        # to simulate uninitialized variables (garbage)
        self.g3 = gallon(3, random.randint(0, 3))
        self.g5 = gallon(5, random.randint(0, 5))

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

    def printMemory(self):
        print("g3: {} | g5: {}".format(self.g3.volume, self.g5.volume))

    # The objective of the problem is to find 4L of liquid in a jug
    # Die Hard 3 - Jugs Problem
    # https://www.youtube.com/watch?v=BVtQNK_ZUJg
    def success(self):
        return self.g5.volume == 4


def main():
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
        VMC.G3_EMPTY,
    ]

    for code in commands:
        vm.printMemory()
        vm.run(code)

    vm.printMemory()
    print("Reached goal: ", vm.success())


if __name__ == "__main__":
    main()
