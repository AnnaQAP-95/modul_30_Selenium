import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.implicitly_wait(10)  # неявные ожидания
implicitly_waits = driver.find_element_by_xpath('//*[@id="all_my_pets"]/table/tbody') #неявные ожидания

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/new_user')
    yield
    pytest.driver.quit()

def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('torgchel@gmail.com')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_class_name('navbar-toggler-icon').click()
    pytest.driver.find_element_by_xpath('//*[contains(text(),"Мои питомцы")]').click()
    try:
        explicit_waits = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]')))  # явные ожидания
        assert explicit_waits == '//*[@id="all_my_pets"]'
        print('Есть совпадение')
    except TimeoutException:
        print('Нет совпадений')
    finally:
        driver.quit()
        images = pytest.driver.find_elements_by_xpath('//*[id="all_my_pets"]//img')
        names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//body/tr/td[0]')
        descriptions = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody')
        for i in range(len(names)):
            assert images[i].get_attribute('scr') != ''
            assert names[i].text != ''
            assert descriptions[i].text != ''
            assert ',' in descriptions[i].text
            parts = descriptions[i].text.split(", ")
            assert len(parts[0]) > 0
            assert len(parts[1]) > 0
        driver.quit()
