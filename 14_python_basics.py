import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # hala board ro besaz
        self.board = self.make_new_board()

        # adadi ke namayesh dade mishe ro mohasebe bokonim
        self.get_board_values()

        # Baraye inke biaim va khoone hayi ke baz shodan ro dashte bashim
        self.history = set()

    def get_board_values(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # in khoone bombe pas lazem nist ke value oon neshoon dade beshe
                    continue
                self.board[r][c] = self.calc_near_bombs(r, c)
    
    def calc_near_bombs(self, row, col):
        # bala chap: row-1, col-1
        # bala: row-1, col
        # bala rast: row-1, col+1
        # chap : row, col-1
        # khodesh: row, col
        # rast: row, col+1
        # pain chap: row+1, col-1
        # pain: row+1, col
        # pain rast: row+1, col+1
        total_near_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1 + 1))):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1 + 1))):
                if r == row and c == col:
                    # yani hamoon khoonas va lazem nist ke bebinim bomb hast toosh yana
                    continue
                if self.board[r][c] == '*':
                    # yani tooye oon khoone bomb hast, pas be bomb haye atraf yeki ezafe beshe
                    total_near_bombs += 1
        
        return total_near_bombs

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # mikhaim bomb haro be soorate random bezarim
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            # agar bomb gozashte boodim nemikhaim dobare bomb bezare pas bere iter e badi
            if board[row][col] == '*':
                continue
            
            # pas bomb bezarim
            board[row][col] = '*'
            bombs_planted += 1
        
        return board

    def dig(self, row, col):
        # User miad yek jai ro dig mikone va khuruji oon True ya False hastesh
        # agar user jai ro click kard ke bomb bood -> khurju ro False bede
        # agar user jai ro click kard ke bomb nabood -> khuruji ro True bede

        # Darkol do halat darim
        # 1. agar bomb ro click kard ke hichi mibazim va False namayesh dade mishe
        # 2. agar yek khoone ro click kard ke bomb nabood bayad check konim ke aya
        # atrafe oon khoone bomb hast ya na, agar bomb nabood bayad khoone haye bishtari baz she
        # va enghadr in karo edame bedim ke be khoone hayi beresim ke doreshoon bombe

        self.history.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1 + 1))):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1 + 1))):
                if (r, c) in self.history:
                    continue # chon ghablan ezafe kardim, nemikhaim dobare ezafe beshe
                self.dig(r, c)
        # chonke bombi ro click nakardim pas bayad True ro return konim
        return True

    def __str__(self):
        user_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r, c) in self.history:
                    user_board[r][c] == str(self.board[r][c])
                else:
                    user_board[r][c] == '  '

        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], user_board)
            widths.append(len(max(columns, key = len)))
        
        indicies = [i for i in range(self.dim_size)]
        indicies_row = '   '
        cells = []
        for idx, col in enumerate(indicies):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indicies_row += '  '.join(cells)
        indicies_row += '  \n'
        
        for i in range(len(user_board)):
            row = user_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indicies_row + '-'*str_len + '\n' + string_rep + '-'*str_len
        
        return string_rep


def play(dim_size=10, num_bombs=10):
    # step 1 : sakhte board va gozashtane bomb ha
    board = Board(dim_size, num_bombs)
    # step 2 : be user board ro neshoon bedim va azash bekhaim yek jaro click bokone
    # step 3 : agar bomb bood user bakhte va agar bomb nabood be bazi edame bede
    # step 4 : bayad in karo enghad tekrar bokonim ta ya user bebaze ya inke bazi ro bebarim
    safe = True
    while len(board.history) < board.dim_size**2 - num_bombs:
        # be user board ro namayesh bede
        print(board)
        
        # az user bepors kudum khoonaro mikhad dig bokone
        
        # 2,3 ya 2, 3 ya 2,    3
        user_input = re.split(',(\\s)*', input("Koja ro mikhain dig bokonin?(mesal: 2,3)"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("khoonei ke moshakhas kardin vojud nadare va kharej az index ast.\nkhoone jadidi dar nazar begirid.")
            continue

        # agar kharej az index naboodim va jaye dorosti ro entekhab karde boodim
        safe = board.dig(row, col)
        if not safe:
            # bomb ro dig kardim
            break

    if safe:
        print('Shoma bordin:)')
    else:
        print('Shoma bakhtin:(')
        board.history = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    play()


