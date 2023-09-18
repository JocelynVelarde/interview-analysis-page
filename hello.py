from flask import Flask, render_template, request

# Import your Chatbot class and other dependencies here
from revChatGPT.V3 import Chatbot

# Create a Flask web application
app = Flask(__name__)

# Create a chatbot with your API key
API_KEY = "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"
chatbot = Chatbot(API_KEY)

# Initialize an empty conversation list
conversation = []

# Define a route to display the chat interface
@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["user_message"]
        # Add the user's message to the conversation
        conversation.append(("User: " + user_message, "user"))

        # Send the message to your chatbot logic and get the response
        response = chatbot.ask(user_message)

        # Add the chatbot's response to the conversation
        conversation.append(("Chatbot: " + response, "chatbot"))

    else:
        response = "Ask me something."

    return render_template("example2.html", conversation=conversation, response=response)

if __name__ == "__main__":
    app.run(debug=True)
