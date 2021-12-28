import os
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pymediainfo import MediaInfo
import random
from pydub import AudioSegment

def media_video(url):
    list_video = tuple(os.listdir(url))
    list_video = tuple(random.sample(list_video, len(list_video)))
    list_time = {}
    for i in list_video:
        media_info = MediaInfo.parse(url + r'/' + i)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                list_time[i] = (float("{}".format(track.to_data()["duration"]/1000.0)), 
                                    "{} x {}".format(track.to_data()["width"], track.to_data()["height"]))
    return list_time

def merge_video(list_time, url, save_dir):
    check_time = 0
    list_sum = []
    px = list(list_time.items())[0][1][1]
    for i in list_time.items():
        if check_time < 3000:
            clip = VideoFileClip(url + r'/' + i[0])
            if i[1][1] == px:
                list_sum.append(clip)
                check_time += i[1][0]
                print(i[0])
            else:
                print('Данный видео-файл пропущен, так как он не совпадает по расширению!: ', i[0])
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
list_video = media_video(url_video)
merge_video(list_video, url_video, save_dir)

# merge music
merge_music(url_music, save_dir)
merge_video_music(save_dir)