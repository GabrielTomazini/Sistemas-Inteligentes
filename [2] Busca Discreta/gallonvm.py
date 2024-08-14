from enum import IntEnum
from collections import deque


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
        self.g3 = Gallon(3, 0)
        self.g5 = Gallon(5, 0)

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

    def success(self):
        return self.g5.volume == 4


def bfs():
    initial_state = (0, 0)
    print(initial_state)
    queue = deque([(initial_state, [])])
    visited = set([initial_state])

    commands = [
        VMC.G3_EMPTY,
        VMC.G5_EMPTY,
        VMC.G5_FILL,
        VMC.G3_FILL,
        VMC.G3_TRANSFER_G5,
        VMC.G5_TRANSFER_G3,
    ]
    """
    for n in range(0, 0):
        print(n)
        if (n, 4):
            print("Já veio certo!\n")
    """
    while queue:
        current_state, path = queue.popleft()
        # print(path)
        # print("\n")
        for command in commands:
            vm = VirtualMachine()
            vm.set_state(current_state)
            vm.run(command)
            new_state = vm.get_state()
            if new_state not in visited:
                if vm.success():
                    return path + [command]
                queue.append((new_state, path + [command]))
                visited.add(new_state)
                print("Fila: ")
                print(queue)
                print("\n")
                print("Visitado: ")
                print(visited)
                print("\n")
        print("ACABOU PRIMEIRO NÍVEL\n")

    return None


def main():
    result = bfs()
    if result:
        path = result
        for command in path:
            print(command.name)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
