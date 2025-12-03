from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    driver.get("https://www.saucedemo.com/")

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Ajouter au panier (backpack)
    add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_btn.click()

    # Vérifier le badge
    badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert badge.text == "1", "Le badge panier devrait afficher 1 après ajout"

    # Créativité part 1 : vérifier que le bouton est bien passé en 'Remove'
    remove_btn = driver.find_element(By.ID, "remove-sauce-labs-backpack")
    assert remove_btn.is_displayed(), "Le bouton Remove devrait apparaître après ajout au panier"

    driver.save_screenshot("screenshots/F3_add_to_cart.png")

finally:
    driver.quit()
