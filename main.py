import sys
import collections  # Para deque

CAPACITY_INF = 2 * 10**9  # Valor para representar infinito nas capacidades

def parse_input_corrected(input_data_str: str):
    """
    Analisa os dados de entrada, convertendo as coordenadas da capital para base 0.
    """
    lines = input_data_str.strip().split('\n')
    n, m = map(int, lines[0].split())
    grid = []
    for i in range(n):
        grid.append(list(map(int, lines[i + 1].split())))
    
    # As coordenadas da capital são 1-indexadas na entrada
    x_cap_1idx, y_cap_1idx = map(int, lines[n + 1].split())
    # Convertendo para 0-indexado
    cap_r, cap_c = x_cap_1idx - 1, y_cap_1idx - 1
    return n, m, grid, cap_r, cap_c

def in_bounds(r, c, n, m):
    """Verifica se as coordenadas (r, c) estão dentro dos limites do grid (n, m)."""
    return 0 <= r < n and 0 <= c < m

def bfs_ek(adj_list, s_node, t_node, parent):
    """
    Executa BFS para encontrar um caminho de s_node para t_node no grafo residual.
    Retorna True se um caminho for encontrado, False caso contrário.
    parent é preenchido para reconstruir o caminho.
    """
    visited = [False] * len(adj_list)
    queue = collections.deque([s_node])
    visited[s_node] = True
    parent[s_node] = -1

    while queue:
        current = queue.popleft()
        for neighbor, capacity in adj_list[current].items():
            if not visited[neighbor] and capacity > 0:  # Não visitado e capacidade > 0
                parent[neighbor] = current
                if neighbor == t_node:
                    return True
                queue.append(neighbor)
                visited[neighbor] = True
    return False

def edmonds_karp_max_flow(adj_list, s_node, t_node):
    """
    Calcula o fluxo máximo usando uma lista de adjacência.
    """
    parent = [-1] * len(adj_list)
    max_flow = 0

    while bfs_ek(adj_list, s_node, t_node, parent):
        # Determina a capacidade de gargalo no caminho encontrado
        path_flow = CAPACITY_INF
        current = t_node
        while current != s_node:
            prev = parent[current]
            path_flow = min(path_flow, adj_list[prev][current])
            current = prev

        # Atualiza as capacidades residuais
        current = t_node
        while current != s_node:
            prev = parent[current]
            adj_list[prev][current] -= path_flow
            adj_list[current][prev] += path_flow
            current = prev

        max_flow += path_flow

    return max_flow

def solve(input_data: str) -> int:
    """
    Resolve o problema principal.
    """
    n, m, grid, cap_r, cap_c = parse_input_corrected(input_data)

    if grid[cap_r][cap_c] == 0:
        return 0

    num_grid_cells = n * m
    S_NODE_IDX = 2 * num_grid_cells
    T_NODE_IDX = 2 * num_grid_cells + 1

    # Lista de adjacência para representar o grafo
    adj_list = [{} for _ in range(2 * num_grid_cells + 2)]

    def get_vin_node_idx(r_idx, c_idx):
        return 2 * (r_idx * m + c_idx)

    def get_vout_node_idx(r_idx, c_idx):
        return 2 * (r_idx * m + c_idx) + 1

    # Construção do grafo
    for r_grid in range(n):
        for c_grid in range(m):
            if grid[r_grid][c_grid] > 0: 
                vin_rc_idx = get_vin_node_idx(r_grid, c_grid)
                vout_rc_idx = get_vout_node_idx(r_grid, c_grid)
                adj_list[vin_rc_idx][vout_rc_idx] = grid[r_grid][c_grid]
                adj_list[vout_rc_idx][vin_rc_idx] = 0  # Aresta reversa

                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in dirs:
                    nr, nc = r_grid + dr, c_grid + dc
                    if in_bounds(nr, nc, n, m) and grid[nr][nc] > 0:
                        vin_nrc_idx = get_vin_node_idx(nr, nc)
                        adj_list[vout_rc_idx][vin_nrc_idx] = CAPACITY_INF
                        adj_list[vin_nrc_idx][vout_rc_idx] = 0  # Aresta reversa

    for r_grid in range(n):
        for c_grid in range(m):
            if grid[r_grid][c_grid] > 0:
                is_border = (r_grid == 0 or r_grid == n - 1 or c_grid == 0 or c_grid == m - 1)
                if is_border:
                    vin_rc_idx = get_vin_node_idx(r_grid, c_grid)
                    adj_list[S_NODE_IDX][vin_rc_idx] = CAPACITY_INF
                    adj_list[vin_rc_idx][S_NODE_IDX] = 0  # Aresta reversa

    vout_cap_idx = get_vout_node_idx(cap_r, cap_c)
    adj_list[vout_cap_idx][T_NODE_IDX] = CAPACITY_INF
    adj_list[T_NODE_IDX][vout_cap_idx] = 0  # Aresta reversa

    # Calcula o fluxo máximo
    min_cut_cost = edmonds_karp_max_flow(adj_list, S_NODE_IDX, T_NODE_IDX)
    return min_cut_cost

def main():
    """
    Função principal que lê a entrada do stdin e imprime o resultado no stdout.
    """
    input_data = sys.stdin.read()
    result = solve(input_data)
    print(result)

if __name__ == "__main__":
    main()