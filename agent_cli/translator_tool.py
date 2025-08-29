def translate_en_to_de(text: str) -> str:
    # Minimal stub to keep assignment self-contained.
    # In real use, call a translation API.
    dictionary = {
        "good morning": "Guten Morgen",
        "have a nice day": "Einen schönen Tag noch",
        "sunshine": "Sonnenschein",
    }
    key = text.strip().lower().strip("'\"")
    return dictionary.get(key, f"[de] {text}")


