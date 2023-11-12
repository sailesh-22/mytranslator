from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, 'audio_files')
RESULT_DIR = os.path.join(BASE_DIR, 'result')
VIDEO_DIR = os.path.join(BASE_DIR, 'video_files')


def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    audio.close()

def STT(audio_path,from_lang):
    # Creating Recogniser() class object
    recog1 = sr.Recognizer()

    # Capture Voice
    with sr.AudioFile(audio_path) as source:
        recog1.adjust_for_ambient_noise(source,duration=0.2)
        audio = recog1.record(source)
        audio_duration = AudioFileClip(audio_path).duration
        try:
            MyText = recog1.recognize_google(audio,language=from_lang)
            MyText = MyText
            MyText = MyText.lower()
            print("Recognized text from the audio file:", MyText)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")

        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
    return MyText,audio_duration

def translate_text(input_text,from_lang,to_lang):
    translator = Translator(from_lang=from_lang,to_lang=to_lang)
    translated_text = translator.translate(input_text)
    return translated_text


def TTS(input_text,translated_audio_full_path,to_lang):
    tts = gTTS(input_text,slow=True, lang=to_lang)
    tts.save(translated_audio_full_path)


def merge_audio_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path)


# def main():
#     input_video_path = "video_files/demo2.mp4"
#     audio_path = "audio_files/output_audio.wav"
#     translated_audio_path = "result/translated_audio/translated.wav"
#     output_path = "result/output_video/output.mp4"
#     from_lang = "en"
#     to_lang = "ja"
#     extract_audio(input_video_path,audio_path)
#     print(f"Audio extracted from {input_video_path} and saved to {audio_path}")
#     transcript,duration= STT(audio_path,from_lang=from_lang)
#     translated_transcript = translate_text(transcript, from_lang=from_lang, to_lang=to_lang)
#     TTS(translated_transcript,translated_audio_path,to_lang=to_lang)
#     print(f"translated_transcript:{translated_transcript}")
#     print(f"Translated text converted to audio and saved to {translated_audio_path}")

#     merge_audio_video(input_video_path, translated_audio_path, output_path)
#     print(f"Audio merged back into the video and saved to {output_path}")


# if __name__ == '__main__':
#     main()
