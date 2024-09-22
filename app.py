from flask import Flask, request, jsonify
from google.cloud import speech
import os
import wave

# Set the environment variable for the service account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'esp32chatgpt.json'

app = Flask(__name__)

def transcribe_audio(file_path):
    """Transcribe the audio file using Google Speech-to-Text API."""
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ar-SA'
    )

    response = client.recognize(config=config, audio=audio)

    # Print the transcription results
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        
        

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the raw audio data from the request
        audio_data = request.data
        
        # Save the received audio data as a WAV file
        with open('received_audio.wav', 'wb') as f:
            f.write(audio_data)
            
        transcribe_audio('received_audio.wav')

        return jsonify({"message": "Audio received successfully"}), 200
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
