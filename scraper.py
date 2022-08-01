import os
import time
import sys
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.service import Service
import glob
import datetime
import requests
from pre_processor import processor, extrapolator
from utility import color_print
from dotenv import load_dotenv


def load_app_state():
    print('[+] loading app states')
    global state_count, state_length, city_count, city_length, station_length, station_count, download_count
    with open('state.txt') as file:
        app_states = [int(state.split('\n')[0]) for state in file.readlines()]
        state_count = app_states[0]
        state_length = app_states[1]
        city_count = app_states[2]
        city_length = app_states[3]
        station_count = app_states[4]
        station_length = app_states[5]
        download_count = app_states[6]
        print('[+] app states has been loaded successfully')
        open_driver()


def update_app_state():
    print('[+] updating app states')
    global state_count, state_length, city_count, city_length, station_length, station_count, download_count
    with open('state.txt', 'w') as file:
        app_states = [state_count, state_length, city_count, city_length, station_count, station_length,
                      download_count]
        file.writelines([str(states) + '\n' for states in app_states])
        print('[+] app states has been updated successfully')


def open_driver():
    global driver
    driver = webdriver.Chrome(web_driver_path, options=options)
    driver.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data')
    driver.implicitly_wait(10)
    select_state()


def select_state():
    global state_count, driver, state_length
    print(f'[+] selecting state no: {state_count + 1}')
    try:
        state_dropbox = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                      '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                                      '1]/div/ng-select/div')
        state_dropbox.click()
        if state_length == 0:
            states = driver.find_elements(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                    '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                                    f'1]/div/ng-select/select-dropdown/div/div[2]/ul/li')
            state_length = len(states)
        if state_count < state_length:
            state = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                  '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                                  f'1]/div/ng-select/select-dropdown/div/div[2]/ul/'
                                                  f'li[{state_count + 1}]')

            state.click()
            select_city()
        else:
            process_data()
    except selenium.common.exceptions.NoSuchElementException:
        color_print(255, 0, 0, '[-] website loading timeout')
        driver.quit()
        time.sleep(sleep_time)
        open_driver()


def select_city():
    update_app_state()
    global state_count, city_count, station_count, city_length, station_length
    print(f'[+] selecting city no: {city_count + 1}')
    city_dropbox = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                 '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                                 '2]/div/ng-select/div')
    city_dropbox.click()
    if city_length == 0:
        cities = driver.find_elements(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                                f'2]/div/ng-select/select-dropdown/div/div[2]/ul/li')
        city_length = len(cities)
    if city_count < city_length:
        city = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                             '1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div['
                                             f'2]/div/ng-select/select-dropdown/div/div[2]/ul/li[{city_count + 1}]')
        city.click()
        select_station()
    else:
        state_count += 1
        city_count = 0
        city_length = 0
        station_length = 0
        station_count = 0
        select_state()


def select_station():
    update_app_state()
    global station_count, city_count, station_length
    print(f'[+] selecting station no: {station_count + 1}')
    station_dropbox = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                    '1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div['
                                                    '1]/div/ng-select/div')
    station_dropbox.click()
    if station_length == 0:
        stations = driver.find_elements(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                  '1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div['
                                                  f'1]/div/ng-select/select-dropdown/div/div[2]/ul/li')
        station_length = len(stations)
    if station_count < station_length:
        station = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                '1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div['
                                                f'1]/div/ng-select/select-dropdown/div/div[2]/ul/li'
                                                f'[{station_count + 1}]')
        station.click()
        station_count += 1
        select_parameters()
    else:
        city_count += 1
        station_length = 0
        station_count = 0
        select_city()


def select_parameters():
    parameter_dropbox = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                      '1]/div/main/section/app-caaqm-view-data/div/div/div['
                                                      '2]/div[2]/div/div/multi-select/angular2-multiselect/div')
    parameter_dropbox.click()

    # define 'parameter' variable as below for selecting only PM2.5 parameter
    parameter = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                              '1]/div/main/section/app-caaqm-view-data/div/div/div['
                                              '2]/div[2]/div/div/multi-select/angular2-multiselect/div/div['
                                              '2]/div[2]/ul/li[1]/label')

    parameter.click()
    select_from_date()


