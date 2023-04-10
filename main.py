import os

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt



def readData(file):
    ds = xr.open_dataset(
        file,
        engine="cfgrib",
        backend_kwargs={
            'filter_by_keys': {'stepType': 'accum', 'typeOfLevel': 'surface'}
        }
    )
    print('is this work')
    for v in ds:
        print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))
    print("\n")


    ds = ds.get("tp")
    print(ds)
    df = ds.to_dataframe()

    latitudes = df.index.get_level_values("latitude")
    longitudes = df.index.get_level_values("longitude")

    map_function = lambda lon: (lon - 360) if (
                lon > 180) else lon  # convert from 0 to 360 degrees to -180 to 180 degrees
    remapped_longitudes = longitudes.map(map_function)

    df["longitude"] = remapped_longitudes  # add the configured coordinates to the dataframe
    df["latitude"] = latitudes

    min_lat = 51.5  # closest coordinates corresponding to location of Tylorstown
    max_lat = 51.5
    min_lon = -3.5
    max_lon = -3.5

    # min_lat = 51.6
    # max_lat = 51.7
    # min_lon = -3.4
    # max_lon = -3.3

    lat_filter = (df["latitude"] >= min_lat) & (df["latitude"] <= max_lat)
    lon_filter = (df["longitude"] >= min_lon) & (df["longitude"] <= max_lon)

    df = df.loc[lat_filter & lon_filter]  # obtaining the data corresponding to Tylorstown's coordinates

    entriesToDataframe.append(df.iloc[0])  # add to dataframe


#Probably don't need this; gonna comment it out
# def plotGraph(graphType, date):
#
#     xOnGraph = dfTest["valid_time"]
#     plt.xlabel("Valid Time, in 3-hour Intervals")
#
#     titleCategory = ""
#
#     if graphType == "instant":
#         yOnGraphInstant = dfTest["tp"]
#         titleCategory = "Instantaneous"
#         plt.ylabel("Instantaneous Rainfall, in mm, in 3-hour Intervals")
#         plt.plot(xOnGraph, yOnGraphInstant)
#
#     if graphType == "accum":
#         yOnGraphAccum = dfTest["tp_accum"]
#         titleCategory = "Accumulated"
#         plt.ylabel("Accumulating Rainfall, in mm, in 3-hour Intervals")
#         plt.plot(xOnGraph, yOnGraphAccum)
#
#     plt.title(f"{titleCategory} Rainfall Against Time in 3-Hour Intervals, for {date} Feb 2020")
#
#
#     plt.show()



# parentFolder = (r"E:\GFS Data\Rainfall Data")
# parentFolder = r"E:\GFS Data\caseStudies\2015"
parentFolder = r"E:\GFS Data\caseStudies\2015\0"

print(parentFolder)
os.chdir(parentFolder)

entriesToDataframe = []

readData(r"gfs_4_20150101_0000_003.grb2")


########################
# for folderContainingDate in os.listdir(): #folders of dates
#
#     os.chdir(f"{os.getcwd()}/{folderContainingDate}")#go into each folder which has rainfall data
#     print(f"In folder: {folderContainingDate}")
#     entriesToDataframe = []
#     for fileContainingRainfallData in os.listdir():
#         if fileContainingRainfallData.endswith(("idx","csv","000.grb2")):
#             continue
#
#         readData(fileContainingRainfallData)
#
#     dfTest = pd.DataFrame(entriesToDataframe)
#     dfTest["tp_accum"] = dfTest["tp"].cumsum()
#
#     plotGraph("instant", folderContainingDate)
#
#     dfTest.to_csv(f"rainData{folderContainingDate}.csv")
#
#     print("Finished")
#
#     os.chdir(parentFolder)
#     print("back to parent folder")
#     print("\n")
# print("all is done")
########################

