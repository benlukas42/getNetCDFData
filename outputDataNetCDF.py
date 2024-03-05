import xarray as xr
import matplotlib.pyplot as plt

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
'''
def createVector(info):

    db = openDatabase(info['filename'])
    if db is None:
        return -1

    plotted_variable = db.__getitem__(info['variable'])
    dimensions = plotted_variable.dims
    num_vectors = int(len(info['position'])/2)

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
            print("-> Vector #" + str(i*2))
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

        ## Print the data's dimensions/coordinates
        print(str(selection.coords))
    return 0

''''
Finds a data vector and graphs it. Multiple vectors are plotted on the same graph.
For use with "python getNetCDFData.py <netCDF file> <variable> --mode graph <flags...>
'''
def createGraph(info):
    db = openDatabase(info['filename'])
    if db is None:
        return -1

    plotted_variable = db.__getitem__(info['variable'])
    dimensions = plotted_variable.dims
    num_vectors = int(len(info['position']) / 2)

    for i in range(num_vectors):
        selection = plotted_variable
        if dimensions.count("Time") > 0:
            selection = selection.sel(Time=slice(info['time'][0], info['time'][1]))
        else:
            ## Graph must be used with a variable that has Time as a dimension
            return -1
        if dimensions.count("latitude") > 0 and dimensions.count("longitude") > 0:
            selection = selection.sel(latitude=info['position'][2 * i], longitude=info['position'][2 * i + 1],
                                      method="nearest")
        if dimensions.count("altitude") > 0:
            selection = selection.sel(altitude=info['altitude'], method="nearest")

        selection.plot.line(x="Time")

    plt.show()
    return 0