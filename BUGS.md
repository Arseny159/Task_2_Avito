1) Заголовок: Ввод отрицательных чисел в поле "Цена"
2) ID: BR-001
3) Проект: Авито
4) Окружение:
        Операционная система: Windows 10
        Время тестирования: 16 февраля 2025, 05:41
5) Статус дефекта: Открыт
6) Серьезность дефекта: S3 — Значительная (Major)
7) Приоритет дефекта: Средний
8) Шаги для воспроизведения:
        Зайти на сайт http://tech-avito-intern.jumpingcrab.com/
        Нажать на кнопку "Создать"
        Ввести значение -1 в поле "Цена"
        Заполнить остальные поля любыми данными удобными для поиска
        В поиске найти добавленный товар
10) Фактический результат: Цена товара может быть отрицательной
11) Ожидаемый результат: Цена товара НЕ может быть отрицательной ни в каком случае.
12) Классификация дефекта (хэштег): #Logic
13) Тестировщик: Арсений Попов
