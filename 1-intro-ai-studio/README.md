# Раздел 1: Введение в Yandex AI Studio

## Обзор

В этом разделе мы знакомимся с облачной платформой **Yandex AI Studio** и учимся подключаться к ней из кода на языке Python. Мы рассмотрим работу с языковыми моделями Yandex Cloud через **AI Studio SDK** и через совместимое с OpenAI **Responses API**, а также генерацию изображений с помощью **YandexART**.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| 📖 | [AI Studio и Yandex Cloud][LectAIStudio] | Основные концепции Yandex Cloud и вызов API через Yandex AI Studio SDK и Responses API | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectAIStudio] |
| ✏️ | [CloudConnect.ipynb](CloudConnect.ipynb) | Подключение к Yandex Cloud, работа с YandexGPT, YandexART и введение в Responses API | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/1-intro-ai-studio/CloudConnect.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F1-intro-ai-studio%2FCloudConnect.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/1-intro-ai-studio/CloudConnect.ipynb) |
| 🔬 | [LLMTalk.ipynb](Labs/LLMTalk.ipynb) | Две LLM общаются друг с другом — создание класса `Agent` и диалог между двумя LLM | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/1-intro-ai-studio/Labs/LLMTalk.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F1-intro-ai-studio%2FLabs%2FLLMTalk.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/1-intro-ai-studio/Labs/LLMTalk.ipynb) |

[LectAIStudio]: https://disk.yandex.ru/i/tUgkFRO7XAkiOQ

## Авторизация в облаке

Для работы с любым API Yandex Cloud необходимы два ключевых параметра:

- **`folder_id`** — идентификатор каталога (папки) в Yandex Cloud, в которой размещены ресурсы и модели.
- **`api_key`** — API-ключ [сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts), от имени которого выполняются запросы. Сервисному аккаунту необходимы роли `ai.editor` (для работы с моделями) и `serverless.mcpGateway.invoker` (для работы с MCP-шлюзами), или более широкая роль `editor`.

Рекомендуется хранить ключи в файле `.env` и загружать их через библиотеку `python-dotenv`, чтобы избежать случайной утечки секретов при публикации кода.

Варианты получения значений `folder_id`/`api_key`:

