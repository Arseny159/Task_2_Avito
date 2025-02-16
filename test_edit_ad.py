import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


def test_edit_ad_success(driver):
    """TC_008: Успешное редактирование существующего объявления"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*=css-cwl1kn]'))
    )
    product_card = driver.find_elements(By.CSS_SELECTOR, 'img[class*=css-cwl1kn]')
    product_card[0].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "svg[style*=cursor]"))
    )

    edit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    edit_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )

    title_field = driver.find_element(By.NAME, "name")
    title_field.clear()
    WebDriverWait(driver, 5).until(
        lambda driver: title_field.get_attribute('value') == ""
    )
    title_field.send_keys("Куплю ботинки")

    description_field = driver.find_element(By.NAME, "description")
    description_field.clear()
    WebDriverWait(driver, 5).until(
        lambda driver: description_field.get_attribute('value') == ""
    )
    description_field.send_keys("Только новые")

    submit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    submit_button.click()

    assert "Куплю ботинки" in driver.page_source, "Объявление не отредактировано"
    assert "Только новые" in driver.page_source, "Объявление не отредактировано"


def test_edit_foreign_ad(driver):
    """TC_009: Попытка редактирования чужого объявления"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*=css-cwl1kn]'))
    )
    product_card = driver.find_elements(By.CSS_SELECTOR, 'img[class*=css-cwl1kn]')
    product_card[-1].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class*=css-1p0ye0k]"))
    )

    edit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    edit_button.click()

    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='chakra-alert']"))
        )
        assert "У вас нет прав на редактирование этого объявления" in error_message.text, "Ошибка прав доступа"

    except:
        assert False, "Сообщение об ошибке не появилось" 


def test_edit_ad_title_empty(driver):
    """TC_010: Редактирование объявления с удалением всех символов из заголовка"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*=css-cwl1kn]'))
    )
    product_card = driver.find_elements(By.CSS_SELECTOR, 'img[class*=css-cwl1kn]')
    product_card[-1].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class*=css-1p0ye0k]"))
    )

    edit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    edit_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )

    title_field = driver.find_element(By.NAME, "name")
    title_field.clear()
    WebDriverWait(driver, 5).until(
        lambda driver: title_field.get_attribute('value') == ""
    )

    submit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    submit_button.click()

    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='chakra-alert']"))
        )
        assert "обязательно" in error_message.text.lower(), "Некорректное сообщение об ошибке"

    except:
        assert False, "Сообщение об ошибке не появилось" 


def test_edit_ad_invalid_price_with_symbols(driver):
    """TC_011: Редактирование объявления с вводом некорректной цены (символы, буквы)"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*=css-cwl1kn]'))
    )
    product_card = driver.find_elements(By.CSS_SELECTOR, 'img[class*=css-cwl1kn]')
    product_card[-1].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class*=css-1p0ye0k]"))
    )

    edit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    edit_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )

    price_field = driver.find_element(By.NAME, "price")
    price_field.clear()
    price_field.send_keys("qwertyuioplkjhgfdsazxcvbnm!№;%:?*()_-+[]<>/")

    entered_value = price_field.get_attribute("value")

    submit_button = driver.find_element(By.CSS_SELECTOR, "svg[style*=cursor]")
    submit_button.click()

    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*=chakra-form__error-message]"))
        )
        assert "обязательно" in error_message.text.lower(), "Некорректное сообщение об ошибке"
        assert entered_value == "", "Некорректные символы появились в поле цены"
        assert error_message.is_displayed() == "Цена должна быть числом" \
            or error_message.is_displayed() == "Некорректный формат числа" \
            , "Сообщение непонятно пользователю"

    except:
        assert False, "Сообщение об ошибке не появилось" 