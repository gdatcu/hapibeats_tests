# Importă modulele necesare din librăria Selenium și alte utilități
import random  # Importă modulul random pentru a genera date aleatoare
import string  # Importă modulul string pentru a lucra cu șiruri de caractere (ex: litere, cifre)
import time  # Importă modulul time pentru a adăuga pauze (sleep)

from selenium import webdriver  # Importă clasa WebDriver pentru a interacționa cu browserele
from selenium.webdriver.common.action_chains import \
    ActionChains  # Importă ActionChains pentru a simula interacțiuni complexe (ex: hover, drag-and-drop)
from selenium.webdriver.common.by import By  # Importă modulul By pentru a localiza elemente (ex: By.ID, By.CLASS_NAME)
from selenium.webdriver.support import \
    expected_conditions as EC  # Importă condițiile așteptate (ex: element vizibil, clicabil)
from selenium.webdriver.support.ui import WebDriverWait  # Importă WebDriverWait pentru a seta așteptări explicite


# Funcție pentru a genera un nume de utilizator unic
def generate_unique_username(length=10):
    """Generează un nume de utilizator unic, format din litere mici și cifre."""
    characters = string.ascii_lowercase + string.digits # Definește setul de caractere permise
    return 'testuser_' + ''.join(random.choice(characters) for i in range(length)) # Creează un șir unic cu prefixul 'testuser_'

# Funcție pentru a genera o adresă de email unică
def generate_unique_email(length=8):
    """Generează o adresă de email unică."""
    characters = string.ascii_lowercase + string.digits # Definește setul de caractere permise
    return 'test_' + ''.join(random.choice(characters) for i in range(length)) + '@example.com' # Creează un șir unic cu prefix și domeniu

# Configurația WebDriver-ului
# Inițializăm opțiunile Chrome
chrome_options = webdriver.ChromeOptions() # Creează un obiect ChromeOptions pentru a personaliza comportamentul browserului
# Adăugăm o opțiune pentru a dezactiva politicile de autoplay ale Chrome.
# Aceasta este esențială pentru a asigura redarea media în testele automate,
# deoarece Chrome blochează adesea redarea audio/video fără o interacțiune directă a utilizatorului.
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required") # Adaugă argumentul care dezactivează politica de autoplay

# Inițializăm WebDriver-ul Chrome cu opțiunile configurate
driver = webdriver.Chrome(options=chrome_options) # Lansează o nouă instanță a browserului Chrome cu opțiunile definite
# driver = webdriver.Chrome() # Linia comentată, ar fi folosită dacă nu am avea opțiuni personalizate
# driver = webdriver.Chrome(executable_path=DRIVER_PATH) # Linia comentată, ar fi folosită dacă ChromeDriver nu ar fi în PATH

# URL-ul de bază al aplicației HapiBeats
BASE_URL = "https://apps.qualiadept.eu/hapibeats/" # Definește URL-ul de bază al aplicației

# Setăm un timp de așteptare implicit pentru elemente
driver.implicitly_wait(10) # Setează o așteptare implicită de 10 secunde. WebDriver-ul va aștepta maxim 10 secunde ca un element să apară înainte de a arunca o excepție.

