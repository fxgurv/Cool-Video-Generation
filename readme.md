# Cool Video Generation 🎥

## What is This?
Cool Video Generation is an AI-powered tool that automatically creates engaging videos with synchronized subtitles and word-level highlighting. It combines audio transcription, video generation, and dynamic subtitle effects to create professional-looking content.

## Why Use This?
- Save hours of manual video editing time
- Create consistent, professional-looking videos
- Automatically generate subtitles with perfect timing
- Multiple video formats for different social media platforms
- Customizable subtitle styles and animations

## How It Works
1. **Audio Processing**
   - Upload your audio/video file
   - AI transcribes the audio using Whisper
   - Generates word-by-word timestamps

2. **Video Generation**
   - Automatically searches for relevant video clips based on content
   - Combines clips to match audio duration
   - Supports multiple aspect ratios (16:9, 9:16, 1:1)

3. **Subtitle Generation**
   - Creates synchronized subtitles
   - Word-level highlighting
   - Multiple subtitle styles
   - Customizable fonts, colors, and positions

## Features
- 🎙️ **Audio Transcription**
  - Supports multiple audio formats
  - Accurate word-level timing
  - Multiple language support

- 🎬 **Video Processing**
  - Auto clip selection
  - Smooth transitions
  - Background music integration
  - Multiple aspect ratios

- 📝 **Subtitle Styles**
  - Word highlighting
  - Background highlighting
  - Word-by-word animation
  - Custom positioning

 Word Highlight Subtitles:

Each word is highlighted individually as it is spoken
Words appear in normal color (default: white) and get highlighted in an accent color (default: #4CAF50 green) when spoken
Words are positioned dynamically with proper line breaks
Example: "This is a" (white) "sample" (green) "text" (white)






Background Highlight Subtitles:

Similar to word highlighting but instead of changing text color, it adds a background color behind each word
Words appear with a transparent background initially
When a word is spoken, its background gets highlighted with the chosen color
Example: "This is a" (no background) "sample" (green background) "text" (no background)
Simple Line-Level Subtitles
Traditional subtitle style where full lines of text appear
Supports customization of:
Font family (Arial, Helvetica, Times New Roman, etc.)
Font size
Text color
Position on screen
Maximum characters per line (default: 80)
Maximum number of lines (default: 2)
Stroke/outline color and width
Key Features for All Subtitle Types:

Customizable styling through the UI
Draggable positioning on screen
Support for different video dimensions (16:9, 9:16, 1:1)
Automatic line breaking based on maximum characters
Synchronized with audio using timestamp data from Whisper transcription
Support for template saving and loading
The subtitles are implemented in the subtitle.py utility file and can be previewed/customized through the subtitle_editor.html interface before being applied to videos.

1. WORD HIGHLIGHT SUBTITLES ✨
python
Copy code
Style Type: word_highlight
Default Configuration:
{
    "font": "Helvetica-Bold",
    "fontsize": 30,
    "color": "white",
    "highlight_color": "#4CAF50",
    "stroke_width": 1.5,
    "stroke_color": "black"
}
Technical Implementation:

Creates two TextClips for each word:
Base clip: Normal state (white)
Highlight clip: Active state (green)
Dynamic positioning system:
X_buffer = frame_width * 0.1
Y_buffer = frame_height * 0.2
Word spacing = fontsize * 0.3
Automatic line breaks when x_pos + word_width > frame_width
Vertical spacing = fontsize + 10px between lines
Animation Flow:

Words appear in default white color
Each word highlights in green during its spoken duration
Returns to white after word completion
Smooth transition effects between states
2. BACKGROUND HIGHLIGHT SUBTITLES 🎯
python
Copy code
Style Type: background_highlight
Default Configuration:
{
    "font": "Helvetica-Bold",
    "fontsize": 30,
    "color": "white",
    "bg_color": "black",
    "highlight_color": "#4CAF50"
}
Technical Implementation:

Single TextClip per word with background property
Background transitions:
Initial: Transparent/Black
Active: Highlight color (#4CAF50)
Positioning system matches word_highlight
Maintains consistent word spacing
Background padding for visual clarity
Animation Flow:

Words appear with black/transparent background
Background fills with highlight color during word timing
Returns to transparent after completion
Clean transitions between states
Common Features for Both Styles 🛠️
Text Handling:

python
Copy code
Max Characters: 80 per line
Max Lines: 2
Word Spacing: 0.3 × font size
Line Spacing: font size + 10px
Customization Options:

python
Copy code
Font Properties:
- Family: Any system font
- Size: Adjustable (default 30px)
- Weight: Bold/Normal
- Color: Any hex/RGB value

Position Controls:
- Draggable interface
- X/Y coordinate system
- Percentage-based positioning
- Frame-aware boundaries
Video Support:

python
Copy code
Aspect Ratios:
- Landscape (16:9)
- Portrait (9:16)
- Square (1:1)

Frame Adaptation:
- Auto-scaling
- Responsive positioning
- Edge padding (10% of frame)
Performance Features:

python
Copy code
- GPU acceleration support
- Efficient clip composition
- Memory-optimized rendering
- Real-time preview capability

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fxgurv/cool-video-generation.git
cd cool-video-generation
pip install -r requirements.txt
python main.py
