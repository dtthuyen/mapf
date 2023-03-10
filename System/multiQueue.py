from collections import deque, defaultdict
import numpy as np

class MultiQueue:
    def __init__(self):
        self.queues = defaultdict(deque)

    def add_to_queue(self, item, queue_name):
        self.queues[queue_name].append(item)

    def get_from_queue(self, queue_name):
        if not self.queues[queue_name]:
            return None
        return self.queues[queue_name].popleft()

def bfs_multi_robot(grid, start, targets):
    height, width = len(grid), len(grid[0])
    q = MultiQueue()
    visited = set()

    for i, target in enumerate(targets):
        q.add_to_queue([start[i]], f'path_{i}')
        visited.add((start[i], i))

    while True:
        paths = [q.get_from_queue(f'path_{i}') for i in range(len(targets))]
        if None in paths:
            return None
        nodes = [(path[-1], i) for i, path in enumerate(paths)]
        if all(node in targets for node in nodes):
            return paths
        for node, robot_idx in nodes:
            visited.add((node, robot_idx))
            for neighbor in get_neighbors(node, height, width):
                if neighbor in visited or grid[neighbor[0]][neighbor[1]] == '#':
                    continue
                new_path = list(paths[robot_idx])
                new_path.append(neighbor)
                q.add_to_queue(new_path, f'path_{robot_idx}')

def get_neighbors(node, height, width):
    neighbors = []
    if node[0] > 0:
        neighbors.append((node[0] - 1, node[1]))
    if node[0] < height - 1:
        neighbors.append((node[0] + 1, node[1]))
    if node[1] > 0:
        neighbors.append((node[0], node[1] - 1))
    if node[1] < width - 1:
        neighbors.append((node[0], node[1] + 1))
    return neighbors


start_positions = [(0, 0), (1, 1), (2, 2), (3, 3)]
goal_positions = [(4, 4), (3, 3), (1, 4), (4, 1)]
obstacles = [(1, 0), (2, 1), (3, 2), (4, 3)]
grid = np.zeros((5,5))
path = bfs_multi_robot(grid,start_positions, goal_positions)

print(path) # ((4, 4), (3, 3), (1, 4), (4, 1))