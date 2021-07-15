import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Replace the need to manually provide chrome binary path 
from chromedriver_py import binary_path

def main():
    # define the options of our chrome instance 
    chrome_options = Options()

    print("Starting Chrome Browser...")

    # get an instance of the chrome browser and open google.com
    driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)

    driver.get("https://www.google.com")

    #find the search field and send the text before submitting using Enter.
    search_term = "I love automation"
    print(f"Searching for {search_term}.")

    lucky_button = driver.find_element_by_css_selector("[name='q'")
    lucky_button.send_keys(search_term)
    lucky_button.send_keys(Keys.ENTER)



if __name__ == '__main__':
    main()