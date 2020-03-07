import random

RIGHT = 1, 0
UP = 0, 1
LEFT = -1, 0
DOWN = 0, -1
EMPTY = 0
WALL = 1

NEIGHBORS = [RIGHT, DOWN, LEFT, UP]

class Engine:
    def __init__(self, map_filename):
        self.board = []
        self.enemies = []
        with open(map_filename) as map_file:
            for y, line in enumerate(map_file):
                row = []
                for x, cell in enumerate(line.strip()):
                    if cell == '.':
                        row.append(EMPTY)
                    elif cell == '#':
                        row.append(WALL)
                    elif cell == 'K':
                        row.append(EMPTY)
                        self.position = x, y
                    elif cell == 'Z':
                        row.append(EMPTY)
                        self.enemies.append((x,y))
                    else:
                        raise NotImplementedError()
                self.board.append(row)
        self.height = len(self.board)
        self.width = len(self.board[0])
        for row in self.board:
            if len(row) != self.width:
                raise ValueError('Bad board')
        self.game_continues = True
        self.game_over = False
        self.move_number = 0

    def move_wins(self, new_position):
        x, y = new_position
        if y > self.height-1 or y < 0:
            return True
        if x > self.width-1 or x < 0:
            return True
        return False


    def move_legal(self, new_position):
        x, y = new_position
        if self.board[y][x] == WALL:
            return False
        else:
            return True

    def make_move(self, direction):
        if self.game_continues:
            x, y = self.position
            dx, dy = direction
            new_position = x + dx, y + dy
            if self.move_wins(new_position):
                self.game_continues = False
                self.position = new_position
                self.move_number += 1
                self.enemy_move()
            elif self.move_legal(new_position):
                self.position = new_position
                self.move_number += 1
                self.enemy_move()
            for enemy in self.enemies:
                if enemy == self.position:
                    self.game_continues = False
                    self.game_over = True


    def get_walls(self):
        return [(x, y)
                for x in range(self.width)
                for y in range(self.height)
                if self.board[y][x] == WALL]

    def enemy_move(self):
        if self.game_continues and self.move_number % 2 == 1:
            distances = self.bfs()
            new_enemies = set()
            for ex, ey in self.enemies:
                old_dist = distances[ey][ex]
                candidates = []
                for dx, dy in NEIGHBORS:
                    nex = ex + dx
                    ney = ey + dy
                    if not self.move_wins((nex, ney)) and (nex, ney) not in new_enemies:
                        if distances[ney][nex] < old_dist:
                            candidates.append((nex, ney))
                if len(candidates) == 0:
                    candidates.append((ex, ey))
                new_enemies.add(random.choice(candidates))
            self.enemies = list(new_enemies)

    def bfs(self):
        to_do = [self.position]
        distances = [[self.width*self.height + 1 for i in range(self.width)] for i in range(self.height)]
        x, y = self.position
        distances[y][x] = 0
        i = 0
        while i < len(to_do):
            x, y = to_do[i]
            for dx, dy in NEIGHBORS:
                nx = x+dx
                ny = y+ dy
                if not self.move_wins((nx,ny)):
                    if distances[ny][nx] == self.width*self.height + 1 and self.board[ny][nx] != WALL:
                        distances[ny][nx] = distances[y][x]+1
                        to_do.append((nx, ny))
            i += 1
        return distances














