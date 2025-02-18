class Text:
    def __init__(self, text):
        self.text = text
        self.position = 0

    def Get(self, index):
        return self.text[self.position + index]

    def Next(self):
        self.position += 1

    def Copy(self):
        return Text(self.text[self.position:])

def B(text: list[Text]) -> bool:
    print("B", text[0].text)
    return C(text) and E(text)

def E(text: list[Text]) -> bool:
    print("E", text[0].text)
    if "ку " == text[0].Get(0) + text[0].Get(1) + text[0].Get(2):
        newText = text[0].Copy()
        newText.Next()
        newText.Next()
        newText.Next()
        a = [newText]
        if B(a):
            text[0] = a[0]

    return True

def D(text: list[Text]) -> bool:
    print("D", text[0].text)
    if "ау " == text[0].Get(0) + text[0].Get(1) + text[0].Get(2):
        newText = text[0].Copy()
        newText.Next()
        newText.Next()
        newText.Next()
        a = [newText]
        if A(a):
            text[0] = a[0]

    return True

def C(text: list[Text]) -> bool:
    print("C", text[0].text)
    # Проверяем, начинается ли с "ух-ты "
    if text[0].Get(0) == 'у' and text[0].Get(1) == 'х' and text[0].Get(2) == '-' and text[0].Get(3) == 'т' and text[0].Get(4) == 'ы':
        text[0].Next()
        text[0].Next()
        text[0].Next()
        text[0].Next()
        text[0].Next()
        return True

    if text[0].Get(0) == 'х' and text[0].Get(1) == 'о':
        text[0].Next()
        text[0].Next()
        if C(text):  # Рекурсивный вызов для Правила3
            return True

    if text[0].Get(0) == 'н' and text[0].Get(1) == 'у':
        text[0].Next()
        text[0].Next()
        if A(text):  # Проверяем Правило1
            # Проверяем наличие " и ну"
            if text[0].Get(0) == 'и' and text[0].Get(1) == ' ' and text[0].Get(2) == 'н' and text[0].Get(3) == 'у':
                text[0].Next()
                text[0].Next()
                text[0].Next()
                text[0].Next()
                return True

    return False


def A(text: list[Text]) -> bool:
    print("A", text[0].text)
    return B(text) and D(text)
text = Text("ну ух-ты и ну ")
print(A([text]))