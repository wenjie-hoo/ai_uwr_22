def V(i, j):
    return 'V%d_%d' % (i, j)

def domains(Vs):
    return [q + ' in 1..9' for q in Vs]

def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'

def get_column(j):
    return [V(i, j) for i in range(9)]

def get_row(i):
    return [V(i, j) for j in range(9)]

def horizontal():
    return [all_different(get_row(i)) for i in range(9)]

def vertical():
    return [all_different(get_column(j)) for j in range(9)]

def get_square(i, j):
    inside = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    return [V(i + k[0], j + k[1]) for k in inside]

def in_cell():
    squares = [(0, 0), (0, 3), (0, 6), (3, 3), (3, 6), (6, 6), (3, 0), (6, 0)]
    results = []
    for s in squares:
        square = get_square(s[0], s[1])
        results.append(all_different(square))
    return results


def print_constraints(Cs, indent, d):
    position = indent
    print((indent - 1) * ' ', end=' ', file=out_file)
    for c in Cs:
        print(c + ',', end=' ', file=out_file)
        position += len(c)
        if position > d:
            position = indent
            print(file=out_file)
            print(indent * ' ', end=' ', file=out_file)


def sudoku(assigments):
    variables = [V(i, j) for i in range(9) for j in range(9)]

    print(':- use_module(library(clpfd)).', file=out_file)
    print('solve([' + ', '.join(variables) + ']) :- ', file=out_file)

    cs = domains(variables) + vertical() + horizontal() + in_cell()
    for i, j, val in assigments:
        cs.append('%s #= %d' % (V(i, j), val))

    print_constraints(cs, 4, 70),
    print(file=out_file)
    print('    labeling([ff], [' + ', '.join(variables) + ']).', file=out_file)
    print(file=out_file)
    print(':- solve(X), write(X), nl.', file=out_file)


if __name__ == "__main__":
    out_file = open("zad_output.txt", "w", encoding='utf8')
    input_file = open("zad_input.txt", encoding='utf8').readlines()

    row = 0
    triples = []

    for x in input_file:
        x = x.strip()
        if len(x) == 9:
            for col in range(9):
                if x[col] != '.':
                    triples.append((row, col, int(x[col])))
            row += 1
    sudoku(triples)

    out_file.close()

    
"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
"""    