from django.shortcuts import render
import shutil
from .utils import extract_audio, STT, translate_text, TTS, merge_audio_video
import os
from django.conf import settings



def clear_directories():
        directories_to_clear = ['audio_files', 'downloads', 'video_files']

        for directory in directories_to_clear:
                directory_path = os.path.join(settings.MEDIA_ROOT, directory)

        # Check if the directory exists
                if os.path.exists(directory_path):
            # Remove all files in the directory
                        for file_name in os.listdir(directory_path):
                                file_path = os.path.join(directory_path, file_name)
                                try:
                                        if os.path.isfile(file_path):
                                                os.unlink(file_path)
                                        elif os.path.isdir(file_path):
                                                shutil.rmtree(file_path)
                                except Exception as e:
                                        print(f"Error deleting {file_path}: {e}")

                        print(f"All files removed from {directory}")
                else:
                        print(f"Directory {directory} does not exist.")

# video_path = "video_files/demo2.mp4"
audio_path = "media/audio_files/audio.wav"
# translated_audio_path = "audio_files/translated.wav"
# output_path = "downloads/output.mp4"
# from_lang = "en"
# to_lang = "ja"


def translate_video(request):
        clear_directories()
        if request.method == 'POST':
                original_filename = ""
                video_file = request.FILES.get('video_path')
                if video_file:
                        original_filename = video_file.name
                        save_path = os.path.join(settings.MEDIA_ROOT, 'video_files', original_filename)

                        with open(save_path, 'wb') as destination:
                                for chunk in video_file.chunks():
                                        destination.write(chunk)
                
                video_path = original_filename
                from_lang = request.POST.get('from_lang', '')
                to_lang = request.POST.get('to_lang', '')

                output_path = f"downloads/output_{from_lang}_to_{to_lang}.mp4"
                translated_audio_path = f"audio_files/{video_path}_{from_lang}_to_{to_lang}.wav"

                video_full_path = os.path.join(settings.MEDIA_ROOT, 'video_files',video_path)

                output_full_path = os.path.join(settings.MEDIA_ROOT, output_path)
                translated_audio_full_path = os.path.join(settings.MEDIA_ROOT, translated_audio_path)

                extract_audio(video_path=video_full_path,audio_path=audio_path)
                print(f"Audio extracted from {video_path} and saved to {audio_path}")
                transcript,duration= STT(audio_path,from_lang=from_lang)
                translated_transcript = translate_text(transcript, from_lang=from_lang, to_lang=to_lang)
                TTS(translated_transcript, translated_audio_full_path, to_lang=to_lang)
                merge_audio_video(video_full_path, translated_audio_full_path, output_full_path)

                return render(request, 'translator/result.html', {'output_path':f"{output_path}",'transcript':transcript,'translated_text':translated_transcript})
        return render(request, 'translator/translate_form.html') 