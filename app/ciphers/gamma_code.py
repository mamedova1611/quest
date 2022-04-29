def gamma(text, key):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
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
        new_text = new_text + alphabet[(count + count_2) % 33]
    return new_text


