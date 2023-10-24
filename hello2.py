import json
from flask import Flask, render_template, jsonify, request
from revChatGPT.V3 import Chatbot
from auth import spreadsheet_service
from google.cloud import speech
from google.oauth2 import service_account

app = Flask(__name__)

chatbot = Chatbot("key")

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
                write_data_to_sheet(response)
                print(response)

    else:
        response = "Ask me something."

    return render_template("example22.html", conversation=conversation, response=response)

def write_data_to_sheet(texto):
    data = json.loads(texto)
    range_name = 'Sheet1!A2:R'  # Modifica esto para que abarque toda la columna donde deseas agregar datos.
    
    # Obten los datos actuales en la hoja de cálculo.
    result = spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    
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


@app.route('/transcribe', methods=['GET'])

def do_transcription():
    print("transcription route")
    gcs_uri = "gs://audiofile01/audioTwo.wav"
    transcription = transcribe_gcs(gcs_uri)
    return transcription

# Function to transcribe audio
def transcribe_gcs(gcs_uri):
    print("transcribe_gcs function")
    # Your transcription code here
    client_file = 'sa_speech_text.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding='LINEAR16',
        sample_rate_hertz=8000,
        language_code="es-MX",
        audio_channel_count=2,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript_builder.append(f"{result.alternatives[0].transcript}")
        #transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

    transcript = "".join(transcript_builder)
    print(transcript)

    return transcript


if __name__ == "__main__":
    app.run(debug=True)
