# Раздел 3: Function Calling (Tool Calling)

## Обзор

В этом разделе мы изучаем механизм **Function Calling** (вызов функций), который позволяет LLM взаимодействовать с внешними инструментами. Мы рассматриваем два способа определения инструментов — через JSON Schema и через **Pydantic**, строим универсальный класс `Agent` и создаём исследовательского агента для работы с arXiv API.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| 📖 | [Вызов инструментов][LectFunctionCalling] | Изучаем, как можно расширить LLM дополнительными инструментами, и как упростить реализацию с помощью pydantic | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectFunctionCalling] |
| ✏️ | [ToolCalling.ipynb](ToolCalling.ipynb) | Основы Function Calling на примере калькулятора: работа с JSON Schema и Pydantic | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/ToolCalling.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FToolCalling.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/ToolCalling.ipynb) |
| ✏️ | [ArxivResearch.ipynb](ArxivResearch.ipynb) | Исследовательский агент для arXiv: поиск статей, Pydantic-инструменты, веб-поиск | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/ArxivResearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FArxivResearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/ArxivResearch.ipynb) |
| 🔬 | [GrapherTool.ipynb](Labs/GrapherTool.ipynb) | Агент-аналитик с построением графиков — создание агента, который строит графики по запросу и извлекает данные из текста | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/Labs/GrapherTool.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FLabs%2FGrapherTool.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/Labs/GrapherTool.ipynb) |
| 🔬 | [AgentDrawing.ipynb](Labs/AgentDrawing.ipynb) | Агент-художник с Turtle Graphics — управление черепашкой через Function Calling | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/Labs/AgentDrawing.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FLabs%2FAgentDrawing.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/Labs/AgentDrawing.ipynb) |

[LectFunctionCalling]: https://disk.yandex.ru/d/ouAHZ-tAkJ1LLA

## Теоретический материал

### Зачем нужен Function Calling

