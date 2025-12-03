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

    # Ajouter produit
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    # Aller au panier
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    # Supprimer
    remove_btn = driver.find_element(By.ID, "remove-sauce-labs-backpack")
    remove_btn.click()

    # Vérifier panier vide
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 0, "Le panier devrait être vide après suppression"

    # Créativité : vérifier que le bouton 'Add to cart' réapparaît si on revient à la liste
    driver.find_element(By.ID, "continue-shopping").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    add_btn_again = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    assert add_btn_again.is_displayed(), "Le bouton Add to cart devrait réapparaître après suppression"

    driver.save_screenshot("screenshots/F4_remove_from_cart.png")

finally:
    driver.quit()
