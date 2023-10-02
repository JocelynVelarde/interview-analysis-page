from flask import Flask, render_template, request
from revChatGPT.V3 import Chatbot
from config import API_KEY

app = Flask(__name__)

chatbot = Chatbot("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")

conversation = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_prompt = request.form.get("user_prompt")
        uploaded_files = request.files.getlist("files")
        #user_message = ""

        for uploaded_file in uploaded_files:
            if uploaded_file.filename != "":
                user_message = uploaded_file.read().decode("utf-8")

                # Combine the user's custom prompt and the uploaded text file for analysis
                combined_prompt = user_prompt + " " + user_message
                
                # Use ChatGPT to analyze the combined prompt and text file
                response = chatbot.ask(combined_prompt)

                conversation.append((user_prompt, "User Prompt"))
                conversation.append((user_message, "Uploaded Text"))
                conversation.append((response, "Response"))

    else:
        response = "Ask me something."

    return render_template("example22.html", conversation=conversation, response=response)


if __name__ == "__main__":
    app.run(debug=True)
