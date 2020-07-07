import key_schedule
import round
import utilities
import os


def generate_cipher_key():
    return os.urandom(16)


class AES:
    def __init__(self, cipher_key):
        self.__keys = []
        hex_cipher_key = map(ord, cipher_key)
        self.__produce_keys(hex_cipher_key)

    def __produce_keys(self, cipher_key):
        cipher_key = utilities.create_block(cipher_key, 0)
        self.__keys.append(cipher_key)
        for i in range(10):
            last_key = self.__keys[len(self.__keys)-1]
            expansion = key_schedule.KeyExpansion(last_key).expand(i)
            self.__keys.append(expansion)

    @staticmethod
    def __produce_blocks(plain_text):
        blocks = []
        hex_text = map(ord, plain_text)
        utilities.add_padding(hex_text)
        for i in range(0, len(hex_text), 16):
            if i >= len(hex_text):
                break
            blocks.append(utilities.create_block(hex_text, i))

        return blocks

    def __encryption_round(self, block):
        state = round.Round(block, round.REGULAR).initial_round(self.__keys[0])
        for i in range(1, 10):
            state = round.Round(state, round.REGULAR).main_round(self.__keys[i])
        state = round.Round(state, round.REGULAR).final_round(self.__keys[10])

        return state

    def __decryption_round(self, block):
        state = round.Round(block, round.INVERSE).final_round(self.__keys[10])
        for i in range(9, 0, -1):
            state = round.Round(state, round.INVERSE).main_round(self.__keys[i])
        state = round.Round(block, round.INVERSE).initial_round(self.__keys[0])

        return state

    def encrypt(self, plain_text):
        blocks = self.__produce_blocks(plain_text)
        cipher_blocks = []
        for i in range(len(blocks)):
            cipher_blocks.append(self.__encryption_round(blocks[i]))

        return utilities.blocks_list_to_text(cipher_blocks)

    def decrypt(self, cipher_text):
        blocks = self.__produce_blocks(cipher_text)
        decrypted_blocks = []
        for i in range(len(blocks)):
            decrypted_blocks.append(self.__decryption_round(blocks[i]))
        text = utilities.blocks_list_to_text(decrypted_blocks)
        unpadded_text = utilities.remove_padding(text)
        return unpadded_text

    def __handle_file(self, filename, action):
        with open(filename, "rb+") as f:
            target_file = f.read()
            if action == 0:
                data = self.encrypt(target_file)
            else:
                data = self.decrypt(target_file)

            f.seek(0)
            f.write(data)
            f.truncate()

    def encrypt_file(self, filename):
        self.__handle_file(filename, 0)

    def decrypt_file(self, filename):
        self.__handle_file(filename, 1)
