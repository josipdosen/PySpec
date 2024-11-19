import sys
import time
from PySpec_v2_0 import SystemInfo
from CPUStress import CPUStressTester

def main_menu():
    ''' Displays the main menu of the program.'''
    while True:
        print("\nPySpec Main Menu \n Choose an option:")
        print("1. Display System Information")
        print("2. Run CPU Stress Test")
        print("3. About the Program")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print ("Entering PySpec System Information")
            system_info = SystemInfo()
            system_info.display_all_info()
        elif choice == '2':
            print ("Entering Pyspec CPU Stress Test")
            tester = CPUStressTester()
            tester.cpu_stress_test()
        elif choice == '3':
            About()
        elif choice == '4':
            print ("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def About():
    ''' Displays information about the program '''
    print("\n PySpec (c) 2024 Josip Dosen \n https://github.com/josipdosen \n Version: v2.0")

if __name__ == "__main__":
    main_menu()