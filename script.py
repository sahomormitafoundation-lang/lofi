import os
import random

def get_assets():
    music_dir = "Lo-Fi"
    image_dir = "Images"

    if not os.path.exists(music_dir) or not os.path.exists(image_dir):
        music_dir, image_dir = "music", "images"

    try:
        music_files = [f for f in os.listdir(music_dir) if f.lower().endswith('.mp3')]
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    except Exception:
        return "Error|Error|Error|Error|Error|Error|Error"

    if not music_files or not image_files:
        return "Empty|Empty|Error|Error|Error|Error|Error"

    selected_music = os.path.join(music_dir, random.choice(music_files))
    selected_image = os.path.join(image_dir, random.choice(image_files))

    facts = [
        "Silence is the best revenge.",
        "The eyes never lie, even when the lips do.",
        "Stay private, stay lowkey, stay happy.",
        "To gain power, learn to be unpredictable.",
        "Your biggest enemy is your own overthinking."
    ]
    
    selected_facts = random.sample(facts, 5)
    
    return f"{selected_music}|{selected_image}|{'|'.join(selected_facts)}"

if __name__ == "__main__":
    print(get_assets())
