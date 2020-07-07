import box

REGULAR = 0
INVERSE = 1


class Round:
    def __init__(self, state, mode):
        self.__state = state
        self.__xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
        self.__mode = mode

    def __sub_bytes(self):
        table = box.s_box if self.__mode == REGULAR else box.inverse_s_box
        for i in range(4):
            for j in range(4):
                index = self.__state[i][j]
                self.__state[i][j] = table[index]

    def __shift_rows(self):
        self.__state[1][0], self.__state[1][1], self.__state[1][2], self.__state[1][3] = \
            self.__state[1][1], self.__state[1][2], self.__state[1][3], self.__state[1][0]
        self.__state[2][0], self.__state[2][1], self.__state[2][2], self.__state[2][3] = \
            self.__state[2][2], self.__state[2][3], self.__state[2][0], self.__state[2][1]
        self.__state[3][0], self.__state[3][1], self.__state[3][2], self.__state[3][3] = \
            self.__state[3][3], self.__state[3][0], self.__state[3][1], self.__state[3][2]

    def __inverse_shift_rows(self):

        self.__state[1][0], self.__state[1][1], self.__state[1][2], self.__state[1][3] = \
            self.__state[1][3], self.__state[1][0], self.__state[1][1], self.__state[1][2]

        self.__state[2][0], self.__state[2][1], self.__state[2][2], self.__state[2][3] = \
            self.__state[2][2], self.__state[2][3], self.__state[2][0], self.__state[2][1]

        self.__state[3][0], self.__state[3][1], self.__state[3][2], self.__state[3][3] = \
            self.__state[3][1], self.__state[3][2], self.__state[3][3], self.__state[3][0]

    def __mix_single_column(self, a):
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ self.__xtime(a[0] ^ a[1])
        a[1] ^= t ^ self.__xtime(a[1] ^ a[2])
        a[2] ^= t ^ self.__xtime(a[2] ^ a[3])
        a[3] ^= t ^ self.__xtime(a[3] ^ u)

    def __mix_columns(self):
        for i in range(4):
            self.__mix_single_column(self.__state[i])

    def __inv_mix_columns(self):
        for i in range(4):
            u = self.__xtime(self.__xtime(self.__state[i][0] ^ self.__state[i][2]))
            v = self.__xtime(self.__xtime(self.__state[i][1] ^ self.__state[i][3]))
            self.__state[i][0] ^= u
            self.__state[i][1] ^= v
            self.__state[i][2] ^= u
            self.__state[i][3] ^= v

        self.__mix_columns()

    def __add_round_key(self, cipher_key):
        for i in range(4):
            for j in range(4):
                self.__state[i][j] = (self.__state[i][j] ^ (cipher_key[i][j]))

    ###################
    # Round executions
    ###################

    def initial_round(self, cipher_key):
        self.__add_round_key(cipher_key)
        return self.__state

    def main_round(self, cipher_key):
        if self.__mode == REGULAR:
            self.__sub_bytes()
            self.__shift_rows()
            self.__mix_columns()
            self.__add_round_key(cipher_key)
        elif self.__mode == INVERSE:
            self.__add_round_key(cipher_key)
            self.__inv_mix_columns()
            self.__inverse_shift_rows()
            self.__sub_bytes()

        return self.__state

    def final_round(self, cipher_key):
        if self.__mode == REGULAR:
            self.__sub_bytes()
            self.__shift_rows()
            self.__add_round_key(cipher_key)
        elif self.__mode == INVERSE:
            self.__add_round_key(cipher_key)
            self.__inverse_shift_rows()
            self.__sub_bytes()

        return self.__state
