import os
directory_path = "output"

if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created successfully.")
else:
    print(f"Directory '{directory_path}' already exists.")

!pip install g4f
!pip install --quiet ipython-autotime
!pip install ffmpeg-python==0.2.0
!pip install pysrt==1.1.2
!pip install git+https://github.com/openai/whisper.git
!apt install imagemagick

cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml



import os
from google.colab import userdata
os.environ["PEXELS_API_KEY"] = userdata.get('PEXELS_API_KEY')


import whisper
import json
import os
from moviepy.editor import AudioFileClip, VideoFileClip

def convert_to_mp3(input_file):
    """Convert input audio/video to MP3 format if not already in MP3 format."""
    if not input_file.endswith(".mp3"):
        filename, ext = os.path.splitext(input_file)
        mp3_filename = f"{filename}.mp3"
        if ext in [".wav", ".flac", ".m4a"]:
            # Use moviepy to convert audio files
            clip = AudioFileClip(input_file)
            clip.write_audiofile(mp3_filename)
        else:
            # Use moviepy to extract audio from video files
            clip = VideoFileClip(input_file)
            audio = clip.audio
            audio.write_audiofile(mp3_filename)
        input_file = mp3_filename
    return input_file

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def split_text_into_lines(data):
    MaxChars = 80
    MaxDuration = 3.0
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0

    for idx, word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start
        temp = " ".join(item["word"] for item in line)
        new_line_chars = len(temp)
        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx > 0:
            gap = word_data['start'] - data[idx - 1]['end']
            maxgap_exceeded = gap > MaxGap
        else:
            maxgap_exceeded = False

        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0

    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)
    return subtitles

# Load the Whisper model
model = whisper.load_model("base")

# Get the input file and convert to MP3 if needed
INPUT = "/content/Intro.mp4"  #@param {type:"string"}
audio_file = convert_to_mp3(INPUT)

# Transcribe the audio file
result = model.transcribe(audio_file, word_timestamps=True)

# Word-by-word timestamps
wordlevel_info = []
srt_word_lines = []
counter = 1

for each in result['segments']:
    words = each['words']
    for word in words:
        wordlevel_info.append({'word': word['word'].strip(), 'start': word['start'], 'end': word['end']})
        srt_word_lines.append(f"{counter}\n{format_time(word['start'])} --> {format_time(word['end'])}\n{word['word']}\n\n")
        counter += 1

# Save word-by-word timestamps in JSON format
filename_without_ext = os.path.splitext(INPUT)[0]
json_filename = "WORD_BY_WORD.json"
with open(json_filename, 'w') as f:
    json.dump(wordlevel_info, f, indent=4)

# Save word-by-word timestamps in SRT format
srt_filename = "WORD_BY_WORD.srt"
with open(srt_filename, 'w') as f:
    f.writelines(srt_word_lines)

# Line-level timestamps in JSON and SRT format
linelevel_subtitles = split_text_into_lines(wordlevel_info)
srt_line_lines = []
counter = 1

for line in linelevel_subtitles:
    srt_line_lines.append(f"{counter}\n{format_time(line['start'])} --> {format_time(line['end'])}\n{line['word']}\n\n")
    counter += 1

# Save line-level timestamps in JSON format
json_filename = "WORD_HIGHLIGHT.json"
with open(json_filename, 'w') as f:
    json.dump(linelevel_subtitles, f, indent=4)

# Save line-level timestamps in SRT format
srt_filename = "WORD_HIGHLIGHT.srt"
with open(srt_filename, 'w') as f:
    f.writelines(srt_line_lines)

# Get the duration of the audio file
audio = AudioFileClip(audio_file)
duration_in_seconds = round(audio.duration)
# Print the name of the audio file and its duration
print(f"Audio File: {os.path.basename(audio_file)} | Duration: {duration_in_seconds}s")

import pysrt
import string

subs = pysrt.open('/content/WORD_HIGHLIGHT.srt')
for sub in subs:
    sub.text = sub.text.translate(str.maketrans("", "", string.punctuation))
    if len(sub.text) > 20:
        words = sub.text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) <= 30:
                current_line += word.title() + " "
            else:
                lines.append(current_line.strip())
                current_line = word.title() + " "
        if current_line:
            lines.append(current_line.strip())
        sub.text = "\n".join(lines)
    else:
        sub.text = sub.text.title()
subs.save("/content/CLIP_TITLES.srt")

from g4f.client import Client

