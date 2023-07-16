from selenium.webdriver.common.by import By
from toolz import partition
import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from conftest import my_email, my_password, my_nickname
import re

@pytest.fixture(autouse=True)
def testing(web_browser):
        web_browser.get("http://petfriends.skillfactory.ru/login")
        # Вводим email
        field_email = WebDriverWait(web_browser, 10).until(ec.presence_of_element_located((By.ID, "email")))
        field_email.clear()
        field_email.send_keys(my_email)

        # Водим password
        field_pass = WebDriverWait(web_browser, 10).until(ec.presence_of_element_located((By.ID, "pass")))
        field_pass.clear()
        field_pass.send_keys(my_password)

        # click submit button
        btn_submit = WebDriverWait(web_browser, 10).until(ec.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        btn_submit.click()
        # Убедимся что мы на нужной странице
        assert web_browser.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

        btn_MyPets = WebDriverWait(web_browser, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div#navbarNav > ul > li > a")))
        # web_browser.find_element(By.CSS_SELECTOR, "div#navbarNav > ul > li > a")
        btn_MyPets.click()
        # Убедимся что мы на нужной странице
        assert web_browser.find_element(By.CSS_SELECTOR, "html > body > div > div > div > h2").text == my_nickname


def test_num_my_pets(web_browser):
    web_browser.implicitly_wait(10)
    # Получаем информацию из карточки пользователя
    user_info = web_browser.find_element(By.CSS_SELECTOR, "html > body > div > div > div").text
    # Полученную информацию переводим в список
    user_info1 = re.split('\n|:', user_info)
    # Из списка получаем нужную нам информацию о  колличчестве питомцов и переводим ее в целочисленное значение
    num_pets = int(user_info1[2])
    # Получам список из карточек питомцев
    all_my_pets = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Сравниваем полученное число питомцев из карточки пользователя с колличеством элемнтов списка карточек питомцев
    assert num_pets == len(all_my_pets)



def test_Foto_my_pets(web_browser):
    web_browser.implicitly_wait(10)
    # Получам список из карточек питомцев
    all_my_pets = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Получам список фото из карточек питомцев
    images = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    # Создаем счетчик для питомцев с фото
    count_foto = 0
    # Создаем счетчик для питомцев без фото
    count_nullfoto = 0
    # При помощи цикла из списка фото узнаем значение каждого элемента
    for i in range(len(all_my_pets)):
        # Если значение не пустое увеличиваем счетчик питоцев с фото на один
        if images[i].get_attribute('src') != '':
            count_foto = count_foto + 1
        # Иначе увеличиваем счетчик питоцев без фото на один
        else:
            count_nullfoto = count_nullfoto +1
    # Сравниваем полученные значения счетчиков чтобы проверить, что у не менее половины питомцев есть фото
    assert count_foto >= count_nullfoto

#




def test_neededAtributes_my_pets(web_browser):
    web_browser.implicitly_wait(10)
    # Создаем список атрибутов из карточек питомцев для всех питомцев
    all_my_pets_atr = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td')
    # Созадем список значений этих атрибутов
    all_pets_data = [pet.text for pet in all_my_pets_atr]
    # Удаляем все значения "х"
    del all_pets_data[3::4]
    # При помощи цикла из полученного списка получаем значение каждого атрибута и проверяем что оно не пустое
    for i in all_pets_data:
        assert all_pets_data != ''

def test_differntNames_my_pets(web_browser):
    web_browser.implicitly_wait(10)
    # Создаем список атрибутов из карточек питомцев для всех питомцев
    all_my_pets_atr = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td')
    # Созадем список значений этих атрибутов
    all_pets_data = [pet.text for pet in all_my_pets_atr]
    # Созадем новый список состоящий только из имен питомцев
    names_pets = all_pets_data[::4]
    # Проверяем что у всех питомцев разные имена
    assert len(set(names_pets)) == len(names_pets)

def test_differntPets_my_pets(web_browser):
    web_browser.implicitly_wait(10)
    # Создаем список атрибутов из карточек питомцев для всех питомцев
    all_my_pets_atr = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td')
    # Созадем список значений этих атрибутов
    all_pets_data = [pet.text for pet in all_my_pets_atr]
    # Удаляем все значения "х"
    del all_pets_data[3::4]
    # Создаем новый список из списка атрибутов, в котором каждый элемент будет содержать инофрмацию об одном питомце
    # состоящию из его имени, прорды и возраста
    l = all_pets_data
    n = 3
    prts_atr = list(partition(n, l))
    # Проверяем что нет повторяющихся питомцев
    assert len(set(prts_atr)) == len(prts_atr)
