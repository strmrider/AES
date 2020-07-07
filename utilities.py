def create_block(text, start):
    matrix = []
    index = start
    for i in range(4):
        vector = []
        for j in range(4):
            vector.append((text[index]))
            index += 1
        matrix.append(vector)

    return matrix


def block_to_text(block):
    text = ""
    for i in range(4):
        text += "".join(map(chr, block[i]))

    return text


def blocks_list_to_text(blocks):
    text = ""
    for i in range(len(blocks)):
        text += block_to_text(blocks[i])

    return text


def add_padding(text):
    text_len = len(text)
    if text_len % 16 != 0:
        text.append(128)
        padding_number = 16 - (text_len % 16)
        for i in range(1, padding_number):
            text.append(0)
    # add dummy padding
    else:
        text.append(128)
        for i in range(15):
            text.append(0)

    return text


def remove_padding(text):
    padding_start = 0
    for i in range(len(text)-1, 0, -1):
        if text[i] == chr(128):
            padding_start = i

    return text[0: padding_start]

