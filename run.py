import sys
import heapq

HALLWAY_POSITIONS = (0, 1, 3, 5, 7, 9, 10)
ROOM_ENTRANCES = {"A": 2, "B": 4, "C": 6, "D": 8}
TARGET_ROOMS = {"A": 0, "B": 1, "C": 2, "D": 3}
MOVE_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


def parse_state(lines: list[str]) -> tuple:
    room_depth = len(lines) - 3
    hallway = tuple(["."] * 11)
    rooms_list = [[] for _ in range(4)]

    for r in range(room_depth):
        line = lines[r + 2]
        for i, room_char in enumerate("ABCD"):
            rooms_list[i].append(line[ROOM_ENTRANCES[room_char] + 1])

    rooms = tuple(tuple(r) for r in rooms_list)
    return (hallway, rooms)


def is_target_state(state: tuple, room_depth: int) -> bool:
    _, rooms = state
    for owner_char, room in zip("ABCD", rooms):
        if any(room_char != owner_char for room_char in room):
            return False
    return True


def heuristic(state: tuple, room_depth: int) -> int:
    hallway, rooms = state
    total_estimate = 0
    dist_in = 1  # +1 чтобы посчитать минимальный заход в нужный коридор
    for i, char in enumerate(hallway):
        if char != ".":
            dist = abs(i - ROOM_ENTRANCES[char]) + dist_in
            total_estimate += dist * MOVE_COSTS[char]

    for i, room in enumerate(rooms):
        owner_char = "ABCD"[i]
        for depth, char in enumerate(room):
            if char != "." and char != owner_char:
                dist_out = depth + 1
                current_room_entrance = ROOM_ENTRANCES["ABCD"[i]]
                target_room_entrance = ROOM_ENTRANCES[char]
                dist_hallway = abs(current_room_entrance - target_room_entrance)
                total_estimate += (dist_out + dist_hallway + dist_in) * MOVE_COSTS[char]

    return total_estimate


def get_possible_moves(state: tuple, room_depth: int) -> list:
    hallway, rooms = state
    moves = []

    for i, room in enumerate(rooms):
        owner_char = "ABCD"[i]
        if all(room_char == owner_char for room_char in room):
            continue

        for depth, char in enumerate(room):
            if char != ".":
                break
        else:
            continue

        current_room_entrance = ROOM_ENTRANCES["ABCD"[i]]
        for target_pos in HALLWAY_POSITIONS:
            start, end = sorted((current_room_entrance, target_pos))
            if all(hallway[p] == "." for p in range(start, end + 1)):
                steps = (depth + 1) + abs(current_room_entrance - target_pos)
                cost = steps * MOVE_COSTS[char]

                new_hallway = list(hallway)
                new_hallway[target_pos] = char

                new_rooms = [list(r) for r in rooms]
                new_rooms[i][depth] = "."

                new_state = (tuple(new_hallway), tuple(map(tuple, new_rooms)))
                moves.append((cost, new_state))

    for i, char in enumerate(hallway):
        if char == ".":
            continue

        target_room_idx = TARGET_ROOMS[char]
        room = rooms[target_room_idx]

        if not all(room_char == char or room_char == "." for room_char in room):
            continue

        target_room_entrance = ROOM_ENTRANCES[char]
        start, end = sorted((i, target_room_entrance))
        if not all(hallway[p] == "." for p in range(start + 1, end)):
            continue

        for depth in range(room_depth - 1, -1, -1):
            if room[depth] == ".":
                target_depth = depth
                break
        else:
            continue

        steps = abs(i - target_room_entrance) + (target_depth + 1)
        cost = steps * MOVE_COSTS[char]

        new_hallway = list(hallway)
        new_hallway[i] = "."

        new_rooms = [list(r) for r in rooms]
        new_rooms[target_room_idx][target_depth] = char

        new_state = (tuple(new_hallway), tuple(map(tuple, new_rooms)))
        moves.append((cost, new_state))

    return moves


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    room_depth = len(lines) - 3
    initial_state = parse_state(lines)

    # (оценка_до_цели + цена, цена, состояние)
    pq = [(heuristic(initial_state, room_depth), 0, initial_state)]
    visited = {initial_state: 0}

    while pq:
        _, cost, current_state = heapq.heappop(pq)

        if cost > visited[current_state]:
            continue

        if is_target_state(current_state, room_depth):
            return cost

        for move_cost, next_state in get_possible_moves(current_state, room_depth):
            new_cost = cost + move_cost
            if next_state not in visited or new_cost < visited[next_state]:
                visited[next_state] = new_cost
                priority = new_cost + heuristic(next_state, room_depth)
                heapq.heappush(pq, (priority, new_cost, next_state))

    return -1


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip("\n"))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
