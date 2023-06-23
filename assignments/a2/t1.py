
from itertools import combinations
import numpy as np 

def create_possibilities(values, no_of_other):
    possibilities = []
    for v in values:
        groups = len(v)
        no_empty = no_of_other-sum(v)-groups+1
        ones = [[1]*x for x in v]
        res = _create_possibilities(no_empty, groups, ones)
        possibilities.append(res)  
    return possibilities

def _create_possibilities(n_empty, groups, ones):
    res_opts = []
    for p in combinations(range(groups+n_empty), groups):
        selected = [-1]*(groups+n_empty)
        ones_idx = 0
        for val in p:
            selected[val] = ones_idx
            ones_idx += 1
        res_opt = [ones[val]+[-1] if val > -1 else [-1] for val in selected]
        res_opt = [item for sublist in res_opt for item in sublist][:-1]
        res_opts.append(res_opt)
    return res_opts

def select_index_not_done(possibilities, row_ind):
        s = [len(i) for i in possibilities]
        if row_ind:
            return [(i, n, row_ind) for i, n in enumerate(s) if rows_done[i] == 0]
        else:
            return [(i, n, row_ind) for i, n in enumerate(s) if cols_done[i] == 0]

def get_only_one_option(values):
    return [(n, np.unique(i)[0]) for n, i in enumerate(np.array(values).T) if len(np.unique(i)) == 1]

def remove_possibilities(possibilities, i, val):
    return [p for p in possibilities if p[i] == val]

def check_done(row_ind, idx):
    if row_ind: return rows_done[idx]
    else: return cols_done[idx]
    
def update_done(row_ind, idx):
    if row_ind: vals = board[idx]
    else: vals = [row[idx] for row in board]
    if 0 not in vals:
        if row_ind: rows_done[idx] = 1
        else: cols_done[idx] = 1 
        
def check_solved(rows_done,cols_done):
    if 0 not in rows_done and 0 not in cols_done:
        return 
    
if __name__ == '__main__':
    num_row_col = []
    row_col_val = []
    with open("./zad_input.txt", "r") as file:
        for i, line in enumerate(file):
            if i == 0:
                line = line.strip()
                num_row_col = [int(x) for x in line.split(" ")]
            else:
                line = line.strip()
                data = [int(x) for x in line.split(" ")]
                row_col_val.append(data)

    ROWS_VALUES = row_col_val[:num_row_col[0]]
    COLS_VALUES = row_col_val[num_row_col[0]:]

    no_of_rows = num_row_col[0]
    rows_changed = [0] * no_of_rows
    rows_done = [0] * no_of_rows

    no_of_cols = num_row_col[1]
    cols_changed = [0] * no_of_cols
    cols_done = [0] * no_of_cols

    solved = False 
    shape = (no_of_rows, no_of_cols)
    board = [[0 for c in range(no_of_cols)] for r in range(no_of_rows)]
    COLS_VALUES = COLS_VALUES
    no_of_cols = len(COLS_VALUES)
    cols_changed = [0] * no_of_cols
    cols_done = [0] * no_of_cols

    solved = False 
    shape = (no_of_rows, no_of_cols)
    board = [[0 for c in range(no_of_cols)] for r in range(no_of_rows)]
    rows_possibilities = create_possibilities(ROWS_VALUES, no_of_cols)
    cols_possibilities = create_possibilities(COLS_VALUES, no_of_rows)

    while not solved:
        lowest_rows = select_index_not_done(rows_possibilities, 1)
        lowest_cols = select_index_not_done(cols_possibilities, 0)
        lowest = sorted(lowest_rows + lowest_cols, key=lambda element: element[1])

        for ind1, _, row_ind in lowest:
            if not check_done(row_ind, ind1):
                if row_ind: values = rows_possibilities[ind1]
                else: values = cols_possibilities[ind1]
                same_ind = get_only_one_option(values)
                for ind2, val in same_ind:
                    if row_ind: ri, ci = ind1, ind2
                    else: ri, ci = ind2, ind1 
                    if board[ri][ci] == 0:
                        board[ri][ci] = val
                        if row_ind: cols_possibilities[ci] = remove_possibilities(cols_possibilities[ci], ri, val)
                        else: rows_possibilities[ri] = remove_possibilities(rows_possibilities[ri], ci, val)
                update_done(row_ind, ind1)
        if 0 not in rows_done and 0 not in cols_done:
            # print(board)   
            solved = True     
            break
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                board[i][j] = '#'
            if board[i][j] == -1:
                board[i][j] = '.'
    with open("./zad_output.txt", "w") as f:
        for row in board:
            line = "".join(str(x) for x in row) + "\n"
            f.write(line)
