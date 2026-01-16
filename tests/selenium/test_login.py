from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_login_page_loads():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("http://localhost:5000")
    time.sleep(3)

    assert "Login" in driver.page_source or "Inventory" in driver.page_source

    driver.quit()
