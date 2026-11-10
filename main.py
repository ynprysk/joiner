from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, url_changes
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string

# --- CONFIGURATION ---
SERVER_INVITE_URL = "https://nexa.pm/invite/YOUR_CODE_HERE"  # Replace with actual invite link
PASSWORD = "SecurePass123!"       # Use same password for all accounts
DELAY_MIN = 2                     # Minimum seconds between actions
DELAY_MAX = 5                     # Maximum seconds between actions

def generate_4letter_username():
    """Generates a random 4-character username (letters and numbers)"""
    length = 4
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_account_and_join():
    # Setup Chrome Driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Run in headless mode to save resources on your tablet/cloud
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("🚀 Starting Nexa.pm Account Creator & Joiner...")
        
        # Step 1: Go to Signup Page
        driver.get("https://nexa.pm/signup") 
        print(f"Opened signup page: {driver.current_url}")

        wait = WebDriverWait(driver, 15)
        
        # Wait for the Username field to be available
        username_field = wait.until(presence_of_element_located((By.NAME, "username")))
        
        # Generate unique credentials
        username = generate_4letter_username()
        password = PASSWORD
        
        print(f"Creating account: {username}")

        # Fill fields
        username_field.clear()
        username_field.send_keys(username)
        
        # Find password field
        try:
            password_field = driver.find_element(By.NAME, "password")
        except:
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
        password_field.clear()
        password_field.send_keys(password)

        # Click Sign Up button
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button.btn-primary")
        submit_btn.click()
        print("✅ Submitted registration.")

        # Wait for redirect or page change after signup
        wait.until(url_changes(driver.current_url))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        # Step 2: Join Server
        print(f"Joining server via: {SERVER_INVITE_URL}")
        driver.get(SERVER_INVITE_URL)
        
        # Wait for the Join button to appear
        try:
            join_btn = wait.until(presence_of_element_located((By.XPATH, "//button[contains(text(), 'Join')]")))
            join_btn.click()
            print(f"🎉 Successfully joined server with account {username}!")
        except Exception as e:
            print(f"⚠️ Could not find Join button. Current URL: {driver.current_url}")
            print("Page content might indicate success or error.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
        print("🔒 Browser closed.")

if __name__ == "__main__":
    create_account_and_join()
