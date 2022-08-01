"""
This code takes the downloaded file from CPCB in .xlsx format
and extracts the PM2.5 data from them into a single file.
The data is then extrapolated to 3.4 million data points across
India. This extrapolated data is then exported as .CSV and 
read by the application. 
"""

import pandas as pd
import scipy.interpolate as interpolator
import numpy as np
from glob import glob


def processor(raw_data_folder, location_data_path, file_name):
    """
    The function reads data the .xlsx files downloaded from CPCB, 
    extracts the relevant PM 2.5 information.
    Args:
        raw_data_folder ('str'): Location of xlsx files downloaded from CPCB.
        location_data_path ('str'): Location of file which has the coordinates of CPCB stations.
        file_name ('str'): The name of the zip file
    Return:
        A dataframe with PM 2.5 values extracted from CPCB.
    """

    print('[+] processing data')
    cpcb_file_list = glob(raw_data_folder)
    df_list = []
    print('[+] converting individual xlsx files into single csv file')
    for file in cpcb_file_list:
        try:
            cpcb_df = pd.read_excel(file)
            column_mapping = {"CENTRAL POLLUTION CONTROL BOARD": "tags",
                              "Unnamed: 1": "col_1",
                              "Unnamed: 2": "col_2"}
            cpcb_df.rename(columns=column_mapping, inplace=True)
            station_name_index = int(cpcb_df[cpcb_df["tags"] == "Station"].index.values)
            station_name = cpcb_df["col_1"].iloc[station_name_index]
            df_station = pd.read_csv(location_data_path)
            temp = df_station[df_station["Station Name"] == station_name]
            latitude = temp["latitude"].iloc[0]
            longitude = temp["longitude"].iloc[0]
            data_point_start_index = int(cpcb_df[cpcb_df["tags"] == "From Date"].index.values)
            index = data_point_start_index + 1
            output_data = pd.DataFrame({
                "station": [station_name],
                "latitude": [latitude],
                "longitude": [longitude],
                "from_date": [cpcb_df["tags"].iloc[index]],
                "to_date": [cpcb_df["col_1"].iloc[index]],
                "pm2.5": [cpcb_df["col_2"].iloc[index]]
            })
            df_list.append(output_data)
        except IndexError:
            print(file)

    return_df = pd.concat(df_list)
    print('[+] converted individual xlsx files into single csv file')
    return_df["pm2.5"] = pd.to_numeric(return_df["pm2.5"], errors='coerce')
    return_df.dropna(inplace=True)
    return_df.to_csv(path_or_buf=f'./files/RAW_{file_name}.csv')
    print('[+] saved csv file')
    return return_df


def extrapolator(input_data, to_extrapolate_data_path, file_name, model="to_add"):
    """
    A function which extrapolates PM 2.5 from input coordinates to output coordinates.
    Args:
        model: The interpolation model, the default model is CloughTocher2DInterpolator
        input_data: The input data is dataframe created from the downloaded CPCB data.
        to_extrapolate_data_path: The CSV file path which contains the coordinates at which we want to extrapolate.
        file_name: The name of the zip file
    """
    print('[+] interpolating data')
    output = pd.read_csv(to_extrapolate_data_path)

    x = np.array(input_data["longitude"])
    y = np.array(input_data["latitude"])
    z = np.array(input_data["pm2.5"])

    interpolate = interpolator.NearestNDInterpolator(list(zip(x, y)), z)

    xi = output["longitude"]
    yi = output["latitude"]
    output["pm2.5"] = interpolate(xi, yi)
    print('[+] interpolated data')
    output.dropna(inplace=True)
    output.to_csv(path_or_buf=f'./processed_data/{file_name}.csv', index=False)
    print('[+] saved csv file containing interpolated data')
    return output
