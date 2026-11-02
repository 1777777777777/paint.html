import sys

GRID_SIZE = 10
TOTAL_PIXELS = GRID_SIZE * GRID_SIZE
ITERATIONS = 30

if "--iterations" in sys.argv:
    try:
        idx = sys.argv.index("--iterations")
        ITERATIONS = int(sys.argv[idx + 1])
    except (ValueError, IndexError):
        pass

def flood_fill(raw_payload, width, height):
    grid = [char for char in raw_payload if not char.isspace()]
    if len(grid) != width * height or any(char not in "01b" for char in grid):
        raise ValueError("Drawing must contain exactly the expected number of pixels (0, 1 or b).")
    queue = [i for i, j in enumerate(grid) if j == 'b']

    while queue:
        near = []
        curr = queue.pop(0)
        row = curr // width
        col = curr % width

        if row > 0:
            near.append(curr - width)
        if row < height - 1:
            near.append(curr + width)
        if col > 0:
            near.append(curr - 1)
        if col < width - 1:
            near.append(curr + 1)

        for n in near:
            if grid[n] == "0":
                grid[n] = "b"

                queue.append(n)

    return "".join(grid).replace("b", "1")
