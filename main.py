class CrossZeroField:
    """Это поле, которое мы будем заполнять крестиками и ноликами"""

    def __init__(self, size: int = 3, k: int = 3):
        self.__size = size
        self.__k = k
        self.__field = [[0] * size for i in range(size)]
        self.__queue = 1
        self.__win = 0

    def get_size(self):
        return self.__size

    def get_queue(self):
        return self.__queue

    def get_k(self):
        return self.__k

    def get_win(self):
        return self.__win

    def is_empty(self, line, column):
        if self.__field[line][column] == 0:
            return True
        return False

    def print_field(self):
        print(" ", end="")
        for i in range(self.__size):
            print("|", i, end="", sep="")
        print("|")
        j = 0
        for line in self.__field:
            print(j, end="")
            j += 1
            for elem in line:
                print("|", end="")
                if elem == 0:
                    print(" ", end="")
                elif elem == 1:
                    print("x", end="")
                elif elem == -1:
                    print("o", end="")
                else:
                    raise ValueError("В поле обнаружена что-то кроме 1, -1 и 0")
            print("|")

    def __check_num_line(self, value: int):
        if not isinstance(value, int):
            raise ValueError("что-то пошло не так3")
        if value >= self.__size or value < 0:
            return False
        return True

    def draw_sign(self, num_column: int, num_line: int):
        if (not CrossZeroField.__check_num_line(self, num_line) or
                not CrossZeroField.__check_num_line(self, num_column)):
            raise ValueError("что-то пошло не так4")
        if self.__field[num_column][num_line] != 0:
            return False
        self.__field[num_column][num_line] = self.__queue
        self.__check_winner(num_column, num_line)
        CrossZeroField.__next_queue(self)
        return True

    def __check_winner(self, line, column):
        i0, j0, k, size, field = line, column, self.__k, self.__size, self.__field
        flag = field[i0][j0]
        for p, q in [(1, 1), (1, 0), (0, 1), (1, -1)]:
            t = 0
            i, j = i0, j0
            while CrossZeroField.__check_coord(i, j, size):
                if field[i][j] == flag:
                    t += 1
                    i += p
                    j += q
                else:
                    break
            t -= 1
            i, j = i0, j0
            while CrossZeroField.__check_coord(i, j, size):
                if field[i][j] == flag:
                    t += 1
                    i -= p
                    j -= q
                else:
                    break
            if t >= k:
                self.__win = flag
                print("win")
                return True
        return False

    def clear_field(self):
        for line in self.__field:
            for i in range(self.__size):
                line[i] = 0

    def __next_queue(self):
        self.__queue *= -1

    @staticmethod
    def __check_coord(i: int, j: int, size: int):
        if i >= size or i < 0 or j >= size or j < 0:
            return False
        return True


