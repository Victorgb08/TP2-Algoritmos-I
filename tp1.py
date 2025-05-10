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

def bfs_ek(residual_capacity_graph, s_node, t_node, parent_array, num_total_nodes_in_graph):
    """
    Executa BFS para encontrar um caminho de s_node para t_node no grafo residual.
    Retorna True se um caminho for encontrado, False caso contrário.
    parent_array é preenchido para reconstruir o caminho.
    """
    visited_nodes = [False] * num_total_nodes_in_graph
    queue = collections.deque()

    queue.append(s_node)
    visited_nodes[s_node] = True
    parent_array[s_node] = -1  # Marca a fonte como não tendo pai

    while queue:
        u_node = queue.popleft()
        # Itera sobre todos os possíveis nós vizinhos v_node
        for v_node in range(num_total_nodes_in_graph):
            # Se v_node não foi visitado e há capacidade residual de u_node para v_node
            if not visited_nodes[v_node] and residual_capacity_graph[u_node][v_node] > 0:
                queue.append(v_node)
                visited_nodes[v_node] = True
                parent_array[v_node] = u_node
                if v_node == t_node:
                    return True  # Caminho encontrado até o sumidouro
    return False  # Nenhum caminho encontrado

def edmonds_karp_max_flow(capacity_adj_matrix, s_node, t_node, num_total_nodes_in_graph):
    """
    Calcula o fluxo máximo de s_node para t_node usando o algoritmo de Edmonds-Karp.
    capacity_adj_matrix: Matriz de adjacência representando as capacidades iniciais.
    """
    residual_capacity_graph = [row[:] for row in capacity_adj_matrix]
    parent_array = [0] * num_total_nodes_in_graph  # Array para armazenar o caminho encontrado pelo BFS
    current_max_flow = 0

    while bfs_ek(residual_capacity_graph, s_node, t_node, parent_array, num_total_nodes_in_graph):
        path_flow_capacity = CAPACITY_INF  # Capacidade do caminho aumentador atual
        
        # Encontra a capacidade de gargalo do caminho
        current_node_in_path = t_node
        while current_node_in_path != s_node:
            previous_node_in_path = parent_array[current_node_in_path]
            path_flow_capacity = min(path_flow_capacity, residual_capacity_graph[previous_node_in_path][current_node_in_path])
            current_node_in_path = previous_node_in_path

        # Atualiza as capacidades residuais
        v_node_in_path = t_node
        while v_node_in_path != s_node:
            u_node_in_path = parent_array[v_node_in_path]
            residual_capacity_graph[u_node_in_path][v_node_in_path] -= path_flow_capacity
            residual_capacity_graph[v_node_in_path][u_node_in_path] += path_flow_capacity
            v_node_in_path = u_node_in_path
        
        current_max_flow += path_flow_capacity

    return current_max_flow

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
    num_total_nodes_in_graph = 2 * num_grid_cells + 2

    capacity_adj_matrix = [[0] * num_total_nodes_in_graph for _ in range(num_total_nodes_in_graph)]

    def get_vin_node_idx(r_idx, c_idx):
        return 2 * (r_idx * m + c_idx)

    def get_vout_node_idx(r_idx, c_idx):
        return 2 * (r_idx * m + c_idx) + 1

    for r_grid in range(n):
        for c_grid in range(m):
            if grid[r_grid][c_grid] > 0: 
                vin_rc_idx = get_vin_node_idx(r_grid, c_grid)
                vout_rc_idx = get_vout_node_idx(r_grid, c_grid)
                capacity_adj_matrix[vin_rc_idx][vout_rc_idx] = grid[r_grid][c_grid]

                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in dirs:
                    nr, nc = r_grid + dr, c_grid + dc
                    if in_bounds(nr, nc, n, m) and grid[nr][nc] > 0:
                        vin_nrc_idx = get_vin_node_idx(nr, nc)
                        capacity_adj_matrix[vout_rc_idx][vin_nrc_idx] = CAPACITY_INF

    for r_grid in range(n):
        for c_grid in range(m):
            if grid[r_grid][c_grid] > 0:
                is_border = (r_grid == 0 or r_grid == n - 1 or c_grid == 0 or c_grid == m - 1)
                if is_border:
                    vin_rc_idx = get_vin_node_idx(r_grid, c_grid)
                    capacity_adj_matrix[S_NODE_IDX][vin_rc_idx] = CAPACITY_INF

    vout_cap_idx = get_vout_node_idx(cap_r, cap_c)
    capacity_adj_matrix[vout_cap_idx][T_NODE_IDX] = CAPACITY_INF

    min_cut_cost = edmonds_karp_max_flow(capacity_adj_matrix, S_NODE_IDX, T_NODE_IDX, num_total_nodes_in_graph)
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