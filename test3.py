import psutil
def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                process_handles=proc.num_handles()
                if process_handles >900:
                    print(process_handles)
                    if process_handles >=1150:
                        return True
                    elif process_handles <= 1150 and process_handles >=980:
                        proc.terminate()
                        return False
                    else:
                        return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if checkIfProcessRunning("zoom"):
    print("true")
else:
    print("false")
    
