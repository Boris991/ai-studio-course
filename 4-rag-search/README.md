# Раздел 4: RAG и поиск

## Обзор

В этом разделе мы изучаем два встроенных инструмента Responses API для расширения знаний LLM: **Web Search** (поиск в интернете) и **File Search** (поиск по загруженным документам). Мы создаём персональную базу знаний на основе научных статей, сравниваем подходы RAG и Tool Calling, а также учимся интегрировать агента с Telegram-ботом.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| 📖 | [Файловый поиск (RAG) и веб-поиск][LectSearch] | Учимся расширять модели с помощью втроенных в Responses API инструментов поиска | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectSearch] |
| ✏️ | [WebSearch.ipynb](WebSearch.ipynb) | Web Search: поиск в интернете, суммаризация новостей, конкурентный анализ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/WebSearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FWebSearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/WebSearch.ipynb) |
| ✏️ | [FileSearch.ipynb](FileSearch.ipynb) | File Search: создание базы знаний из файлов, Vector Store, Telegram-бот | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/FileSearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FFileSearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/FileSearch.ipynb) |
| 🔬 | [OpenAlexLab.ipynb](Labs/OpenAlexLab.ipynb) | RAG vs Tool Calling — сравнение подходов на базе подмножества научных статей из OpenAlex | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/Labs/OpenAlexLab.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FLabs%2FOpenAlexLab.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/Labs/OpenAlexLab.ipynb) |

[LectSearch]: https://disk.yandex.ru/d/_ji2zdWwYiRQgg

## Теоретический материал

### Проблема актуальности знаний и RAG

Языковые модели обучаются на конечном наборе данных и имеют **дату отсечки знаний** — они не знают о событиях, произошедших после обучения. Кроме того, LLM не имеют доступа к приватным данным организации: внутренним документам, базам знаний, корпоративным файлам. Для решения этих проблем используется подход **RAG — Retrieval-Augmented Generation** (генерация, дополненная поиском).

Суть RAG: перед тем как генерировать ответ, система с помощью вызова инструмента **ищет релевантную информацию** во внешних источниках и **добавляет найденные фрагменты в контекст** запроса к модели. Таким образом, модель отвечает не только на основе своих «встроенных» знаний, но и с опорой на актуальные данные.

> **Важно:** во многих случаях, когда заказчики говорят «давайте дообучим нейросеть на нашу предметную область», на самом деле речь идёт именно о добавлении RAG, а не о дообучении модели. RAG — это значительно более простой, быстрый и контролируемый способ дать модели новые знания.

Responses API поддерживает два встроенных инструмента для реализации RAG: **Web Search** и **File Search**.

### Web Search — поиск в интернете

