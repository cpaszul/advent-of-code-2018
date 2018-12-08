DEFAULT_INPUT = 'day8.txt'

class Node:
    def __init__(self, data, i):
        self.num_children = data[i]
        self.num_metadata = data[i + 1]
        self.metadata = []
        self.children = []
        i += 2
        for _ in range(self.num_children):
            child = Node(data, i)
            i = child.endpoint
            self.children.append(child)
        for _ in range(self.num_metadata):
            self.metadata.append(data[i])
            i += 1
        self.endpoint = i

    def total_metadata(self):
        return sum(self.metadata) + \
               sum(child.total_metadata() for child in self.children)

    def value(self):
        if self.children:
            total = 0
            for entry in self.metadata:
                if entry <= len(self.children):
                    total += self.children[entry - 1].value()
            return total
        else:
            return sum(self.metadata)
        
        
def day_8(loc=DEFAULT_INPUT):
    with open(loc) as f:
        data = list(map(int, f.readline().split(' ')))
    tree = Node(data, 0)
    return tree.total_metadata(), tree.value()
        
if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_8()))
