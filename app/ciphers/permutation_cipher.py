#шифр одинарной перестановки

def single_permutation(text, key):
    new_text = ''
    for i in key:
        new_text += text[i-1]
    return new_text
