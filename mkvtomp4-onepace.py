import os
import sys
import zlib
import argparse
import shutil
import subprocess

def crc(fileName):
  prev = 0
  for eachLine in open(fileName,"rb"):
    prev = zlib.crc32(eachLine, prev)
  return "%X"%(prev & 0xFFFFFFFF)

# Argparse
parser = argparse.ArgumentParser(description='Convert an .mkv file to .mp4 losslessly.')
parser.add_argument('input', metavar='infile', type=str, help='Input path')
parser.add_argument('audio_track_index', type=int, default=1, help='Audio track index')
parser.add_argument('episode_num', metavar='episodenum', type=int, help='Episode number')
parser.add_argument('source', metavar='source', type=str, help='Raw source')
parser.add_argument('--dub', action='store_true', help='If is dub')
parser.add_argument('out_dir', metavar='dirout', type=str, help='Output dir')

args = parser.parse_args()
print(args)

# Vars
pwd = os.path.dirname(os.path.realpath(__file__))
tmp_output = os.path.join(pwd, 'tmp_ep.mp4')

mkvtomp4_command = ['python', os.path.join(pwd, 'mkvtomp4.py'), args.input, str(args.audio_track_index), tmp_output]
print(mkvtomp4_command)
subprocess.call(mkvtomp4_command)

print('Calculating checksum...')
crc32 = crc(tmp_output)
print(crc32)
d = '[dub]' if args.dub else ''
out_file = str(args.episode_num) + ' [' + args.source + ']' + d + '[' + crc32 + '].mp4'
out_path = os.path.join(args.out_dir, out_file)
print(out_path)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
shutil.move(tmp_output, out_path)
