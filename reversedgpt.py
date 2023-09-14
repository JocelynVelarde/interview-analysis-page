from revChatGPT.V3 import Chatbot
from config import API_KEY

# Initialize the Chatbot with API key
if API_KEY is None:
    print("API key not found. Please set the API_KEY environment variable.")
    exit(1)
chatbot = Chatbot(API_KEY)

#Create a conversation with the interview text
file_path = "transcript.txt"
try:
    with open(file_path, "r", encoding="utf-8") as file:
        interview_text = file.read()
        print("Interview Text: " + interview_text)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit(1)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit(1)

# Create a system message to set the context
system_prompt = "Se te entregara un archivo de texto en donde se encuentra la transcripcion de una llamada telefonica entre cliente-vendedor, se te pedira que analices distintos aspectos de la conversacion."
chatbot.add_to_conversation(system_prompt, "system")

# Add the interview text as a user message
chatbot.add_to_conversation(interview_text, "user")

# Present options to the user
print("Elige una opción para analizar la entrevista:")
print("1. Reconocimiento de emociones")
print("2. Extracción de palabras clave")
print("3. Análisis de tono")
print("4. Estructura y flujo de la entrevista")

user_choice = input("Ingresa el numero con la opción de tu elección (1-4): ")

# Send predefined prompts based on the user's choice
if user_choice == "1":
    emotion_prompt = "Analiza las palabras que se utilizan en la entrevista y asignales una emocion. Entregame un parrafo con las distintas emociones que encontraste en el tono de la entrevista y muestrame su descripcion."
    response = chatbot.ask(emotion_prompt)
elif user_choice == "2":
    keywords_prompt = "Explica en un parrafo las palabras clave que le dan contexto a la entrevista, son palabras utiles que usa el vendedor para convencer al cliente."
    response = chatbot.ask(keywords_prompt)
elif user_choice == "3":
    tone_prompt = "Analiza el tono de la entrevista y entregame un parrafo con la descripcion de este."
    response = chatbot.ask(tone_prompt)
elif user_choice == "4":
    meta_analysis_prompt = "Realiza un meta-analisis de la estructura y el flujo de ella en un parrafo, es decir la introducción y conceptos clave, el cuerpo de la entrevista y la conclusión. Y en que sección se mostro un mayor interes del cliente."
    response = chatbot.ask(meta_analysis_prompt)
else:
    print("Opcion invalida. Intente nuevamente utilizando (1-4)")

# Print the chatbot's response
print("Respuesta de GPT-3:")
print(response)
