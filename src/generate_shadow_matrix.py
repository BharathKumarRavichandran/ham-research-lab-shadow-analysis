import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.utils.solarposition import get_solarposition
from src.utils.shadowingfunction_wallheight_13 import shadowingfunction_wallheight_13
from src.utils.db import create_db_client
from src.utils.helpers import visualize_shadow_matrix
from src.utils.logger import logger


def load_dsm_data():
    dsm_data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data/dsm_local_array.npy")
    dsm = np.load(dsm_data_path)
    dsm = np.nan_to_num(dsm, nan=0)
    return dsm


def plot_dsm(dsm):
    f, ax = plt.subplots()
    plt.imshow(dsm, cmap='viridis')
    plt.show()


def create_date_range(start_datatime):
    end_datetime = start_datatime + pd.DateOffset(minutes=10)
    timestamps = pd.date_range(start_datatime, end_datetime, freq='30T')
    return timestamps


def preprocess_solar_data(df_solar_data, utc_offset):
    df_solar_data['TimeStamp'] = pd.DatetimeIndex(df_solar_data['TimeStamp']) - pd.DateOffset(hours=utc_offset)
    df_solar_data["TimeStamp"] = df_solar_data["TimeStamp"].apply(pd.to_datetime)
    df_solar_data.set_index("TimeStamp", inplace=True)
    logger.info(f"Datetime in preprocess solar data: {df_solar_data.index[0]}")
    return df_solar_data


def get_solar_positions(df_solar_data, lat, lon, utc_offset):
    df_solar = get_solarposition(df_solar_data.index, lat, lon)
    df_solar['TimeStamp'] = pd.DatetimeIndex(df_solar.index) + pd.DateOffset(hours=utc_offset)
    df_solar = df_solar[['TimeStamp', 'apparent_zenith', 'zenith', 'apparent_elevation', 'elevation',
                         'azimuth', 'equation_of_time']]
    df_solar["TimeStamp"] = df_solar["TimeStamp"].apply(pd.to_datetime)
    df_solar.set_index("TimeStamp", inplace=True)
    df_solar["TimeStamp"] = df_solar.index
    df_solar = df_solar[['TimeStamp', 'elevation', 'zenith', 'azimuth']]
    df_solar = df_solar.rename(columns={"elevation": "Elevation", "azimuth": "Azimuth", "zenith": "Zenith"})
    return df_solar


def calculate_shadowing(azimuth, altitude, dsm, scale, walls, dirwalls):
    sh, wallsh, wallsun, facesh, facesun = shadowingfunction_wallheight_13(
        dsm, azimuth, altitude, scale, walls, dirwalls * np.pi / 180.
    )
    return sh


def generate_shadow_matrix_for_datetime(start_datetime):
    dsm = load_dsm_data()
    # plot_dsm(dsm)

    # constants
    utc_offset = -6
    lat = 29.73463
    lon = -95.30052
    scale = 1
    walls = np.zeros((dsm.shape[0], dsm.shape[1]))
    dirwalls = np.zeros((dsm.shape[0], dsm.shape[1]))

    timestamps = create_date_range(start_datetime)
    df_solar_data = pd.DataFrame({'TimeStamp': timestamps})

    df_solar_data = preprocess_solar_data(df_solar_data, utc_offset)
    df_solar = get_solar_positions(df_solar_data, lat, lon, utc_offset)

    # len(df_solar) is 1 here
    for i in range(len(df_solar)):
        current_datetime = df_solar.index[i]
        altitude = df_solar['Elevation'].iloc[i]
        azimuth = df_solar['Azimuth'].iloc[i]
        hour = df_solar.index[i].hour
        minute = df_solar.index[i].minute
        logger.info(f"DF solar data: hour: "
                    f"{hour}, minute: {minute}, "
                    f"altitude: {altitude}, azimuth: {azimuth}")

        sh = calculate_shadowing(azimuth, altitude, dsm, scale, walls, dirwalls)
        sh_binary = pickle.dumps(sh)
        # visualize_shadow_matrix(sh, hour, minute)

        logger.info(f"Storing the generated shadow matrix with datetime: {current_datetime}")
        data = {
            "datetime": current_datetime,
            "shadow_matrix": sh_binary,
            "hour": hour,
            "minute": minute,
            "altitude": altitude,
            "azimuth": azimuth
        }

        db_client, collection = create_db_client()
        collection.insert_one(data)
        db_client.close()

        return current_datetime
