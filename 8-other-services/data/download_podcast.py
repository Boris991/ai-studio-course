#!/usr/bin/env python3
"""
Простой скрипт для скачивания MP3-файлов с podcast.ru.
Использует регулярные выражения для извлечения прямой ссылки на аудио.
"""
import re
import sys
import requests

def extract_mp3_url(html_content):
    """
    Извлекает URL MP3-файла из HTML страницы podcast.ru.
    Ищет паттерн "trackUrl":"..." в JSON объекте window.__APOLLO_STATE__.
    """
    pattern = r'"trackUrl":"([^"]+)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    return None

def extract_episode_name(html_content):
    """
    Извлекает название эпизода для использования в имени файла.
    Ищет паттерн "name":"..." в JSON объекте window.__APOLLO_STATE__.
    """
    pattern = r'"name":"([^"]+)"'
    match = re.search(pattern, html_content)
    if match:
        name = match.group(1)
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        return name[:100]
    return None

def download_file(url, filename):
    """
    Скачивает файл по URL и сохраняет его с заданным именем.
    """
    print(f"Скачивание: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Файл сохранён как: {filename}")

def main():
    # URL по умолчанию
    default_url = "https://podcast.ru/e/9bFbT8jlXh2"
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
        print(f"Используется URL по умолчанию: {url}")
    
    print(f"Загрузка страницы: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        sys.exit(1)
    
    mp3_url = extract_mp3_url(html)
    if not mp3_url:
        print("Не удалось найти ссылку на MP3-файл")
        sys.exit(1)
    
    episode_name = extract_episode_name(html)
    if episode_name:
        filename = f"{episode_name}.mp3"
    else:
        # Используем часть URL как имя файла
        slug = url.rstrip('/').split('/')[-1]
        filename = f"{slug}.mp3"
    
    print(f"Найдена ссылка на MP3: {mp3_url}")
    print(f"Имя файла: {filename}")
    
    try:
        download_file(mp3_url, filename)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()