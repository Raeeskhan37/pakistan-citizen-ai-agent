def detect_language(text):

    urdu_characters = 0

    for char in text:

        if "\u0600" <= char <= "\u06ff":
            urdu_characters += 1

    if urdu_characters > 5:
        return "Urdu"

    return "English"
