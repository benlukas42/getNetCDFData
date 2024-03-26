"""
Contains useful functions for the program getNetCDFData.py

Author: Ben Lukas
"""



import xarray as xr
import matplotlib.pyplot as plt
import math
import numpy as np

def openDatabase(filename):
    try:
        db = xr.open_dataset(filename, decode_times=False)
        return db
    except ValueError:
        print("-> Error: Invalid filepath")
        return None

'''
Prints each variable name and its details.
For use with "python getNetCDFData.py <netCDF file>"
'''
def printVariables(filename):

    db = openDatabase(filename)
    if db is None:
        return -1
    variables = db.variables
    for var in variables:
        print('-> ' + str(var) + '\n\tAttributes:\t' + str(variables[var].attrs) + '\n\tDimensions:\t' + str(variables[var].dims))
    return 0

'''
Finds a data vector (or multiple) and prints it in a fancy-schmancy way.
For use with "python getNetCDFData.py <netCDF file> <variable> --mode vector <flags...>
returnTypes: 
        data_vectors (for general use)
        selections (for graphing)
'''
def createVectors(info, returnType):
    if returnType != 'data_vectors' and returnType != 'selections':
        print("-> Error: invalid returnType for createVector: " + str(returnType))
        return []

    db = openDatabase(info['filename'])
    if db is None:
        return []

    plotted_variable = db.__getitem__(info['variable'])
    dimensions = plotted_variable.dims
    num_vectors = int(len(info['position'])/2)

    data_vectors = []
    selections = []

    for i in range(num_vectors):
        selection = plotted_variable

        if dimensions.count("Time") > 0:
            selection = selection.sel(Time=slice(info['time'][0],info['time'][1]))

        if dimensions.count("latitude") > 0 and dimensions.count("longitude") > 0:
            selection = selection.sel(latitude=info['position'][2*i], longitude=info['position'][2*i+1], method="nearest")

        if dimensions.count("altitude") > 0:
            selection = selection.sel(altitude=info['altitude'], method="nearest")

        ## Print a header with some useful information
        if num_vectors > 1:
            if i > 0:
                print()
            print("-> Vector #" + str(i+1))
        if selection.attrs.__contains__('title') and selection.attrs.__contains__('units'):
            print(str(selection.attrs['title']) + " (" + str(selection.attrs['units']) + "):")
        elif selection.attrs.__contains__('title'):
            print(str(selection.attrs['title']) + ":")
        elif selection.attrs.__contains__('long_name') and selection.attrs.__contains__('units'):
            print(str(selection.attrs['long_name']) + " (" + str(selection.attrs['units']) + "):")
        elif selection.attrs.__contains__('long_name'):
            print(str(selection.attrs['title']) + ":")

        ## Print the data vector
        print("    " + str(selection.data))

        ## Add the data vector to dataVectors and selections
        data_vectors.append(selection.data)
        selections.append(selection)

        ## Print the data's dimensions/coordinates
        print(str(selection.coords))

        ## Print statistical information if --analyze flag
        if info['analyze']:
            analyzeVectors(selection)

    if returnType == 'data_vectors':
        return data_vectors
    elif returnType == 'selections':
        return selections


''''
Finds a data vector and graphs it. Multiple vectors are plotted on the same graph.
For use with "python getNetCDFData.py <netCDF file> <variable> --mode graph <flags...>
'''
def createGraph(info):
    selections = createVectors(info, "selections")
    data_vectors = []
    for selection in selections:
        selection.plot.line(x="Time")
        data_vectors.append(selection.data)
    plt.show()
    return data_vectors


'''
Helper function for analyzeVectors
Finds the coordinates of a given data point in a selection
'''
def printCoords(selection, find):
    data = selection.data
    index = -1
    for i in range(len(data)):
        if data[i] == find:
            index = i
    if index < 0:
        return

    for dim in selection.dims:
        if selection[index][dim].attrs.__contains__("long_name"):
            print("\t" + str(selection[index][dim].attrs["long_name"]) + " =", end = '')
        elif selection[index][dim].attrs.__contains__("title"):
            print("\t" + str(selection[index][dim].attrs["title"]) + " =", end = '')
        print(" " + str(selection[index][dim].data), end = '')
        if selection[index][dim].attrs.__contains__("units"):
            print(" " + str(selection[index][dim].attrs["units"]), end = '')
        print()
    return


'''
Takes a data vector (actually "selection") as an argument and prints statistics
'''
def analyzeVectors(selection):
    data = selection.data
    units = ""
    if selection.attrs.__contains__('units'):
        units = selection.attrs['units']

    # Print max
    maximum = max(data)
    print("Max:\t" + str(maximum) + " " + str(units))
    printCoords(selection, maximum)

    # Print min
    minimum = min(data)
    print("Min:\t" + str(minimum) + " " + str(units))
    printCoords(selection, minimum)

    # Print average
    average = sum(data) / len(data)
    print("Avg:\t" + str(average) + " " + str(units))

    return
