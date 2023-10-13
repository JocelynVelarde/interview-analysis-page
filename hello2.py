from flask import Flask, render_template, request
from revChatGPT.V3 import Chatbot
from config import API_KEY
from auth import spreadsheet_service

app = Flask(__name__)

chatbot = Chatbot("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")

spreadsheet_id = '1EyFOt8CQmxNi9lKRLWCnHIYUCf-mDjLFX6jrFjTPUO0' 

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
                write_json_to_sheet(response)
                print(response)

    else:
        response = "Ask me something."

    return render_template("example22.html", conversation=conversation, response=response)

def write_data_to_sheet(text):
    range_name = 'Sheet1!A2'  # Puedes especificar la celda donde deseas escribir el texto
    value_input_option = 'USER_ENTERED'
    body = {
        'values': [[text]]
    }
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('1 cell updated with text: {0}'.format(text))


def write_json_to_sheet(text):
    range_name = 'Sheet1!A2:R1'
    values = [list(text.keys()), list(text.values())]
    value_input_option = 'USER_ENTERED'
    body = {
        'values': values
    }
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == "__main__":
    app.run(debug=True)
