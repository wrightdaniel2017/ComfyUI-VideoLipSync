import subprocess
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clone_repo():
    repo_url = 'https://github.com/vinthony/video-retalking.git'
    repo_path = 'video-retalking'
    if not os.path.exists(repo_path):
        logging.info("Cloning video-retalking repository...")
        subprocess.check_call(['git', 'clone', repo_url])

def install_requirements():
    os.chdir('video-retalking')
    logging.info("Installing requirements...")
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt', '--upgrade'])

def download_models():
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
    checkpoints_dir = './checkpoints'
    os.makedirs(checkpoints_dir, exist_ok=True)
    for url in model_urls:
        filename = os.path.join(checkpoints_dir, url.split('/')[-1])
        logging.info(f"Downloading {filename}")
        subprocess.check_call(['wget', url, '-P', checkpoints_dir])

def main():
    try:
        clone_repo()
        install_requirements()
        download_models()
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()