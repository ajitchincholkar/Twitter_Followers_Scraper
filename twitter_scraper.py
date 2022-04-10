import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_followers_and_bio(cardd):
    screen_name = cardd.find_element_by_xpath('./div//span').text
    username = cardd.find_element_by_xpath('.//span[contains(text(), "@")]').text
    i = cardd.text.split("\n").index('Follow')
    bio = cardd.text.split("\n")[i+1:]
    
    user = (screen_name, username, bio)
    return user

# Create instance of the web driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Navigate to login screen
driver.get('https://www.twitter.com/login')
driver.maximize_window()
sleep(5)

username = driver.find_element_by_xpath('//input[@name="text"]')
username.send_keys('your email id here')
username.send_keys(Keys.RETURN)
sleep(10)
username1 = driver.find_element_by_xpath('//input[@name="text"]')
username1.send_keys('your username here')
username1.send_keys(Keys.RETURN)
my_password = getpass()
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
sleep(5)

# Find search input and search for term or user
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys('Username whose followers you want to scrape')
search_input.send_keys(Keys.RETURN)
sleep(5)

driver.find_element_by_link_text('People').click()
sleep(5)
driver.find_element_by_link_text('Username whose followers you want to scrape').click()
sleep(5)

# Opening user's followers list
driver.find_element_by_xpath("//a[@href='/username without @/followers']").click()
sleep(5)

# Get all followers and their bio on the page
followers_list = []
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    cards = driver.find_elements_by_xpath('//div[@data-testid="UserCell"]')
    for card in cards:
        data = get_followers_and_bio(card)
        if data:
            followers_list.append(data)
    
    scroll_attempt = 0
    while True:
        # Check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')   
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # End of scroll region
            if scroll_attempt >= 5:
                scrolling = False
                break
            else:
                sleep(3)  # Attempt to scroll again
        else:
            last_position = curr_position
            break
