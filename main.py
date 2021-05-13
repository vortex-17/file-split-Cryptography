#This is the main function for the file-split cryptography

from split import split, recreate_file
import os
import pyfiglet

def main(filename):
    result = pyfiglet.figlet_format("FILE SHARDING", font = "slant"  )
    print(result)
    if filename == "":
        print("Please enter the name of the file : ")
    # if filechunks < 1:
    #     print("The number of chunks should be greater than 1")
    # print("Welcome to the file-split cryptography")
    # pwd = str(input("Create new password for the protection of the file : "))
    pwd = "sangam"
    # split(filename,pwd,1)  
    recreate_file(filename, pwd)

# filename = str(input("Enter the filename : "))
filename = "sample.txt"
main(filename)
    


