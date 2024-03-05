def parseArgs(args):
    info = {
        "filename": args[0],
        "variable": args[1],
        "mode": "vector",
        "position": [],
        "altitude": 0,
        "time": []
    }

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
        elif(args[i] == '--position'):
            positionArg = True
        elif(args[i] == '--altitude'):
            positionArg = False
            info['altitude'] = float(args[i+1])
            skip+=1
        elif(args[i] == '--time'):
            positionArg = False
            if(i+1 > len(args)-1 or not args[i+1].isnumeric() or i+2 > len(args)-1 or not args[i+2].isnumeric()):
                print('->Error: time flag is not followed by two numbers')
                return -1
            info['time'].append(float(args[i+1]))
            info['time'].append(float(args[i+2]))
            skip+=2
        else:
            if positionArg:
                if(not args[i].isnumeric() or i+1>len(args)-1 or not args[i+1].isnumeric()):
                    print('->Error: position flag is not passed pairs of numbers')
                    return -1
                info['position'].append(float(args[i]))
                info['position'].append(float(args[i+1]))
                skip+=1
            else:
                #Unknown argument
                print('->Error: Invalid argument: ' + str(args[i]))
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