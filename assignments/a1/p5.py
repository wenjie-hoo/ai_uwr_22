import random

class Puzzle:
    def __init__(self, row_nums, col_nums):
        self.row_nums = row_nums
        self.col_nums = col_nums
        self.reset()
    
    def reset(self):
        self.rows = [[0] * len(self.col_nums) for _ in self.row_nums]
        self.cols = [[0] * len(self.row_nums) for _ in self.col_nums]
        for x in range(len(self.cols)):
            for y in range(len(self.rows)):
                if random.randint(0, 1):
                    self.flip(x, y)

    def try_to_solve(self):
        for _ in range(10000):
            if self.is_solved():
                return
            if random.randint(0, 1):
                self.change_random_row()
            else:
                self.change_random_col()
    
    def opt_dist(self, digits, num_digits):
        total_ones = sum(digits)
        ones_in_window = sum(digits[:num_digits])
        min_flips = (num_digits - ones_in_window) + (total_ones - ones_in_window)
        for start, end in zip(digits, digits[num_digits:]):
            ones_in_window -= start
            ones_in_window += end
            curr_flips = (num_digits - ones_in_window) + (total_ones - ones_in_window)
            min_flips = min(curr_flips, min_flips)
        return min_flips

    def is_solved(self):
        for i, row in enumerate(self.rows):
            if self.opt_dist(row, self.row_nums[i]) != 0:
                return False
        for i, col in enumerate(self.cols):
            if self.opt_dist(col, self.col_nums[i]) != 0:
                return False
        return True

    def change_random_row(self):
        y = random.randint(0, len(self.row_nums) - 1)
        row, row_num = self.rows[y], self.row_nums[y]
        best_flip_x, min_dist = 0, len(row) + len(self.col_nums) + 1
        for x, (col, col_num) in enumerate(zip(self.cols, self.col_nums)):
            self.flip(x, y)
            curr_dist = self.opt_dist(row, row_num) + self.opt_dist(col, col_num)
            if curr_dist < min_dist:
                min_dist = curr_dist
                best_flip_x = x
            self.flip(x, y)
        self.flip(best_flip_x, y)
    
    def change_random_col(self):
        x = random.randint(0, len(self.col_nums) - 1)
        col, col_num = self.cols[x], self.col_nums[x]
        best_flip_y, min_dist = 0, len(col) + len(self.row_nums) + 1
        for y, (row, row_num) in enumerate(zip(self.rows, self.row_nums)):
            self.flip(x, y)
            curr_dist = self.opt_dist(col, col_num) + self.opt_dist(row, row_num)
            if curr_dist < min_dist:
                min_dist = curr_dist
                best_flip_y = y
            self.flip(x, y)
        self.flip(x, best_flip_y)

    def flip(self, x, y):
        self.rows[y][x] ^= 1
        self.cols[x][y] ^= 1

    def as_image(self):
        image_rows = []
        for row in self.rows:
            image_row = ""
            for cell in row:
                if cell == 1:
                    image_row += "#"
                else:
                    image_row += "."
            image_rows.append(image_row)
        return "\n".join(image_rows)

if __name__ == '__main__':
    with open('zad5_input.txt') as f:
        size_raw = f.readline()
        num_rows, num_cols = map(int, size_raw.split())
        row_nums = [int(f.readline()) for _ in range(num_rows)]
        col_nums = [int(f.readline()) for _ in range(num_cols)]
    
    puzzle = Puzzle(row_nums, col_nums)

    while not puzzle.is_solved():
        puzzle.reset()
        puzzle.try_to_solve()
    with open('zad5_output.txt', 'w+') as out:
        out.write(puzzle.as_image())