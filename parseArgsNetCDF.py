"""
This program simply parses arguments passed to getNetCDFData.py, ensuring that they're all there and valid.

Author: Ben Lukas
"""


def parseArgs(args):
    info = {
        "filename": args[0],
        "variable": args[1],
        "mode": "vector",
        "position": [],
        "altitude": 0,
        "time": [],
        "analyze": False
    }

    if info['variable'][0:2] == "--":
        print("-> Error: missing variable argument")
        return -1


    skip = 0
    positionArg = False
    ## For args[2] and greater, look for flags
    for i in range(2, len(args)):
        if skip > 0:
            skip-=1
            continue
        if(args[i] == '--mode'):
            positionArg = False
            info['mode'] = args[i+1]
            skip+=1
        elif(args[i] == '--analyze'):
            positionArg = False
            info['analyze'] = True
        elif(args[i] == '--position'):
            positionArg = True
        elif(args[i] == '--altitude'):
            positionArg = False
            info['altitude'] = float(args[i+1])
            skip+=1
        elif(args[i] == '--time'):
            positionArg = False
            if(i+1 > len(args)-1 or
                    i+2 > len(args)-1 or
                    (not type(args[i + 1]) == int and not type(args[i + 2]) == int) and
                    (not args[i+1].isnumeric() and not args[i+2].isnumeric())):
                print('-> Error: time flag is not followed by two numbers')
                return -1
            info['time'].append(float(args[i+1]))
            info['time'].append(float(args[i+2]))
            skip+=2
        else:
            if positionArg:
                if i+1>len(args)-1:
                    print('-> Error: position flag is not passed pairs of numbers')
                    return -1
                info['position'].append(float(args[i]))
                info['position'].append(float(args[i+1]))
                skip+=1
            else:
                #Unknown argument
                print('-> Error: Invalid argument: ' + str(args[i]))
                return -1
    if len(info['position']) == 0:
        info['position'].append(0)
        info['position'].append(0)
    if len(info['time']) == 0:
        info['time'].append(1)
        info['time'].append(2)

    ## For testing
    # print('filename: ' + str(info['filename']))
    # print('variable: ' + str(info['variable']))
    # print('mode: ' + str(info['mode']))
    # print('position: ' + str(info['position']))
    # print('altitude: ' + str(info['altitude']))
    # print('time: ' + str(info['time']))

    return info