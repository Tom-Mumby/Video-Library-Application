from video_library_application.config.sizes.fixed_sizes import ImageSize, ScreenSize
from PIL import Image
import ffmpeg
import os


class ThumbnailMake:
    """Creates a thumbnail from a video file, preserving the aspect ratio"""

    # size to make the cropped thumbnail
    picture_max = ImageSize

    @classmethod
    def generate_thumbnail(cls, video_path, output_path, thumbnail_fraction=0.3):
        """Creates and saves thumbnail given the path of the video and the name of the image to make"""

        def get_dimensions(width, height):
            """Given video dimensions returns dimensions of thumbnail image to fully fit into specified picture size"""
            width = int(width)
            height = int(height)
            if height * ScreenSize.aspect_ratio > width: # narrow screen
                scale = cls.picture_max.width / width
            else:
                scale = cls.picture_max.height / height # wide screen

            return int(round(width * scale)), int(round(height * scale))

        def get_dimensions_AR(aspect_ratio_string):
            """Given video aspect ratio returns dimensions of thumbnail image to fully fit into specified picture size"""
            aspect_ratio_split = aspect_ratio_string.split(":")
            aspect_ratio_float = float(aspect_ratio_split[0]) / float(aspect_ratio_split[1])

            if aspect_ratio_float < 0:  # in rare cases aspect ratio is negative
                aspect_ratio_float *= -1

            if aspect_ratio_float < ScreenSize.aspect_ratio: # narrow screen
                return int(round(cls.picture_max.width)), int(round(cls.picture_max.width / aspect_ratio_float))
            else:  # wide screen
                return int(round(cls.picture_max.height * aspect_ratio_float)), int(round(cls.picture_max.height))

        def crop_dims(dims):
            """Takes image dimensions and returns crop corners so thumbnail is the same size as the specified picture size"""
            if cls.picture_max.width == dims[0]:# width is right, crop height
                extra = int((dims[1] - cls.picture_max.height)/2)
                return 0, extra, cls.picture_max.width, extra+cls.picture_max.height

            elif cls.picture_max.height == dims[1]:# height is right, crop width
                extra = int((dims[0] - cls.picture_max.width)/2)
                return extra, 0, extra+cls.picture_max.width, cls.picture_max.height

        def get_string(nested_obj, search):
            """Takes object made up of multiple dictionaries and strings finds int after search string"""
            nested_obj = str(nested_obj) # converts object to string
            # splits string according to search string and gets part after this occurs
            nested_obj_split = nested_obj.split("\'" + search + "\': ")
            nested_obj_split = nested_obj_split[1]
            # splits string according to various characters that may appear after needed int value and gets first part
            info = nested_obj_split.split('}')
            info = info[0]
            info = info.split(',')
            info = info[0]
            info = info.split(']')
            info = info[0]
            # if value is surrounded in single quotes remove these
            if info[0] == "\'":
                info = info[1:-1]
            return info
        print("making thumbnail")


        # get info about video
        try:
            probe = ffmpeg.probe(video_path)
        except ffmpeg._run.Error:
            print("\tError with probe to get video info")
            return False

        try: # try to find the length of the video using 'duration' to search
            time = float(get_string(probe,'duration')) # seconds

        except KeyError: #i f not there find using different search string
            time = get_string(probe,'DURATION-eng') # minutes : seconds
            time_list = time.split(":")
            time = float(time_list[-1]) + float(time_list[-2]) * 60 # set time in seconds

        time = int(time * thumbnail_fraction) # set time to get thumbnail from

        # use ffmpeg to get thumbnail from video and save to file
        try:
            (
                ffmpeg
                    .input(video_path, ss=time) #path of video and time in seconds to get thumbnail
                    #.filter('scale', thumbnail_dimensions[0], thumbnail_dimensions[1]) # set size of thumbnail to get
                    .output(output_path, vframes=1) # set output path
                    #.overwrite_output() # set to overwrite
                    #.run()
                    .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg._run.Error:
            print("\tError with thumbnail creation")

        if os.path.isfile(output_path):  # if thumbnail has been created
            # crop and save image
            try:
                thumbnail_dimensions = get_dimensions_AR(get_string(probe, 'display_aspect_ratio'))
            except IndexError:  # no display_aspect_ratio
                thumbnail_dimensions = get_dimensions(get_string(probe, 'width'), get_string(probe, 'height'))
            im = Image.open(output_path)
            im = im.resize(thumbnail_dimensions, Image.LANCZOS)
            im = im.crop(crop_dims(thumbnail_dimensions))
            im.save(output_path)
            return True # if image has been made
        else:
            return False # if image was not made
