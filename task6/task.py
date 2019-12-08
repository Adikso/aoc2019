with open('input') as file:
    data = [x.strip().split(")") for x in file.readlines()]


def part1():
    orbits_count = 0
    graph = dict(reversed(x) for x in data)

    for obj in graph.keys():
        while obj in graph:
            obj = graph[obj]
            orbits_count += 1

    return orbits_count


# Part 2
class Node:
    def __init__(self, name):
        self.name = name
        self.childs = set()
        self.parent = None
        self.path = None

    def __repr__(self):
        return self.name


def build_graph():
    planets = {}
    for left, right in data:
        if left not in planets:
            planets[left] = Node(left)

        if right not in planets:
            planets[right] = Node(right)

        planets[right].parent = planets[left]
        planets[right].childs.add(planets[left])
        planets[left].childs.add(planets[right])

    return planets


def traverse(node, path):
    if not node.path or len(path) < len(node.path):
        node.path = path

    for child in node.childs:
        if child != node and child not in path:
            traverse(child, [*path, node])


def find_shortest_path(start, end):
    traverse(start, [])
    return end.path


def part2():
    graph = build_graph()
    path = find_shortest_path(graph['YOU'], graph['SAN'])
    return len(path) - 2


print(part1())
print(part2())
