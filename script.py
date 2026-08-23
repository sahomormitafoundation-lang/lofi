import os
import subprocess
import glob
import random

def get_media_lists():
    # মিউজিক, ছবি এবং ভিডিও ফোল্ডার থেকে ফাইলগুলো খুঁজে বের করবে
    music_files = sorted(glob.glob('Lo-Fi/*.mp3') + glob.glob('music/*.mp3'))
    image_files = sorted(glob.glob('Images/*.jpg') + glob.glob('Images/*.png') + glob.glob('images/*.jpg'))
    video_files = sorted(glob.glob('Videos/*.mp4') + glob.glob('Videos/*.mkv'))
    
    return music_files, image_files, video_files

def start_stream():
    stream_key = os.environ.get("YOUTUBE_STREAM_KEY")
    if not stream_key:
        print("Stream key not found!")
        return

    while True:
        music_files, image_files, video_files = get_media_lists()
        
        if not music_files:
            print("No music files found!")
            break
            
        # র‍্যান্ডম একটি মিউজিক, ছবি বা ভিডিও সিলেক্ট করা
        selected_music = random.choice(music_files)
        
        # যদি ভিডিও থাকে তবে ভিডিও চালাবে, না থাকলে ছবি ও মিউজিক দিয়ে স্লাইডশো করবে
        if video_files:
            selected_video = random.choice(video_files)
            print(fPlaying Video: {selected_video} with Music: {selected_music})
            
            # ভিডিও এবং ব্যাকগ্রাউন্ড মিউজিক একসাথে স্ট্রিম করার FFmpeg কমান্ড
            command = [
                'ffmpeg', '-re', '-i', selected_video, '-stream_loop', '-1', '-i', selected_music,
                '-vf', 'scale=720:1280:force_original_aspect_ratio=increase,pad=720:1280:(ow-iw)/2:(oh-ih)/2',
                '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k',
                '-c:a', 'aac', '-b:a', '128k', '-shortest',
                '-f', 'flv', f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'
            ]
        else:
            print("No video found, waiting for files...")
            break
            
        subprocess.run(command)

if __name__ == '__main__':
    start_stream()
