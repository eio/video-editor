from moviepy.editor import (
    VideoFileClip,
    VideoClip,
    clips_array,
)

# Input video files
INPUT_VIDEOS = [
    "input/video1.mov",
    "input/video2.mov",
    "input/video3.mov",
]
# Output triptych video
OUTPUT_VIDEO = "output/triptych_output.mov"
# If the original videos have an aspect ratio of 1280x720,
# and we want to divide the width into 3 equal sections,
# we should divide 1280 by 3 to determine the pixel coordinates for each section.
# In this case, each section would cover approximately 426.67 pixels in width.
# Define pixel coordinates for each section
# (left section, middle section, right section)
SECTIONS = [
    (0, 426),
    (426, 853),
    (853, 1280),
]

# Function to extract a specific section from a video by pixels
def extract_section_by_pixels(input_video, output_video_clip, section):
    print(f"Extracting section by pixels: `{input_video}`")
    clip = VideoFileClip(input_video)
    section_start = section[0]
    section_end = section[1]
    extracted_clip = clip.crop(x1=section_start, x2=section_end)
    # Ensure all extracted sections have the same height
    extracted_clip = extracted_clip.resize(height=clip.h)
    extracted_clip.write_videofile(output_video_clip, codec="libx264")


# Function to load component clips and crop them accordingly
def get_video_clips():
    # The output paths of the clip sectinos
    clip_output_paths = []
    # Initialize with a very large value
    min_duration = float("inf")
    # Extract specific sections from each video
    for i, input_video in enumerate(INPUT_VIDEOS):
        output_section_video = f"section_video_{i}.mov"
        extract_section_by_pixels(input_video, output_section_video, SECTIONS[i])
        clip_output_paths.append(output_section_video)
        # Keep track of the shortest video clip
        clip_duration = VideoFileClip(input_video).duration
        if clip_duration < min_duration:
            min_duration = clip_duration

    # Load the extracted section clips with the same minimum duration
    # (i.e. the duration of the shortest video clip)
    video_clips = [
        VideoFileClip(path).set_duration(min_duration) for path in clip_output_paths
    ]
    ##############################################################
    # # Load the extracted section clips
    # video_clips = [VideoFileClip(path) for path in clip_output_paths]
    # # Synchronize the clips by setting the same duration for all
    # duration = video_clips[0].duration
    # for clip in video_clips:
    #     clip = clip.set_duration(duration)
    # # Load the extracted section clips with the same duration
    # video_clips = [
    #     VideoFileClip(path).set_duration(VideoFileClip(input_videos[0]).duration)
    #     for path in clip_output_paths
    # ]
    ##############################################################
    return video_clips


if __name__ == "__main__":
    # Get the clip sections we want to stitch together
    video_clips = get_video_clips()
    # Use clips_array to create a horizontal triptych
    row_of_vids = [clip for clip in video_clips]
    # Use the row of vids to compose the clips_array matrix
    final_clip = clips_array([row_of_vids])
    # Write the final video
    final_clip.write_videofile(OUTPUT_VIDEO, codec="libx264", fps=video_clips[0].fps)
