from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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

def test_dropdown_selection():
    """
    Assumes the driver is already on the dashboard page or a page
    containing the dropdown. Navigates to the dashboard if not already there,
    then identifies and interacts with a dropdown element.
    """
    print(f"\n--- Starting dropdown test ---")
    # Ensure we are on the dashboard page to find the dropdown
    if driver.current_url != DASHBOARD_URL:
        print(f"Navigating to dashboard page for dropdown test: {DASHBOARD_URL}")
        driver.get(DASHBOARD_URL)
        time.sleep(2) # Give page time to load

    try:
        wait = WebDriverWait(driver, 10)

        # Identify the dropdown element by its ID (from the simulated HTML in previous canvas)
        # Note: This assumes a dropdown with id="jobType" exists on the dashboard or a linked page.
        dropdown_element = wait.until(EC.visibility_of_element_located((By.ID, "jobType")))
        print("✅ Dropdown element identified.")

        # Create a Select object for the dropdown
        select = Select(dropdown_element)

        # Select an option by visible text
        option_to_select = "Full-time"
        select.select_by_visible_text(option_to_select)
        print(f"✅ Selected '{option_to_select}' from the dropdown.")

        # Optional: Verify the selected value
        if select.first_selected_option.text == option_to_select:
            print(f"✅ Dropdown selection verified: '{option_to_select}' is currently selected.")
        else:
            print(f"⚠️ Dropdown selection verification failed. Expected '{option_to_select}', but found '{select.first_selected_option.text}'.")

        return True

    except TimeoutException:
        print("❌ Dropdown element not found or not visible within timeout.")
        return False
    except NoSuchElementException:
        print("❌ Dropdown element not found (check selector or if it exists on this page).")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred during dropdown test: {e}")
        return False

# --- Run the script ---
if __name__ == "__main__":
    try:
        print("--- Starting element identification and login test ---")
        login_success = identify_and_login()

        if login_success:
            print("\nElement identification and login test executed successfully!")
            # Now, run the dropdown test
            dropdown_test_success = test_dropdown_selection()
            if dropdown_test_success:
                print("\nDropdown test executed successfully!")
            else:
                print("\nDropdown test finished with errors.")
        else:
            print("\nElement identification and login test finished with errors. Skipping dropdown test.")

    except Exception as final_e:
        print(f"\nAn unexpected error occurred during script execution: {final_e}")
    finally:
        print("\nClosing browser in 5 seconds...")
        time.sleep(5)
        driver.quit() # Ensure the browser closes at the end
