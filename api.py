import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from src.utils import audio, video, subtitle
from src.config import Config

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Load environment variables
load_dotenv()

# Create necessary directories
def create_directories():
    """Create necessary directories for storing outputs"""
    directories = ['output', 'temp', 'uploads']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Route for main page
@app.route('/')
def index():
    """Render the main subtitle editor page"""
    return render_template('subtitle_editor.html')

# Route for video generation
@app.route('/generate', methods=['POST'])
def generate_video():
    """
    Generate video with subtitles
    Workflow:
    1. Upload audio/video file
    2. Transcribe audio to text
    3. Generate video clips
    4. Add subtitles
    5. Combine everything
    """
    try:
        # Get file and parameters from request
        input_file = request.files['file']
        style = request.form.get('style', 'default')
        dimension = request.form.get('dimension', '16:9')
        
        # Process the file
        temp_path = os.path.join('uploads', input_file.filename)
        input_file.save(temp_path)
        
        # Convert to MP3 if needed
        audio_file = audio.convert_to_mp3(temp_path)
        
        # Transcribe audio
        transcription = audio.transcribe(audio_file)
        
        # Generate video
        video_path = video.generate_video(transcription, style, dimension)
        
        # Add subtitles
        final_video = subtitle.add_subtitles(video_path, transcription, style)
        
        return jsonify({
            'status': 'success',
            'video_url': final_video
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Route for transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file to text with timestamps"""
    try:
        audio_file = request.files['audio']
        result = audio.transcribe(audio_file)
        return jsonify({
            'status': 'success',
            'transcription': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Route for updating subtitle style
@app.route('/update-style', methods=['POST'])
def update_style():
    """Update subtitle styling parameters"""
    try:
        style_data = request.get_json()
        updated_style = subtitle.update_style(style_data)
        return jsonify({
            'status': 'success',
            'style': updated_style
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    create_directories()
    app.run(debug=True)
