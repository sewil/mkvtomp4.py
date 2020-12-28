set /p episode_number="Episode number: "
set /p audio_track_index="Audio track (2 is usually jpn): "
set /p source="Raw source (df68, FUNi, etc.): "
set /p dir_out="Save directory: "
set /p is_dub="Is the audio track dub? (y/n): "

if "%is_dub%"=="y" (
  set dub_flag=--dub
)

python "%~dp0mkvtomp4-onepace.py" %1 %audio_track_index% %episode_number% %source% "%dir_out%" %dub_flag%
pause