client = Client()
template = """Imagine you're a highly imaginative artist with the unique ability to map the subjects
in a given SRT caption to a one word real-world objects and scenes.
It's important to keep the titles exactly one word, and title must be a real word object or scenes
That human can vision, avoid providing theoretical titles like: Paradox, Chrysalis, Journey, Reality, Accomplishment
Instead use real world titles that can be seen by human eyes like Mansion, Yoga, Car, Money.
Give me exactly {num_clips} distinct clip titles.
Each title should seamlessly flow into the next, creating a captivating narrative,
and each title will be precisely 5 seconds long.
I want you to understand and imagine the big picture of the video and give me titles that matches
The entire video, not just individual scenes.

Get inspired by the SRT caption provided:

{srt_caption}

Output Instruction:
Provide only the titles. Each title must be separated by a new line,
do not mention numbers in titles and titles must be URL-encoded friendly.
Example Output:
Yoga
Forest
Office
Jogging
Sunset
Cafe
Hiking
Spa
Beach
Tea
Luxury
Money
"""

# Calculate the number of clips
duration_in_seconds = 60  # Example duration, replace with actual duration
num_clips = (duration_in_seconds // 5) + 1

# Read the SRT caption from the file
with open("/content/CLIP_TITLES.srt", "r") as f:
    srt_caption = f.read()

# Format the template with the actual values
formatted_template = template.format(num_clips=num_clips, srt_caption=srt_caption)

# Send the formatted template to the AI model
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": formatted_template}],
)

# Process the response
clips_titles = response.choices[0].message.content.strip().split("\n")
print(clips_titles)

import os
import random
import requests
from collections import Counter
from google.colab import userdata
from moviepy.editor import AudioFileClip

os.environ["PEXELS_API_KEY"] = userdata.get('PEXELS_API_KEY')
DIMENSION = "Landscape (Youtube 16:9)" # @param ["Landscape (Youtube 16:9)", "Portrait  (Tiktok 9:16)", "Square (Instagram 10:10)"]

clip_counter = Counter(clips_titles)
clips_paths = []
selected_videos = set()
for title, count in clip_counter.items():
    headers = {
        "Authorization": os.environ["PEXELS_API_KEY"],
    }

    # Adjust orientation based on DIMENSION
    if DIMENSION == "Landscape (Youtube 16:9)":
        orientation = "landscape"
    elif DIMENSION == "Portrait (Tiktok 9:16)":
        orientation = "portrait"
    elif DIMENSION == "Square (Instagram 10:10)":
        orientation = "square"
    else:
        orientation = "landscape"  # Default to landscape if DIMENSION is not recognized

    url = f"https://api.pexels.com/videos/search?query={title}&per_page=15&orientation={orientation}&size=medium"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        videos = response.json()["videos"]
        for i in range(count):
            available_videos = [
                video
                for video in videos
                if video["video_files"][0]["link"] not in selected_videos
            ]
            if not available_videos:
                print(f"No more available videos for title '{title}'.")
                break

            video = random.choice(available_videos)
            video_url = video["video_files"][0]["link"]
            temp_name = f"{title}_{i}.mp4"
            video_path = os.path.join("output", temp_name)
            with open(video_path, "wb") as video_file:
                video_file.write(requests.get(video_url).content)
            clips_paths.append(video_path)
            selected_videos.add(video_url)
    else:
        print(
            f"Failed to fetch videos for title '{title}'. Status code: {response.status_code}"
        )

# Ensure that clips_paths has num_clips elements
for i in range(num_clips - len(clips_paths)):
    clips_paths.append(clips_paths[0])

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.fx.all import resize


def resize_clip(input_video_path, duration=5, new_dimensions = (1920, 1080)):
    video_clip = VideoFileClip(input_video_path)
    total_duration = video_clip.duration
    start_time = (total_duration - duration) / 2
    end_time = start_time + duration
    video_clip = video_clip.subclip(start_time, end_time)

    video_clip = resize(video_clip, new_dimensions)
    return video_clip


clips = [resize_clip(cp) for cp in clips_paths]
clips

from moviepy.editor import VideoFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx.all import volumex

