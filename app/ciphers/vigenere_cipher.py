def vigenere(text, key):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    count = 0
    while True:
        if len(text) == len(key):
            break
        key = key + key[count]
        count += 1
        if count == 5:
            count = 0
    new_text = ''
    for i in range(len(text)):
        count = 0
        for j in alphabet:
            if key[i] == j:
                break
            count += 1

        count_2 = 0
        for j in alphabet:
            if text[i] == j:
                break
            count_2 += 1
        num = count_2 + count
        if num >= len(alphabet):
            num = num - len(alphabet)
        new_text = new_text + alphabet[num]
    return new_text
