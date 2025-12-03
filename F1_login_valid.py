from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialisation du navigateur via webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

def log(step):
    print(f"[LOG] {step}")

log("STARTING TEST")

try:
    log("Opening browser")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    log("Navigating to login page")
    driver.get("https://www.saucedemo.com/")

    log("Typing username")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")

    log("Typing password")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    log("Clicking login button")
    driver.find_element(By.ID, "login-button").click()

    log("Waiting for inventory page")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    log("Login successful")
    print("[PASS] TEST OK")

except Exception as e:
    print("[FAIL] ERROR OCCURRED")
    print(str(e))
    driver.save_screenshot("error.png")

finally:
    log("Closing browser")
    driver.quit()
    log("END OF TEST")
