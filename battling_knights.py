import json
from io import StringIO

class Knight:
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        self.attack = 1
        self.defence = 1
        self.item = None
        self.alive = True

class Item:
    def __init__(self, name, attack_bonus, defence_bonus):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defence_bonus = defence_bonus
        self.position = None  # Add this line to initialize the position attribute

class Arena:
    def __init__(self):
        self.board = [['_' for _ in range(8)] for _ in range(8)]
        self.knights = {
            'red': Knight('red', 0, 0),
            'blue': Knight('blue', 7, 0),
            'green': Knight('green', 7, 7),
            'yellow': Knight('yellow', 0, 7)
        }
        self.items = {
            'axe': Item('axe', 2, 0),
            'dagger': Item('dagger', 1, 0),
            'helmet': Item('helmet', 0, 1),
            'magic_staff': Item('magic_staff', 1, 1)
        }

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')

    def update_board(self):
        self.board = [['_' for _ in range(8)] for _ in range(8)]
        for knight in self.knights.values():
            if knight.alive:
                self.board[knight.row][knight.col] = knight.name.upper()
        for item in self.items.values():
            if item.position is not None:  # Check if the item has a position
                self.board[item.position[0]][item.position[1]] = item.name.upper()

    def move_knight(self, knight, direction):
        if not knight.alive:
            return
        new_row, new_col = knight.row, knight.col
        if direction == 'N' and knight.row > 0:
            new_row -= 1
        elif direction == 'E' and knight.col < 7:
            new_col += 1
        elif direction == 'S' and knight.row < 7:
            new_row += 1
        elif direction == 'W' and knight.col > 0:
            new_col -= 1
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            self.check_item_pickup(knight, new_row, new_col)
            self.board[knight.row][knight.col] = '_'
            knight.row, knight.col = new_row, new_col
            self.board[new_row][new_col] = knight.name.upper()

    def check_item_pickup(self, knight, row, col):
        item = self.items.get(self.board[row][col].lower())
        if item:
            knight.item = item
            item.position = None

    def fight(self, attacker, defender):
        if not attacker.alive or not defender.alive:
            return
        attack_score = attacker.attack + (attacker.item.attack_bonus if attacker.item else 0) + 0.5
        defence_score = defender.defence + (defender.item.defence_bonus if defender.item else 0)
        if attack_score > defence_score:
            defender.alive = False
            if defender.item:
                defender.item.position = [defender.row, defender.col]
                defender.item = None

    def update_knights(self):
        for knight1 in self.knights.values():
            for knight2 in self.knights.values():
                if knight1 != knight2 and knight1.row == knight2.row and knight1.col == knight2.col:
                    self.fight(knight1, knight2)

def parse_moves(file_path):
    if isinstance(file_path, str):
        with open(file_path, 'r') as file:
            moves = file.read().split('\n')
    else:
        moves = file_path.getvalue().split('\n')
    
    return [move.strip() for move in moves if move.strip()]




def update_board_with_moves(arena, moves):
    for move in moves:
        if move == "GAME-START" or move == "GAME-END":
            # Ignore these moves
            continue

        # Split the move string into tokens
        tokens = move.split(":")
        
        # Check if there are enough tokens to proceed
        if len(tokens) != 2:
            print(f"Ignore invalid move: {move}")
            continue

        knight_name, direction = tokens

        # Check if the knight_name is valid
        if knight_name not in arena.knights:
            print(f"Ignore invalid move: {move}")
            continue

        # Perform the move
        arena.move(knight_name, direction)

        # Check if there are any items to pick up
        arena.pick_up_items()

        # Check for knight battles
        arena.battle_knights()




def output_final_state(arena, output_file):
    final_state = {
        'red': [arena.knights['red'].row, arena.knights['red'].col,
                'LIVE' if arena.knights['red'].alive else 'DEAD' if not arena.knights['red'].alive else 'DROWNED',
                arena.knights['red'].item.name if arena.knights['red'].item else None,
                arena.knights['red'].attack,
                arena.knights['red'].defence],

        'blue': [arena.knights['blue'].row, arena.knights['blue'].col,
                 'LIVE' if arena.knights['blue'].alive else 'DEAD' if not arena.knights['blue'].alive else 'DROWNED',
                 arena.knights['blue'].item.name if arena.knights['blue'].item else None,
                 arena.knights['blue'].attack,
                 arena.knights['blue'].defence],

        'green': [arena.knights['green'].row, arena.knights['green'].col,
                  'LIVE' if arena.knights['green'].alive else 'DEAD' if not arena.knights['green'].alive else 'DROWNED',
                  arena.knights['green'].item.name if arena.knights['green'].item else None,
                  arena.knights['green'].attack,
                  arena.knights['green'].defence],

        'yellow': [None,
                   None,
                   'LIVE' if arena.knights['yellow'].alive else 'DEAD' if not arena.knights['yellow'].alive else 'DROWNED',
                   arena.knights['yellow'].item.name if arena.knights['yellow'].item else None,
                   arena.knights['yellow'].attack,
                   arena.knights['yellow'].defence],

        'magic_staff': [arena.items['magic_staff'].position, False],
        'helmet': [arena.items['helmet'].position, False],
        'dagger': [arena.items['dagger'].position, False],
        'axe': [arena.items['axe'].position, False]
    }

    # Create a StringIO object to capture the JSON output
    output_buffer = StringIO()
    output_buffer.write(json.dumps(final_state, indent=2))

    # Use getvalue() to retrieve the contents of the StringIO object
    with open(output_file, 'w') as output:
        output.write(output_buffer.getvalue())


if __name__ == "__main__":
    arena = Arena()
    moves = parse_moves("moves.txt")
    update_board_with_moves(arena, moves)
    output_final_state(arena, "final_state.json")

