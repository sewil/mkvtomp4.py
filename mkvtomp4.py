import os
import sys
import shutil
import json

# Functions
def mkvextract(mkv_path, audio_track_index, video_path, audio_path):
  mkvextract_path = os.path.join(pwd, 'Tools', 'mkvextract', 'mkvextract')
  print(mkvextract_path)
  mkvextract_call = mkvextract_path + ' tracks "' + mkv_path + '" 0:"' + video_path + '" ' + str(audio_track_index) + ':"' + audio_path + '"'
  print(mkvextract_call)
  os.system(mkvextract_call)

def get_mediainfo(mkv_path):
  mediainfo_path = os.path.join(pwd, 'Tools', 'MediaInfo', 'x64', 'MediaInfo')
  print(mediainfo_path)
  mediainfo_command = mediainfo_path + ' --Full --Output=JSON "' + mkv_path + '"'
  print(mediainfo_command)
  info = json.loads(os.popen(mediainfo_command).read())
  return info

def delay_audio(delay, audio_path, audio_2_path):
  eac3to_path = os.path.join(pwd, "Tools", "eac3to", "eac3to")
  print(eac3to_path)
  eac3to_call = eac3to_path + ' "' + audio_path + '" "' + audio_2_path + '" ' + delay + ' -progressnumbers'
  print(eac3to_call)
  os.system(eac3to_call)

def convert_audio(audio_out_path, audio_2_path):
  azid_path = os.path.join(pwd, 'Tools', 'Azid', 'azid')
  print(azid_path)
  wav_path = os.path.join(pwd, 'tmp', 'audio.wav')
  print(wav_path)
  azid_command = azid_path + ' -d 3/2 -l 1.0 -L 0.0 -o L,R,C,LFE,SL,SR -a -n true "' + audio_2_path + '" "' + wav_path + '"'
  print(azid_command)
  os.system(azid_command)

  qaac_path = os.path.join(pwd, 'Tools', 'qaac', 'qaac')
  print(qaac_path)
  qaac_command = qaac_path + ' --quality 2 --ignorelength --tvbr 95 "' + wav_path + '" -o "' + audio_out_path + '"'
  print(qaac_command)
  os.system(qaac_command)

def mp4box(video_path, audio_out_path, framerate, out_path):
  mp4box_path = os.path.join(pwd, 'Tools', 'mp4box', 'x64', 'MP4Box.exe')
  mp4box_command = mp4box_path + ' -add "' + video_path + '":fps=' + framerate + ' -add "' + audio_out_path + '":fps=' + framerate + ' "' + out_path + '"'
  print(mp4box_command)
  os.system(mp4box_command)
  return

if (len(sys.argv) < 3):
  print('Usage: python mkvtomp4.py <input> <audio track number> <output>')
  exit(1)

# Vars
pwd = os.path.dirname(os.path.realpath(__file__))
print(pwd)

audio_track_index = int(sys.argv[2])

out_path = sys.argv[3]
print(out_path)

mkv_path = sys.argv[1]
info = get_mediainfo(mkv_path)

video_track = info['media']['track'][0]
framerate = video_track['FrameRate']
print(framerate)

audio_track = info['media']['track'][audio_track_index + 1]
audio_format = audio_track['Format']
print(audio_format)

audio_extension = '.ac3' if audio_format == 'AC-3' else '.aac'
print(audio_extension)

video_path = os.path.join(pwd, "tmp", "video.h264")
print(video_path)
audio_path = os.path.join(pwd, "tmp", "audio" + audio_extension)
print(audio_path)

audio_2_path = os.path.join(pwd, "tmp", "audio_delayed" + audio_extension)
print(audio_2_path)

video_delay = int(float(audio_track['Video_Delay'])*1000)
video_delay_s = ('+' + str(video_delay) if video_delay > 0 else str(video_delay)) + 'ms'
print(video_delay_s)

audio_out_path = os.path.join(pwd, "tmp", "audio" + ('.m4a' if audio_format == 'AC-3' else '.aac'))
print(audio_out_path)

# Run
mkvextract(mkv_path, audio_track_index, video_path, audio_path)
delay_audio(video_delay_s, audio_path, audio_2_path)

if audio_format == 'AC-3':
  convert_audio(audio_out_path, audio_2_path)

mp4box(video_path, audio_out_path, framerate, out_path)

shutil.rmtree(os.path.join(pwd, 'tmp'))
