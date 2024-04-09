from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

#driver_path = './chromedriver.exe'   # 본인의 chromedriver 경로를 넣어줍니다.

# 크롬 옵션을 설정해줍니다.
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('window-size=1920x1080')

# 웹 드라이버에 service와 option값을 전달
#s = Service(driver_path)
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get('https://www.naver.com')  # url에는 본인이 열고자하는 웹페이지 주소를 넣어주세요
driver.find_element(By.ID, 'query').send_keys('크롤링')

time.sleep(2)