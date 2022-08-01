CPCB Web Scraping Tool
==============================

A web scraping tool to scrape the data from CPCB website, process the downloaded files and upload it to the Kaatru
web server.

Getting Started
------------

The following things are required for this tool to function properly:

    -> Chrome browser
    -> Chrome driver (version matching the browser)
    -> india_coordinates.csv
    -> station_coordinates.csv

Project Organization
------------

    ├── README.md                          <- The top-level README for developers using this project.
    │
    ├── driver
    │   └── chromedriver.exe               <- The required driver to do the scraping
    │
    ├── files                              <- The directory in which the CPCB data files are downloaded
    │
    ├── processed_data                     <- The directory in which the processed interpolated data will be saved
    │
    ├── station_coordinates.csv            <- The CSV file containing the coordinates (lat, lng) of all the CPCB stations
    │
    ├── main.py                            <- The main script file containing the scraping logic
    │
    ├── india_coordinates.csv              <- The CSV file containing the coordinates of pan India
    │
    ├── requirements.txt                   <- The requirements file containing all the libraries needed to run this tool
    │
    ├── state.txt                          <- The text file containing the states of the scraping tool.
    │
    └── pre_processor.py                   <- The script file containing the logic for processing the downloaded data.
    


--------
