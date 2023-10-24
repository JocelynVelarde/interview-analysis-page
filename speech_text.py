from flask import Flask, request, jsonify
from google.cloud import speech
from google.oauth2 import service_account

app = Flask(__name__)

# Function to transcribe audio
def transcribe_gcs(gcs_uri):
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

@app.route('/')
def index():
    return open('demo2.html').read()

@app.route('/transcribe', methods=['GET'])
def do_transcription():
    gcs_uri = "gs://audiofile01/audioTwo.wav"
    transcription = transcribe_gcs(gcs_uri)
    return jsonify({"transcription": transcription})

if __name__ == '__main__':
    app.run(debug=True)
