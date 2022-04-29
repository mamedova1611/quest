def caesar(text):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    alphabet_c = 'ГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВ'
    new_text = ''
    for i in text:
        count = 0
        for x in alphabet:
            if i == x:
                break
            count += 1
        new_text = new_text + alphabet_c[count]
    return new_text
