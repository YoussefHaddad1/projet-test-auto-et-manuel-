from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # ---- Cas 1 : Utilisateur bloqué ----
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )

    # Créativité : vérification du message EXACT
    expected_msg_locked = "Epic sadface: Sorry, this user has been locked out."
    assert error1.text == expected_msg_locked, "Le message d'erreur pour locked_out_user ne correspond pas exactement"

    driver.save_screenshot("screenshots/F2_locked_out_user.png")

    # ---- Cas 2 : Mauvais mot de passe ----
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )

    # Créativité : vérifier au moins le préfixe commun
    assert "Epic sadface:" in error2.text, "Le message d'erreur attendu n'est pas affiché pour mot de passe incorrect"

    driver.save_screenshot("screenshots/F2_wrong_password.png")

finally:
    driver.quit()