def select_from_date():
    from_date_input = driver.find_element(By.XPATH, '//*[@id="date"]/angular2-date-picker/div/div[1]')
    from_date_input.click()
    calendar_table = driver.find_element(By.XPATH, '//*[@id="date"]/angular2-date-picker/div/div[2]/table[2]/tbody')
    for day in calendar_table.find_elements(By.XPATH, './/tr'):
        for date in day.find_elements(By.XPATH, './/td'):
            if date.text == str(datetime.datetime.now().date().day - day_difference):
                date.click()
    submit()


def select_to_date():
    from_date_input = driver.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[1]')
    from_date_input.click()
    calendar_table = driver.find_element(By.XPATH,
                                         '//*[@id="date2"]/angular2-date-picker/div/div[2]/table[2]/tbody')
    for day in calendar_table.find_elements(By.XPATH, './/tr'):
        for date in day.find_elements(By.XPATH, './/td'):
            if date.text == str(datetime.datetime.now().date().day - day_difference + 1):
                date.click()
    submit()


def submit():
    global download_count
    submit_button = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                  '1]/div/main/section/app-caaqm-view-data/div/div/div[5]/button')
    submit_button.click()
    download_count += 1
    download()


def download():
    try:
        download_button = driver.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div['
                                                        '1]/div/main/section/app-caaqm-view-data-report/div[2]/div['
                                                        '1]/div[ '
                                                        '2]/div/div/a[2]')
        download_button.click()
        time.sleep(5)
        # driver.quit()
        update_download_count()
    except [selenium.common.exceptions.ElementClickInterceptedException, selenium.common.exceptions
            .NoSuchElementException]:
        driver.close()
        time.sleep(3)
        download()


def update_download_count():
    global station_count, download_count
    path = os.listdir(data_download_path)
    if download_count > len(path):
        color_print(255, 0, 0, f'[-] file no {download_count} download failed')
        download_count -= 1
        station_count -= 1
    else:
        print(f'[+] file no {download_count} has been downloaded')
        time.sleep(5)
    update_app_state()
    driver.back()
    select_state()
    # open_driver()


def process_data():
    global file_name
    print("[+] scraping has been completed. processing data now")
    file_name = (datetime.datetime.now() - datetime.timedelta(days=day_difference)).strftime("%Y_%m_%d_%H_%M")
    df = processor(CPCB_raw_data_path, CPCB_station_coords_path, file_name)
    extrapolator(df, to_extrapolate_data_path, file_name)
    with open('state.txt', 'w') as file:
        file.writelines(['0\n' for _ in range(7)])
        print('[+] app states has been refreshed')
    upload_data()


def upload_data():
    print('[+] uploading the processed data to the server')
    res: requests.Response
    with open(f'./processed_data/{file_name}.csv', 'rb') as data:
        try:
            res = requests.post(os.environ.get('SERVER_URL'), data=data)
        except requests.exceptions.ConnectionError:
            color_print(255, 0, 0, '[-] uploading has been failed')
    if res.status_code == 200:
        print('[+] uploading has been completed')
        os.remove(f'processed_data/{file_name}.csv')
        print('[+] processed data is removed')
    else:
        color_print(255, 0, 0, '[-] uploading has been failed')
    file_list = glob.glob(data_download_path + "*.xlsx")
    print('[+] removing downloaded xlsx files')
    for file in file_list:
        os.remove(file)
    print('[+] removed downloaded xlsx files')


state_count = 0
state_length = 0
city_count = 0
city_length = 0
station_count = 0
station_length = 0
download_count = 0
TOTAL_STATIONS = 361

web_driver_path = os.getcwd() + r"\driver\\chromedriver.exe"
data_download_path = os.getcwd() + r"\files\\"
CPCB_station_coords_path = os.getcwd() + r"\station_coordinates.csv"
to_extrapolate_data_path = os.getcwd() + r"\india_coordinates.csv"
data_write_path = "./processed_data/"
CPCB_raw_data_path = "./files/*.xlsx"
file_name = ''
day_difference = 0
sleep_time = 2

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('headless')
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": data_download_path,
         "directory_upgrade": True}

options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(web_driver_path, options=options)
sys.setrecursionlimit(10000)
