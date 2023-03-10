# -*- coding: utf-8 -*-

from collections import deque

class MultiQueue:
    """
    Lớp đối tượng hàng đợi đa điểm.
    """
    def __init__(self, n_queues):
        self.queues = [deque() for _ in range(n_queues)]

    def append(self, item, queue_index):
        self.queues[queue_index].append(item)

    # def popleft(self, queue_index):
    #     return self.queues[queue_index].popleft()

    def popleft(self, queue_index, default=None):
        return self.queues[queue_index].popleft() if self.queues[queue_index] else default

    def __bool__(self):
        return any(self.queues)

def bfs_multi_robot(start_positions, goal_positions, obstacles):
    """
    Tìm đường đi cho đa robot bằng BFS.
    start_positions: danh sách các vị trí ban đầu của các robot.
    goal_positions: danh sách các vị trí kết thúc của các robot.
    obstacles: danh sách các ô bị chiếm bởi các robot.
    """
    q = MultiQueue(len(start_positions))
    visited = set()
    n_robots = len(start_positions)
    start_state = tuple(start_positions)
    goal_state = tuple(goal_positions)
    q.append(start_state, 0)
    visited.add(start_state)

    while True:
        # print(q)
        current_state = q.popleft(0, None)
        if current_state is None:
            break
        
        if current_state == goal_state:
            return current_state

        for robot_id in range(n_robots):
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x = start_positions[robot_id][0] + dx
                new_y = start_positions[robot_id][1] + dy
                if new_x < 0:
                    new_x = 0
                if new_y < 0:
                    new_y = 0
                new_pos = (new_x, new_y)
                if new_pos in obstacles:
                    continue
                print(current_state)
                new_positions = list(current_state)
                new_positions[robot_id] = new_pos
                new_state = tuple(new_positions)
                if new_state not in visited:
                    visited.add(new_state)
                    q.append(new_state, robot_id)
        # print(visited)

    return None

# Tìm đường đi cho 4 robot trên một bản đồ có kích thước 5x5
start_positions = [(0, 0), (1, 1), (2, 2), (3, 3)]
goal_positions = [(4, 4), (3, 3), (1, 4), (4, 1)]
obstacles = [(1, 0), (2, 1), (3, 2), (4, 3)]

path = bfs_multi_robot(start_positions, goal_positions, obstacles)

print(path) # ((4, 4), (3, 3), (1, 4), (4, 1))
