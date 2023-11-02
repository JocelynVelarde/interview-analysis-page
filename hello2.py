import json
import os
from flask import Flask, render_template, request
from revChatGPT.V3 import Chatbot
from auth import spreadsheet_service
import assemblyai as aai



app = Flask(__name__)

chatbot = Chatbot("")

spreadsheet_id = '1EyFOt8CQmxNi9lKRLWCnHIYUCf-mDjLFX6jrFjTPUO0'

conversation = []


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_prompt = request.form.get("user_prompt")
        uploaded_files = request.files.getlist("files")
        # user_message = ""

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
                write_data_to_sheet(response)
                print(response)

    else:
        response = "Ask me something."

    return render_template("example22.html", conversation=conversation, response=response)


def write_data_to_sheet(texto):
    data = json.loads(texto)
    # Modifica esto para que abarque toda la columna donde deseas agregar datos.
    range_name = 'Sheet1!A2:R'

    # Obten los datos actuales en la hoja de cálculo.
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()

    values = result.get('values', [])

    if not values:
        # Si no hay datos en la hoja de cálculo, agrega las llaves como la primera fila.
        values.append(list(data.keys()))

    # Agrega los nuevos datos al final de la lista.
    values.append(list(data.values()))

    # Actualiza la hoja de cálculo con los datos combinados.
    body = {
        'values': values
    }

    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))
    print(result)


@app.route('/transcribe', methods=['GET', 'POST'])
def do_transcription():
    # Replace with your API token
    
    transcript = ""  # Initialize transcript variable
    
    if request.method == 'POST':
        if 'audio_file' in request.files:
                audio_file = request.files['audio_file']
                file_path = os.path.join(os.getcwd(), audio_file.filename)
                audio_file.save(file_path)
                print(file_path)

                config = aai.TranscriptionConfig(language_code="es", speaker_labels=True)
                transcriber = aai.Transcriber(config=config)
                transcript = transcriber.transcribe(file_path)
                write_transcription(transcript.text)
                os.remove(file_path)
        else: 
            return render_template('error.html')
    #transcripcion mandarla a google sheet
    # Return the transcript
    return render_template('success.html', transcript=transcript.text)
   

def write_transcription(texto):
    spreadsheet_id = "1Vs-EdeZcPZ5Ozac1-_AZQ-l35rMffaZukoDlzEXhl2Y"
    range_name = 'Transcripción!A:A'

    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    
    values = result.get('values', [])
    next_row = len(values) + 1 

    body = {
        'range': f'Transcripción!A{next_row}',  
        'majorDimension': 'ROWS',
        'values': [
            [texto]  
        ]
    }

    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=f'Transcripción!A{next_row}',
        valueInputOption='USER_ENTERED', body=body).execute()

    print('New response written to row', next_row)
    print(result)

if __name__ == "__main__":
    app.run(debug=True)