Инструмент **[Web Search](https://yandex.cloud/ru/docs/ai-studio/concepts/tools/search)** позволяет агенту искать актуальную информацию в интернете через Yandex Search. В отличие от ручного Function Calling, где клиент должен самостоятельно обрабатывать вызовы функций, Web Search — это **hosted tool**: Responses API самостоятельно выполняет поиск и возвращает уже окончательный результат работы модели.

Инструмент настраивается минимальным описанием:
```python
web_search_tool = {
    "type": "web_search",
    "search_context_size": "high"  # low/medium/high — объём контекста
}
```

Можно также ограничивать поиск определёнными фильтрами. Доступные параметры фильтрации:
- **`search_context_size`** — объём контекста из найденных страниц (`low`, `medium`, `high`). Больший контекст даёт более подробные ответы, но увеличивает потребление токенов.
- **`filters.allowed_domains`** — ограничение поиска конкретными доменами (до 5 штук). Например, `["arxiv.org"]` для поиска только научных статей.
- **`filters.user_location.region`** — код региона для локализации результатов.

В структуре ответа Responses API содержится информация о поисковом запросе, который модель сформировала автоматически (доступно через `res.output[0].action.query`), что полезно для отладки и понимания логики агента.

Типичные применения Web Search: создание новостных обзоров, конкурентный анализ, мониторинг трендов, ответы на вопросы, требующие актуальных данных.

### File Search — поиск по документам

Инструмент **[File Search](https://yandex.cloud/ru/docs/ai-studio/concepts/tools/searchindex)** реализует полноценный RAG-конвейер для поиска по загруженным документам. Архитектура включает три компонента:

1. **Загрузка файлов** (`client.files.create`) — файлы (PDF, TXT и другие форматы) загружаются в облако Yandex Cloud. Каждый файл получает уникальный идентификатор.

2. **Векторное хранилище** ([Vector Store](https://yandex.cloud/ru/docs/ai-studio/concepts/searchindex)) — специализированный индекс для семантического поиска. При добавлении файла в хранилище (`client.vector_stores.files.create`) происходит:
   - **Конвертация** — PDF и другие форматы преобразуются в текст.
   - **Чанкование** — длинные документы разбиваются на фрагменты (чанки) с перекрытием. Параметры чанкования (`max_chunk_size_tokens`, `chunk_overlap_tokens`) позволяют настроить баланс между детализацией и покрытием. Перекрытие необходимо, чтобы информация, попадающая на границу двух чанков, не терялась.
   - **Индексирование** — для каждого чанка вычисляется эмбеддинг-вектор, который помещается в индекс для быстрого семантического поиска.

3. **Гибридный поиск** — при запросе используется комбинация **векторного поиска** (по эмбеддинг-векторам, находящего семантически схожие фрагменты) и **поиска по ключевым словам** (находящего точные совпадения терминов). Такая комбинация обеспечивает наилучшее качество: векторный поиск улавливает смысловую близость, а поиск по ключевым словам — конкретные термины и имена.

Параметр `rewrite_query=True` при поиске позволяет модели перефразировать запрос, повышая разнообразие и полноту найденных фрагментов.

Для использования File Search в качестве инструмента агента достаточно описать его аналогично Web Search:
```python
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [vector_store.id],
    "max_num_results": 5
}
```

### Универсальный класс Agent

Файл [`Agent.py`](Agent.py) в этом разделе содержит расширенную версию класса `Agent`, которая поддерживает три типа инструментов одновременно:
- **Pydantic-классы** — локальные функции, описанные через Pydantic-модели (из раздела 3).
- **Словарные описания** — встроенные инструменты Responses API (`web_search`, `file_search`), описанные как JSON-словари.
- **MCP-инструменты** — инструменты, доступные через Model Context Protocol, о которых мы поговорим позднее в курсе.

Такая универсальность позволяет создавать агентов, которые одновременно ищут в интернете, обращаются к базе документов, вызывают внешние API через MCP, а также используют локальные функции для обработки данных.

> Для удобства класс `Agent` оформлен в виде отдельного Python-файла. Мы будем пере-использовать этот класс в дальнейших уроках. Вы можете использовать его же при выполнении практических заданий.

### Интеграция с Telegram-ботом

Практическое применение File Search демонстрируется через интеграцию с **Telegram-ботом** на базе библиотеки [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/). Бот позволяет загружать новые документы (PDF, TXT) в базу знаний прямо из чата Telegram и задавать вопросы по содержимому загруженных статей. Это демонстрирует, как агентские системы могут быть интегрированы в привычные мессенджеры для создания удобных интерфейсов работы с корпоративными знаниями.

## Практические работы

### 🔬 OpenAlexLab.ipynb

В этой лабораторной работе вы исследуете два разных способа наделения ИИ знаниями об обширной базе данных научных статей. Вы настроите RAG-систему на основе файлового поиска, а также специальный поисковый инструмент на основе Function Calling, чтобы сравнить результаты и понять, какой подход одержит победу при ответах на сложные аналитические вопросы.

Этот критически важный эксперимент даст вам практическое понимание компромиссов между RAG и вызовом функций. Вы разовьете интуицию, необходимую для выбора правильной архитектуры для ваших собственных проектов, и научитесь определять, когда стоит полагаться на "размытую" мощь семантического поиска, а когда — создавать точные, кастомные инструменты для структурированных данных.
