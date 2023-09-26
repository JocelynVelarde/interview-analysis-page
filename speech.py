from google.cloud import speech

client = speech.SpeechClient.from_service_account_file('key.json')

file_name = 'audio.mp3'

with open(file_name, 'rb') as file:
    content = file.read()

audio_file = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    sample_rate_hertz=8000,
    language_code='en-US',
    enable_automatic_punctuation=True,
    model='phone_call'
)

operation = client.long_running_recognize(config=config, audio=audio_file)

print(operation)




