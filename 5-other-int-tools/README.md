# Раздел 5: Дополнительные встроенные инструменты

## Обзор

В этом разделе мы изучаем дополнительные встроенные инструменты Yandex AI Studio для агентных сценариев: 

* **Code Interpreter** - позволяет модели выполнять Python-код, работать с файлами, таблицами и графиками в изолированном контейнере. 
* **Image Generation Tool** - позволяет агенту не просто написать промпт для картинки, а самостоятельно вызвать генерацию изображения при необходимости.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| ✏️ | [CodeInterpreter.ipynb](CodeInterpreter.ipynb) | Code Interpreter: простой inline-инструмент на `exec`, затем встроенный контейнер с Excel-файлом, pandas и графиком плотности населения городов | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/CodeInterpreter.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FCodeInterpreter.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/CodeInterpreter.ipynb) |
| ✏️ | [ImageGeneration.ipynb](ImageGeneration.ipynb) | Image Generation Tool: агент превращает короткую концепцию в изображение, оценивает результат через Qwen3.6 и улучшает промпт | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/ImageGeneration.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FImageGeneration.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/ImageGeneration.ipynb) |
| 🔬 | [DataAnalysis-Solution.ipynb](Labs/DataAnalysis-Solution.ipynb) | Полное решение лабораторной работы: анализ датасета рынка труда с помощью Code Interpreter | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/Labs/DataAnalysis-Solution.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FLabs%2FDataAnalysis-Solution.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/Labs/DataAnalysis-Solution.ipynb) |

## Теоретический материал

### Зачем нужен Code Interpreter

LLM хорошо формулируют план анализа и объясняют результаты, но арифметика, табличные операции и визуализация должны выполняться воспроизводимым кодом. Встроенный [Code Interpreter](https://yandex.cloud/ru/docs/ai-studio/concepts/agents/tools/code-interpreter) решает эту задачу как hosted tool: Responses API запускает Python-код в контейнере, а клиент получает финальный ответ и созданные файлы.

В учебном ноутбуке мы сначала показываем минимальный аналог такого инструмента через Function Calling: модель пишет Python-код, а локальная функция выполняет его через `exec` и возвращает переменную `result`. Это помогает понять механику: модель не считает сама, а делегирует вычисление инструменту. После этого мы переходим к настоящему Code Interpreter, который умеет работать с загруженным Excel-файлом, считать новую колонку и сохранять графики.

### Контейнеры и файлы

Для работы с файлами используется явный контейнер:

```python
file = client.files.create(file=open("data.xlsx", "rb"), purpose="assistants")
container = client.containers.create(
    name="analysis-demo",
    expires_after={"anchor": "last_active_at", "minutes": 20},
    file_ids=[file.id],
)
```

Затем контейнер передаётся в инструмент:

```python
tools=[{"type": "code_interpreter", "container": container.id}]
```

Чтобы увидеть код, который выполнила модель, удобно добавлять `include=["code_interpreter_call.outputs"]`. Если модель прикладывает файлы к ответу, их можно скачать через `client.files.content(file_id)`.

### Image Generation Tool

Ещё одним встроенным инструментов агентов в AI Studio является [инструмент генерации изображений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/image-generation.html) - он позволяет добавить генерацию прямо в вызов Responses API, позволяя избежать отдельного кода для вызова `client.image.create` для генерации изображений. Для использования инструмента передаём в Responses API такое описание инструмента:

```python
tools=[{"type": "image_generation", "size": "1024x1024"}]
```

Полученные изображения затем можно достать из поля `outputs` ответа.

## Практические работы

### 🔬 DataAnalysis.ipynb

В лабораторной работе анализируется файл [`data/job_market_salary_trends.csv`](data/job_market_salary_trends.csv): зарплаты, категории вакансий, страны, формат работы, уровень опыта, использование AI-инструментов и показатели удовлетворённости. Задача - использовать LLM для автоматизации обработки данных с помощью генерации кода.
