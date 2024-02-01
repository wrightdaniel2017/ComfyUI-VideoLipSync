import subprocess
import os
import sys
import logging
from urllib.request import urlopen

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoRetalkingNode:
    """
    A node for integrating the video-retalking library into the ComfyUI system.
    """

    FUNCTION = "retalk_video"
    CATEGORY = "Video Processing"
    RETURN_TYPES = ("VIDEO",)

    def __init__(self):
        self.setup_done = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_input": ("VIDEO",),  # assuming this remains the same
                "audio_input": ("STRING",),  # changed from "AUDIO" to "STRING" to accept a file path
                # Add any other required inputs for retalking
            },
            "optional": {
                # Define any optional inputs here
            },
        }


    def check_internet_connection(self):
        try:
            urlopen('http://google.com', timeout=1)
            return True
        except Exception as e:
            logging.error(f"Internet connection error: {e}")
            return False

    def setup_video_retalking(self):
        if not self.check_internet_connection():
            logging.error("No internet connection detected. Please check your connection.")
            return

        logging.info("Ensure CUDA is available on your system.")
        
        try:
            repo_path = 'video-retalking'
            if not os.path.exists(repo_path):
                logging.info("Cloning video-retalking repository...")
                subprocess.check_output(['git', 'clone', 'https://github.com/vinthony/video-retalking.git'], stderr=subprocess.STDOUT)
            os.chdir(repo_path)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error cloning repository: {e.output.decode()}")
            return
        except FileNotFoundError:
            logging.error(f"Directory '{repo_path}' not found.")
            return

        try:
            logging.info("Installing requirements...")
            subprocess.check_output([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing requirements: {e.output.decode()}")

    def download_models(self):
        model_urls = [
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/30_net_gen.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/BFM.zip",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/DNet.pt",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/ENet.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/expression.mat",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/face3d_pretrain_epoch_20.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/GFPGANv1.3.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/GPEN-BFR-512.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/LNet.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/ParseNet-latest.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/RetinaFace-R50.pth",
        "https://github.com/vinthony/video-retalking/releases/download/v0.0.1/shape_predictor_68_face_landmarks.dat"
    ]
        try:
            checkpoints_dir = './checkpoints'
            os.makedirs(checkpoints_dir, exist_ok=True)
            for url in model_urls:
                filename = os.path.join(checkpoints_dir, url.split('/')[-1])
                logging.info(f"Downloading {filename}")
                subprocess.check_output(['wget', url, '-P', checkpoints_dir], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error downloading models: {e.output.decode()}")

    def ensure_setup(self):
        if not self.setup_done:
            self.setup_video_retalking()
            self.download_models()
            self.setup_done = True

    def retalk_video(self, video_input, audio_input, output_path='results/output.mp4'):
        self.ensure_setup()
        os.chdir('video-retalking')
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
