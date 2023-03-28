from collections import deque as queue
import numpy as np

def multi_bfs(grid, vis, start, goal):
    # Initialize multi-queue with first queue containing start cell
    q = [queue()([start])]
    # Initialize list of expanded cells
    expands = []
    # Initialize distance from start to each cell
    dist = [[-1 for _ in range(grid.shape[1])] for _ in range(grid.shape[0])]
    dist[start[0]][start[1]] = 0

    while q:
        # Get the queue with the shortest distance from start
        curr_q = q[0]
        if not curr_q:
            # Remove empty queue from multi-queue
            q.pop(0)
            continue

        # Get the next cell from the current queue
        cell = curr_q.popleft()
        x, y = cell

        # Add the cell to the list of expanded cells
        expands.append([x, y])

        # Check if the goal has been reached
        if cell == goal:
            break

        # Add neighboring cells to their respective queues
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adjx, adjy = x + dx, y + dy
            if isValid(vis, adjx, adjy, grid.shape):
                if dist[adjx][adjy] == -1:
                    # Create a new queue for cells at this distance
                    q.append(queue())
                    dist[adjx][adjy] = dist[x][y] + 1
                if dist[adjx][adjy] == dist[x][y] + 1:
                    # Add cell to the queue corresponding to its distance
                    q[-1].append((adjx, adjy))
                    vis[adjx][adjy] = True

    # If the goal was not reached, return None
    if dist[goal[0]][goal[1]] == -1:
        return None

    # Find the shortest path from the expanded cells
    path = []
    x, y = goal
    for i in range(dist[x][y], -1, -1):
        path.append((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adjx, adjy = x + dx, y + dy
            if isValid(None, adjx, adjy, grid.shape) and dist[adjx][adjy] == i - 1:
                x, y = adjx, adjy
                break
    path.reverse()

    return path

def findPath_ver2(expands: list, grid):
    path = []
    start = expands[0]
    goal = expands[-1]
    path.append(goal)

    while True:
        goal = expands[-1]
        x, y = goal
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(None, adjx, adjy, grid.shape)) and [adjx, adjy] in expands:
                if expands.index([adjx, adjy]) < expands.index(goal):
                    path.append([adjx, adjy])
                    index_new_goal = expands.index([adjx, adjy])
                    expands = expands[:index_new_goal + 1]
                    if [adjx, adjy] == start:
                        path.reverse()
                        return path
                    break

def bidirectionalBFS(grid, start, end):
    n = grid.shape[0]
    vis_start = np.zeros((n, n), dtype=bool)
    vis_end = np.zeros((n, n), dtype=bool)
    q_start = queue()
    q_end = queue()
    q_start.append(start)
    q_end.append(end)
    vis_start[start] = True
    vis_end[end] = True

    while q_start and q_end:
        if len(q_start) <= len(q_end):
            cell = q_start.popleft()
            x = cell[0]
            y = cell[1]
            if vis_end[y][x]:
                path = findPath_ver2([cell]+expands_end[::-1], grid)
                return path
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if isValid(vis_start, adjy, adjx, grid.shape):
                    q_start.append((adjx, adjy))
                    vis_start[adjy][adjx] = True
                    if vis_end[adjy][adjx]:
                        path = findPath_ver2([cell]+expands_end[::-1], grid)
                        return path
        else:
            cell = q_end.popleft()
            x = cell[0]
            y = cell[1]
            if vis_start[y][x]:
                path = findPath_ver2(expands_start+[cell], grid)
                return path
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if isValid(vis_end, adjy, adjx, grid.shape):
                    q_end.append((adjx, adjy))
                    vis_end[adjy][adjx] = True
                    if vis_start[adjy][adjx]:
                        path = findPath_ver2(expands_start+[cell], grid)
                        return path

    return None
