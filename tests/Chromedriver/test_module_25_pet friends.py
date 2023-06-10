import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(r'C:\Users\liza\PycharmProjects\chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице
   assert pytest.driver.find_element(By.TAG_NAME,'h1').text == "PetFriends"

   # Переходим во вкладку "Мои питомцы", где видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

   #проверяем, что мы оказались на странице с питомцами пользователя
   assert pytest.driver.find_element(By.TAG_NAME,'h2').text == "Чарли"

# тест на то, что присутсвуют все питомцы
def test_all_my_pets_present():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # ожидаем появления заголовка - явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'h1')))

   # Переходим во вкладку "Мои питомцы", где видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

   # находим статистику моих питомцев на странице, находим количество питомцев и сохраняем в переменную
   statistic2 = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]')
   time.sleep(2)
   parts = statistic2.text.split("\n")
   parts2 = parts[1].split(': ')
   # сохраняем в переменную количество питомцев из статистики
   stat_num_of_pets = int(parts2[1])

   #считаем количетсво карточек питомцев на странице (количество строк в таблице в tbody) и сохраняем в переменную pets
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')
   pets = len(pets)
   # проверяем, что количество питомцев из статистики совпадает с количеством карточек на странице
   assert pets == stat_num_of_pets

# тест на то, что хотя бы у половины питомцев есть фото.
def test_more_than_half_photos():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # ожидаем появления заголовка - явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

   # Переходим во вкладку "Мои питомцы", где видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

   # считаем количетсво карточек питомцев на странице (количество строк в таблице в tbody) и сохраняем в переменную pets
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')
   pets = len(pets)

   # вводим переменную для сохранения картинок из карточек питомцев
   images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')

   # вводим переменную счетчик для подсчета карточек с непустыми фото
   count_not_empty_photo = 0
   for i in range(pets):
      if images[i].get_attribute('src') != '':
         count_not_empty_photo += 1
         #return count_not_empty_photo
   #print(count_not_empty_photo)
   #print(pets/2)
   assert count_not_empty_photo >= (pets/2)

# тест на то, что на каждого питомца полностью заполнена карточка с данными
def test_all_pets_have_full_description():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # ожидаем появления заголовка - явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

   # Переходим во вкладку "Мои питомцы", где видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

   # вводим переменную для сохранения отдельных элементов из описаний всех питомцев со страницы
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td')

   for i in range(len(descriptions)):
      assert descriptions[i].text != ''

# тест на уникальность имен всех моих питомцев
def test_check_all_my_pets_names_unique():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # ожидаем появления заголовка - явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

   # устанавливаем неявное ожидание раздела со статистикой при переходе на вкладку Мои питомцы
   pytest.driver.implicitly_wait(10)
   # Переходим во вкладку "Мои питомцы", где видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
   # вводим переменную для сохранения строк таблицы с элементами описаний всех питомцев со страницы
   line_descrip = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr')

   #создаем cсписок, состоящий из имен каждого питомца; чтобы в список не попали данные питомцев, для которых нет установлено имя, ставим условие, что в описании питомца должно быть 3 элемента
   all_names = []
   for i in range(len(line_descrip)):
      parts = line_descrip[i].text.split(' ')
      if len(parts) == 3:
         all_names == all_names.append(parts[0])
   #print(all_names)

   # проводим проверку на уникальнсть элементов в массиве имен Моих питомцев
   for i in range(len(all_names) - 1):
      for j in range(i + 1, len(all_names)):
         assert all_names[i] != all_names[j]

# тест на уникальность всех моих питомцев
def test_check_all_my_pets_unique():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('charliechap@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('BestFriends')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # ожидаем появления заголовка - явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

   # устанавливаем неявное ожидание раздела со статистикой при переходе на вкладку Мои питомцы
   pytest.driver.implicitly_wait(10)
   # Переходим во вкладку "Мои питомцы", где должна быть видна статисктика
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
   # вводим переменную для сохранения строк таблицы с элементами описаний всех питомцев со страницы
   line_descrip = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr')

   # создаем массив из описаний каждого питомцы; каждый элемент массива является в свою очередь массивом из элементов описания питомца
   parts_set = []
   for i in range(len(line_descrip)):
      parts = line_descrip[i].text.split(' ')
      parts_set == parts_set.append(parts)

   # вводим индекс наличия идентичных питомцев. Изначально ему присвоено значение 1, так как мы начинаем сравнивать остальных питомцев относительно одного первого
   identical_pets_index = 0
   for i in range(len(parts_set)-1):
      if len(parts_set[i]) == 3:
         for j in range(i+1, len(parts_set)):
            if len(parts_set[j]) == 3:
               # вводим счетчик, который будет помечать, если у элементов описания двух сравниваемых питомцев будут одинаковые значения
               mark_similar = 0
               print(f'cравниваем {parts_set[i][0]} и {parts_set[j][0]}')
               if parts_set[i][0] == parts_set[j][0]:
                  mark_similar += 1
               print(f'cравниваем {parts_set[i][1]} и {parts_set[j][1]}')
               if parts_set[i][1] == parts_set[j][1]:
                  mark_similar += 1
               print(f'cравниваем {parts_set[i][2]} и {parts_set[j][2]}')
               if parts_set[i][2] == parts_set[j][2]:
                  mark_similar += 1
               if mark_similar == 3:
                  identical_pets_index +=1
                  print('ВНИМАНИЕ! Одинаковые питомцы!!!\n')
   # проверяем, что индекс наличия идентичных питомцев не изменился
   assert identical_pets_index == 0



