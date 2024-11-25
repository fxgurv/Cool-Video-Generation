import os
import json
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

class SubtitleGenerator:
    def __init__(self):
        self.default_style = {
            "font": "Helvetica-Bold",
            "fontsize": 30,
            "color": "white",
            "stroke_color": "black",
            "stroke_width": 1.5,
            "highlight_color": "#4CAF50",
            "bg_color": "black",
            "position": ("center", "bottom"),
            "max_chars": 80,
            "max_lines": 2
        }
        
    def create_word_highlight(self, text_json, video_size, style=None):
        """Create word-by-word highlight effect"""
        if style is None:
            style = self.default_style
            
        word_clips = []
        x_pos = 0
        y_pos = 0
        
        frame_width = video_size[0]
        frame_height = video_size[1]
        x_buffer = frame_width * 0.1
        y_buffer = frame_height * 0.2
        
        for word_data in text_json["textcontents"]:
            # Create normal word clip
            word_clip = TextClip(
                word_data["word"],
                font=style["font"],
                fontsize=style["fontsize"],
                color=style["color"]
            ).set_start(text_json["start"]).set_duration(text_json["end"] - text_json["start"])
            
            # Create highlighted word clip
            highlight_clip = TextClip(
                word_data["word"],
                font=style["font"],
                fontsize=style["fontsize"],
                color=style["highlight_color"]
            ).set_start(word_data["start"]).set_duration(word_data["end"] - word_data["start"])
            
            # Handle word positioning and line breaks
            word_width = word_clip.size[0]
            if x_pos + word_width > frame_width - 2 * x_buffer:
                x_pos = 0
                y_pos += style["fontsize"] + 10
                
            word_clip = word_clip.set_position((x_pos + x_buffer, y_pos + y_buffer))
            highlight_clip = highlight_clip.set_position((x_pos + x_buffer, y_pos + y_buffer))
            
            word_clips.extend([word_clip, highlight_clip])
            x_pos += word_width + style["fontsize"] * 0.3
            
        return word_clips
        
    def create_background_highlight(self, text_json, video_size, style=None):
        """Create background highlight effect"""
        if style is None:
            style = self.default_style
            
        word_clips = []
        
        for word_data in text_json["textcontents"]:
            # Create word clip with background
            word_clip = TextClip(
                word_data["word"],
                font=style["font"],
                fontsize=style["fontsize"],
                color=style["color"],
                bg_color=style["bg_color"]
            ).set_start(word_data["start"]).set_duration(word_data["end"] - word_data["start"])
            
            word_clips.append(word_clip)
            
        return word_clips
        
    def add_subtitles(self, video_path, transcription, style=None):
        """Add subtitles to video"""
        try:
            if style is None:
                style = self.default_style
                
            # Load video
            video = VideoFileClip(video_path)
            
            # Create subtitle clips based on style
            if style.get("type") == "word_highlight":
                subtitle_clips = self.create_word_highlight(transcription, video.size, style)
            elif style.get("type") == "background_highlight":
                subtitle_clips = self.create_background_highlight(transcription, video.size, style)
            else:
                # Default simple subtitles
                generator = lambda txt: TextClip(
                    txt,
                    font=style["font"],
                    fontsize=style["fontsize"],
                    color=style["color"],
                    stroke_color=style["stroke_color"],
                    stroke_width=style["stroke_width"]
                )
                subtitles = SubtitlesClip(transcription, generator)
                subtitle_clips = [subtitles.set_position(style["position"])]
                
            # Combine video with subtitles
            final_video = CompositeVideoClip([video] + subtitle_clips)
            
            # Save output
            output_path = os.path.join("output", "subtitled_video.mp4")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac"
            )
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to add subtitles: {str(e)}")
            
    def update_style(self, style_data):
        """Update subtitle style parameters"""
        try:
            # Validate and merge with default style
            updated_style = self.default_style.copy()
            updated_style.update(style_data)
            
            # Save style to file
            style_path = os.path.join("config", "subtitle_style.json")
            with open(style_path, "w") as f:
                json.dump(updated_style, f, indent=4)
                
            return updated_style
            
        except Exception as e:
            raise Exception(f"Failed to update style: {str(e)}")
            
    def get_templates(self):
        """Get available subtitle templates"""
        try:
            templates_path = os.path.join("config", "subtitle_templates.json")
            if os.path.exists(templates_path):
                with open(templates_path, "r") as f:
                    return json.load(f)
            return []
            
        except Exception as e:
            raise Exception(f"Failed to get templates: {str(e)}")
            
    def save_template(self, name, style):
        """Save subtitle template"""
        try:
            templates = self.get_templates()
            templates.append({
                "name": name,
                "style": style
            })
            
            templates_path = os.path.join("config", "subtitle_templates.json")
            with open(templates_path, "w") as f:
                json.dump(templates, f, indent=4)
                
            return templates[-1]
            
        except Exception as e:
            raise Exception(f"Failed to save template: {str(e)}")

# Create singleton instance
subtitle_generator = SubtitleGenerator()

# Export functions
def add_subtitles(video_path, transcription, style=None):
    return subtitle_generator.add_subtitles(video_path, transcription, style)
    
def update_style(style_data):
    return subtitle_generator.update_style(style_data)
    
def get_templates():
    return subtitle_generator.get_templates()
    
def save_template(name, style):
    return subtitle_generator.save_template(name, style)
