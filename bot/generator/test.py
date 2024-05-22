from selenium import webdriver 
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def send_message(prompt): 
    options = Options() 
    options.headless = True 
    driver = webdriver.Firefox(options=options)

    try: 
        driver.get("https://gemini.google.com")
        # Assuming there is a login process, you may need to automate login here

        # Wait for the text area to be clickable and visible 
        text_area = WebDriverWait(driver, 1000).until( 
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'rich-textarea > div > p')) 
        ) 
        text_area.send_keys(prompt)

        # Find and click the send button 
        send_button = WebDriverWait(driver, 1000).until( 
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class*="send-button-container"] > button')) 
        ) 
        send_button.click()

        # Wait for the response to appear 
        WebDriverWait(driver, 1000).until( 
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'message-content[class*="model-response-text"]')) 
        )

        # Find the response element 
        response_element = driver.find_element(By.CSS_SELECTOR, 'message-content[class*="model-response-text"]')

        # Get the text from the response element 
        response_text = response_element.text 
        return response_text 
    finally: 
        pass
        #driver.quit()

def main(): 
    # Prompt user for what to ask Gemini 
    prompt = input("Ask Gemini: ")

    response_text = send_message(prompt)

    print("\nResponse from Gemini:") 
    print(response_text)

if __name__ == "__main__": 
    main()
