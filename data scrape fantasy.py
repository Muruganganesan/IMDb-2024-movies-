import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# WebDriver setup (Ensure you have the correct WebDriver installed)
driver = webdriver.Chrome()  # Change this if using Firefox or Edge

# Open the target website
url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=fantasy"
driver.get(url)

# Step 3: Maximize window and wait for page to load
driver.maximize_window()
time.sleep(5)

# Step 4: Click the "X more" button 10 times
for i in range(10):
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), ' more')]"))
        )

        for button in buttons:
            text = button.text
            if re.search(r'\d+', text):
                driver.execute_script("arguments[0].click();", button)
                break

        time.sleep(5)
    except Exception:
        break

# XPath to find all list items (li elements)
elements = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')

# Extracting and formatting data
data = []
for index, element in enumerate(elements, start=1):
    text = element.text.strip()
    lines = text.split("\n")  # Split text by new lines
    
    # Parsing data correctly
    title = lines[0] if len(lines) > 0 else None
    runtime = lines[2] if len(lines) > 2 else None
    imdb_score = lines[4] if len(lines) > 4 else None
    votes = lines[5] if len(lines) > 5 else None

    data.append({
        "Title": title,
        "Runtime": runtime,
        "IMDB_Score": imdb_score,
        "Votes": votes,
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Remove columns where all values are NaN
df.dropna(axis=1, how='all', inplace=True)

# Save to CSV
df.to_csv("Fantasy_IMDb2024_list.csv", index=False, encoding="utf-8")

# Close the browser
driver.quit()

print("Data saved successfully!")
