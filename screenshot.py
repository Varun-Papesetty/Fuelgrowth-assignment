import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import pandas as pd

def download_video_with_context_menu(video_url, download_folder, link_id):
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)  
    
    try:
        # Open the video URL
        driver.get(video_url)
        
        # Wait for the video to load 
        time.sleep(5)
        
        # Locate the video element 
        video_element = driver.find_element(By.TAG_NAME, "video")
        
        # Perform right-click on the video to open the context menu
        action = ActionChains(driver)
        action.context_click(video_element).perform()
        
        
        time.sleep(2)
        driver.save_screenshot(f"{link_id}.png")  
        
        # Simulate the "Save As" action with keyboard shortcuts
        pyautogui.hotkey('ctrl', 's')
        
        
        time.sleep(2)  

        
        #pyautogui.write(os.path.join(download_folder, f"{link_id}.mp4")) 
        #pyautogui.press('enter')  

        # Wait for the download to complete (adjust based on file size)
        time.sleep(8)

        print(f"Download initiated for {link_id} to {download_folder}.")
    finally:
        driver.quit()



# Path to your CSV file
csv_file_path = 'Assignment Data.csv'

# Read the CSV into a DataFrame
data = pd.read_csv(csv_file_path)

# Access the video_url and link_id columns
video_urls = data['Video URL']
link_ids = data['Performance']

# Ensure download folder exists
download_folder = os.path.expanduser("~/Downloads")  
os.makedirs(download_folder, exist_ok=True)

# Iterate through rows to access both variables
for index, row in data.iterrows():
    video_url = row['Video URL']
    link_id = row['Performance']
    download_video_with_context_menu(video_url, download_folder, link_id)
