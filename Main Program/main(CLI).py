# Adarssh Athithan A Level Financial Forecasting Program Utilising Machine Learning - Completed March 2022
# This is the file to run
# Imports Classes from the classesmysql.py file. That file contains all functions of the program. This file is just used
# to trigger the starting method in the Main class
from classesMYSQL import *

# Function that creates the Sim Object and then calls the Run methof which is the main method of the program
def MainProgram():
    Sim = Main()
    Sim.Run()

# When file is run the program starts here
if __name__ == "__main__":
    MainProgram()
