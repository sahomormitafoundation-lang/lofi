
import os
import sys
import json
import random
from pathlib import Path


# ==========================================
# CONTINUOUS STUDY STREAM - ASSET GENERATOR
# ==========================================

def find_asset_folder(preferred, fallback):
    """Find the first available asset directory."""

    if os.path.isdir(preferred):
        return Path(preferred)

    if os.path.isdir(fallback):
        return Path(fallback)

    raise FileNotFoundError(
        f"Folder not found: {preferred} or {fallback}"
    )


def get_assets():

    # Locate music and image folders independently
    music_dir = find_asset_folder("Lo-Fi", "music")
    image_dir = find_asset_folder("Images", "images")

    # Collect MP3 files
    music_files = [
        file for file in music_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() == ".mp3"
    ]

    # Collect supported images
    image_files = [
        file for file in image_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in (
            ".jpg", ".jpeg", ".png"
        )
    ]

    # Validate assets
    if not music_files:
        raise FileNotFoundError(
            f"No MP3 files found in {music_dir}"
        )

    if not image_files:
        raise FileNotFoundError(
            f"No images found in {image_dir}"
        )

    # Random selection
    selected_music = random.choice(music_files)
    selected_image = random.choice(image_files)

    # Study and motivational quotes
    facts = [
        "Silence is the best revenge.",
        "The eyes never lie, even when the lips do.",
        "Stay private, stay lowkey, stay happy.",
        "To gain power, learn to be unpredictable.",
        "Your biggest enemy is your own overthinking.",
        "Focus on your goals, not on distractions.",
        "Discipline creates freedom.",
        "Small progress is still progress.",
        "Your future needs your attention.",
        "Peace begins when comparison ends.",
        "Work hard in silence.",
        "Consistency beats temporary motivation.",
        "Protect your energy.",
        "Make your dreams bigger than your excuses.",
        "Be patient with your progress.",
        "Every day is a new opportunity.",
        "Stay focused and trust the process.",
        "Success starts with self-discipline.",
        "Less noise, more productivity.",
        "Believe in your own journey.",
        "Dream big, study hard.",
        "One page at a time.",
        "Your effort today builds your future.",
        "Stay calm and keep learning.",
        "Great things take time.",
        "Never stop improving yourself.",
        "Focus on progress, not perfection.",
        "Your dedication will pay off.",
        "Make today count.",
        "Learn something new every day."
    ]

    # Select five unique random quotes
    selected_facts = random.sample(facts, 5)

    # Return data in the format expected by live.yml
    return {
        "music": str(selected_music),
        "image": str(selected_image),
        "facts": selected_facts
    }


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    try:
        assets = get_assets()

        # JSON output for GitHub Actions
        print(
            json.dumps(
                assets,
                ensure_ascii=False
            )
        )

    except Exception as error:

        print(
            f"ASSET ERROR: {error}",
            file=sys.stderr
        )

        sys.exit(1)