Языковые модели превосходно справляются с генерацией текста, рассуждениями и анализом, но у них есть принципиальные ограничения: они **не умеют точно считать**, **не имеют доступа к внешним сервисам** и **не знают актуальных данных** за пределами обучающей выборки. Механизм [Function Calling](https://yandex.cloud/ru/docs/ai-studio/concepts/tools/function-calling) (также называемый Tool Calling) решает эту проблему, позволяя модели вызывать доступные ей внешний инструменты для выполнения таких функций.

Ключевой принцип: **модель сама решает**, когда и какую функцию вызвать, и **формирует аргументы** вызова на основе запроса пользователя. При этом модель не выполняет функцию самостоятельно — она лишь сообщает клиентскому коду, что хочет вызвать определённую функцию с определёнными аргументами.

### Как работает Function Calling

Полный цикл Function Calling выглядит следующим образом:

1. **Описание инструментов.** При вызове Responses API клиент передаёт описания доступных функций — их названия, описания и параметры.
2. **Анализ запроса.** LLM анализирует запрос пользователя и решает, нужно ли вызвать какую-либо функцию.
3. **Запрос вызова.** Если функция нужна, модель возвращает объект `function_call` с именем функции и JSON-аргументами, а также уникальным `call_id`.
4. **Выполнение.** Клиентский код выполняет функцию локально и получает результат.
5. **Передача результата.** Результат отправляется обратно модели в виде объекта `function_call_output` с соответствующим `call_id`.
6. **Финальный ответ.** Модель формулирует окончательный ответ пользователю, используя результат функции.

Этот цикл может повторяться многократно: модель может вызывать несколько функций последовательно (или даже параллельно), анализируя промежуточные результаты и принимая решения о дальнейших действиях. Это создаёт **цикл взаимодействия LLM ↔ инструменты**, который лежит в основе агентских систем.

### Описание инструментов: JSON Schema

Первый способ описания инструментов — через **JSON Schema**. Каждый инструмент описывается словарём с полями:
- `type: "function"` — тип инструмента.
- `name` — имя функции.
- `description` — описание того, что делает функция (LLM использует это для принятия решений).
- `parameters` — JSON Schema параметров: типы, описания, обязательные поля.

Качественное описание инструмента критически важно: модель принимает решение о вызове функции исключительно на основе текстовых описаний в `description` и описаний параметров.

### Описание инструментов: Pydantic

Для больших проектов удобнее использовать библиотеку [Pydantic](https://docs.pydantic.dev/) для описания инструментов. В этом случае каждый инструмент описывается как Pydantic-класс, где:
- **Документация класса** (docstring) используется как описание функции.
- **Поля модели** с типами и `Field(description=...)` описывают параметры.
- **Метод `execute()`** содержит реализацию функции.
- Метод `model_json_schema()` автоматически генерирует JSON Schema из определения класса.

Преимущества Pydantic-подхода:
- **Меньше ручного кода** — схема генерируется автоматически.
- **Автоматическая валидация** — входные данные проверяются при создании объекта.
- **Синхронизация** — код и схема всегда согласованы, так как создаются из одного источника.
- **Типизация** — полная поддержка IDE (автодополнение, проверка типов).

### Универсальный класс Agent

Цикл Function Calling удобно поместить внутрь некоторого универсального класса `Agent`, который автоматизирует весь процесс взаимодействия с инструментами. Класс принимает список Pydantic-моделей, автоматически генерирует JSON Schema для каждого из них, и в цикле обрабатывает вызовы функций, пока модель не выдаст финальный текстовый ответ.

Этот паттерн — **основа агентских систем**: агент получает задачу, планирует действия, вызывает нужные инструменты, анализирует результаты и формирует ответ. Один и тот же класс Agent можно использовать с любым набором инструментов: калькулятором, API научных статей, базами данных, веб-сервисами.

### Работа с arXiv API

Практическое применение Function Calling демонстрируется на примере создания **агента-исследователя**, работающего с [arXiv](https://arxiv.org/) — крупнейшим открытым репозиторием научных препринтов. Агент использует два инструмента:

- **`search_arxiv`** — поиск статей по ключевым словам с фильтрацией по полям (заголовок, аннотация, автор).
- **`get_paper_details`** — получение полной информации о статье по её уникальному arXiv ID.

arXiv предоставляет бесплатный API, возвращающий данные в формате Atom XML. Библиотека `feedparser` используется для разбора результатов. Поиск поддерживает различные префиксы полей (`ti:` — заголовок, `au:` — автор, `abs:` — аннотация, `all:` — все поля) и логические операторы `AND`, `OR`, `ANDNOT`.

Агент-исследователь объединяет эти инструменты с LLM: получает тему от пользователя, формирует поисковые запросы на английском языке, находит релевантные статьи, запрашивает подробности и составляет аналитическое резюме на русском.

## Практические работы

### 🔬 GrapherTool.ipynb

Превратите ваш ИИ в аналитика данных, который умеет оживлять цифры! В этой лабораторной работе ваша миссия — создать агента, способного не только понимать данные, разбросанные по тексту, но и визуализировать их. Вы вооружите своего агента инструментом `Grapher`, который позволит ему создавать наглядные диаграммы и графики прямо из неструктурированной статьи.

### 🔬 AgentDrawing.ipynb

Станьте программистом, который управляет роботом-художником с помощью простого русского языка! Эта лабораторная работа предлагает вам управлять классическим 'черепашьим пером' с помощью естественных команд. Вы создадите агента, который будет переводить ваши инструкции — например, "нарисуй дом с крышей" — в последовательность конкретных команд для рисования, которые черепашка выполнит на экране прямо у вас на глазах.

Это невероятно увлекательное упражнение научит вас основам вызова функций (Function Calling) в наглядной и интерактивной форме. Вы узнаете, как определять набор инструментов, соответствующих реальным действиям, и увидите, как ваш агент воплощает ваши слова в жизнь. А также поймёте, что современные модели пока что не могут достичь уверенного результата в таких казалось бы несложных задачах.
