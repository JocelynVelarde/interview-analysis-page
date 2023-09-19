from flask import Flask, render_template, request
from revChatGPT.V3 import Chatbot

app = Flask(__name__)

API_KEY = "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"
chatbot = Chatbot(API_KEY)

conversation = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        source_prompt = request.form.get("source_prompt")
        user_message = ""

        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename != "":
                # Read the content of the uploaded file
                user_message = uploaded_file.read().decode("utf-8")
        else:
            user_message = request.form["user_message"]
        
        if source_prompt == "1":
            emotion_prompt = "Analiza las palabras que se utilizan en la entrevista y asignales una emoción. Entrega un párrafo con las distintas emociones que encontraste en el tono de la entrevista y muéstrame su descripción."
            response = chatbot.ask(emotion_prompt)
        elif source_prompt == "2":
            keywords_prompt = "Explica en un párrafo las palabras clave que le dan contexto a la entrevista, son palabras útiles que usa el vendedor para convencer al cliente."
            response = chatbot.ask(keywords_prompt)
        elif source_prompt == "3":
            tone_prompt = "Analiza el tono de la entrevista y entrega un párrafo con la descripción de este."
            response = chatbot.ask(tone_prompt)
        elif source_prompt == "4":
            meta_analysis_prompt = "Realiza un meta-análisis de la estructura y el flujo de la entrevista en un párrafo, es decir, la introducción y conceptos clave, el cuerpo de la entrevista y la conclusión. Indica en qué sección se mostró un mayor interés del cliente."
            response = chatbot.ask(meta_analysis_prompt)
        else:
            response = "Option not recognized."

        conversation.append(("User: " + user_message, "user"))
        conversation.append(("Chatbot: " + response, "Chatbot"))

    else:
        response = "Ask me something."

    return render_template("example2.html", conversation=conversation, response=response)

if __name__ == "__main__":
    app.run(debug=True)
































