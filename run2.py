import sys
from collections import deque


def build_graph(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph = {}
    for node1, node2 in edges:
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph


def is_gateway(node: str) -> bool:
    return node.isupper()


def is_blocked_edge(edge: tuple[str, str], blocked_edges: set[tuple[str, str]]) -> bool:
    return edge in blocked_edges or (edge[1], edge[0]) in blocked_edges


def next_node(path: dict[str, str], target_gateway: str, current_pos: str) -> str:
    current = target_gateway
    while path[current] != current_pos:
        current = path[current]
    return current


def find_nearest(
    start_node: str,
    graph: dict[str, list[str]],
    blocked_edges: set[tuple[str, str]],
) -> tuple[tuple[str, str], str]:
    target_gateway = ""
    target_edge = ()
    visited = dict.fromkeys(graph.keys(), -1)
    parent = dict.fromkeys(graph.keys(), None)
    queue = deque()
    queue.append((start_node, 0))
    min_distance = float("inf")
    while queue:
        current, depth = queue.popleft()
        if visited[current] != -1:
            continue
        visited[current] = depth

        for neighbor in sorted(graph.get(current, [])):
            if is_blocked_edge((current, neighbor), blocked_edges):
                continue
            if is_gateway(neighbor) and depth + 1 <= min_distance:
                min_distance = depth + 1
                if target_gateway > neighbor or not target_gateway:
                    target_gateway = neighbor
                    target_edge = (current, neighbor)
                    parent[neighbor] = current
            elif visited[neighbor] == -1:
                parent[neighbor] = current
                queue.append((neighbor, depth + 1))

    return target_edge, parent


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    graph = build_graph(edges)
    blocked_edges_set = set()
    blocked_edges = []
    virus_node = "a"
    while True:
        edge, _ = find_nearest(virus_node, graph, blocked_edges_set)
        blocked_edges_set.add(edge)
        blocked_edges.append(edge)
        edge, parent = find_nearest(virus_node, graph, blocked_edges_set)
        if not edge:
            break
        virus_node = next_node(parent, edge[1], virus_node)
    result = []
    for edge in blocked_edges:
        result.append(f"{edge[1]}-{edge[0]}")
    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition("-")
            if sep:
                edges.append((node1, node2))
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