* От преподавателя в рамках курса. В этом случае либо адрес для скачивания `.env`-файла будет "зашит" в ноутбуках, либо он будет предоставлен вам отдельно, и в ноутбуках будет нужно вручную заменить строку `{{url_of_dotenv_file}}` на адрес скачивания
* Если у вас есть доступ к Yandex Cloud, вы можете создать эти значения самостоятельно, запустив [один из скриптов](Scripts), или создав сервисный аккаунт и API-ключ вручную в веб-консоли облака.
* Если у вас нет доступа к Yandex Cloud, вы можете подключиться к облаку и использовать [приветственный грант](https://yandex.cloud/ru/docs/billing/concepts/trial-period)

## Теоретический материал

### Что такое Yandex AI Studio

[Yandex AI Studio](https://yandex.cloud/ru/docs/ai-studio/) — это облачная платформа компании Яндекс, предоставляющая доступ к фундаментальным моделям искусственного интеллекта: языковым моделям для генерации и анализа текста, моделям для генерации изображений и мультимодальным моделям, способным работать как с текстом, так и с визуальной информацией, а также к ряду других интеллектуальных сервисов. Платформа является частью экосистемы **Yandex Cloud** и поддерживает работу через несколько программных интерфейсов.

### Способы работы с AI Studio

Yandex AI Studio предоставляет несколько способов взаимодействия с моделями:

1. **Responses API** — OpenAI-совместимый API, который является стандартом де факто и наиболее современным способом взаимодействия с языковыми моделями и построения агентских систем. Благодаря совместимости с OpenAI, весь код, написанный для работы с OpenAI, можно адаптировать для Yandex Cloud, изменив лишь `base_url`, `api_key` и название модели. Этот протокол поддерживает работу с инструментами (Function Calling, Web Search, File Search, MCP), поддержание диалогового контекста, структурированный вывод и многое другое. Все эти возможности мы будем рассматривать в рамках курса.

2. **Yandex AI Studio SDK** — нативный Python SDK ([GitHub](https://github.com/yandex-cloud/yandex-ai-studio-sdk)), предоставляющий высокоуровневый интерфейс для работы со всеми сервисами платформы. SDK особенно удобен для работы с функциями, которые не поддерживаются через Responses API, такими как **пакетная обработка запросов** или **генерация изображений** с помощью YandexART. Пакетный режим полезен, когда необходимо обработать большие объёмы данных без жёстких ограничений по времени — облако самостоятельно планирует ресурсы, и стоимость такого режима ниже.

### Модели YandexGPT и YandexART

**YandexGPT** — это семейство [языковых моделей](https://yandex.cloud/ru/docs/ai-studio/concepts/generation/models), доступных через AI Studio. Модели поддерживают русский и английский языки и оптимизированы для задач генерации текста, анализа, суммаризации и ведения диалога.

Помимо моделей Yandex, в AI Studio доступны и другие модели, такие как **Qwen3**, **Gemma 3** и **Alice** — каждая из которых имеет свои особенности и лучше подходит для определённых задач.

**YandexART** — модель генерации изображений по текстовому описанию. В отличие от текстовых моделей, генерация изображений, как и любая генерация мультимедийного контента, выполняется в **асинхронном режиме**: запрос отправляется на обработку, и затем результат получается через отдельный вызов. Это связано с тем, что генерация изображений требует значительных вычислительных ресурсов и занимает заметно больше времени, чем генерация текста.

### Responses API и диалоговый контекст

При работе с Responses API можно подключаться к моделям через стандартный [OpenAI SDK](https://github.com/openai/openai-python), указав адрес Yandex Cloud в параметре `base_url`. Модели задаются в формате `gpt://{folder_id}/{model_name}/{version}`.

> **Важно:** для корректной работы всех функций Responses API необходимо передавать `folder_id` в параметр `project` при создании объекта `OpenAI`.

Одна из ключевых возможностей Responses API — **поддержание диалогового контекста**. Без контекста каждый запрос к модели является изолированным, и она не помнит предыдущие вопросы и ответы. Для поддержания осмысленного диалога существуют три подхода:

1. **Ручное накопление сообщений** — формирование списка `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]` и передача его целиком в каждый запрос.
2. **Объект `conversation`** — специальный объект для хранения и управления диалогом.
3. **Параметр `previous_response_id`** — простейший способ, при котором в каждый следующий запрос передаётся идентификатор предыдущего ответа, а облако само восстанавливает цепочку диалога. Для этого необходимо установить `store=True` (сохранение ответов в облаке).

## Практические работы

### 🔬 LLMTalk.ipynb

Вы когда-нибудь задумывались, о чем могли бы говорить два продвинутых искусственных интеллекта, оставшись наедине? Эта лабораторная работа предлагает вам стать цифровым драматургом и организовать беседу между двумя различными языковыми моделями. Вы создадите простой класс `Agent` и подготовите сцену для увлекательного диалога на выбранную вами тему, наблюдая за тем, как раскрываются их уникальные личности.

По окончании этого упражнения вы не только станете свидетелем разговора между двумя ИИ, но и создадите основополагающий компонент для всех будущих многоагентных систем в этом курсе. Это ваш первый шаг от простого использования ИИ к управлению целым оркестром из них, что открывает мир возможностей для создания сложных, взаимодействующих интеллектуальных систем.

## Вспомогательные файлы

- [`Scripts/create_sa.bat`](Scripts/create_sa.bat) / [`Scripts/create_sa.sh`](Scripts/create_sa.sh) — скрипты для создания сервисного аккаунта и API-ключа
