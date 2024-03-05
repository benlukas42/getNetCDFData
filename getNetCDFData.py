## Imports for command line argument handling
import sys
import parseArgsNetCDF as parser

## Imports for netCDF/graphing
import outputDataNetCDF


'''
Prints some details about this python application.
For use with "python getNetCDFData.py --help"
'''
def printHelp():
    print('-> Takes a netCDF file and a variable as an argument, and extracts a vector of data.')
    print('-> Optionally use graph mode to plot data vectors on a graph. This mode requires a variable that has Time as a dimension.')
    print('-> Use optional flags to set mode, as well as variable dimensions.')
    print('-> By default, mode=vector, latitude=0, longitude=0, altitude=0, time=1:2')
    return


'''
Prints the usage information of this python application.
Prints on incorrect usage or when passing "--help" flag
'''
def printUsage():
    print('-> Usage: python getNetCDFData.py [--help] <netCDF file> <variable> <flags...>')
    print('-> Run "python getNetCDFData.py <netCDF file>" to see corresponding variables and their details.')
    print('       Optional flags:')
    print('         --help (prints useful information about getNetCDFData.py)')
    print('         --mode <vector or graph>')
    print('         --position <latitude_1> <longitude_1> <latitude_2> <longitude_2>... <latitude_n> <longitude_n>')
    print('         --altitude <altitude>')
    print('         --time <start> <end>')
    return


def main():
    ## Setting up command line argument parsing
    args = sys.argv[1:]

    if len(args) == 0:
        printUsage()
        return -1
    elif len(args) == 1:
        if (args[0] == '--help'):
            printHelp()
            printUsage()
            return -1
        else:
            if outputDataNetCDF.printVariables(args[0]) < 0:
                return -1
            return 0
        pass

    info = parser.parseArgs(args)
    if info == -1:
        printUsage()
        return -1

    if(info['mode'] == 'vector'):
        print("-----------Vector Mode-------------")
        if(outputDataNetCDF.createVector(info) < 0):
            return -1
    elif(info['mode'] == 'graph'):
        print("-----------Graph Mode-------------")
        if(outputDataNetCDF.createGraph(info) < 0):
            return -1

    return 0


if __name__ == '__main__':
    print('-> Main returned with ' + str(main()))
