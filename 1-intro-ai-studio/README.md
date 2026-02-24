# Раздел 1: Введение в Yandex AI Studio

## Обзор

В этом разделе мы знакомимся с облачной платформой **Yandex AI Studio** и учимся подключаться к ней из Jupyter-ноутбуков. Мы рассмотрим работу с языковой моделью **YandexGPT** через SDK и **Responses API**, а также генерацию изображений с помощью **YandexART**.

## Ключевые темы

- Авторизация в Yandex Cloud: `folder_id` и `api_key`
- Работа с YandexGPT через Yandex Cloud SDK
- Генерация изображений с помощью YandexART
- Введение в OpenAI-совместимый **Responses API**
- Ведение диалога с сохранением контекста (`previous_response_id`)
- Мультимодальные модели (анализ изображений)

## Материалы

### Лекция

| Материал | Описание |
|----------|----------|
| [CloudConnect.ipynb](CloudConnect.ipynb) | Подключение к Yandex Cloud, работа с YandexGPT, YandexART и введение в Responses API |

### Лабораторная работа

| Материал | Описание |
|----------|----------|
| [LLMTalk.ipynb](Labs/LLMTalk.ipynb) | **Две LLM общаются друг с другом** — создание простого класса `Agent` на основе Responses API и организация диалога между двумя LLM-агентами с разными системными промптами |

## Предварительные требования

- Python 3.10+
- Аккаунт Yandex Cloud с доступом к AI Studio
- Библиотеки: `openai`, `python-dotenv`, `yandex-cloud-ml-sdk`

## Вспомогательные файлы

- [`Scripts/create_sa.bat`](Scripts/create_sa.bat) / [`Scripts/create_sa.sh`](Scripts/create_sa.sh) — скрипты для создания сервисного аккаунта и API-ключа
