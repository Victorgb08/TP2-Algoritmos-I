import sys
from collections import deque

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)

    def BFS(self, s, t, parent):
        visited = [False] * self.ROW
        queue = deque()
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.popleft()
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False

    def FordFulkerson(self, source, sink):
        parent = [-1] * self.ROW
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        return max_flow

def solve(input_data):
    input = input_data.strip().split()
    ptr = 0
    n = int(input[ptr])
    ptr += 1
    m = int(input[ptr])
    ptr += 1

    grid = []
    for _ in range(n):
        row = list(map(int, input[ptr:ptr + m]))
        ptr += m
        grid.append(row)

    x = int(input[ptr]) - 1
    ptr += 1
    y = int(input[ptr]) - 1

    size = 2 * n * m + 2
    graph = [[0] * size for _ in range(size)]
    source = size - 2
    sink = size - 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for i in range(n):
        for j in range(m):
            cell_in = 2 * (i * m + j)
            cell_out = cell_in + 1
            
            if grid[i][j] != 0:
                graph[cell_in][cell_out] = grid[i][j]

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] != 0:
                    neighbor_in = 2 * (ni * m + nj)
                    graph[cell_out][neighbor_in] = float('inf')

            if (i == 0 or i == n - 1 or j == 0 or j == m - 1) and grid[i][j] != 0:
                graph[cell_out][sink] = float('inf')

    capital_in = 2 * (x * m + y)
    if grid[x][y] != 0:
        graph[source][capital_in] = float('inf')
    else:
        print("Erro: A capital está em uma montanha e não pode ser conectada ao source.")

    g = Graph(graph)
    return g.FordFulkerson(source, sink)

if __name__ == "__main__":
    input_data = sys.stdin.read()
    print(solve(input_data))