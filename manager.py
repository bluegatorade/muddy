import time
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
import threading

import res
from res_config import ResConfig

lock = threading.Lock()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')

DRIVER = webdriver.Chrome(chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))
DRIVER.implicitly_wait(1.0)

# function to check for reservations on a given date
def exec(config: ResConfig) -> [str]:
    return res.reserve(DRIVER, config, 'out.html')

def exec_all(d: str) -> {str: [str]}:
    # double check formatting before reading a file
    try: 
        datetime.strptime(d, '%Y-%m-%d')
    except ValueError as e:
        return {'all': 'incorrect date'} 

    err_map : {str: str} = {} 

    try:
        f = open(f"data/{d}", "r")
        for l in f.readlines():
            c = ResConfig.FromString(l)
            if not c:
                # TODO handle err?
                print(f"skipping line, couldn't parse: '{l}'")
                continue

            errs = exec(c)
            if len(errs) == 0:
                err_map[c.lastname] = "success"
            else: 
                err_map[c.lastname] = errs
        f.close()
        with open(f"data/{d}", "w") as f:
            f.write("")
            print(f"flushed reservations for {d}")

    except FileNotFoundError as e:
        print(f"no reservations found for {d}")
        pass
    return err_map

# write new reservations to file of date
def PlanRes(config: ResConfig) -> [str]:
    lock.acquire()
    errs = []
    try: 
        d = datetime.strptime(config.date, '%Y-%m-%d')

        # requested date is less than 3 days away.
        if date.today() >= (d - timedelta(days=3)).date():
            print(f"res for {d}, executing immediately")
            errs = exec(config)
        else:
            # save to appropiate file
            with open(f"data/{config.date}", 'a+') as f:
                f.write(f"{str(config)}\n")
    except Exception as e:
        errs = [str(e)]
    except:
        pass

    lock.release()
    return errs 

INTERVAL_S = 600
def Start():
    while True:
        d = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        print(f"cron executing {d}. results below")
        lock.acquire()
        for lastname, errs in exec_all(d).items():
            print(f"{lastname}: {errs}")
        lock.release()
        print(f"done cron executing {d}")
        time.sleep(INTERVAL_S)