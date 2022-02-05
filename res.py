import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from res_config import ResConfig

VALID_ACCESS_TOKENS = ["sae"]

def parse_alert(a) -> str:
    if a == "Reservation Time: Reservations for this business can be only made 3 days in advance!":
        return "res too far in future"
    else: 
        return f"unknown {a}"

def set_date(driver, date):
    driver.find_element(By.ID, 'reservationdate').click()
    ms = f"{int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000 - 18000000)}"
    driver.find_element(By.XPATH, f"//*[@data-date='{ms}']").click()
    return True

def set_time(driver, t):
    el = driver.find_element(By.ID, 'reservationtime')
    for o in el.find_elements(By.TAG_NAME, 'option'):
        if o.text == t:
            o.click()
            return True
    return False
    
def set_party(driver, size):
    el = driver.find_element(By.ID, 'partysize')
    for o in el.find_elements(By.TAG_NAME, 'option'):
        if o.text == f"{size} people" or o.text == f"{size} person":
            o.click()
            return True
    return False

def submit(driver):
    driver.find_element(By.ID, 'submit-button').click()

def fill_fields(driver, firstname, lastname, phone, email):
    driver.find_element(By.XPATH, "//*[@name='guestfirstname']").send_keys(firstname)
    driver.find_element(By.XPATH, "//*[@name='guestlastname']").send_keys(lastname)
    driver.find_element(By.XPATH, "//*[@name='guestphone']").send_keys(phone)
    driver.find_element(By.XPATH, "//*[@name='guestemail']").send_keys(email)
    return True

def get_alert(driver):
    alert = driver.find_element(By.CLASS_NAME, 'alert')
    if alert:
        return alert.text
    return None 

   
def reserve(driver, c: ResConfig, outfile: str):
    print(f"reserving for {c.firstname} {c.lastname} ({c.phone}, {c.email}) on {c.date} at 5:00 pm for {c.size}.")
    driver.get("https://tableagent.com/boston/muddy-charles-pub/table-search/")
    time.sleep(1.0) # This sleep is required.

    errs = []
    if not set_date(driver, c.date):
        errs.append("failed to set date. make sure date is in the future")
    time.sleep(0.5)

    if not set_time(driver, '5:00 pm'):
        errs.append("failed to set time. might be closed on that day")
    time.sleep(0.5)

    if not set_party(driver, c.size):
        errs.append("failed to set party. must be in [1-4]")

    if len(errs) > 0:
        return errs 

    submit(driver)
    if driver.current_url != "https://tableagent.com/boston/muddy-charles-pub/table-select/":
        return [parse_alert(get_alert(driver))]

    # fill_fields(driver, c.firstname, c.lastname, c.phone, c.email)

    # # This sleep is optional.
    # time.sleep(1.0)

    # with open(outfile, 'w+') as f:
    #     f.write(driver.page_source)
    #     f.close()

    return [] 