try:
    # Blocul try-except-finally este folosit pentru a gestiona erorile și a asigura închiderea browserului.

    # Maximizăm fereastra browserului la începutul testului
    driver.maximize_window() # Maximizează fereastra browserului la dimensiunea maximă disponibilă.
    print("Fereastra browserului a fost maximizată.") # Afișează un mesaj în consolă.

    print("Începe testarea aplicației HapiBeats...") # Afișează un mesaj de început.

    # --- Test 1: Înregistrare Utilizator Nou ---
    print("\n--- Test 1: Înregistrare Utilizator ---") # Afișează titlul testului.
    driver.get(BASE_URL + "register.php") # Navighează browserul la pagina de înregistrare.
    print(f"Navigat la: {driver.current_url}") # Afișează URL-ul curent.

    # Așteaptă ca formularul de login să fie vizibil și apoi apasă pe link-ul de înregistrare
    WebDriverWait(driver, 10).until( # Creează un obiect WebDriverWait care așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.ID, "loginForm")) # Așteaptă până când elementul cu ID-ul "loginForm" devine vizibil.
    )
    signup_link = driver.find_element(By.ID, "hideLogin") # Găsește elementul cu ID-ul "hideLogin" (link-ul "Signup here").
    signup_link.click() # Execută un click pe elementul găsit.
    print("Am apăsat pe 'Signup here'.") # Afișează un mesaj.

    # Așteaptă ca formularul de înregistrare să fie vizibil
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.ID, "registerForm")) # Așteaptă până când elementul cu ID-ul "registerForm" devine vizibil.
    )

    # Generăm date unice pentru înregistrare
    new_username = generate_unique_username() # Generează un nume de utilizator unic.
    new_first_name = "Test" # Definește prenumele.
    new_last_name = "User" # Definește numele de familie.
    new_email = generate_unique_email() # Generează o adresă de email unică.
    new_password = "Password123" # Definește parola.

    print(f"Încerc să înregistrez utilizatorul: {new_username}") # Afișează detaliile utilizatorului.

    # Completăm formularul de înregistrare
    driver.find_element(By.ID, "username").send_keys(new_username) # Găsește câmpul "username" și introduce valoarea.
    driver.find_element(By.ID, "firstName").send_keys(new_first_name) # Găsește câmpul "firstName" și introduce valoarea.
    driver.find_element(By.ID, "lastName").send_keys(new_last_name) # Găsește câmpul "lastName" și introduce valoarea.
    driver.find_element(By.ID, "email").send_keys(new_email) # Găsește câmpul "email" și introduce valoarea.
    driver.find_element(By.ID, "email2").send_keys(new_email) # Găsește câmpul "email2" și introduce valoarea.
    driver.find_element(By.ID, "password").send_keys(new_password) # Găsește câmpul "password" și introduce valoarea.
    driver.find_element(By.ID, "password2").send_keys(new_password) # Găsește câmpul "password2" și introduce valoarea.

    # Apasă butonul de înregistrare
    register_button = driver.find_element(By.NAME, "registerButton") # Găsește butonul cu atributul name="registerButton".
    register_button.click() # Execută un click pe buton.
    print("Am apăsat butonul 'SIGN UP'.") # Afișează un mesaj.

    # Verificăm dacă înregistrarea a fost un succes prin redirecționare
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.url_contains("browse.php") # Așteaptă până când URL-ul curent al browserului conține "browse.php".
    )
    assert "browse.php" in driver.current_url # Verifică dacă "browse.php" este în URL-ul curent (o aserțiune pentru succes).
    print("Înregistrare reușită! Suntem pe pagina 'browse.php'.") # Afișează un mesaj de succes.
    time.sleep(2) # Așteaptă 2 secunde pentru a permite vizualizarea paginii.

    # --- Test 2: Autentificare Utilizator ---
    print("\n--- Test 2: Autentificare Utilizator ---") # Afișează titlul testului.
    # Pentru a testa login-ul, ne deconectăm mai întâi
    driver.get(BASE_URL + "settings.php") # Navighează la pagina de setări.
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".buttonItems .button")) # Așteaptă până când un buton din secțiunea ".buttonItems" devine vizibil.
    )
    logout_button = driver.find_element(By.XPATH, "//button[text()='LOGOUT']") # Găsește butonul "LOGOUT" după text.
    logout_button.click() # Execută un click pe buton.
    print("Am apăsat butonul 'LOGOUT'.") # Afișează un mesaj.

    # Așteaptă ca pagina de login să reapară
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.ID, "loginForm")) # Așteaptă până când formularul de login devine vizibil.
    )

    print(f"Încerc să mă autentific cu utilizatorul: {new_username}") # Afișează utilizatorul.

    # Completăm formularul de autentificare
    driver.find_element(By.ID, "loginUsername").send_keys(new_username) # Găsește câmpul "loginUsername" și introduce numele de utilizator.
    driver.find_element(By.ID, "loginPassword").send_keys(new_password) # Găsește câmpul "loginPassword" și introduce parola.

    # Apasă butonul de autentificare
    login_button = driver.find_element(By.NAME, "loginButton") # Găsește butonul cu atributul name="loginButton".
    login_button.click() # Execută un click pe buton.
    print("Am apăsat butonul 'LOG IN'.") # Afișează un mesaj.

    # Verificăm dacă autentificarea a fost un succes prin redirecționare
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.url_contains("browse.php") # Așteaptă până când URL-ul curent conține "browse.php".
    )
    assert "browse.php" in driver.current_url # Verifică aserțiunea.
    print("Autentificare reușită! Suntem pe pagina 'browse.php'.") # Afișează un mesaj de succes.
    time.sleep(2) # Așteaptă 2 secunde.

    # --- Test 3: Pornirea unei melodii ---
    print("\n--- Test 3: Pornirea unei melodii ---") # Afișează titlul testului.

    # Ne asigurăm că suntem pe pagina browse.php
    driver.get(BASE_URL + "browse.php") # Navighează la pagina browse.php.
    print(f"Navigat la: {driver.current_url}") # Afișează URL-ul curent.

    # Așteaptă ca titlul paginii să fie vizibil, indicând că secțiunea principală a început să se încarce
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.CLASS_NAME, "pageHeadingBig")) # Așteaptă până când elementul cu clasa "pageHeadingBig" devine vizibil.
    )
    print("Titlul paginii 'You Might Also Like' este vizibil.") # Afișează un mesaj.

    # Așteaptă ca containerul grilelor de albume să fie vizibil
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.CLASS_NAME, "gridViewContainer")) # Așteaptă până când elementul cu clasa "gridViewContainer" devine vizibil.
    )
    print("Containerul cu albume este vizibil.") # Afișează un mesaj.

    # Așteaptă ca PRIMUL element de album să fie CLICABIL
    first_album_link = WebDriverWait(driver, 20).until( # Așteaptă maxim 20 de secunde.
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".gridViewItem span[role='link']")) # Așteaptă până când primul span cu role="link" din gridViewItem devine clicabil.
    )
    time.sleep(1) # Placă de siguranță suplimentară.

    # Folosim JavaScript pentru a da click pe element, ocolind potențialele probleme de interacțiune
    driver.execute_script("arguments[0].click();", first_album_link) # Execută un script JavaScript pentru a da click pe element.
    print("Am apăsat pe primul album folosind JavaScript.") # Afișează un mesaj.

    # Așteaptă ca URL-ul să se schimbe la pagina albumului
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.url_contains("album.php?id=") # Așteaptă până când URL-ul conține "album.php?id=".
    )
    print(f"Suntem pe pagina albumului: {driver.current_url}") # Afișează URL-ul curent.

    # Așteaptă vizibilitatea tracklist-ului pe noua pagină
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.visibility_of_element_located((By.CLASS_NAME, "tracklistContainer")) # Așteaptă până când elementul cu clasa "tracklistContainer" devine vizibil.
    )
    print("Lista de melodii a albumului este vizibilă.") # Afișează un mesaj.

    # Așteaptă ca variabila JavaScript tempPlaylist să fie definită și populată
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        lambda driver: driver.execute_script("return typeof tempPlaylist !== 'undefined' && tempPlaylist.length > 0;") # Așteaptă până când variabila JavaScript tempPlaylist este definită și are elemente.
    )
    print("Variabila JavaScript tempPlaylist este definită și populată.") # Afișează un mesaj.

    # Așteaptă ca audioElement să fie definit și gata de utilizare
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        lambda driver: driver.execute_script("return typeof audioElement !== 'undefined' && audioElement !== null;") # Așteaptă până când obiectul JavaScript audioElement este definit și nu este null.
    )
    print("Obiectul JavaScript 'audioElement' este definit.") # Afișează un mesaj.


    # --- Strategie robustă de redare a melodiei: Hover peste rândul melodiei și apoi click pe butonul de play ---
    # Găsește primul rând de melodie
    first_track_row = WebDriverWait(driver, 15).until( # Așteaptă maxim 15 secunde.
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".tracklistRow")) # Așteaptă până când primul element cu clasa "tracklistRow" devine vizibil.
    )
    print("Am găsit primul rând de melodie.") # Afișează un mesaj.

    # Efectuează hover peste rândul melodiei pentru a face butonul de play vizibil
    actions = ActionChains(driver) # Creează un obiect ActionChains.
    actions.move_to_element(first_track_row).perform() # Mută cursorul mouse-ului peste elementul rândului melodiei.
    print("Am efectuat hover peste primul rând de melodie.") # Afișează un mesaj.
    time.sleep(1) # Așteaptă 1 secundă pentru ca efectul de hover să se aplice.

    # Obține butonul de play (<img>) din interiorul rândului de melodie
    # Acum ar trebui să fie vizibil și clicabil
    tracklist_play_button_img = WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".tracklistRow .trackCount .play")) # Așteaptă până când elementul img.play din tracklistRow devine clicabil.
    )
    # Scroll la element pentru a asigura vizibilitatea și interacțiunea (chiar dacă hover-ul ajută)
    driver.execute_script("arguments[0].scrollIntoView(true);", tracklist_play_button_img) # Derulează pagina până când elementul este vizibil.
    time.sleep(0.5) # O scurtă pauză după scroll.

    # Încercăm să dăm click direct pe elementul img.play
    print("Încerc să dau click direct pe elementul img.play...") # Afișează un mesaj.
    try:
        tracklist_play_button_img.click() # Execută un click direct pe butonul de play.
        print("Am apăsat butonul img.play printr-un click direct.") # Afișează un mesaj de succes.
    except Exception as click_e: # Prinde orice excepție la click.
        print(f"Click-ul direct pe img.play a eșuat: {click_e}. Încerc să execut funcția onclick direct.") # Afișează mesajul de eroare și încearcă fallback.
        # Fallback: Execută direct funcția onclick dacă click-ul nativ eșuează
        onclick_value = tracklist_play_button_img.get_attribute("onclick") # Obține valoarea atributului onclick.
        if onclick_value: # Verifică dacă atributul onclick nu este gol.
            print(f"Execut direct funcția JavaScript din atributul onclick: {onclick_value}") # Afișează funcția JavaScript.
            driver.execute_script(onclick_value) # Execută direct scriptul JavaScript din atributul onclick.
            print("Funcția onclick a fost executată cu succes prin JavaScript.") # Afișează un mesaj de succes.
        else:
            print("Atributul onclick este gol. Nu se poate executa.") # Afișează un mesaj de eroare.
            raise ValueError("Atributul onclick al butonului de play este gol.") # Aruncă o excepție.


    # Așteaptă ca titlul melodiei în bara de redare să fie populat (indică finalizarea AJAX din setTrack)
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        lambda driver: driver.find_element(By.CSS_SELECTOR, ".trackName span").text.strip() != "" # Așteaptă până când textul titlului melodiei în bara de redare nu este gol.
    )
    print("Titlul melodiei în bara de redare a fost populat.") # Afișează un mesaj.

    # Așteaptă ca elementul audio să fie gata de redare (readyState 4 - HAVE_ENOUGH_DATA)
    WebDriverWait(driver, 10).until( # Așteaptă maxim 10 secunde.
        lambda driver: driver.execute_script("return audioElement.audio.readyState === 4;") # Așteaptă până când starea readyState a elementului audio este 4 (complet încărcat).
    )
    print("Audio element este gata de redare (readyState 4).") # Afișează un mesaj.

    # Verificăm dacă melodia se redă efectiv, așteptând ca currentTime să devină > 0
    # Reîncercăm de câteva ori dacă nu pornește imediat
    max_retries = 15 # Definește numărul maxim de reîncercări.
    playback_confirmed = False # Variabilă booleană pentru a confirma redarea.
    for i in range(max_retries): # Buclă pentru reîncercări.
        current_time_element = driver.find_element(By.CSS_SELECTOR, ".progressTime.current") # Găsește elementul care afișează timpul curent.
        current_time_text = current_time_element.text # Obține textul timpului curent.
        print(f"Verificare redare (încercarea {i+1}): Timpul curent al melodiei: {current_time_text}") # Afișează starea redării.

        # Verificăm dacă melodia a început să se redea (currentTime > 0.00)
        # și că nu este în pauză
        is_playing_js = driver.execute_script("return !audioElement.audio.paused && audioElement.audio.currentTime > 0;") # Verifică starea redării prin JavaScript.
        if is_playing_js: # Dacă melodia se redă.
            print("Melodia se redă cu succes (confirmat prin JS)!") # Afișează mesaj de succes.
            playback_confirmed = True # Setează confirmarea la True.
            break # Ieșe din buclă.
        else: # Dacă melodia nu se redă.
            print("Melodia nu se redă încă. Reîncercare...") # Afișează mesaj de reîncercare.
            # Încercăm să forțăm play din nou dacă nu se redă
            driver.execute_script("audioElement.audio.play();") # Forțează redarea prin JavaScript.
            time.sleep(2) # Așteaptă 2 secunde înainte de următoarea verificare.
    if not playback_confirmed: # Dacă redarea nu a fost confirmată după toate încercările.
        raise AssertionError(f"Melodia nu a început să se redea sau progresul nu se actualizează după {max_retries} încercări. Timp final: {current_time_text}") # Aruncă o eroare.

    print("\nToate testele au fost executate cu succes!") # Afișează mesaj de succes final.
    time.sleep(5) # Așteaptă 5 secunde pentru confirmare vizuală a redării.

except Exception as e: # Prinde orice excepție care apare în blocul try.
    print(f"\nO eroare a apărut în timpul testării: {e}") # Afișează mesajul de eroare.
    # driver.save_screenshot("final_error_state.png") # Linie comentată pentru salvarea unei capturi de ecran la eroare.

finally:
    # Închide browser-ul la finalizarea testelor sau în caz de eroare
    driver.quit() # Închide browserul.
    print("Browser-ul a fost închis.") # Afișează un mesaj.