from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from config import *

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# Initialize the driver
service = Service('chromedriver')  # Update this path if needed
driver = webdriver.Chrome(service=service, options=options)

def login():
    """Log in to LinkedIn"""
    driver.get("https://www.linkedin.com/login")
    
    try:
        # Wait for page to load
        WebDriverWait(driver, PAGE_LOAD_WAIT).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Enter credentials
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(LINKEDIN_EMAIL)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        # Click login button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for login to complete
        WebDriverWait(driver, PAGE_LOAD_WAIT).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
        print("Login successful")
        
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        exit()

def send_connection_request(profile_element):
    """Send connection request with custom note"""
    try:
        # Click the "Connect" button
        connect_button = profile_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Invite')]")
        connect_button.click()
        
        # Wait for modal to appear
        time.sleep(1)
        
        try:
            # Click "Add a note"
            add_note = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']"))
            )
            add_note.click()
            
            # Get the name of the person
            name = profile_element.find_element(By.XPATH, ".//span[contains(@class, 'entity-result__title-text')]//a//span[@dir='ltr']").text.split()[0]
            
            # Enter custom note
            note_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "custom-message"))
            )
            note_field.send_keys(CONNECTION_NOTE.format(name=name))
            
        except (NoSuchElementException, TimeoutException):
            # If "Add a note" button doesn't exist, it might be a 2nd+ connection
            print("Couldn't add note - might be a 2nd+ connection")
            pass
        
        # Send the request
        send_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now']"))
        )
        send_button.click()
        
        print(f"Connection request sent")
        time.sleep(1)  # Pause between requests
        
    except Exception as e:
        print(f"Failed to send connection request: {e}")

def main():
    login()
    
    # Navigate to search page
    driver.get(SEARCH_URL)
    time.sleep(PAGE_LOAD_WAIT)
    
    connections_sent = 0
    
    while connections_sent < MAX_CONNECTIONS:
        # Scroll to load more results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Get all profile elements
        profiles = driver.find_elements(By.XPATH, "//li[contains(@class, 'reusable-search__result-container')]")
        
        for profile in profiles:
            if connections_sent >= MAX_CONNECTIONS:
                break
                
            try:
                # Check if "Connect" button is present
                connect_button = profile.find_element(By.XPATH, ".//button[contains(@aria-label, 'Invite')]")
                
                # Check if not already connected
                try:
                    profile.find_element(By.XPATH, ".//span[text()='Pending']")
                    continue  # Skip if already connected
                except NoSuchElementException:
                    pass
                
                send_connection_request(profile)
                connections_sent += 1
                
            except NoSuchElementException:
                continue  # Skip if no connect button
        
        # Check if we've reached the end of results
        try:
            end_results = driver.find_element(By.XPATH, "//div[contains(@class, 'search-reusable-search-no-results')]")
            print("Reached end of search results")
            break
        except NoSuchElementException:
            pass
    
    print(f"Sent {connections_sent} connection requests")
    driver.quit()

if __name__ == "__main__":
    main()