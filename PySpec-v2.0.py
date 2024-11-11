
#Import Modules

import platform
import cpuinfo
import psutil
import GPUtil
import time
import wmi
import sys
import os
from datetime import datetime
from tabulate import tabulate

class MultiStream:
    def __init__(self, *streams):
        '''Initializes the MultiStream with multiple output streams'''
        self.streams = streams
    
    def write(self, message):
        '''Writes a message to all streams'''
        for stream in self.streams:
            stream.write(message)
            stream.flush()
    
    def flush(self):
        '''Flushes all streams'''
        for stream in self.streams:
            stream.flush()

class SystemInfo:
    def __init__(self):
        '''Initializes the system information'''
        self.uname = platform.uname()
        self.cpu_info = cpuinfo.get_cpu_info()
        self.svmem = psutil.virtual_memory()
        self.gpus = GPUtil.getGPUs()
        self.my_system = wmi.WMI().Win32_ComputerSystem()[0]
        self.boot_time = psutil.boot_time()
    
    def get_size(self, bytes, suffix="B"):
        '''Scales bytes to its proper format'''
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
    
    def Initilize(self):
        '''Prints the initial information about the program'''
        print ("Program has started and is executing")
        print (" ")
        print ("PySpec (c) 2024 Josip Dosen")
        print ("https://github.com/josipdosen")
        print ("Version: v2.0")
        time.sleep(5)
        print ("")
        print ("Scanning your Computer *Please Wait*")
        time.sleep(5)
    
    def display_system_info(self):
        '''Displays the system information about the computer'''
        print("="*40, "System Information about your PC", "="*40)
        print(f"Operating System (OS): {self.uname.system}")
        print(f"Operating System Version: {self.uname.release}")
        print(f"Operating System Build Number: {self.uname.version}")
        print(f"Computer Name: {self.uname.node}")
        print("Processor Vendor:", self.cpu_info["vendor_id_raw"])
        print("Processor (CPU):", self.cpu_info["brand_raw"])
        print("System Type and Architecture:", self.cpu_info["arch"])
        print(f"Installed Memory (RAM): {self.get_size(self.svmem.total)}")
        print(f"Motherboard Manufacturer: {self.my_system.Manufacturer}")
        print(f"Motherboard Model: {self.my_system.Model}")
        print("Installed GPUs:")
        self.display_gpu_info_partial()
        time.sleep(5)
    
    def display_gpu_info_partial(self):
        '''Displays the GPU information'''
        list_gpus = []
        for gpu in self.gpus:
            list_gpus.append((gpu.id, gpu.name, f"{gpu.memoryTotal}MB"))
        print(tabulate(list_gpus, headers=("id", "GPU name", "total video memory (VRAM)")))
    
    def display_boot_time(self):
        '''Displays the boot time of the computer'''
        bt = datetime.fromtimestamp(self.boot_time)
        print("="*40, "Boot Time", "="*40)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        time.sleep(5)

    def get_cpu_codename(self, cpu_name):
        '''Returns the CPU codename based on the CPU name'''
        intel_codenames = {
            'i7-14700K': 'Raptor Lake',
            'i7-13700H': 'Raptor Lake',
            'i7-9700K' : 'Coffee Lake',
            'i5-8500T' : 'Coffee Lake',
            'i3-10100Y': 'Amber Lake',
            'E5-2470 v2' : 'Ivy Bridge EN',
        }
        for model in intel_codenames.keys():
            if model in cpu_name:
                return intel_codenames[model]
        return "N/A"
    
    def display_cpu_info(self):
        '''Displays the CPU information'''
        print("="*40, "CPU Information", "="*40)
        print("Processor (CPU):", self.cpu_info["brand_raw"])
        cpu_codename = self.get_cpu_codename(self.cpu_info["brand_raw"])
        print(f"Processor Codename: {cpu_codename}")
        print(f"Processor Family, Model and Manufacturer: {self.uname.processor}")
        print("CPU Architecture:", self.cpu_info["arch"])
        print("CPU Base Clock:", self.cpu_info["hz_advertised_friendly"])
        print("Physical Cores:", psutil.cpu_count(logical=False))
        print("Logical Threads:", psutil.cpu_count(logical=True))
        print("CPU L2 Cache:", self.cpu_info["l2_cache_size"], "B")
        print("CPU L3 Cache:", self.cpu_info["l3_cache_size"], "B")
        print("CPU Instruction Sets:", self.cpu_info["flags"])
        time.sleep(5)
    
    def display_gpu_info_full(self):
        '''Displays the full GPU information'''
        print("="*40, "GPU Information", "="*40)
        list_gpus = []
        for gpu in self.gpus:
            list_gpus = []
            for gpu in self.gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load*100}%"
                gpu_free_memory = f"{gpu.memoryFree}MB"
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory, gpu_total_memory, gpu_temperature, gpu_uuid
                ))
        print(tabulate(list_gpus, headers=("id", "GPU name", "GPU Load", "Free Memory", "Used Memory", "Total Memory", "Temperature", "UUID")))
        time.sleep(5)
    
    def display_memory_info(self):
        '''Displays the memory information'''
        print ("="*40, "System Memory (RAM) Information", "="*40)
        print(f"Total: {self.get_size(self.svmem.total)}")
        print(f"Available: {self.get_size(self.svmem.available)}")
        print(f"Used: {self.get_size(self.svmem.used)}")
        print(f"Percentage: {self.svmem.percent}%")
        time.sleep(5)

    def display_storage_info(self):
        '''Displays the storage information'''
        print("="*40, "Storage Information", "="*40)
        print("Partitions and Usage:")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            print(f"  Total Size: {self.get_size(partition_usage.total)}")
            print(f"  Used: {self.get_size(partition_usage.used)}")
            print(f"  Free: {self.get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {self.get_size(disk_io.read_bytes)}")
        print(f"Total write: {self.get_size(disk_io.write_bytes)}")
        time.sleep(5)

    def display_all_info(self):
        '''Desplays all system information and writes it to a file to the desktop'''
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        filepath = os.path.join(desktop, 'system_info.txt')
        with open(filepath, 'w') as f:
            muti_stream = MultiStream(sys.stdout, f)
            sys.stdout = muti_stream
            try:
                self.Initilize()
                self.display_system_info()
                self.display_boot_time()
                self.display_cpu_info()
                self.display_gpu_info_full()
                self.display_memory_info()
                self.display_storage_info()
            finally:
                sys.stdout = sys.__stdout__
                print("*Scanning complete**Information ready*")
                print(f"System information has been saved to {filepath}")
        input("Press ENTER to exit and terminate the program")

if __name__ == "__main__":
    '''Main function'''
    system_info = SystemInfo()
    system_info.display_all_info()
