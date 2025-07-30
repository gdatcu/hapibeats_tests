from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# --- Configurare WebDriver ---
# Asigură-te că ai ChromeDriver descărcat și că este în PATH-ul sistemului tău,
# sau specifică calea completă către el.
driver = webdriver.Chrome()
driver.maximize_window() # Maximizează fereastra browserului

# URL-urile paginilor Hapible
LOGIN_URL = "https://apps.qualiadept.eu/hapible/frontend/login.html"
DASHBOARD_URL = "https://apps.qualiadept.eu/hapible/frontend/dashboard.html"

def run_xpath_examples():
    """
    Navighează la pagina de login Hapible și demonstrează diverse căutări XPATH.
    """
    print(f"Navighez la pagina de login: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 10)

    print("\n--- Exemple de XPATH ---")

    # --- 1. XPATH Absolut (DOAR PENTRU DEMONSTRAȚIE - NU RECOMANDAT!) ---
    # Acest XPATH absolut ar putea arăta așa pentru câmpul de username:
    # /html/body/div[1]/div/div/div[2]/div[4]/div/form/div[1]/input
    # Îl afișăm doar pentru a înțelege de ce este fragil.
    print("\n--- XPATH Absolut (NU RECOMANDAT!) ---")
    absolute_xpath_example = "/html/body/div[1]/div/div[2]/div/form/div[1]/input" # Exemplu bazat pe structura login.html
    print(f"Exemplu XPATH Absolut pentru câmpul username: {absolute_xpath_example}")
    print("Acest tip de XPATH este extrem de fragil și nu ar trebui folosit în automatizare.")
    # Nu vom încerca să găsim elemente cu XPATH absolut din cauza fragilității.

    # --- 2. Căutare după Tag ---
    print("\n--- Căutare după Tag: //input ---")
    try:
        inputs = driver.find_elements(By.XPATH, "//input")
        print(f"✅ Am găsit {len(inputs)} elemente de tip <input> pe pagină.")
        if inputs:
            print(f"Primul input găsit (name): {inputs[0].get_attribute('name')}")
    except Exception as e:
        print(f"❌ Eroare la căutarea după tag: {e}")

    # --- 3. Căutare după Atribut=Valoare (Tag specific) ---
    print("\n--- Căutare după Atribut=Valoare (Tag specific): //input[@name='username'] ---")
    try:
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
        print(f"✅ Câmpul 'username' identificat: {username_field.tag_name} cu name='{username_field.get_attribute('name')}'")
        username_field.send_keys("testuser_selenium_login")
        print("Text introdus în câmpul username.")
    except TimeoutException:
        print("❌ Câmpul 'username' nu a fost găsit la timp.")
    except Exception as e:
        print(f"❌ Eroare la căutarea după atribut (tag specific): {e}")

    print("\n--- Căutare după Atribut=Valoare (Tag specific): //button[@type='submit'] ---")
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        print(f"✅ Butonul de login identificat: {login_button.tag_name} cu type='{login_button.get_attribute('type')}'")
    except TimeoutException:
        print("❌ Butonul de login nu a fost găsit la timp.")
    except Exception as e:
        print(f"❌ Eroare la căutarea butonului de login: {e}")

    # --- 4. Căutare după Atribut=Valoare (Indiferent de Tag) ---
    print("\n--- Căutare după Atribut=Valoare (Indiferent de Tag): //*[@name='password'] ---")
    try:
        password_field_any_tag = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='password']")))
        print(f"✅ Câmpul 'password' identificat (orice tag): {password_field_any_tag.tag_name} cu name='{password_field_any_tag.get_attribute('name')}'")
        password_field_any_tag.send_keys("Password123")
        print("Text introdus în câmpul password.")
    except TimeoutException:
        print("❌ Câmpul 'password' nu a fost găsit la timp (orice tag).")
    except Exception as e:
        print(f"❌ Eroare la căutarea după atribut (orice tag): {e}")

    # --- 5. Căutare după Text ---
    print("\n--- Căutare după Text: //button[contains(text(), 'Autentificare')] ---")
    try:
        auth_button_by_text = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        print(f"✅ Butonul 'Autentificare' identificat după text: {auth_button_by_text.text}")
        # Click pe buton pentru a încerca logarea
        auth_button_by_text.click()
        time.sleep(2)
        if driver.current_url == DASHBOARD_URL:
            print("✅ Logare reușită după click pe butonul găsit după text!")
        else:
            print(f"⚠️ Logare eșuată sau redirecționare incorectă. URL curent: {driver.current_url}")
            # Ne întoarcem la pagina de login pentru a continua exemplele, dacă eșuează
            driver.get(LOGIN_URL)
            wait.until(EC.visibility_of_element_located((By.NAME, "username"))) # Așteptăm reîncărcarea paginii
    except TimeoutException:
        print("❌ Butonul 'Autentificare' nu a fost găsit la timp după text.")
    except Exception as e:
        print(f"❌ Eroare la căutarea după text: {e}")

    # Reîncărcăm pagina de login pentru exemplele de Axis Navigation
    driver.get(LOGIN_URL)
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))

    # --- 6. Axis Navigation ---
    print("\n--- Axis Navigation ---")

    # Părinte în Copil (descendent direct)
    print("\n--- Părinte în Copil (direct): //form[@id='loginForm']/div ---")
    try:
        form_divs = driver.find_elements(By.XPATH, "//form[@id='loginForm']/div")
        print(f"✅ Am găsit {len(form_divs)} div-uri copii directe ale formularului de login.")
    except Exception as e:
        print(f"❌ Eroare la Părinte în Copil (direct): {e}")

    # Copil în Părinte
    print("\n--- Copil în Părinte: //input[@name='username']/parent::div ---")
    try:
        username_parent_div = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']/parent::div")))
        print(f"✅ Părintele câmpului 'username' identificat (tag: {username_parent_div.tag_name}, class: {username_parent_div.get_attribute('class')}).")
    except TimeoutException:
        print("❌ Părintele câmpului 'username' nu a fost găsit la timp.")
    except Exception as e:
        print(f"❌ Eroare la Copil în Părinte: {e}")

    # Frate Ulterior
    # Căutăm div-ul câmpului username, apoi fratele ulterior care conține câmpul password
    print("\n--- Frate Ulterior: //div[input[@name='username']]/following-sibling::div[input[@name='password']] ---")
    try:
        password_div_via_sibling = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[input[@name='username']]/following-sibling::div[input[@name='password']]")))
        print(f"✅ Div-ul câmpului 'password' identificat prin fratele ulterior al div-ului 'username'.")
    except TimeoutException:
        print("❌ Div-ul câmpului 'password' nu a fost găsit prin fratele ulterior.")
    except Exception as e:
        print(f"❌ Eroare la Frate Ulterior: {e}")

    # Frate Anterior
    # Căutăm div-ul câmpului password, apoi fratele anterior care conține câmpul username
    print("\n--- Frate Anterior: //div[input[@name='password']]/preceding-sibling::div[input[@name='username']] ---")
    try:
        username_div_via_sibling = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[input[@name='password']]/preceding-sibling::div[input[@name='username']]")))
        print(f"✅ Div-ul câmpului 'username' identificat prin fratele anterior al div-ului 'password'.")
    except TimeoutException:
        print("❌ Div-ul câmpului 'username' nu a fost găsit prin fratele anterior.")
    except Exception as e:
        print(f"❌ Eroare la Frate Anterior: {e}")

    print("\n--- Toate exemplele XPATH au fost rulate ---")

# --- Rularea scriptului ---
if __name__ == "__main__":
    try:
        run_xpath_examples()
    except Exception as final_e:
        print(f"\nO eroare neașteptată a apărut în timpul execuției scriptului: {final_e}")
    finally:
        print("\nÎnchid browserul în 10 secunde...")
        time.sleep(10)
        driver.quit() # Asigură-te că browserul se închide la final
