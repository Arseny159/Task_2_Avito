##  Данный проект содержит функциональные E2E тесты для сайта Avito, покрывающие следующие сценарии:
1) Создание объявлений
2) Редактирование объявлений
3) Поиск объявлений
##  Технологии
Python
pytest — фреймворк для написания и запуска тестов
Selenium WebDriver — для взаимодействия с браузером
ChromeDriver — драйвер для браузера Google Chrome
##  Установка
###  Клонирование репозитория
git clone [<URL_репозитория>](https://github.com/Arseny159/Task_2_Avito.git)
###  Установка зависимостей
Рекомендуется использовать виртуальное окружение:
python -m venv venv
source venv/bin/activate        # Для MacOS/Linux
venv\Scripts\activate           # Для Windows
###  Установка пакетов:
pip install -r requirements.txt
###  Установка WebDriver
Убедитесь, что у вас установлен браузер Google Chrome.
Скачайте ChromeDriver, соответствующий версии браузера: https://chromedriver.chromium.org/downloads
Добавьте путь к ChromeDriver в системную переменную PATH.
## Запуск тестов
Напишите в терминале команду "pytest" для тестирования файлов test_create_ad.py и test_edit_ad.py
