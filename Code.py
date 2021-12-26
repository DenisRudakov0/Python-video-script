import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pymediainfo import MediaInfo
import random
from pydub import AudioSegment

def file_dir(url):
    content = os.listdir(url)
    return(content)

def media_info():
    media_info = MediaInfo.parse('C:/Users/Denis/Desktop/pythonvideo/my_concatenation.mp4')
    for track in media_info.tracks:
        #for k in track.to_data().keys():
        #    print("{}.{}={}".format(track.track_type,k,track.to_data()[k]))
        if track.track_type == 'Video':
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("{} width                 {}".format(track.track_type,track.to_data()["width"]))
            print("{} height                {}".format(track.track_type,track.to_data()["height"]))
            print("{} duration              {}s".format(track.track_type,track.to_data()["duration"]/1000.0))
            print("{} duration              {}".format(track.track_type,track.to_data()["other_duration"][3][0:8]))
            print("{} other_format          {}".format(track.track_type,track.to_data()["other_format"][0]))
            print("{} codec_id              {}".format(track.track_type,track.to_data()["codec_id"]))
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        elif track.track_type == 'Audio':
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("{} format                {}".format(track.track_type,track.to_data()["format"]))
            print("{} codec_id              {}".format(track.track_type,track.to_data()["codec_id"]))
            print("{} channel_s             {}".format(track.track_type,track.to_data()["channel_s"]))
            print("{} other_channel_s       {}".format(track.track_type,track.to_data()["other_channel_s"][0]))
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("********************************************************************")

def media_video(img, url):
    img = random.sample(img, len(img))
    list_time = {}
    for i in img:
        media_info = MediaInfo.parse(url + r'/' + i)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                list_time[i] = float("{}".format(track.to_data()["duration"]/1000.0))
    return list_time

def merge_video(list_time, url, save_dir):
    check_time = 0
    list_sum = []
    for i in list_time.items():
        if check_time < 3000:
            clip = VideoFileClip(url + r'/' + i[0])
            list_sum.append(clip)
            check_time += i[1]
        else:
            print(i)
            break
    final_clip = concatenate_videoclips(list_sum)
    final_clip.write_videofile(save_dir + r'/' + 'merge_video.mp4')
    print('Ok')

def merge_music(url, save_dir):
    content = os.listdir(url)
    content = random.sample(content, 2)
    list_sum = []
    for i in content:
        clip = AudioSegment.from_wav(url + r'/' + i)
        list_sum.append(clip)
        print(url + '/' + i)
    combined_sounds = sum(list_sum)
    # Требуется указание места для сохранения аудио
    combined_sounds.export(save_dir + r'/' + 'merge_music.wav', format="wav")
    print(content)

def merge_video_music(save_dir, fps=60):
    my_clip = VideoFileClip(save_dir + r'/' + 'merge_video.mp4')
    audio_background = AudioFileClip(save_dir + r'/' + 'merge_music.wav')
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(save_dir + r'/' + 'result.mp4', fps=fps)

url_video = input('Укажите папку с видеофрагментами (Пример: D:\\Video): ')
# r"C:\\Users\Denis\Desktop\pythonvideo\image1"
url_music = input('Укажите папку с аудиофрагментами (Пример: D:\\Video): ')
# r"C:\\Users\Denis\Desktop\new_music"
save_dir = input('Укажите папку для сохранения видео (Пример: D:\\Video): ')
# Result

# merge video
video = file_dir(url_video)
list_video = media_video(video, url_video)
merge_video(list_video, url_video, save_dir)

# merge music
merge_music(url_music, save_dir)
merge_video_music(save_dir)