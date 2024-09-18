import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

@pytest.fixture
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
    
    
@pytest.mark.parametrize("username, password, expected_url, expected_text",[
    ("student", "Password123", "https://practicetestautomation.com/logged-in-successfully/", "Congratulations student. You successfully logged in!"),  #This is for valid credentials
    ("incorrectUser", "Password123", "https://practicetestautomation.com/practice-test-login/", "Your username is invalid!"),     #This is for invalid username credentials
    ("student", "incorrectPassword", "https://practicetestautomation.com/practice-test-login/", "Your password is invalid!")    #This is for invalid password credentials
])

def test_login(setup_driver,username, password, expected_url, expected_text):
    driver = setup_driver
    
    
    # Open the Website
    driver.get("https://practicetestautomation.com/practice-test-login/")
    
    # Enter the credentials
    username_field = driver.find_element(By.ID, "username")
    sleep(1)        #Adding a little delay
    username_field.send_keys(username)
    
    password_field = driver.find_element(By.ID, "password")
    sleep(1)        #Adding a little delay
    password_field.send_keys(password)
    
    submit_btn = driver.find_element(By.ID, "submit")
    sleep(1)        #Adding a little delay
    submit_btn.click()
    
    # Now, let's verify that we are on the expectedURL or we can verify the error message
    
    if "logged-in-successfully" in expected_url:
        assert expected_url in driver.current_url
        
        # Verify the page contains the success message
        
        page_text = driver.page_source
        assert expected_text in page_text
        
        
        #Verify the presence of the log out button
        logout_button = driver.find_element(By.XPATH, "//a[normalize-space()='Log out']")
        assert logout_button.is_displayed()
        
    else:
        
        #Verify the error message for the invalid credentials
        error_message = driver.find_element(By.ID, "error").text
        assert expected_text in error_message