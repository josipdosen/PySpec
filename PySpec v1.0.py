#Start of Program Code

# Importing the proper moduels
import platform
import cpuinfo
import psutil
import GPUtil
import time
import wmi 
from datetime import datetime
from tabulate import tabulate

##
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
        
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

##
print ("Program has started and is executing")
print (" ")
print ("PySpec (c) 2022 Josip Dosen")
print ("https://github.com/josipdosen")
print ("Version: v1.0")

time.sleep(5)

print ("")
print ("Scanning your Computer *Please Wait*")


time.sleep(5)

print("="*40, "System Information about your PC", "="*40)
uname = platform.uname()
print(f"Operating System (OS): {uname.system}")
print(f"Operating System Version: {uname.release}")
print(f"Operating System Build Number: {uname.version}")
print(f"Computer Name: {uname.node}")
print ("Processor Vendor:", cpuinfo.get_cpu_info()["vendor_id_raw"])
print ("Processor (CPU):",cpuinfo.get_cpu_info()["brand_raw"] )
print ("System Type and Architecture:",cpuinfo.get_cpu_info()["arch"] )
svmem = psutil.virtual_memory()
print(f"Installed Memory (RAM): {get_size(svmem.total)}")

c = wmi.WMI() 
my_system = c.Win32_ComputerSystem()[0]
print(f"Motherboard Manufacturer: {my_system.Manufacturer}")
print(f"Motherboard Model: {my_system.Model}")

# Grab info of installed GPUs

print ("Installed GPUs:")

gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_total_memory, 
      
    ))
print(tabulate(list_gpus, headers=("id", "GPU name","total video memory (VRAM)")))

print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

#CPUID - Grab Processor Info
print("="*40, "CPU Information (CPUID)", "="*40)
print ("Processor (CPU):",cpuinfo.get_cpu_info()["brand_raw"] )
print(f"Processor Family, Model and Manufacturer: {uname.processor}")
print ("CPU Architecture:",cpuinfo.get_cpu_info()["arch"])
print ("CPU Base Clock:", cpuinfo.get_cpu_info()["hz_advertised_friendly"])
print("Physical Cores:", psutil.cpu_count(logical=False))
print("Logical Threads:", psutil.cpu_count(logical=True))
#print("CPU L1 Cache:", cpuinfo.get_cpu_info()["L1_icache_size"],"B") <--- L1 cache command does not exist
print("CPU L2 Cache:", cpuinfo.get_cpu_info()["l2_cache_size"],"B")
print("CPU L3 Cache:", cpuinfo.get_cpu_info()["l3_cache_size"],"B")
print("CPU Instruction Sets:", cpuinfo.get_cpu_info()["flags"])

print("""
Taking a snapshot of CPU Usage per Core. *Please Wait*""")
time.sleep(10)

print("Stamp of CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

#GPUID - Grab GPU Info

print("="*40, "GPU Information (GPUID)", "="*40)

gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))

print(tabulate(list_gpus, headers=("id", "GPU name", "load", "free video memory", "used video memory", "total video memory (VRAM)",
                                   "temperature", "uuid")))

print("="*40, "System Memory (RAM) Information ", "="*40)

svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")

print("="*40, "System Storage Infomation , Hard Drives(HDDs) and/ or Solid State Drives(SSDs)", "="*40)

print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")


print ("")
print ("*Scanning Complete* Information Ready")

print("""
Press ENTER to exit and terminate the program""")
input() 


#End of Program Code
