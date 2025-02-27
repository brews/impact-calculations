"""Helper functions for reading IRI forecasts."""

import numpy as np
from netCDF4 import Dataset

temp_path = "/shares/gcp/climate/IRI/final_v2/tas_aggregated_forecast_Feb-Jun2017.nc"
prcp_path = "/shares/gcp/climate/IRI/final_v2/prcp_aggregated_forecast_Feb-Jun2017.nc"
temp_mean_climate_path = "/shares/gcp/climate/IRI/final_v2/tas_aggregated_climatology_1982-2010.nc"
prcp_mean_climate_path = "/shares/gcp/climate/IRI/final_v2/prcp_aggregated_climatology_1982-2010.nc"
temp_sdev_climate_path = "/shares/gcp/climate/IRI/final_v2/tas_aggregated_historical_std_1982-2010_IR.nc"
temp_adm0sdev_climate_path = "/shares/gcp/climate/IRI/final_v2/tas_aggregated_historical_std_1982-2010_ISO.nc"

def readncdf_allpred(filepath, variable, lead):
    """
    Yield weather for each region for each forecast month, of the given lead
    """
    rootgrp = Dataset(filepath, 'r', format='NETCDF4')
    alldata = rootgrp.variables[variable][:, :, :]
    rootgrp.close()

    for month in range(alldata.shape[0]):
        yield maskmissing(alldata[month, lead, :])

def readncdf_allmonths(filepath, variable):
    """
    Return weather for each region for a variable with just 12 values
    """
    rootgrp = Dataset(filepath, 'r', format='NETCDF4')
    alldata = rootgrp.variables[variable][:, :]
    rootgrp.close()

    return alldata

def maskmissing(weather):
    weather[weather > 1e10] = np.nan
    return weather

def get_means(regions, getvalues):
    bycountry = {} # {iso: [values]}
    bycountry2 = {} # same, but with every country
    for ii in range(len(regions)):
        values = getvalues(ii)
        
        if regions[ii][:3] in bycountry2:
            bycountry2[regions[ii][:3]].append(values)
        else:
            bycountry2[regions[ii][:3]] = [values]

        if not np.all(np.isfinite(values)):
            continue

        if regions[ii][:3] in bycountry:
            bycountry[regions[ii][:3]].append(values)
        else:
            bycountry[regions[ii][:3]] = [values]

    for country in bycountry2:
        if country in bycountry:
            bycountry[country] = np.mean(bycountry[country], axis=0)
        else:
            bycountry[country] = np.mean(bycountry2[country], axis=0)

    return bycountry
