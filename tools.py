import requests
from agents import function_tool


@function_tool
def get_meaning(word:str):
    """
    Fetch the definition, part of speech, synonyms, and antonyms for a word.
    """
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if res.status_code != 200:
            return {"error": f"Could not find meaning for '{word}'."}
        data = res.json()

        # Extract from the first meaning only for simplicity
        meaning_data = data[0]["meanings"][0] 
        part_of_speech = meaning_data["partOfSpeech"]
        definition = meaning_data["definitions"][0]["definition"]
        example = meaning_data["definitions"][0].get("example", "No example available.")
        synonyms = meaning_data["definitions"][0].get("synonyms", [])
        antonyms = meaning_data["definitions"][0].get("antonyms", [])

        return {
            "word": word,
            "part_of_speech": part_of_speech,
            "definition": definition,
            "example": example,
            "synonyms": synonyms[:5],   # limit to 5
            "antonyms": antonyms[:5]    # limit to 5
        }
    except Exception as e:
        return {"error":str(e)}