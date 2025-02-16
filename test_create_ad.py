import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link = "http://tech-avito-intern.jumpingcrab.com/"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("http://tech-avito-intern.jumpingcrab.com/")
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def reset_state(driver):
    yield
    driver.get("http://tech-avito-intern.jumpingcrab.com/")


def test_create_ad_success(driver):
    """TC_001: Успешное создание объявления с валидными данными"""
    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам отличный велосипед")
    price_field.send_keys("15000")
    description_field.send_keys("В отличном состоянии, почти новый!")
    image_url_field.send_keys("https://avatars.mds.yandex.net/get-mpic/96484/img_id4004763490218087115/600x800")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    assert "Продам отличный велосипед" in driver.page_source, "Объявление не создано"
    assert "15000" in driver.page_source, "Объявление не создано"
    assert "В отличном состоянии, почти новый!" in driver.page_source, "Объявление не создано"
    assert "avatars.mds.yandex.net/get-mpic/96484/img_id4004763490218087115/600x800" in driver.page_source, "Объявление не создано"


def test_create_ad_empty_fields(driver):
    """TC_002: Попытка создания объявления с пустыми полями"""
    
    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    error_message = driver.find_element(By.CSS_SELECTOR, "div[class*=chakra-form__error-message]")

    assert error_message.is_displayed(), "Сообщение об ошибке не отображается"
    assert "обязательно" in error_message.text.lower(), "Некорректное сообщение об ошибке"


def test_create_ad_invalid_price(driver):
    """TC_003: Попытка создания объявления с ценой, содержащей символы"""

    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам отличный диван")
    price_field.send_keys("qwertyuioplkjhgfdsazxcvbnm!№;%:?*()_-+[]<>/")
    description_field.send_keys("В хорошем состоянии!")
    image_url_field.send_keys("https://santreyd.ru/upload/staff/upload/staff/vplate/all_photos/b20504d232c585014b9da55329cc447ed26278bf.jpg")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    entered_value = price_field.get_attribute("value")

    error_message = driver.find_element(By.CSS_SELECTOR, "div[class*=chakra-form__error-message]")

    assert entered_value == "", "Некорректные символы появились в поле цены"
    assert error_message.is_displayed() == "Цена должна быть числом" \
        or error_message.is_displayed() == "Некорректный формат числа" \
        , "Сообщение непонятно пользователю"
    assert "обязательно" in error_message.text.lower(), "Некорректное сообщение об ошибке"


def test_create_ad_invalid_price_multiple_dots(driver):
    """TC_004: Попытка создания объявления с ценой, содержащей несколько точек"""

    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам хороший ноутбук!!!")
    price_field.send_keys("1.2.3")
    description_field.send_keys("Состояние нового, использовался редко!")
    image_url_field.send_keys("https://frankfurt.apollo.olxcdn.com/v1/files/fm1e02ol2qvv2-KZ/image")

    corrected_value = price_field.get_attribute("value")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    assert corrected_value == "1,23" or corrected_value == "1.23", f"Цена была исправлена некорректно, ожидали: '1.23', получили: {corrected_value}"
    assert "Продам хороший ноутбук!!!" in driver.page_source, "Объявление не было создано"


def test_create_ad_invalid_price_multiple_commas(driver):
    """TC_005: Попытка создания объявления с ценой, содержащей несколько запятых"""

    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам хороший плеер")
    price_field.send_keys("1,2,4")
    description_field.send_keys("Состояние хорошее")
    image_url_field.send_keys("https://www.123.ru/xl_pics/8847771.jpg")

    corrected_value = price_field.get_attribute("value")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    assert corrected_value == "1,24" or corrected_value == "1.24", f"Цена была исправлена некорректно, ожидали: '1.24', получили: {corrected_value}"
    assert "Продам хороший плеер" in driver.page_source, "Объявление не было создано"


def test_create_ad_invalid_price_dots_and_commas(driver):
    """TC_006: Попытка создания объявления с ценой, содержащей точки и запятые"""
    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам замечательное ведро")
    price_field.send_keys("1.2,5")
    description_field.send_keys("Железное")
    image_url_field.send_keys("https://avatars.mds.yandex.net/get-mpic/4355034/img_id6127460495383306953.jpeg/orig")

    corrected_value = price_field.get_attribute("value")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    assert corrected_value == "1,25" or corrected_value == "1.25", f"Цена была исправлена некорректно, ожидали: '1.25', получили: {corrected_value}"
    assert "Продам замечательное ведро" in driver.page_source, "Объявление не было создано"


def test_create_ad_invalid_price_negative(driver):
    """TC_007: Попытка создания объявления с отрицательной ценой"""
    create_ad_link = driver.find_element(By.XPATH, "//button[text()='Создать']")
    create_ad_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header[class*=chakra-modal__header]"))
    )

    title_field = driver.find_element(By.NAME, "name")
    price_field = driver.find_element(By.NAME, "price")
    description_field = driver.find_element(By.NAME, "description")
    image_url_field = driver.find_element(By.NAME, "imageUrl")

    title_field.send_keys("Продам замечательный телевизор")
    price_field.send_keys("-1")
    description_field.send_keys("Дисплей без выгораний")
    image_url_field.send_keys("https://ogo1.ru/upload/iblock/075/0756b7e1ddfc8dd878eb06dc58f526bd.jpeg")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[class*=css-u6bxse]")
    submit_button.click()

    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='chakra-alert']"))
        )
        assert "Цена должна быть неотрицательным числом" in error_message.text, "Сообщение об ошибке не отображается или неверно"

    except:
        assert False, "Сообщение об ошибке не появилось"
    