voice_audio = AudioFileClip("/content/Intro.mp3").fx(volumex, 3)
music_path = ""  # Replace with the actual path of the music file if provided
if music_path:  # Check if music file path is provided
    music_audio = AudioFileClip(music_path).fx(volumex, 0.5)
    t_start = int(music_audio.duration // 2 - duration_in_seconds // 2)
    music_audio = music_audio.subclip(t_start, duration_in_seconds + t_start)
    audio = CompositeAudioClip([voice_audio, music_audio])
else:
    audio = voice_audio
final_clip = concatenate_videoclips(clips, method="compose").subclip(0, duration_in_seconds)
final_clip = final_clip.set_audio(audio)
final_clip.write_videofile("output/composite_video.mp4", codec="libx264",
                           audio_codec="aac", fps=24)

"""## Step7: Use Moviepy to create an audiogram with word-level highlights as they are spoken"""

import os
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip

VIDEO = "Composite_video"  # @param ["Composite_video", "input_Video", "Audiogram"]
SUBTITLE = "WORD_HIGHLIGHT"  # @param ["WORD_HIGHLIGHT", "WORD-BY-WORD", "Simple"]

def create_caption(textJSON, framesize, font='Helvetica-Bold', fontsize=30, color='white', bgcolor='blue'):
    wordcount = len(textJSON['textcontents'])
    full_duration = textJSON['end'] - textJSON['start']

    word_clips = []
    xy_textclips_positions = []

    x_pos = 0
    y_pos = 0
    frame_width = framesize[0]
    frame_height = framesize[1]
    x_buffer = frame_width * 1 / 10
    y_buffer = frame_height * 1 / 5

    space_width = ""
    space_height = ""

    for index, wordJSON in enumerate(textJSON['textcontents']):
        duration = wordJSON['end'] - wordJSON['start']
        word_clip = TextClip(wordJSON['word'], font=font, fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
        word_clip_space = TextClip(" ", font=font, fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
        word_width, word_height = word_clip.size
        space_width, space_height = word_clip_space.size
        if x_pos + word_width + space_width > frame_width - 2 * x_buffer:
            # Move to the next line
            x_pos = 0
            y_pos = y_pos + word_height + 50

            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos": x_pos + x_buffer,
                "y_pos": y_pos + y_buffer,
                "width": word_width,
                "height": word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos + x_buffer, y_pos + y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos + word_width + x_buffer, y_pos + y_buffer))
            x_pos = word_width + space_width
        else:
            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos": x_pos + x_buffer,
                "y_pos": y_pos + y_buffer,
                "width": word_width,
                "height": word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos + x_buffer, y_pos + y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos + word_width + x_buffer, y_pos + y_buffer))

            x_pos = x_pos + word_width + space_width

        word_clips.append(word_clip)
        word_clips.append(word_clip_space)

    for highlight_word in xy_textclips_positions:
        word_clip_highlight = TextClip(highlight_word['word'], font=font, fontsize=fontsize, color=color, bg_color=bgcolor).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
        word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
        word_clips.append(word_clip_highlight)

    return word_clips

# Load the line-level subtitles
with open("/content/WORD_HIGHLIGHT.json", "r") as f:
    linelevel_subtitles = json.load(f)

# Define the video filename
videofilename = "/content/output/composite_video.mp4"

# Set the frame size based on the desired dimension
if SUBTITLE == "Simple" and VIDEO == "input_Video":
    frame_size = (1920, 1080)  # 16:9 aspect ratio
else:
    frame_size = (1080, 1080)  # Square aspect ratio

# Create word highlight clips
all_linelevel_splits = []
for line in linelevel_subtitles:
    out = create_caption(line, frame_size)
    all_linelevel_splits.extend(out)

# Handle the final video based on the user's choice
if VIDEO == "Composite_video":
    # Load the composite video
    input_video = VideoFileClip("output/composite_video.mp4")
elif VIDEO == "input_Video":
    # Load the input video
    input_video = VideoFileClip(videofilename)
else:
    # Create a black video
    input_video_duration = linelevel_subtitles[-1]['end']
    input_video = ColorClip(size=frame_size, color=(0, 0, 0)).set_duration(input_video_duration)

# Get the duration of the input video
input_video_duration = input_video.duration

# Create the final video with subtitles
final_video = CompositeVideoClip([input_video] + all_linelevel_splits)
final_video = final_video.set_audio(input_video.audio)

# Handle the subtitle choice
if SUBTITLE == "WORD_HIGHLIGHT":
    # Word highlight subtitles are already included in final_video
    pass
elif SUBTITLE == "WORD-BY-WORD":
    # Add word-by-word subtitles
    generator = lambda txt: TextClip(txt, font="Nimbus-Sans-Bold", fontsize=36, color='white', size=(final_video.w, final_video.h), stroke_color='black', stroke_width=1.5)
    subtitles = SubtitlesClip("/content/input_video_line_timestamps.json", generator)
    final_video = CompositeVideoClip([final_video, subtitles.set_position(('center'))])
else:
    # Add line-level subtitles
    generator = lambda txt: TextClip(txt, font="Nimbus-Sans-Bold", fontsize=36, color='white', size=(final_video.w, final_video.h), stroke_color='black', stroke_width=1.5)
    subtitles = SubtitlesClip("/content/Intro_line_timestamps.srt", generator)
    final_video = CompositeVideoClip([final_video, subtitles.set_position(('center'))])

# Add a watermark
watermark_clip = TextClip("@Enterprisium", font="Nimbus-Sans-Bold", fontsize=24, color='white', size=(640, 480)).set_duration(final_video.duration)
final_video = CompositeVideoClip([final_video, watermark_clip.set_position(('center', 'bottom'))])

# Save the final video
final_video.write_videofile("output/out.mp4", fps=24, codec="libx264", audio_codec="aac")