class GameManager:
    __phrases = {
        "start": [
            "Приветствую! Это игра крестики-нолики.\n"
            "Введите Enter чтобы начать:"
        ],
        "exit": [
            "Вы вышли из игры. До втречи ;\n)"
        ],
        "none": [
            "Я накосячил с ключом фразы\n"
        ],
        "bad": [
            "Неправильный ввод\n",
            "Стоп, k должно быть не больше n\n",
            "Стоп, вы не попали в поле\n",
            "Эта клетка уже занята\n"
        ],
        "menu": [
            "Чтобы снова выйти в меню, введите 'menu'\n"
            "### Чтобы вернуться к предыдущему вводу параметров введите 'back'\n"
            "Введите Enter чтобы начать:",

            "Выберите тип игры.\n"
            "### 1 - это игра в двоём\n"
            "### Ввод Enter расценивается как ввод '1'\n"
            "### Остальное не завезли\n"
            "Введите число или Enter",

            "Напишите размер поля n и длину линии k, необходимую для выигрыша\n"
            "### Ввод Enter расценивается как ввод '3 3'\n"
            "Введите два числа или Enter",

            "Введите 'start' или Enter, чтобы начать\n"
        ],
        "game1": [
            "Ход ноликов. Сначала вводится номер столбца, потом номер линии.\n",
            "Ход крестиков. Сначала вводится номер столбца, потом номер линии.\n"
        ],
        "win": [
            "Нолики выиграли!\n",
            "Крестики выиграли!\n"
        ]
    }

    def __init__(self):
        self.__phase = "start"
        self.__stage = 0
        self.__exit = False
        self.__keys = ["start", 0]
        self.__mode = 0
        self.__bad_flag = False
        self.__bad_out = 0
        self.__n = 3
        self.__k = 3
        self.__end_game = False

    def __create_keys(self):
        self.__keys[0] = self.__phase
        self.__keys[1] = self.__stage

    def __next_stage(self):
        self.__stage += 1
        GameManager.__create_keys(self)

    def __back_stage(self):
        self.__stage = max(0, self.__stage - 1)
        GameManager.__create_keys(self)

    def __go_menu(self):
        self.__end_game = False
        self.__phase = "menu"
        self.__stage = 0
        GameManager.__create_keys(self)

    def __go_game1(self):
        self.__phase = "game1"
        self.__stage = 0
        GameManager.__create_keys(self)
        self.__field = CrossZeroField(self.__n, self.__k)

    def __create_bad(self, p: int = 0):
        self.__bad_flag = True
        self.__bad_out = p

    def __disable_bad(self):
        self.__bad_flag = False
        self.__bad_out = 0

    def ingame(self, received: str):
        if received == "menu":
            self.__go_menu()
        elif received == "exit":
            self.__out("exit")
            self.__exit = True
        elif self.__phase == "start":
            GameManager.__go_menu(self)
        elif self.__phase == "menu":
            GameManager.__menu(self, received)
        elif self.__phase == "game1":
            GameManager.__game1(self, received)

    def __menu(self, received: str):
        if received == "back":
            GameManager.__back_stage(self)
        elif self.__stage == 0:
            GameManager.__next_stage(self)
        elif self.__stage == 1:
            if received == "1" or received == "":
                GameManager.__next_stage(self)
                self.__mode = 1
            else:
                GameManager.__create_bad(self)
        elif self.__stage == 2:
            if received == "":
                self.__n, self.__k = 3, 3
                GameManager.__next_stage(self)
                return None
            received = received.split()
            if len(received) == 2 and GameManager.__check_dig(received[0], received[1]):
                if int(received[1]) <= int(received[0]):
                    self.__n, self.__k = int(received[0]), int(received[1])
                    GameManager.__next_stage(self)
                else:
                    GameManager.__create_bad(self, 1)

            else:
                GameManager.__create_bad(self)
        elif self.__stage == 3:
            if received == "start" or received == "":
                GameManager.__go_game1(self)
            else:
                GameManager.__create_bad(self)

    def __game1(self, received: str):
        received = received.split()
        if len(received) == 2 and GameManager.__check_dig(received[0], received[1]):
            i, j = int(received[0]), int(received[1])
            if GameManager.__check_coord(i, j, self.__field.get_size()):
                if not self.__field.draw_sign(int(received[0]), int(received[1])):
                    GameManager.__create_bad(self, 3)
                if self.__field.get_win() != 0:
                    self.__end_game = True
            else:
                GameManager.__create_bad(self, 2)
        else:
            GameManager.__create_bad(self)

    def outgame(self):
        if self.__bad_flag:
            self.__out(self.__phrases["bad"][self.__bad_out])
            GameManager.__disable_bad(self)
        elif self.__phase == "game1":
            if self.__end_game:
                if self.__field.get_win() == 1:
                    self.__out(self.__phrases["win"][1])
                else:
                    self.__out(self.__phrases["win"][0])
                self.__go_menu()
                return None
            if self.__field.get_queue() == 1:
                self.__out(self.__phrases["game1"][1])
            else:
                self.__out(self.__phrases["game1"][0])
            self.__field.print_field()
        else:
            phrase = self.__phrases
            for key in self.__keys:
                phrase = phrase[key]
            self.__out(phrase)


    @staticmethod
    def __check_coord(i: int, j: int, size: int):
        if i >= size or i < 0 or j >= size or j < 0:
            return False
        return True

    @staticmethod
    def __check_dig(a: str, b: str):
        if a.isdigit() and b.isdigit():
            return True
        return False

    @staticmethod
    def __out(phrase):
        print("###", phrase, end="")

    def get_exit(self):
        return not self.__exit


game = GameManager()
go = True
while go:
    game.outgame()
    cin = input()
    game.ingame(cin)
    go = game.get_exit()
