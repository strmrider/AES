import box


class KeyExpansion:
    def __init__(self, cipher_key):
        self.__cipher_key = cipher_key

    def __get_rot_word(self):
        rot_word = self.__cipher_key[3][:]
        rot_word[0], rot_word[1], rot_word[2], rot_word[3] = rot_word[1], rot_word[2], rot_word[3], rot_word[0]
        for i in range(4):
            rot_word[i] = box.s_box[rot_word[i]]

        return rot_word

    def __column_rot_xor(self, round_number):
        rot_word = self.__get_rot_word()
        vector = []
        rcon = box.rcon[round_number]
        for i in range(4):
            xor_result = ((self.__cipher_key[0][i] ^ rot_word[i]) ^ rcon[i])
            vector.append(xor_result)

        return vector

    def __vector_xor(self, i, vector):
        new_vector = []
        for j in range(4):
            xor_result = (self.__cipher_key[i][j] ^ vector[j])
            new_vector.append(xor_result)

        return new_vector

    def expand(self, round_number):
        key = []
        key.append(self.__column_rot_xor(round_number))
        key.append(self.__vector_xor(1, key[0]))
        key.append(self.__vector_xor(2, key[1]))
        key.append(self.__vector_xor(3, key[2]))

        return key
