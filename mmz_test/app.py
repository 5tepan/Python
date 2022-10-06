from lib2to3.pgen2 import driver
from selenium import webdriver


driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
driver.get('file:///D:/PYprog/1/index.html')

a = driver.find_elements("sss")
print(a)

