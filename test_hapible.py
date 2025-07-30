from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# --- WebDriver Configuration ---
# Ensure you have ChromeDriver downloaded and in your system's PATH,
# or specify the full path to it.
driver = webdriver.Chrome()
driver.maximize_window() # Maximize the browser window

# Hapible Application URLs
LOGIN_URL = "https://apps.qualiadept.eu/hapible/frontend/login.html"
DASHBOARD_URL = "https://apps.qualiadept.eu/hapible/frontend/dashboard.html"

# Test Data
TEST_USERNAME = "testuser_selenium_login" # A test username, ensure it exists or register it manually
TEST_PASSWORD = "Password123" # The corresponding password

def identify_and_login():
    """
    Navigates to the login page, identifies username and password fields,
    enters test data, and attempts login.
    """
    print(f"Navigating to login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    try:
        wait = WebDriverWait(driver, 10)

        # Identify and interact with username field
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        username_input.send_keys(TEST_USERNAME)

        # wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(TEST_USERNAME)

        print(f"✅ Username field identified and '{TEST_USERNAME}' entered.")

        # Identify and interact with password field
        password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys(TEST_PASSWORD)
        print("✅ Password field identified and entered.")

        # Identify and click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        print("✅ Login button clicked.")

        # Wait for redirection and verify login success
        time.sleep(2) # Short pause for redirection

        if driver.current_url == DASHBOARD_URL:
            print("✅ Login successful! Redirected to dashboard page.")
            # Optional: Verify dashboard content
            try:
                job_listings_title = driver.find_element(By.CSS_SELECTOR, "h2.text-center")
                if "Job Listings" in job_listings_title.text:
                    print("✅ 'Job Listings' title visible on dashboard.")
            except NoSuchElementException:
                print("⚠️ 'Job Listings' title not found on dashboard.")
            return True
        else:
            print(f"❌ Login failed. Current URL: {driver.current_url}. Expected: {DASHBOARD_URL}")
            return False

    except TimeoutException:
        print("❌ A required element was not found in time on the page.")
        return False
    except NoSuchElementException:
        print("❌ A required element was not found on the page (check selector).")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

# --- Run the script ---
if __name__ == "__main__":
    try:
        print("--- Starting element identification and login test ---")
        if identify_and_login():
            print("\nElement identification and login test executed successfully!")
        else:
            print("\nElement identification and login test finished with errors.")
    except Exception as final_e:
        print(f"\nAn unexpected error occurred during script execution: {final_e}")
    finally:
        print("\nClosing browser in 5 seconds...")
        time.sleep(5)
        driver.quit() # Ensure the browser closes at the end
