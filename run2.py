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


def get_exit_edges(graph: dict[str, list[str]]) -> list[tuple[str, str]]:
    exit_edges = []
    for node, neighbors in graph.items():
        if is_gateway(node):
            for neighbor in neighbors:
                if not is_gateway(neighbor):
                    exit_edges.append((node, neighbor))
    return sorted(exit_edges, key=lambda edge: (edge[0], edge[1]))


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
    visited[start_node] = 0
    parent = dict.fromkeys(graph.keys(), None)
    queue = deque()
    queue.append((start_node, 0))
    min_distance = float("inf")
    while queue:
        current, depth = queue.popleft()

        for neighbor in sorted(graph.get(current, [])):
            if is_blocked_edge((current, neighbor), blocked_edges):
                continue
            if is_gateway(neighbor) and depth + 1 <= min_distance:
                min_distance = depth + 1
                if target_gateway > neighbor or not target_gateway:
                    target_gateway = neighbor
                    target_edge = (neighbor, current)
                    parent[neighbor] = current
                    visited[neighbor] = depth + 1
            elif visited[neighbor] == -1:
                parent[neighbor] = current
                visited[neighbor] = depth + 1
                queue.append((neighbor, depth + 1))

    return target_edge, parent


def backtrack_to_next(
    start_node: str,
    blocked_edges: list[tuple[str, str]],
    exit_edges: list[tuple[str, str]],
    graph: dict[str, list[str]],
):
    for edge in exit_edges:
        if edge not in blocked_edges:
            new_blocked_edges = blocked_edges + [edge]
            if len(new_blocked_edges) == len(exit_edges):
                return True, new_blocked_edges
            target_edge, parent = find_nearest(start_node, graph, new_blocked_edges)
            next_step = next_node(parent, target_edge[0], start_node)
            if is_gateway(next_step):
                continue

            f, result = backtrack_to_next(
                next_step, new_blocked_edges, exit_edges, graph
            )
            if f:
                return True, result
    return False, None


def format_result(result: list[tuple[str, str]]):
    formated_result = []
    for edge in result:
        formated_result.append(f"{edge[0]}-{edge[1]}")
    return formated_result


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = build_graph(edges)
    exit_edges = get_exit_edges(graph)

    _, result = backtrack_to_next("a", [], exit_edges, graph)
    return format_result(result)


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
