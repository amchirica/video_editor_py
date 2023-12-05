import functools
from PIL import Image
import moviepy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QFileDialog
from moviepy.audio.AudioClip import AudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips, transfx, concatenate
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.resize import  resize
from moviepy.audio.fx.volumex import volumex
from moviepy.video.fx.crop import crop
import moviepy.editor as mpe
import moviepy.editor as mpy

def cut_video(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name


def extract_audio(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_audio_name = video_name[: dot_index] + '_audio_{}_{}.mp3'.format(start_time, end_time)
    clip.audio.write_audiofile(cut_audio_name)
    return video_name


def rotate_video(video_name, start_time=0, end_time=None, degree=0):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip1 = clip.subclip(0, start_time)
    clip2 = rotate(clip.subclip(start_time, end_time), degree)
    clip3 = clip.subclip(end_time)
    final_clip = concatenate_videoclips([clip1, clip2, clip3])
    clip = final_clip

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("rotated") + video_name[dot_index:]
    
    # Specify the codec parameter (e.g., 'libx264')
    clip.write_videofile(cut_video_name, codec='libx264')
    return cut_video_name


def fade_in(video_name, duration=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    new_clip = clip.copy()
    clip = fadein(new_clip, duration)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("fade_in") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def fade_out(video_name, duration=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    new_clip = clip.copy()
    clip = fadeout(new_clip, duration)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("fade_out") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def add_text(video_name, text, fontsize, color, align, start_time=0, end_time=None):


    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    duration = end_time - start_time
    text1 = TextClip(text, color=color, fontsize=fontsize, method='caption', align=align)
    #text1 = text1.set_pos(align).set_duration(duration)
    text1 = text1.set_duration(duration)
    text1 = text1.set_pos('center')
    


    composition = CompositeVideoClip([clip, text1])

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("add_text") + video_name[dot_index:]
    composition.write_videofile(cut_video_name)
    return cut_video_name



def concatenate_video(video_name1, videoSamples, slide_out=False, start_time=0, end_time=None):
    videos = []

    if not slide_out:
        for v in videoSamples:
            clip = VideoFileClip(v)
            videos.append(clip)
        finalclip = concatenate_videoclips(videos)

    else:
        for v in videoSamples:
            clip = VideoFileClip(v)
            videos.append(clip)
        clips = videos
        slided_clips = (CompositeVideoClip([clip.fx(transfx.slide_out, 1, 'bottom')]) for clip in clips)
        slided_clips = (CompositeVideoClip([clip.fx(transfx.slide_in, 1, 'top')]) for clip in slided_clips)
        clips = []
        for v in slided_clips:
            clips.append(v)
        finalclip = concatenate_videoclips(clips)

    dot_index = video_name1.rfind('.')
    cut_video_name = video_name1[: dot_index] + '{}'.format("concatenated") + video_name1[dot_index:]
    finalclip.write_videofile(cut_video_name)
    return cut_video_name

def remove_piece_video(video_name, start_time=0, end_time=None):

    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip1 = clip.subclip(0, start_time)
    clip3 = clip.subclip(end_time)
    final_clip = concatenate_videoclips([clip1, clip3])
    clip = final_clip

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("remove_piece") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def add_photo(video_name, photo_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration + clip.duration

    logo = (ImageClip(photo_name))

    logo = logo.set_pos(("center", "center"))

    final = CompositeVideoClip([clip, logo.set_start(5).set_duration(3)])
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("add_photo") + video_name[dot_index:]
    final.write_videofile(cut_video_name)

    return cut_video_name

def change_speed(video_name, speed=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.set_fps(clip.fps * speed)
    final = clip.fx(speedx, speed)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("change_speed") + video_name[dot_index:]
    final.write_videofile(cut_video_name)
    return cut_video_name

def change_size(video_name,  ratioy=1, ratiox=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration
    clip = clip.resize(width=clip.w*ratioy, height=clip.h*ratiox)
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("change_size") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def remove_audio(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    newaudio = clip.audio.fx(volumex, 0)
    new_clip = clip.set_audio(newaudio)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("silent_video") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def concatenate_with_audio(video_name, audio_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    background_music = mpe.AudioFileClip(audio_name)
    new_clip = clip.set_audio(background_music)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("loud_video") + video_name[dot_index:]
    new_clip.write_videofile(cut_video_name, codec='libx264',
                     audio_codec='aac',
                     temp_audiofile='temp-audio.m4a',
                     remove_temp=True)
    return cut_video_name

def add_subclip(video_name1, video_name2, start_time=0, end_time=None):
    clip1 = VideoFileClip(video_name1)
    clip2 = VideoFileClip(video_name2)
    video = CompositeVideoClip([clip1,
                                clip2.set_position(("left", "bottom"))])

    dot_index = video_name1.rfind('.')
    cut_video_name = video_name1[: dot_index] + '{}'.format("add_subclip") + video_name1[dot_index:]
    video.write_videofile(cut_video_name, codec='libx264',
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True)
    return cut_video_name

def crop_clip(video_name, subwidth=1, subheight=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    widt = clip.w*subwidth
    heigh = clip.h*subheight
    clip = crop(clip, x1=((clip.w-widt)/2), y1=((clip.h-heigh)/2), x2=(clip.w - ((clip.w-widt)/2)), y2=(clip.h - ((clip.h-heigh)/2)))

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("crop_video") + video_name[dot_index:]
    clip.write_videofile(cut_video_name, codec='libx264',
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True)
    return cut_video_name

def brightness(video_name, subwidth=1, subheight=1, start_time=0, end_time=None, brightness_factor=1.0):
    if subwidth <= 1 or subheight <= 1:
        raise ValueError("Subwidth and subheight must be positive values.")
     
    clip = mpy.VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    subclip = clip.subclip(start_time, end_time)
    subclip = subclip.resize(width=subwidth * clip.w, height=subheight * clip.h)

    final_clip = subclip.fx(mpy.vfx.colorx, brightness_factor)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[:dot_index] + '{}'.format("_brightness") + video_name[dot_index:]
    final_clip.write_videofile(cut_video_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                               remove_temp=True)
    return cut_video_name


def contrast(video_name, subwidth=1, subheight=1, start_time=0, end_time=None, contrast_factor=1.0):
    clip = mpy.VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    subclip = clip.subclip(start_time, end_time)
    subclip = subclip.resize(width=subwidth * clip.w, height=subheight * clip.h)

    final_clip = subclip.fx(mpy.vfx.colorx, contrast_factor)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[:dot_index] + '{}'.format("_contrast") + video_name[dot_index:]
    final_clip.write_videofile(cut_video_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                               remove_temp=True)
    return cut_video_name
