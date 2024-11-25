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

- 🎨 **Customization Options**
  - Font selection
  - Color schemes
  - Text size and position
  - Animation effects

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fxgurv/cool-video-generation.git
cd cool-video-generation
pip install -r requirements.txt
python main.py
