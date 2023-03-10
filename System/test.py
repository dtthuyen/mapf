from collections import defaultdict
import heapq

class MultiQueue:
    def __init__(self):
        self.queues = defaultdict(list)

    def add_to_queue(self, item, queue_name, priority):
        heapq.heappush(self.queues[queue_name], (priority, item))

    def get_from_queue(self, queue_name):
        if not self.queues[queue_name]:
            return None
        return heapq.heappop(self.queues[queue_name])[1]

    def not_empty(self):
        return any(self.queues)

def bfs_multi_robot(grid, start, targets):
    height, width = len(grid), len(grid[0])
    q = MultiQueue()
    visited = set()

    for i, target in enumerate(targets):
        q.add_to_queue([start[i]], f'path_{i}', 0)
        visited.add((start[i], i))
        
    while q.not_empty():
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
                distance = manhattan_distance(neighbor, targets[robot_idx])
                q.add_to_queue(new_path, f'path_{robot_idx}', distance)

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

def manhattan_distance(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

# if __name__ == "__main__":
#     grid = [
#         ['#', '#', '#', '#', '#', '#', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '.', '.', '.', '.', '.', '#'],
#         ['#', '#', '#', '#', '#', '#', '#'],
#     ]

#     start = [(1, 1), (5, 1)]
#     targets = [(1, 5), (5, 5)]

#     paths = bfs_multi_robot(grid, start, targets)
if __name__ == '__main__':
    grid = ['..#.',
            '..#.',
            '....',
            '####']
    start = [(0, 0), (1, 2)]
    targets = [(3, 2), (0, 3)]
    result = bfs_multi_robot(grid, start, targets)
    print(result)

    # if paths is None:
    #     print("No paths found")
    # else:
    #     for i, path in enumerate(paths):
    #         print(f"Path for robot {i}: {path}")
