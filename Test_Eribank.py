from appium import webdriver
# from appium.webdriver.common.appiumby import By
from selenium.webdriver.common.by import By
from time import time
from cgitb import text
from h11 import Data
import pytest
from _pytest import mark
from _pytest.mark.structures import Mark
from appium.webdriver.common.touch_action import TouchAction

# Desired capabilites is set depend on device
desired_caps = {
  "appium:appPackage": "com.experitest.ExperiBank",
  "appium:appActivity": "com.experitest.ExperiBank.LoginActivity",
  "platformName": "Android",
  "appium:deviceName": "Pixel 3a API 30",
  "appium:udid": "emulator-5554"
}

# desired_caps ['platformName'] = 'Android'
# desired_caps ['appium:deviceName'] = 'Pixel 3a API 30'
# desired_caps ['appPackcage'] = 'com.experitest.ExperiBank'
# desired_caps ['appActivity'] = 'com.experitest.ExperiBank.LoginActivity'
# desired_caps ['appium:udid'] = 'emulator-5554'

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps) 
driver.implicitly_wait(15)
	
# logintxt = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').text


def test_closepopup():
  pop_up = driver.find_element(By.ID, 'android:id/button1')
  pop_up.click()
  driver.implicitly_wait(5)
  
  logintxt = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').text
  assert logintxt == "Login"


login_invalid_data =[
  ("",""), #empty username, empty password
  ("com","company"), #wrong username, correct password
  ("company","com") #correct username, wrong password
  ]

@pytest.mark.parametrize('username,password',login_invalid_data)
def test_invalid_login(username,password):
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/usernameTextField').click()
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/usernameTextField').send_keys(username)
  driver.implicitly_wait(5)
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/passwordTextField').click()
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/passwordTextField').send_keys(password)
  driver.implicitly_wait(5)
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').click()
  driver.find_element(By.ID, 'android:id/button3').click()

  logintxt = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').text
  assert logintxt == "Login"

def test_login():
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/usernameTextField').click()
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/usernameTextField').send_keys('company')
  driver.implicitly_wait(5)
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/passwordTextField').click()
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/passwordTextField').send_keys('company')
  driver.implicitly_wait(5)
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').click()
  payment = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/makePaymentButton').text
  assert payment == "Make Payment"




@pytest.fixture
def precondition_payment():
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/makePaymentButton').click()
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/phoneTextField').send_keys('08226634')
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/nameTextField').send_keys('Kristian Pratama')
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/amountTextField').send_keys('20')
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/countryTextField').send_keys('Indonesia')
  # driver.swipe(500, 1600, 500, 600, 400)
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/sendPaymentButton').click()

def test_send_payment(precondition_payment):
  driver.find_element(By.ID, 'android:id/button1').click()
  final_amount = driver.find_element(By.CLASS_NAME,'android.view.View').text
  assert final_amount == "Your balance is: 80.00$"

def test_cancel_payment(precondition_payment):
  driver.find_element(By.ID, 'android:id/button2').click()
  sendPaymentButton = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/sendPaymentButton').text
  assert sendPaymentButton == "Send Payment"

def test_close_payment_page():
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/cancelButton').click()
  final_amount = driver.find_element(By.CLASS_NAME,'android.view.View').text
  assert final_amount == "Your balance is: 80.00$"

def test_logout():
  driver.find_element(By.ID, 'com.experitest.ExperiBank:id/logoutButton').click()
  logintxt = driver.find_element(By.ID, 'com.experitest.ExperiBank:id/loginButton').text
  assert logintxt == "Login"  