from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pytest
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # ou Firefox, Edge, etc.
    yield driver
    driver.quit()
# Classe utilitaire de base
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def enter_text(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def click(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        self.driver.find_element(*locator).click()


# Page de connexion
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def login_with_credentials(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)


# Page de commande
class CommandePage(BasePage):

    def ajouter_produit(self, produit="Savon Argan"):
        commandes = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "menu.orders"))
        )
        commandes.click()

        nouvelle_commandes = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "menu.new_order"))
        )
        nouvelle_commandes.click()

        selectionner_un_produit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchinput_products"))
        )
        selectionner_un_produit.click()

        choisir_un_produit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "product-title-20110"))
        )
        choisir_un_produit.click()

        quantity_input = self.driver.find_element(By.ID, "quantity")
        quantity_input.clear()
        quantity_input.send_keys("5")

        add_to_cart_button = self.driver.find_element(By.ID, "add")
        add_to_cart_button.click()

    def selectionner_mode_livraison(self, mode="Siège"):
        wait = WebDriverWait(self.driver, 20)

        # 1. Cliquer sur le champ Select2 (le conteneur)
        for _ in range(3):
            try:
                select2 = wait.until(EC.element_to_be_clickable((By.ID, "select2-addDeliveryType-container")))
                select2.click()
                break
            except StaleElementReferenceException:
                print("Element became stale, retrying...")
        # 2. Attendre l'affichage de la liste d'options
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//li[contains(text(), 'Siège')]"  # adapte ici le texte visible de l'option
        )))

        # 3. Cliquer sur l'option
        option.click()

    def choisir_depot(self, depot="Agence Tunis"):

        wait = WebDriverWait(self.driver, 20)

        # 1. Cliquer sur le champ Select2 (le conteneur)
        for _ in range(3):
            try:
                select2 = wait.until(EC.element_to_be_clickable((By.ID, "select2-addDepot-container")))
                select2.click()
                break
            except StaleElementReferenceException:
                print("Element became stale, retrying...")
        # 2. Attendre l'affichage de la liste d'options
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//li[contains(text(), '{depot}')]"  # adapte ici le texte visible de l'option
        )))

        # 3. Cliquer sur l'option
        option.click()




        # depot_field = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "select2-addDepot-container"))
        # )
        # depot_field.click()
        # depot_option = self.driver.find_element(By.XPATH, f"//span[text()='{depot}']")
        # depot_option.click()

    def choisir_mode_paiement(self, paiement="A la livraison"):

        wait = WebDriverWait(self.driver, 20)

        # 1. Cliquer sur le champ Select2 (le conteneur)
        for _ in range(3):
            try:
                select2 = wait.until(EC.element_to_be_clickable((By.ID, "select2-paymentMode-container")))
                select2.click()
                break
            except StaleElementReferenceException:
                print("Element became stale, retrying...")
        # 2. Attendre l'affichage de la liste d'options
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//li[contains(text(), '{paiement}')]"  # adapte ici le texte visible de l'option
        )))

        # 3. Cliquer sur l'option
        option.click()


        # payment_mode_field = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "select2-paymentMode-container"))
        # )
        # payment_mode_field.click()
        # payment_option = self.driver.find_element(By.XPATH, f"//span[text()='{paiement}']")
        # payment_option.click()

    def passer_commande(self):
        commander_button = self.driver.find_element(By.ID, "saveOrderBtn")
        commander_button.click()

    def verifier_message_succes(self):
        success_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "swal-modal"))
        )
        titre = self.driver.find_element(By.CLASS_NAME, "swal-title")
        assert titre.text == "Succès", "Le message de succès n'est pas affiché correctement."

        content_text = self.driver.find_element(By.CLASS_NAME, "swal-content__p")
        assert "Votre Net à payer" in content_text.text, "Le montant à payer n'est pas affiché."

        bouton_ok = self.driver.find_element(By.CLASS_NAME, "swal-button--confirm")
        bouton_ok.click()

        return True

    def deconnecter_utilisateur(self):
        avatar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar-status"))
        )
        avatar.click()

        deconnexion_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Se déconnecter')]"))
        )
        deconnexion_option.click()

        old_url = self.driver.current_url
        WebDriverWait(self.driver, 30).until(EC.url_changes(old_url))
        print("Déconnexion réussie.")


# Fonction principale de test
def test_login_success(driver):
    login_page = LoginPage(driver)
    driver.get("https://qa-test:mdw@@2025@recrutement.arvea-test.ovh/")
    login_page.login_with_credentials("TN25000000", "maisonduweb123")

    commande_page = CommandePage(driver)
    commande_page.ajouter_produit()
    commande_page.selectionner_mode_livraison()
    commande_page.choisir_depot()
    commande_page.choisir_mode_paiement()
    commande_page.passer_commande()

    assert commande_page.verifier_message_succes(), "Le message de succès n'a pas été détecté."
    commande_page.deconnecter_utilisateur()


# === Point d'entrée du script ===
if __name__ == "__main__":
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        test_login_success(driver)
    finally:
        time.sleep(2)
    driver.quit()