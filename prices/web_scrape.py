from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def scrape_economic_calendar():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    driver.get("https://www.investing.com/economic-calendar/")

    # Wait for the table to load
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "economicCalendarData")))

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # List to store the scraped data
    events_data = []

    # Get current date
    current_date = datetime.now().strftime("%Y/%m/%d")

    # Iterate through the rows
    for row in rows:
        try:
            # Check if the row is for today and USD
            date_attr = row.get_attribute("data-event-datetime")
            currency = row.find_element(By.CLASS_NAME, "flagCur").text

            if date_attr and date_attr.startswith(current_date) and currency == "USD":
                # Check if it's high impact
                impact = row.find_element(By.CLASS_NAME, "sentiment").find_elements(By.TAG_NAME, "i")
                if len(impact) == 3:
                    # Extract required information
                    time = row.find_element(By.CLASS_NAME, "time").text
                    event = row.find_element(By.CLASS_NAME, "event").text
                    actual = row.find_element(By.CLASS_NAME, "act").text
                    forecast = row.find_element(By.CLASS_NAME, "fore").text
                    previous = row.find_element(By.CLASS_NAME, "prev").text

                    # Add to the list
                    events_data.append({
                        "Time": time,
                        "Event": event,
                        "Actual": actual,
                        "Forecast": forecast,
                        "Previous": previous
                    })
        except Exception as e:
            print(f"Error processing row: {e}")

    # Close the browser
    driver.quit()

    return events_data

# Usage
if __name__ == "__main__":
    economic_data = scrape_economic_calendar()
    for event in economic_data:
        print(event)