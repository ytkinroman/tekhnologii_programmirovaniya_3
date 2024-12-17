import yt_dlp
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from gtts import gTTS
import time
import os
import psutil
from multiprocessing import Process


def get_memory_usage() -> float:
    """Получение используемой памяти в мегабайтах."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024)


def video_downloader(video_url: str) -> str:
    """Функция для скачивания видео с YouTube."""
    ydl_opts = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "retries": 10,
        "fragment_retries": 10,
        "retry_sleep_functions": {
            "sleep": lambda x: time.sleep(x),
            "sleeper": lambda x: time.sleep(x)
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_name = ydl.prepare_filename(info)

    base_name = file_name.rsplit(".", 1)[0]
    print("[ИНФОРМАЦИЯ] Файл", f'"{base_name}"', "скачан")
    return file_name


def translate_name(name_to_translate: str) -> str:
    """Перевод названия с Русского на Английский язык."""
    translator = Translator()
    translated_text = translator.translate(name_to_translate, dest="en", src="ru").text
    return translated_text


def transcribe_audio(audio_file, file_name):
    """Создаёт текстовый файл из аудиофайла."""
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    transcription = r.recognize_google(audio, language="ru-RU")

    new_name = f"{file_name}.txt"

    with open(new_name, "w", encoding="utf-8") as f:
        f.write(transcription)

    return new_name


def translate_text(text_to_translate: str) -> str:
    """Перевод текст с Русского на Английский язык."""
    with open(text_to_translate, "r", encoding="utf-8") as f:
        text = f.read()

    translator = Translator()
    translated_text = translator.translate(text, dest="en", src="ru").text
    return translated_text


def translate_video(file_name: str) -> None:
    """Создаёт видео с переводом речи на Английский язык."""
    output_file = translate_name(file_name)
    print("[ИНФОРМАЦИЯ] Перевод файла...")

    video = VideoFileClip(file_name)
    audio = video.audio
    base_name = file_name.rsplit(".", 1)[0]
    temp_audio_file = f"{base_name}.wav"
    audio.write_audiofile(temp_audio_file)

    audio_text = transcribe_audio(temp_audio_file, base_name)
    translated_text = translate_text(audio_text)

    new_name_file = f"{base_name}.mp3"
    tts = gTTS(text=translated_text, lang="en")
    tts.save(new_name_file)

    new_audio = AudioFileClip(new_name_file)
    final_video = video.set_audio(new_audio)
    final_video.write_videofile(output_file)

    os.remove(file_name)
    os.remove(temp_audio_file)
    os.remove(audio_text)
    os.remove(new_name_file)

    print("[ИНФОРМАЦИЯ] Файл", f'"{base_name}"', "переведён")
    print("=" * 100)


def sequential_download(youtube_urls: tuple) -> None:
    """Последовательное скачивание видео."""
    print("=" * 72)
    for url in youtube_urls:
        print(f"[ИНФОРМАЦИЯ] Скачивание видео с URL: {url}")
        filename = video_downloader(url)
        translate_video(filename)


def start_parallel(url):
    """Метод для запуска процесса."""
    filename = video_downloader(url)
    translate_video(filename)


def parallel_download(youtube_urls: tuple) -> None:
    """Параллельное скачивание видео с помощью процессов."""
    print("=" * 72)
    print("[ИНФОРМАЦИЯ] Начинается параллельное скачивание видео с использованием процессов.")

    processes = []

    for url in youtube_urls:
        process = Process(target=start_parallel, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("[ИНФОРМАЦИЯ] Все видео успешно скачаны.")


def main() -> None:
    youtube_urls = (
        "https://youtu.be/cS2vYtDq8l4?si=tFQWjb1gXrB0-ici",
        "https://youtu.be/SfmFOvVMc-o?si=GY_OsGJryPTPk54N",
        "https://youtu.be/_gKhXrDDYBM?si=pf4bJJDOiRcoPIyt"
    )
    # sequential_download(youtube_urls)
    parallel_download(youtube_urls)


def app() -> None:
    start_time = time.perf_counter()
    main()
    stop_time = time.perf_counter()
    print("=" * 100)
    print(f"    Время выполнения: {stop_time - start_time:0.5f} секунд.")
    final_memory = get_memory_usage()
    print(f"    Использовано памяти: {final_memory:.2f} Mb.")
    print("=" * 100)


if __name__ == "__main__":
    app()
