from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

print("[START] F5_checkout_error_user")

try:
    print("Opening browser and navigating to SauceDemo...")
    driver.get("https://www.saucedemo.com/")

    # Login avec l'utilisateur error_user (comportement buggé connu)
    print("Logging in with error_user ...")
    driver.find_element(By.ID, "user-name").send_keys("error_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    print("Login successful, inventory page displayed.")

    # Ajouter un produit au panier
    print("Adding 'Sauce Labs Backpack' to cart...")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )
    print("Cart page opened with at least one item.")

    # Aller au checkout
    driver.find_element(By.ID, "checkout").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    print("Checkout: Your Information page opened.")

    # Tentative de remplir les champs
    first = driver.find_element(By.ID, "first-name")
    last = driver.find_element(By.ID, "last-name")
    postal = driver.find_element(By.ID, "postal-code")

    print("Trying to fill customer information fields...")
    first.send_keys("Alaeddine")
    last.send_keys("Jeridi")
    postal.send_keys("1000")

    # Screenshot de l’état du formulaire (bug visible sur Last Name)
    driver.save_screenshot("F5_checkout_error_user_before_assert.png")

    # Vérifier que le champ Last Name contient bien la valeur saisie
    last_value = last.get_attribute("value")
    print(f"Value read in last-name field: '{last_value}'")

    # Attendu (spécification) : la valeur doit être présente.
    # En réalité, pour error_user, le champ peut rester vide -> BUG.
    assert last_value == "Jeridi", (
        "BUG détecté : le champ 'Last Name' ne garde pas la valeur saisie "
        "(comportement anormal pour error_user)."
    )

    # Si jamais l’assertion passe (au cas où le bug serait corrigé un jour)
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "finish"))
    )
    driver.find_element(By.ID, "finish").click()

    driver.save_screenshot("screenshots/F5_checkout_error_user_after_finish.png")
    print("[PASS] F5_checkout_error_user (aucun bug détecté)")

except AssertionError as e:
    # On log le FAIL proprement
    print("[FAIL] F5_checkout_error_user")
    print(str(e))
    driver.save_screenshot("screenshots/F5_checkout_error_user_fail.png")
    raise

finally:
    driver.quit()