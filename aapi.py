from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from src.utils import audio, video, subtitle
import os
import json

app = Flask(__name__)
api = Api(app)

class VideoGenerationAPI(Resource):
    """Handle video generation requests"""
    
    def post(self):
        """
        Generate video with subtitles
        
        Expected JSON payload:
        {
            "audio_file": "base64_encoded_audio",
            "style": {
                "font_family": "Arial",
                "font_size": 30,
                "text_color": "#ffffff",
                "highlight_color": "#4CAF50",
                "position": {"x": 50, "y": 50},
                "max_chars": 80,
                "max_lines": 2
            },
            "dimension": "16:9"
        }
        """
        try:
            # Get request data
            data = request.get_json()
            
            # Validate required fields
            if 'audio_file' not in data:
                return {
                    'status': 'error',
                    'message': 'Audio file is required'
                }, 400
                
            # Process audio file
            audio_data = data['audio_file']
            style = data.get('style', {})
            dimension = data.get('dimension', '16:9')
            
            # Save audio file
            temp_audio_path = os.path.join('temp', 'input_audio.mp3')
            with open(temp_audio_path, 'wb') as f:
                f.write(audio_data)
            
            # Generate video
            video_path = video.generate_video(
                audio_path=temp_audio_path,
                style=style,
                dimension=dimension
            )
            
            return {
                'status': 'success',
                'video_url': video_path
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500

class TranscriptionAPI(Resource):
    """Handle audio transcription requests"""
    
    def post(self):
        """
        Transcribe audio to text with timestamps
        
        Form data:
        - audio: Audio file
        - language: Language code (optional)
        """
        try:
            # Check if file was uploaded
            if 'audio' not in request.files:
                return {
                    'status': 'error',
                    'message': 'No audio file provided'
                }, 400
                
            audio_file = request.files['audio']
            language = request.form.get('language', 'en')
            
            # Save temporary file
            temp_path = os.path.join('temp', audio_file.filename)
            audio_file.save(temp_path)
            
            # Transcribe audio
            transcription = audio.transcribe(
                audio_path=temp_path,
                language=language
            )
            
            # Clean up
            os.remove(temp_path)
            
            return {
                'status': 'success',
                'transcription': transcription
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500

class SubtitleStyleAPI(Resource):
    """Handle subtitle style updates"""
    
    def post(self):
        """
        Update subtitle styling
        
        Expected JSON payload:
        {
            "font_family": "Arial",
            "font_size": 30,
            "text_color": "#ffffff",
            "highlight_color": "#4CAF50",
            "position": {"x": 50, "y": 50},
            "max_chars": 80,
            "max_lines": 2,
            "style_type": "word_highlight"
        }
        """
        try:
            style_data = request.get_json()
            
            # Validate style data
            required_fields = ['font_family', 'font_size', 'text_color']
            for field in required_fields:
                if field not in style_data:
                    return {
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }, 400
            
            # Update style
            updated_style = subtitle.update_style(style_data)
            
            return {
                'status': 'success',
                'style': updated_style
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500

class SubtitleTemplatesAPI(Resource):
    """Handle subtitle template operations"""
    
    def get(self):
        """Get all available subtitle templates"""
        try:
            templates = subtitle.get_templates()
            return {
                'status': 'success',
                'templates': templates
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500
    
    def post(self):
        """
        Save new subtitle template
        
        Expected JSON payload:
        {
            "name": "Template Name",
            "style": {
                // style parameters
            }
        }
        """
        try:
            template_data = request.get_json()
            
            if 'name' not in template_data or 'style' not in template_data:
                return {
                    'status': 'error',
                    'message': 'Template name and style are required'
                }, 400
                
            saved_template = subtitle.save_template(
                name=template_data['name'],
                style=template_data['style']
            )
            
            return {
                'status': 'success',
                'template': saved_template
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500

# Register API routes
api.add_resource(VideoGenerationAPI, '/api/generate-video')
api.add_resource(TranscriptionAPI, '/api/transcribe')
api.add_resource(SubtitleStyleAPI, '/api/subtitle-style')
api.add_resource(SubtitleTemplatesAPI, '/api/subtitle-templates')

if __name__ == '__main__':
    app.run(debug=True)
