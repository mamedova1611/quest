def magic_square(text, matrix):
    size_matrix = 4

    while True:  # Цикл для проверки входного текста если короче дополнеяем точками
        if len(text) == size_matrix * size_matrix:
            break
        elif len(text) > size_matrix * size_matrix:  # Если длинее текст то укорачиваем до матрица
            text = text[:size_matrix * size_matrix]
        else:  # Если длинее то удлиняем путем добавленим от начала текста
            text += text[:size_matrix * size_matrix - len(text)]

    encrypt_text = ''

    for i in range(size_matrix):  # Цикл для шифрования
        for j in range(size_matrix):
            encrypt_text += text[matrix[i][j] - 1]

    return encrypt_text
