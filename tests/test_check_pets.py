from selenium.webdriver.common.by import By



def test_show_al_pets(web_browser):
   web_browser.implicitly_wait(10)
   web_browser.get("http://petfriends.skillfactory.ru/login")
   # Вводим email
   field_email = web_browser.find_element(By.ID, "email")
   field_email.clear()
   field_email.send_keys("PyApiFAS@mail.com")

   # add password
   field_pass = web_browser.find_element(By.ID, "pass")
   field_pass.clear()
   field_pass.send_keys("12345678")

   # click submit button
   btn_submit = web_browser.find_element(By.XPATH, "//button[@type='submit']")
   btn_submit.click()
   assert web_browser.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   images = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')




   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0