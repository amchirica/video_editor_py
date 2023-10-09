from PyQt5.QtCore import QThread, pyqtSignal
from VideoCut import cut_video, extract_audio, rotate_video, fade_in, fade_out, add_text, concatenate_video, \
    change_speed, remove_piece_video, add_photo, change_size, remove_audio, concatenate_with_audio, add_subclip, \
    crop_clip, brightness, contrast


class Thread(QThread):
    MSG_CUT_VIDEO = 1
    MSG_EXTRACT_AUDIO = 2
    MSG_ROTATE_VIDEO = 3
    MSG_FADE_IN_VIDEO = 4
    MSG_FADE_OUT_VIDEO = 5
    MSG_ADD_TEXT_VIDEO = 6
    MSG_CONCATENATE_VIDEO = 7
    MSG_REMOVE_PIECE_VIDEO = 8
    MSG_ADD_PHOTO_VIDEO = 9
    MSG_CHANGE_SPEED_VIDEO = 10
    MSG_RATIO_VIDEO = 11
    MSG_REMOVE_AUDIO_VIDEO = 12
    MSG_CONCATENATE_AUDIO_VIDEO = 13
    MSG_ADD_VIDEO_VIDEO = 14
    MSG_CROP_VIDEO = 15
    MSG_BRIGHTNESS_VIDEO = 16
    MSG_CONTRAST_VIDEO = 17


    signal_return_value = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def set_params(self, msg, video_name, start_time, end_time, rotate_degree=0, duration=0,
                   text="", fontsize=30, color="black", align="center", x=20, y=190, video_name2=None,
                   photo_name=None, speed=1, ratiox=1, ratioy=1, slide_out=False, audio_name=None,
                   subwidth=1, subheight=1, videoSamples=None):
        self.videoSamples = videoSamples
        self.subwidth = subwidth
        self.subheight = subheight
        self.audio_name = audio_name
        self.slide_out = slide_out
        self.ratiox = ratiox
        self.ratioy = ratioy
        self.speed = speed
        self.photo_name = photo_name
        self.video_name2 = video_name2
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.align = align
        self.x = x
        self.y = y
        self.msg = msg
        self.video_name = video_name
        self.start_time = start_time
        self.end_time = end_time
        self.rotate_degree = int(rotate_degree)
        self.duration = int(duration)

    def run(self):
        global subclip_name
        if self.msg == Thread.MSG_CUT_VIDEO:
            if self.rotate_degree == 0:
                subclip_name = cut_video(self.video_name, self.start_time, self.end_time)
            else:
                subclip_name = rotate_video(self.video_name, self.start_time, self.end_time, self.rotate_degree)
        elif self.msg == Thread.MSG_ROTATE_VIDEO:
            subclip_name = rotate_video(self.video_name, self.start_time, self.end_time, self.rotate_degree)
        elif self.msg == Thread.MSG_FADE_IN_VIDEO:
            subclip_name = fade_in(self.video_name, self.duration, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_FADE_OUT_VIDEO:
            subclip_name = fade_out(self.video_name, self.duration, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_EXTRACT_AUDIO:
            subclip_name = extract_audio(self.video_name, self.start_time, self.end_time)


        elif self.msg == Thread.MSG_ADD_TEXT_VIDEO:
            subclip_name = add_text(self.video_name, self.text, self.fontsize, self.color, self.align, self.start_time, self.end_time)


        elif self.msg == Thread.MSG_CONCATENATE_VIDEO:
            subclip_name = concatenate_video(self.video_name, self.videoSamples, self.slide_out)
        elif self.msg == Thread.MSG_REMOVE_PIECE_VIDEO:
            subclip_name = remove_piece_video(self.video_name, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_ADD_PHOTO_VIDEO:
            subclip_name = add_photo(self.video_name, self.photo_name, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_CHANGE_SPEED_VIDEO:
            subclip_name = change_speed(self.video_name, self.speed)


        elif self.msg == Thread.MSG_RATIO_VIDEO:
            subclip_name = change_size(self.video_name, self.ratioy, self.ratiox)


        elif self.msg == Thread.MSG_REMOVE_AUDIO_VIDEO:
            subclip_name = remove_audio(self.video_name,  self.start_time, self.end_time)
        elif self.msg == Thread.MSG_CONCATENATE_AUDIO_VIDEO:
            subclip_name = concatenate_with_audio(self.video_name, self.audio_name, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_ADD_VIDEO_VIDEO:
            subclip_name = add_subclip(self.video_name, self.video_name2, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_CROP_VIDEO:
            subclip_name = crop_clip(self.video_name, self.subwidth, self.subheight, self.end_time)
        elif self.msg == Thread.MSG_BRIGHTNESS_VIDEO:
            subclip_name = brightness(self.video_name, self.subwidth, self.subheight, self.end_time)
        elif self.msg == Thread.MSG_CONTRAST_VIDEO:
            subclip_name = contrast(self.video_name, self.subwidth, self.subheight, self.end_time)
        self.signal_return_value.emit(1, subclip_name)