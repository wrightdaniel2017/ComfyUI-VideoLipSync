import subprocess
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoRetalkingNode:
    """
    A node for integrating the video-retalking library into the ComfyUI system.
    """

    FUNCTION = "retalk_video"
    CATEGORY = "Video Processing"
    RETURN_TYPES = ("VIDEO",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_input": ("VIDEO",),
                "audio_input": ("STRING",),
            },
            "optional": {
                # Define any optional inputs here
            },
        }

    def retalk_video(self, video_input, audio_input, output_path='results/output.mp4'):
        os.chdir('video-retalking')  # Ensure the working directory is correct
        command = [
            sys.executable, 'inference.py',
            '--face', video_input,
            '--audio', audio_input,
            '--outfile', output_path
        ]
        try:
            subprocess.check_call(command)
            logging.info(f"Retalking video generated at {output_path}")
        except subprocess.CalledProcessError as e:
            logging.error("Failed to retalk video:", e)
            return None
        return output_path

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoRetalkingNode": VideoRetalkingNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoRetalkingNode": "Video Retalking Node"
}
