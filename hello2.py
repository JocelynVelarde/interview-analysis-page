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
        user_message = ""

        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename != "":
                # Read the content of the uploaded file
                user_message = uploaded_file.read().decode("utf-8")
        else:
            user_message = request.form["user_message"]

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
