import openai
import json
import os
from src.config import get_settings
from dotenv import load_dotenv

load_dotenv()  # Cargamos el archivo .env

_SETTINGS = get_settings()

openai.api_key = os.environ.get("OPENAI_API_KEY")

class AnalysisModel:
    def perform_analysis(self, text):
        # Definimos la funcion que le pasaremos al modelo de openai para obtener el análisis de texto
        ner_gpt_function = [
            {
                "name": "find_juridics",
                "description": "Analyze the following text and return the entities and problematics found, they all have to be juridics related.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "entity": {"type": "string",
                                               "description": "A named entity extracted from text."},
                                    "problematic": {"type": "string",
                                                 "description": "Problematic found on the text, that the named entity is facing."}
                                }
                            }
                        }
                    }
                },
                "required": ["entities"]
            }
        ]

        # Hacemos la busqueda usando GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}],
            functions=ner_gpt_function,
            function_call={"name": "find_juridics"},
        )

        cleaned_string = response['choices'][0]['message']['function_call']['arguments'].replace("\\n", "\n")
        parsed_object = json.loads(cleaned_string)

        return parsed_object