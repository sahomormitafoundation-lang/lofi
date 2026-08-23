import os
import subprocess
import glob
import random

def get_assets():
    music_dir = "Lo-Fi"
    image_dir = "Images"
    video_dir = "Videos"

    if not os.path.exists(music_dir):
        music_dir = "music"
    if not os.path.exists(image_dir):
        image_dir = "images"

    try:
        music_files = [f for f in os.listdir(music_dir) if f.lower().endswith('.mp3')]
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        video_files = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.mkv'))] if os.path.exists(video_dir) else []
    except Exception:
        return None, None, None, ["Error"]

    if not music_files:
        return None, None, None, ["Empty Music"]

    selected_music = os.path.join(music_dir, random.choice(music_files))
    selected_image = os.path.join(image_dir, random.choice(image_files)) if image_files else None
    selected_video = os.path.join(video_dir, random.choice(video_files)) if video_files else None

    facts = [
        "Silence is the best revenge.",
        "The eyes never lie, even when the lips do.",
        "Stay private, stay lowkey, stay happy.",
        "To gain power, learn to be unpredictable.",
        "Your biggest enemy is your own overthinking."
    ]
    
    selected_facts = random.sample(facts, min(len(facts), 5))
    
    return selected_music, selected_image, selected_video, selected_facts

def start_stream():
    stream_key = os.environ.get("YOUTUBE_STREAM_KEY")
    if not stream_key:
        print("Stream key not found!")
        return

    while True:
        selected_music, selected_image, selected_video, facts = get_assets()
        
        if not selected_music:
            print("No music found!")
            break

        # যদি Videos ফোল্ডারে ভিডিও থাকে, তবে ভিডিও চালাবে; না থাকলে ছবি ও টেক্সট দিয়ে স্লাইডশো করবে
        if selected_video:
            print(f"Playing Video: {selected_video} with Music: {selected_music}")
            command = [
                'ffmpeg', '-re', '-i', selected_video, '-stream_loop', '-1', '-i', selected_music,
                '-vf', 'scale=720:1280:force_original_aspect_ratio=increase,pad=720:1280:(ow-iw)/2:(oh-ih)/2',
                '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k', '-maxrate', '2500k', '-bufsize', '4000k',
                '-pix_fmt', 'yuv420p', '-g', '60', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                '-shortest', '-f', 'flv', f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'
            ]
        elif selected_image:
            print(f"Playing Image with Music: {selected_music} and Texts...")
            # আগের মতো ছবি এবং টেক্সট ওভারলে করার কমান্ড এখানে কাজ করবে
            filter_complex = f"[0:v]scale=720:1280:force_original_aspect_ratio=increase,pad=720:1280:(ow-iw)/2:(oh-ih)/2[bg];"
            
            command = [
                'ffmpeg', '-loop', '1', '-i', selected_image, '-stream_loop', '-1', '-i', selected_music,
                '-filter_complex', filter_complex + "[bg]format=yuv420p[v]",
                '-map', '[v]', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k',
                '-c:a', 'aac', '-b:a', '128k', '-shortest',
                '-f', 'flv', f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'
            ]
        else:
            print("No media found!")
            break

        subprocess.run(command)

if __name__ == '__main__':
    start_stream()
