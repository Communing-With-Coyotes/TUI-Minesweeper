import random


INVALID_NEIGHBOR_COUNT = -1
NO_TILE_SELECTED = (-1, -1)


class Minefield:

    def __init__(self, x_size, y_size, mine_count, selected = NO_TILE_SELECTED):
        self.x_size = x_size
        self.y_size = y_size
        self.mine_count = mine_count
        self.selected = selected

        self.grid = self.setup_grid()


    def setup_grid(self):
        grid = {}
        random.seed()

        for n in range(self.mine_count):
            rand_x = random.randrange(0, self.x_size)
            rand_y = random.randrange(0, self.y_size)

            grid[(rand_x, rand_y)] = self.create_spot(rand_x, rand_y, mined = True)
        
        return grid


    def create_spot(self, x, y, mined = False, searched = False):
        return {
            "mined": mined,
            "searched": searched, 
            "neighbors": INVALID_NEIGHBOR_COUNT if mined else 0
        }


    def select(self, x, y):
        self.selected = (x, y)


    # Moves the selection by the given amount. If no tile is currently selected, then start at the 
    # appropriate edge of the game board.
    def move_selection(self, by_x, by_y, wrap_around = True):
        # We want the edge we select, to be opposite the move direction.
        if self.selected == NO_TILE_SELECTED:
            start_x = 0 if by_x > 0 else self.x_size - 1
            start_y = 0 if by_y > 0 else self.y_size - 1

            self.selected = (start_x, start_y)
        else:
            x, y = (self.selected)

            if wrap_around:
                x += by_x
                y += by_y

                if x < 0 or x >= self.x_size:
                    x = x % self.x_size
                if y < 0 or y >= self.y_size:
                    y = y % self.y_size
            else:
                x = max( 0, min(self.x_size - 1, x + by_x) )
                y = max( 0, min(self.y_size - 1, y + by_y) )

            self.selected = (x, y)


    # Returns true if you uncover a mine.
    def search_spot(self, x, y):
        position = (x, y)

        if not self.grid.get(position):
            self.grid[position] = self.create_spot(x, y, searched = True)
            self.count_neighbors(x, y)
            
            return False
        
        self.grid[position]["searched"] = True
        return self.grid[position]["mined"]


    def count_neighbors(self, x, y):
        position = (x, y)
        spot = self.grid.get(position)

        if not spot or spot["mined"]:
            return

        nw_key = (x - 1, y - 1)
        n_key = (x, y - 1)
        ne_key = (x + 1, y - 1)
        w_key = (x - 1, y)
        e_key = (x + 1, y)
        sw_key = (x - 1, y + 1)
        s_key = (x, y + 1)
        se_key = (x + 1, y + 1)

        neighbor_count = 0
        neighbor_count += 1 if self.has_mine_at_position(*nw_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*n_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*ne_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*w_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*e_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*sw_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*s_key) else 0
        neighbor_count += 1 if self.has_mine_at_position(*se_key) else 0

        spot["neighbors"] = neighbor_count


    def has_mine_at_position(self, x, y):
        spot = self.grid.get((x, y))
        if spot:
            return spot["mined"]

        return False

