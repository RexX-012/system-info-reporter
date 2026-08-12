import os
from pickle import TRUE
import sys
import platform
import psutil
import winreg
import GPUtil

print("==" * 25)
print("      SYSTEM INFORMATION REPORTER       ")
print("==" * 25)

print()

print("OS:", platform.system())
print("OS Version:", platform.release())
print("Processor:", platform.processor())
print("Machine:", platform.machine())
print("Computer Name:", platform.node())
print("Python Version:", sys.version.split()[0])
print("Current User:", os.getlogin())

#RAM
mem = psutil.virtual_memory()
ram_total = round(mem.total/(1024 ** 3), 1)
ram_used = round(mem.used/(1024 ** 3), 1)
ram_free = round(mem.available/(1024 ** 3), 1)
ram_percent = mem.percent

#Storage
disk = psutil.disk_usage('/')
disk_total = round(disk.total/(1024 ** 3), 1)
disk_used = round(disk.used/(1024 ** 3), 1)
disk_free = round(disk.free/(1024 ** 3), 1)
disk_percent = disk.percent

print()

print("--" * 25)
print("     MEMORY (RAM)    ")
print("--" * 25)

print(f"Total RAM: {ram_total} GB" )
print(f"Currently Used: {ram_used} GB ({ram_percent} % in use)" )
print(f"Free: {ram_free} GB" )

print("--" * 25)
print("     STORAGE    ")
print("--" * 25)

print(f"Total Storage: {disk_total} GB" )
print(f"Currently Used: {disk_used} GB" )
print(f"Free: {disk_free} GB ({round(100 - disk.percent, 1)} % remaining)") 

#CPU

cpu_physical = psutil.cpu_count(logical=False)
cpu_logical = psutil.cpu_count(logical = True)
cpu_freq = psutil.cpu_freq()
cpu_speed = round(cpu_freq.current / 1000 , 2)
cpu_percent = psutil.cpu_percent(interval= 1)

print()

print("--" * 25)
print("     CPU INFORMATIONS    ")
print("--" * 25)

#print(f"Processor: {platform.processor()}")

print("----CPU NAME---")

try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
    cpu_name = winreg.QueryValueEx(key, "ProcessorNameString" )[0].strip()
    winreg.CloseKey(key)
    print(f"Processor: {cpu_name}")
except Exception as e:
    cpu_name = platform.processor()
    print(f"Failed: {e}")

#print(f"Processor: {cpu_name}")

print()

print(f"Physical Cores: {cpu_physical}")
print(f"Logical Cores: {cpu_logical}")
print(f"Current Speed: {cpu_speed} GHz")
print(f"CPU Usage: {cpu_percent} %")


#GPU
print()

print("--" * 25)
print("     GPU INFORMATIONS    ")
print("--" * 25)

gpus = GPUtil.getGPUs()

#CASE 1
if len(gpus) == 0:
    print("No GPU found.")
elif len(gpus) == 1:
    gpu = gpus[0]   
else:
    print(f"{len(gpus)} GPU's found")
    for i, gpu in enumerate(gpus):
        print(f"{i+1}. {gpu[i]}")
    while True:
        try:
            choice = int(input("\n Which GPU do you want to know about?"))
            if 1<= choice <= gpus[i]:
                gpu = gpus[choice - 1]
                break
            else:
                print("Choose a valid GPU number")
        except ValueError:
            print("Enter a valid Value")

print(f"Selected GPU: {gpu.name}")

gpu_total_memory = round(gpu.memoryTotal/1024, 2)
gpu_used_memory =  round(gpu.memoryUsed/1024, 2)
gpu_free_memory = round(gpu.memoryFree/1024, 2)
gpu_usage = round(gpu.load * 100, 2)
gpu_temperature = gpu.temperature

print(f"Total Memory: {gpu_total_memory}")
print(f"Used Memory: {gpu_used_memory}")
print(f"Free Memory: {gpu_free_memory} ")
print(f"GPU Usage: {gpu_usage} %")
print(f"GPU Temperature: {gpu_temperature} %")

