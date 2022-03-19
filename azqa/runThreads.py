import threading

def createThreads(functions, params):
    threads = []
    i = 0
    for function in functions:
        if type(params) is dict:
            threads.append(threading.Thread(target=function, args=(params,)))        
        elif (len(params) == 0):
            threads.append(threading.Thread(target=function))
        elif (len(params) == 1):
            threads.append(threading.Thread(target=function, args=(params[0])))
        else:
            threads.append(threading.Thread(target=function, args=(params[i])))
            i = i + 1
    return threads
    
def startThreads(functions, params):
    threads = createThreads(functions, params)
    runThreads(threads)

def runThreads(threads):
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()