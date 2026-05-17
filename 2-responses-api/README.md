# Раздел 2: Responses API

## Обзор

В этом разделе мы углубляемся в возможности **Responses API** — OpenAI-совместимого интерфейса Yandex Cloud для работы с языковыми моделями. Мы изучаем поддержание диалогового контекста, извлечение структурированных данных с помощью **Pydantic** и JSON mode, визуализацию данных и работу с мультимодальными моделями.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| 📖 | [Вызов LLM через Responses API][LectRespAPI] | Изучаем, как использовать Reponses API для поддержания контекста диалога, формирования структурного ответа и работы с мульимодальными моделями | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectRespAPI] |
| ✏️ | [ResponsesAPI.ipynb](ResponsesAPI.ipynb) | Responses API: диалоговый контекст, структурированный вывод (Pydantic, JSON mode), визуализация данных и мультимодальные модели | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/ResponsesAPI.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FResponsesAPI.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/ResponsesAPI.ipynb) |
| 🔬 | [PaperSummarize.ipynb](Labs/PaperSummarize.ipynb) | Суммаризация научной статьи — извлечение ключевой информации из текста | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/Labs/PaperSummarize.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FLabs%2FPaperSummarize.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/Labs/PaperSummarize.ipynb) |
| 🔬 | [AgenticImageGeneraton.ipynb](Labs/AgenticImageGeneraton.ipynb) | Агентный цикл генерации изображений — итеративная генерация и улучшение изображений с помощью LLM | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/Labs/AgenticImageGeneraton.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FLabs%2FAgenticImageGeneraton.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/Labs/AgenticImageGeneraton.ipynb) |

[LectRespAPI]: https://disk.yandex.ru/i/yRGTadYhxkmb5Q

## Теоретический материал

### Responses API: современный стандарт взаимодействия с LLM

[Responses API](https://yandex.cloud/ru/docs/ai-studio/api-ref/responses/) — это OpenAI-совместимый протокол, который Yandex Cloud поддерживает для работы с языковыми моделями. Он является преемником более ранних протоколов (Chat Completions, AI Assistant API) и предлагает единый интерфейс для решения широкого спектра задач: от простых вопросов к модели до построения сложных агентских систем с инструментами.

Responses API предоставляет два ключевых метода:
- **`client.responses.create()`** — стандартный запрос к модели, возвращающий текстовый ответ.
- **`client.responses.parse()`** — специализированный метод для получения **структурированного вывода**, привязанного к заданной Pydantic-модели.

### Системный промпт (System Prompt)

Системный промпт задаётся через параметр `instructions` и определяет «роль» и правила поведения модели. Например, можно указать, что модель — эксперт по определённой теме и должна отвечать кратко. Хорошо написанный системный промпт критически важен для качества ответов: он направляет модель, определяет тональность, ограничения и формат выходных данных. Промпт является частью [промпт-инжиниринга](https://yandex.cloud/ru/docs/ai-studio/prompts/) — дисциплины и набора техник оптимизации взаимодействия с языковыми моделями.

### Извлечение структурированных данных

Одно из наиболее практических применений LLM — **извлечение структурированной информации** из неструктурированного текста. Например, из текстовых отзывов можно извлекать тональность, оценки по различным критериям, ключевые темы и плюсы/минусы.

Существуют два подхода к получению структурированного вывода:

#### JSON Mode

В простейшем случае можно попросить модель вернуть ответ в формате JSON, указав желаемую структуру в промпте. Однако этот подход ненадёжен: модель может ошибиться с именами полей, нарушить синтаксис JSON или добавить лишние данные. Результат приходится парсить вручную, вылавливая JSON из текста ответа.

#### Structured Outputs (Pydantic)

Гораздо более надёжный подход — использование **Structured Outputs** с Pydantic-моделями. Библиотека [Pydantic](https://docs.pydantic.dev/) позволяет описать точную структуру ожидаемых данных на Python с типизацией, валидацией и описанием полей. Responses API гарантирует, что ответ модели будет соответствовать этой структуре.

Для использования Structured Outputs:
1. Определяется Pydantic-модель с полями, типами и описаниями (`Field(description=...)`).
2. Вместо `client.responses.create()` вызывается `client.responses.parse()` с параметром `text_format=MyModel`.
3. Результат доступен через `response.output_parsed` — это готовый объект Pydantic-модели, который можно преобразовать в словарь через `.dict()` для дальнейшей обработки в Pandas.

Этот подход незаменим для задач массовой обработки данных: извлечения сущностей, классификации, анализа тональности, суммаризации. При обработке сотен записей гарантированная структура вывода позволяет автоматизировать весь конвейер без ручной обработки ошибок парсинга.

### Визуализация и агрегация данных с помощью LLM

После извлечения структурированных данных из большого количества текстов, результаты можно агрегировать и визуализировать стандартными средствами Python — `pandas`, `matplotlib`. Это позволяет, например, построить графики распределения тональности по объектам, сравнить средние оценки по различным критериям или сгенерировать текстовые сводки.

Важным шагом является **LLM-агрегация**: после извлечения отдельных фактов из множества текстов можно снова обратиться к модели, передав ей собранную информацию, и попросить создать обобщающее резюме. Такая двухуровневая обработка — «сначала извлекаем структуру из каждого текста, затем обобщаем по всем текстам» — является мощным паттерном для аналитических задач.

### Мультимодальные модели

Помимо текстовых входных данных, некоторые модели способны принимать на вход **изображения**. Такие модели называются **VLM** — Vision Language Models, и они являются частным случаем **мультимодальных** моделей, способных работать помимо текста с другими модальностями (изображения, звук и т.д.). В Yandex Cloud доступна VLM-модель **Gemma 3**, которая может анализировать содержимое изображений: распознавать текст (OCR), описывать сцены, извлекать информацию из фотографий и диаграмм.

Для передачи изображения модели его необходимо закодировать в формат **base64** и передать в structured input — специальном формате, где сообщение состоит из нескольких частей разного типа:
- `input_text` — текстовая часть запроса (промпт).
- `input_image` — изображение, закодированное в base64 с указанием MIME-типа (`data:image/jpeg;base64,...`).

Мультимодальные модели открывают возможности для множества задач: распознавание документов, анализ графиков и схем, извлечение данных из фотографий, мониторинг визуального контента.

## Практические работы

### 🔬 PaperSummarize.ipynb

В этой лабораторной работе вы возьмете классическую академическую статью "Attention Is All You Need" и используете мощь языковых моделей, чтобы извлечь ее ключевые идеи в идеально организованное резюме. Ваша задача — превратить неструктурированный научный текст в чистое, структурированное знание.

Выполнение этой лабораторной работы вооружит вас мощным инструментом для любой наукоемкой деятельности. Вы овладеете искусством извлечения структурированных данных с помощью Pydantic — навыком, который превращает LLM из простых чат-ботов в точные аналитические движки, способные переваривать и организовывать для вас большие объемы информации.

### 🔬 AgenticImageGeneraton.ipynb

Раскройте своего внутреннего арт-директора и направьте ИИ-художника на создание идеальной картины! Эта лабораторная работа ставит вас во главе агентного цикла генерации изображений, где агент не просто один раз генерирует изображение, а итерационно его уточняет и улучшает, давая творческую обратную связь. Вы заставите одну модель критиковать работу другой и направлять генеративный процесс к лучшему результату.
