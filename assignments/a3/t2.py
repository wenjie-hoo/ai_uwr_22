from queue import *

dic = dict()
def opt_dist(v, d):
    h = hash((tuple(v), tuple(d)))
    if h in dic:
        return dic[h]
    n, m = len(v), len(d)
    black, white = [0] * (n + 1), n + 1
    for i in range(1, n + 1):
        black[i] = black[i - 1] + (v[i - 1] == 1)
        if v[i - 1] == 2:
            white = min(white, i - 1)

    ok = [[0] * (m + 1) for _ in range(n + 1)]
    ok[0][0] = 1
    for i in range(1, n + 1):
        ok[i][0] = i - 1 < white
        for j in range(1, m + 1):
            block = d[j - 1]
            if i < block:
                continue
            elif i > block:
                optB = (black[i] == black[i - block]) * (v[i - block - 1] != 2) * ok[i - block - 1][j - 1]
            else:
                optB = (black[i] == 0) * ok[0][j - 1]
            optA = ok[i - 1][j] * (v[i - 1] != 2)
            ok[i][j] = optA + optB
    dic[h] = ok[n][m]
    return ok[n][m]

def revise_line(line):
    x, line_type = line
    changed = []
    check = []
    lines = rows if line_type == 'row' else cols
    opts = row_opts if line_type == 'row' else col_opts
    k = m if line_type == 'row' else n
    linepix = pixels[x] if line_type == 'row' else [pixels[i][x] for i in range(n)]
    for i in range(k):
        if linepix[i] < 3:
            continue
        linepix[i] = 1
        optA = opt_dist(linepix, lines[x])
        linepix[i] = 2
        dom = 2 if optA == 0 else 1 | 2 * (opt_dist(linepix, lines[x]) > 0)
        linepix[i] = dom
        if dom == 0:
            break
        elif dom < 3:
            if line_type == 'row':
                pixels[x][i] = dom
            else:
                pixels[i][x] = dom
            changed.append((x, i) if line_type == 'row' else (i, x))

    check = [(p[1], 'col') if line_type == 'row' else (p[0], 'row') for p in changed]
    opts[x] = opt_dist(linepix, lines[x])
    return opts[x] > 0, changed, check


def full(pix=-1):
    q = Queue()
    if pix == -1:
        for x in range(n):
            q.put((x, 'row'))
        for x in range(m):
            q.put((x, 'col'))
    else:
        x, y = pix
        q.put((x, 'row'))
        q.put((y, 'col'))

    changed = []
    while not q.empty():
        line = q.get()
        success, _changed, check = revise_line(line)
        changed += _changed
        if success:
            q.queue.extend(check)
        else:
            return False, changed
    return True, changed

def backtrack():
    s = set([ (x, y) for x in range(n) for y in range(m) if pixels[x][y] == 3])
    if len(s) == 0:
        return True
    x, y = min(s, key=lambda a: min(row_opts[a[0]], col_opts[a[1]]))
    s.remove((x, y))
    global row_opts, col_opts
    row_cp, col_cp = row_opts[:], col_opts[:]
    pixels[x][y] = 1
    success, changed = full((x, y))
    if success:
        for p in changed:
            s.remove(p)
        if backtrack():
            return True
    row_opts, col_opts = row_cp, col_cp
    for px, py in changed:
        pixels[px][py] = 3
        s.add((px, py))
    pixels[x][y] = 2
    success, changed = full((x, y))
    if success:
        for p in changed:
            s.remove(p)
        if backtrack():
            return True
    row_opts, col_opts = row_cp, col_cp
    for px, py in changed:
        pixels[px][py] = 3
        s.add((px, py))
    pixels[x][y] = 3
    s.add((x, y))
    return False

if __name__ == '__main__':
    with open('zad_input.txt') as f:
        n, m = map(int, f.readline().strip().split())
        rows = [list(map(int, f.readline().strip().split())) for _ in range(n)]
        cols = [list(map(int, f.readline().strip().split())) for _ in range(m)]
    pixels = [[3] * m for _ in range(n)]
    row_opts = [0] * n
    col_opts = [0] * m
    full()
    backtrack()
with open('zad_output.txt', 'w') as f:
    for x in range(n):
        for y in range(m):
            if pixels[x][y] == 1:
                f.write('.')
            else:
                f.write('#')
        f.write('\n')
