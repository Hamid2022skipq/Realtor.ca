import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
file_name = "REALTOR_T.csv"
def main(url, i=None):
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    breakpoint()
    
    listings = driver.find_element(By.ID, "listInnerCon").find_elements(By.CLASS_NAME, 'cardCon')
    realtor_data = []
    for index, listing in enumerate(listings):
        try:

            link = listing.find_element(By.CSS_SELECTOR, "a.blockLink.listingDetailsLink")
            link_href = link.get_attribute("href")
            driver.execute_script("window.open(arguments[0], '_blank');", link_href)
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "listingPriceValue")))
            time.sleep(1)
            try:
                price_element = driver.find_element(By.ID, "listingPriceValue")
                price = price_element.text
            except:
                price = "Not Available"
            try:
                agent_element = driver.find_element(By.CSS_SELECTOR, "span.realtorCardName")
                agent_name = agent_element.text
            except:
                agent_name = 'Not Available'
            try:
                broker_element = driver.find_element(By.CSS_SELECTOR, "div.officeCardName")
                broker_name = broker_element.text
            except:
                broker_name = 'Not Available'

            directions = driver.find_element(By.ID, "listingHeaderRightBtnCon").find_element(By.TAG_NAME, "a").get_attribute('href')
            

            # Get the time text
            try:
                time_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_TimeOnRealtor > div.propertyDetailsSectionContentValue")))

                # Get the time text
                Time = time_element.get_attribute("innerText")
            except:
                Time = "Not Available"
            
            address_element = driver.find_element(By.ID, "listingAddress")
            text = address_element.text
            try:
                lat_long = directions.split("destination=")[1].split("%2c-")
            except:
                lat_long = ["Not Available","Not Available"]
            try:
                address_parts = text.split("\n", 1)
                city, state_postal_code =address_parts[1].split(",", 1)
                state, postal_code = state_postal_code.strip().split(" ", 1)
            except:
                city = "Not Available"
                state = "Not Available"
                postal_code = "Not Available"

            print("\n" + "*" * (index+1) , str(index+1) + "\n")
            data={
            'DATE':date.today(),
            'CITY':str(city.upper()),
            'STATE':str(state.upper()),
            'POSTAL CODE':str(postal_code.upper()),
            'PRICE':str(price.upper()),
            'ADDRESS':str(address_parts[0].upper()),
            'AGENT':str(agent_name.upper()),
            'BROKER':str(broker_name.upper()),
            'LATITUDE':str(lat_long[0].upper()),
            'LONGITUDE':str(lat_long[1].upper()),
            'TIME':str(Time)
            }
            realtor_data.append(data)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred with listing {index + 1}: {e}")
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            driver.quit()
    # print(realtor_data)
    field_names = ['DATE','ADDRESS','CITY','STATE','POSTAL CODE','AGENT','BROKER','PRICE','LATITUDE','LONGITUDE', "TIME"]
    with open(f'{file_name}', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        if i==None:
            writer.writeheader()
        writer.writerows(realtor_data)
    csvfile.close()


if __name__ == "__main__":

    for i in range(1,51):

        url=f'URL'
        # &PriceMin=1500000&PriceMax=1900000 T
        # PriceMin=1300000&PriceMax=2500000 M
        print("\n" + f"Accessing url : {url}" + "\n")
        main(url,i)