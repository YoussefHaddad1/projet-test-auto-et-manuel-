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

    # Ajouter un produit au panier
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    # Checkout
    driver.find_element(By.ID, "checkout").click()

    # Formulaire
    driver.find_element(By.ID, "first-name").send_keys("Alaeddine")
    driver.find_element(By.ID, "last-name").send_keys("Jeridi")
    driver.find_element(By.ID, "postal-code").send_keys("1000")
    driver.find_element(By.ID, "continue").click()

    # Créativité : vérifier le total avant de finaliser
    total_label = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))
    )
    assert "Total" in total_label.text, "Le label du total n'est pas affiché correctement"

    # Finaliser la commande
    driver.find_element(By.ID, "finish").click()

    success = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "thank you for your order" in success.text.lower(), "Le message de confirmation de commande est incorrect"


    driver.save_screenshot("screenshots/F6_checkout.png")

finally:
    driver.quit()
