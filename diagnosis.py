import os.path
from scraper import load_app_state
from utility import color_print
from pyfiglet import Figlet
from dotenv import load_dotenv

load_dotenv()
f = Figlet(font='banner3-D')
print(f.renderText('Kaatru CPCB Web Scraper'))

cwd: str = os.getcwd()
diagnosis: bool = True

print('Requirements:')
if os.path.exists(cwd + r'\driver\chromedriver.exe'):
    print(' - [✓] chrome driver')
else:
    diagnosis = False
    print(' - [✖] chrome driver\n       -> please add chrome driver with the name "chromedriver.exe" inside the '
          '"driver" '
          'directory.')
if not os.path.exists(cwd + r'\cpcb_data'):
    os.mkdir(cwd + r'\cpcb_data')
print(' - [✓] cpcb data download directory')
if not os.path.exists(cwd + r'\processed_data'):
    os.mkdir(cwd + r'\processed_files')
print(' - [✓] processed data download directory')
if os.path.exists(cwd + r'\india_coordinates.csv'):
    print(' - [✓] india coordinates csv file')
else:
    diagnosis = False
    print(' - [✖] india coordinates csv file\n       -> please add india coordinates csv file with the name '
          '"india_coordinates.csv" in the working directory.')
if os.path.exists(cwd + r'\station_coordinates.csv'):
    print(' - [✓] cpcb station coordinates csv file')
else:
    diagnosis = False
    print(' - [✖] cpcb station coordinates csv file\n       -> please add CPCB station coordinates csv file with the '
          'name "station_coordinates.csv" in the working directory')
color_print(240, 230, 140, f'\nDo you wanna change the url for uploading data? current: '
                           f'{os.environ.get("SERVER_URL")}. '
                           f'If yes please type it else press enter')
url = input().strip()
if len(url) > 0:
    os.environ['SERVER_URL'] = url
if not diagnosis:
    color_print(255, 0, 0, '\nWarning: please resolve the issues mentioned above and run the script again')
else:
    color_print(0, 255, 0, '\nSuccess: Running the scraper now...')
    load_app_state()
