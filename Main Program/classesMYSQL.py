# Adarssh Athithan A Level Financial Forecasting Program Utilising Machine Learning - Completed March 2022

# Import all the Libraries required for the Program
try:
    import datetime  # This import allows Python to interact with dates properly
    import os  # This import allows Python To check if paths files are correct and interact with os
    import random  # This import allows Python to generate random numbers
    import sys  # This import allows for Python to interact and execute system functions
    import time  # This import allows Program to Delay outputs purely for aesthetic reason
    import matplotlib.pyplot as plt  # This import allows the program to plot the graphs
    import mysql.connector  # This import allows the program to communicate with MySQL Databases
    import numpy as np  # This import allows the program to complete Mathematical functions needed for ML
    import pandas as pd  # This import allows the program to store data in dataframes which is needed for ML
    from pandas import DataFrame  # This import allows storing data in dataframes which is needed for ML
    from pandas import to_datetime  # This import allows the program to recognise data type input in SQL Databases
    import pymysql  # This import allows the program to connect the SQL Database
    from matplotlib import pyplot  # This import allows the program to plot the graphs
    import plotly.io as pio  # This import allows the program to plot the graphs
    from plotly.subplots import make_subplots  # This import allows the program to plot the graphs
    import plotly.graph_objects as go  # This import allows the program to plot the graphs
    import plotly.express as px  # This import allows the program to plot the graphs
    from prophet import Prophet  # This is a Facebook Machine Learning Library
    from sklearn.metrics import mean_absolute_error  # This is a SKlearn Machine Learning Library required by Prophet
    from sklearn.preprocessing import MinMaxScaler  # This is a Sklearn Machine Learning Library
    from sqlalchemy import create_engine  # This allows the program to communicate with SQL databases
    from sqlalchemy.types import Integer, Float, String  # This allows the process different SQL Datatypes
    import openpyxl
    import xlrd
    pymysql.install_as_MySQLdb()  # This import allows the program to connect the SQL Database
except ImportError:
    # This informs the User that they don't have the correct libraries to install the program and Hence the Program
    # Will Close.
    print()
    print("You Don't Have Correct Libraries Installed and therefore won't be able to execute Program")
    time.sleep(1)
    print("Please Consult Developer Support in order to fix this issue")
    time.sleep(5)
    print()
    time.sleep(5)
    sys.exit("The Program will now exit")

# Sets Parameters to allow More Values to be displayed by Dataframe
pd.set_option('display.max_rows', 500)  # This allows for Max Number of Dataframes to be expanded
pd.set_option('display.max_columns', 500)  # This allows for Max Number of Dataframes to be expanded
pd.set_option('display.width', 1000)  # This allows for Max Number of Dataframes to be expanded


# class that holds all DB details as well as holding the core functionality of the program
class Main:
    # Main Class that handles Menu system and stores DB credentials
    def __init__(self):
        self.hostname = None
        self.username = None
        self.password = None
        self.dbname = None
        self.port = None
        self.Spreadsheet = ""
        self.HistoricalData = ""
        self.Department = ""
        self.Campus = ""
        self.Year = ""
        self.OriginalAmountofYears = 0
        self.pay = ["Income", "EstablishmentPay", "VariablePay", "AgencyPay", "OtherPay", "TotalPay", "NonPay",
                    "SurplusDeficit"]
        self.RedbridgeOptions = "Please Enter the Department you want to Forecast for [1 - Math , 2 - English , 3 - Science, 4 - Media]: "
        self.EppingOptions = "Please Enter the Department you want to Forecast for [5 - Construction, 6 - Engineering, 7 - Physics, 8 - Broadcasting]: "
        self.HackneyOptions = "Please Enter the Department you want to Forecast for [9 - History, 10 - Geography, 11 - Economics , Politics - 12]: "
        self.payDict = {
            1: "Income",
            2: "EstablishmentPay",
            3: "VariablePay",
            4: "AgencyPay",
            5: "OtherPay",
            6: "TotalPay",
            7: "NonPay",
            8: "SurplusDeficit",
            9: "NoOfStudents"
        }
        self.CampusDict = {
            "Redbridge": self.RedbridgeOptions,
            "Epping": self.EppingOptions,
            "Hackney": self.HackneyOptions
        }

    # Methods to check values in the specified Dictionary
    def CheckPayDict(self, index):
        return self.payDict[index]

    def CheckCampusDict(self, Campus):
        return self.CampusDict[Campus]

    # Setters and Getters method
    def Sethostname(self, hostname):
        self.hostname = hostname

    def Setusername(self, username):
        self.username = username

    def Setpassword(self, password):
        self.password = password

    def Setdbname(self, dbname):
        self.dbname = dbname

    def Setport(self, port):
        self.port = port

    def Getport(self):
        return self.port

    def Gethostname(self):
        return self.hostname

    def Getusername(self):
        return self.username

    def Getpassword(self):
        return self.password

    def Getdbname(self):
        return self.dbname

    def GetSpreadsheeet(self):
        return self.Spreadsheet

    def GetHistoricalData(self):
        return self.HistoricalData

    def GetDepartment(self):
        return self.Department

    def GetYear(self):
        return self.Year

    def GetCampus(self):
        return self.Campus

    def SetSpreadsheet(self, Spreadsheet):
        self.Spreadsheet = Spreadsheet

    def SetHistoricalData(self, HistoricalData):
        self.HistoricalData = HistoricalData

    def SetDepartment(self, Department):
        self.Department = Department

    def SetYear(self, Year):
        self.Year = Year

    def SetCampus(self, Campus):
        self.Campus = Campus

    def SetOriginalYear(self, years):
        self.OriginalAmountofYears = years

    def GetOriginalYear(self):
        return self.OriginalAmountofYears

    # Method that Checks whether program has secure connection with SQL Database
    @staticmethod
    def Startup(data):
        if data.InitialiseSQL():
            print()
            time.sleep(1)
            print("Database Initialised")
            data.CreateEngine()
            if data.InitialiseEngine():
                print()
                time.sleep(1)
                print("Database Engine Created")
                return True
            else:
                print()
                time.sleep(1)
                print("Database Engine Failure")
                return False
        else:
            print()
            time.sleep(1)
            print("Database Config Error")
            return False

    # Method that Checks whether Config File exists meaning it checks whether Program has been run before
    @staticmethod
    def FirstTimeCheckFile():
        if os.path.exists("configtempcheck.txt"):
            return False
        else:
            return True

    # Method that deals with displaying to end user the errors in terms of MySQL and explanation how to fix
    @staticmethod
    def StartupError(status):
        print()
        if status == 1:
            time.sleep(1)
            print("MYSQL is essential to this program. Please Install and Setup MySQL from the website "
                  "(https://www.mysql.com/downloads/)")
        if status == 2:
            time.sleep(1)
            print("Credentials Incorrect for MySQL. Please Check Config File And Correct Credentials")
        if status == 3:
            time.sleep(1)
            print("Failure to Set-up Database. Please Check Config File and if Still not working contact Developer")
        time.sleep(4)
        print()
        if status == 1 or status == 2 or status == 3:
            sys.exit("The Program will now exit")

    # This Method is run when program starts and guides user through first time setup for MySQL Config and creates
    # Config Text file if it doesn't exist. If Config File exists then program extracts configuration and passes
    # credentials and path into the program. This Method also calls the SQL setup Functions from the "Initialise" Class
    def StartupCheck(self, data):
        if self.FirstTimeCheckFile():
            print()
            time.sleep(1)
            print(
                "IF YOU HAVE MYSQL INSTALLED ENTER 'YES' (HAS TO BE ALL CAPS), IF ANYTHING OTHER THAN 'YES' (HAS TO BE ALL CAPS) IS ENTERED THE PROGRAM WILL")
            print(
                "ASSUME AND DEFAULT TO THE OPTION THAT YOU DONT HAVE MYSQL AND THEREFORE CLOSE AS MYSQL IS ESSENTIAL: ")
            MySQLCheck = input()
            if MySQLCheck == 'YES':
                print()
                time.sleep(1)
                hostname = input("Please Type Hostname for MySQL Database: ")
                data.Sethostname(hostname)
                print()
                time.sleep(1)
                port = int(input("Please Type Port for MySQL Database: "))
                data.Setport(port)
                print()
                time.sleep(1)
                username = input("Please Type Username for MySQL Database: ")
                data.Setusername(username)
                print()
                time.sleep(1)
                passwd = input("Please Type Password for MySQL Database: ")
                data.Setpassword(passwd)
                dbname = 'ncc'
                data.Setdbname(dbname)
                if not self.Startup(data):
                    self.StartupError(2)
                    return
                try:
                    data.SQL_TO_Python('Setup.sql')
                    print()
                    time.sleep(1)
                    print("ncc Database Successfully Constructed")
                except EnvironmentError:
                    self.StartupError(3)
                Path = os.path.dirname(os.path.abspath(__file__))
                Path = Path.replace('Main Program', '')
                data.Setpath(Path)
                data.Setdftpath(Path)
                with open("configtempcheck.txt", 'w') as file:
                    file.write("{}\n".format(data.Getpath()))
                    file.write("{}\n".format(data.Gethostname()))
                    file.write("{}\n".format(data.Getport()))
                    file.write("{}\n".format(data.Getusername()))
                    file.write("{}\n".format(data.Getpassword()))
                    file.write("{}\n".format(data.Getdbname()))
            else:
                self.StartupError(1)
        else:
            f = open("configtempcheck.txt")
            strippedlines = []
            lines = f.readlines()
            for element in lines:
                strippedlines.append(element.strip())
            data.Setpath(str(strippedlines[0]))
            data.Setdftpath(str(strippedlines[0]))
            data.Sethostname(str(strippedlines[1]))
            data.Setport(str(strippedlines[2]))
            data.Setusername(str(strippedlines[3]))
            data.Setpassword(str(strippedlines[4]))
            data.Setdbname(str(strippedlines[5]))
            if not self.Startup(data):
                self.StartupError(2)

    # Method that Displays the Main Menu options to the User
    @staticmethod
    def DisplayMenu():
        # Menu System for CLI
        print()
        time.sleep(1)
        print("MAIN MENU")
        time.sleep(1)
        print("1. Guide to Program")
        print("2. Import Historical Data")
        print("3. Visualise Spreadsheet")
        print("4. Forecast")
        print("5. Exit")

    # Method that Displays the ML Menu options to the User
    @staticmethod
    def DisplayMLMenu():
        # Menu System for ML Algorithm
        print()
        print("ML Algorithm Menu")
        time.sleep(1)
        print("1. Facebook Prophet Algorithm")
        print("2. Custom")

    # Method that Displays the Error Menu when user chooses to Forecast for A Campus and Department that has no
    # Historical Data in SQL Database
    @staticmethod
    def MissingDataMenu():
        print()
        print("!!! ERROR MESSAGE !!!")
        time.sleep(1)
        print("There seems to be no data for your chosen Campus and Department")
        print("You now have these options")
        time.sleep(1)
        print("1. Be Re-Directed to Main Menu")
        print("2. Import Historical Data For your Chosen Department and Try Forecasting Again")

    # Method that Gets the Main Menu Choice from the end user
    @staticmethod
    # Validation Checking Method
    def GetMainMenuChoice():
        # Gets Main Menu System Choice for CLI
        print()
        while True:
            time.sleep(1)
            print("Please enter your choice: ", end="")
            Choice = input()
            if Choice.isdigit() is False:
                time.sleep(1)
                print("Incorrect Value, Please try again with a value between 1 - 5 ")
            else:
                Choice = int(Choice)
                if 1 <= Choice < 6:
                    return Choice
                else:
                    time.sleep(1)
                    print("Incorrect Value, Please try again with a value between 1 - 5 ")

    # Method that Gets the ML Menu Choice from the end user
    @staticmethod
    # Validation Checking Method
    def GetMLChoice():
        # Gets Choice for ML and has Validation in order to ensure that the User is unable to type an Incorrect
        # Input and ensure that program runs smoothly
        print()
        counter = 0
        while True:
            print("Please enter which ML Algorithm You want to use: ", end="")
            Choice = input()
            if Choice.isdigit() is False:
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")
            else:
                Choice = int(Choice)
                if 1 <= Choice < 3:
                    return Choice
                else:
                    counter = counter + 1
                    if counter == 4:
                        time.sleep(1)
                        print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                        return False
                    else:
                        time.sleep(1)
                        print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")

    # Method that Gets the Error Menu Choice from the end user
    @staticmethod
    # Validation Checking Method
    def GetMissingDataChoice():
        # Gets Choice for Error Menu and has Validation in order to ensure that the User is unable to type an Incorrect
        # Input and ensure that program runs smoothly
        print()
        counter = 0
        while True:
            time.sleep(1)
            print("Please enter your choice: ", end="")
            Choice = input()
            if Choice.isdigit() is False:
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")
            else:
                Choice = int(Choice)
                if 1 <= Choice < 3:
                    return Choice
                else:
                    counter = counter + 1
                    if counter == 4:
                        time.sleep(1)
                        print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                        return False
                    else:
                        time.sleep(1)
                        print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")

    # Method that Gets the Campus Menu Choice from the end user
    @staticmethod
    # Validation Checking Method
    def GetCampusChoice():
        # Gets Choice for Campus and has Validation in order to ensure that the User is unable to type an Incorrect
        # Input and ensure that program runs smoothly
        print()
        counter = 0
        while True:
            time.sleep(1)
            print("Please Enter the Campus you want to Forecast for [1 - Redbridge , 2 - Epping , 3 - Hackney]: ")
            inputCampus = input()
            if inputCampus.isdigit() is False:
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")
            else:
                inputCampus = int(inputCampus)
                if 1 <= inputCampus < 4:
                    if inputCampus == 1:
                        return "Redbridge"
                    if inputCampus == 2:
                        return "Epping"
                    if inputCampus == 3:
                        return "Hackney"
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")

    # Method that Gets the Department Menu Choice from the end user
    # Validation Checking Method
    def GetDepartmentChoice(self, query):
        # Gets Choice for Department and has Validation in order to ensure that the User is unable to type an Incorrect
        # Input and ensure that program runs smoothly
        print()
        counter = 0
        while True:
            time.sleep(1)
            print(query)
            inputDepartment = input()
            if inputDepartment.isdigit() is False:
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")
            else:
                inputDepartment = int(inputDepartment)
                if query == self.RedbridgeOptions:
                    if 1 <= inputDepartment < 5:
                        if inputDepartment == 1:
                            return "Math"
                        if inputDepartment == 2:
                            return "English"
                        if inputDepartment == 3:
                            return "Science"
                        if inputDepartment == 4:
                            return "Media"
                elif query == self.EppingOptions:
                    if 5 <= inputDepartment < 9:
                        if inputDepartment == 5:
                            return "Construction"
                        if inputDepartment == 6:
                            return "Engineering"
                        if inputDepartment == 7:
                            return "Physics"
                        if inputDepartment == 8:
                            return "Broadcasting"
                elif query == self.HackneyOptions:
                    if 9 <= inputDepartment < 13:
                        if inputDepartment == 9:
                            return "History"
                        if inputDepartment == 10:
                            return "Geography"
                        if inputDepartment == 11:
                            return "Economics"
                        if inputDepartment == 12:
                            return "Politics"
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")

    # Method that Gets the Year Choice from the end user
    @staticmethod
    # Validation Checking Function
    def GetYearChoice():
        # Gets Choice for Year and has Validation in order to ensure that the User is unable to type an Incorrect
        # Input and ensure that program runs smoothly
        print()
        counter = 0
        while True:
            time.sleep(1)
            print("Please Enter How many Years [ Maximum Value is 20 ] you want to forecast for: ")
            inputYear = input()
            if inputYear.isdigit() is False:
                counter = counter + 1
                if counter == 4:
                    time.sleep(1)
                    print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                    return False
                else:
                    time.sleep(1)
                    print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")
            else:
                inputYear = int(inputYear)
                if 1 <= inputYear <= 20:
                    return inputYear
                else:
                    counter = counter + 1
                    if counter == 4:
                        time.sleep(1)
                        print("You have reached Max Amount of Tries and will now be re-directed to Main Menu")
                        return False
                    else:
                        time.sleep(1)
                        print(f"Incorrect Value You have {4 - counter} attempts left, Please try again")

    # Method that outputs Simple Guide on how to use Program and Lists out Campuses and Departments that are
    # available to be forecasted
    @staticmethod
    def Option1():
        print()
        time.sleep(1)
        print("Welcome to the Financial Forecasting Program :)")
        time.sleep(1)
        print()
        time.sleep(1)
        print("This program allows you to input Historical Data from Excel Sheets into the SQL Database")
        time.sleep(1)
        print("The program also allows you to input an Excel Spreadsheet and Be able to Visualise the data")
        time.sleep(1)
        print("The program also allows you to Forecast Data for your Chosen Department and College")
        time.sleep(1)
        print()
        time.sleep(1)
        print("Please Remember that Department Codes are unique to each College")
        time.sleep(1)
        print("Here is a List of the College - Department - Department Code if you don't remember")
        time.sleep(1)
        print()
        time.sleep(1)
        print("Redbridge - Maths - 1")
        time.sleep(1)
        print("Redbridge - English - 2")
        time.sleep(1)
        print("Redbridge - Science - 3")
        time.sleep(1)
        print("Redbridge - Media - 4")
        time.sleep(1)
        print("Epping - Construction - 5")
        time.sleep(1)
        print("Epping - Engineering - 6")
        time.sleep(1)
        print("Epping - Physics - 7")
        time.sleep(1)
        print("Epping - Broadcasting - 8")
        time.sleep(1)
        print("Hackney - History - 9")
        time.sleep(1)
        print("Hackney - Geography - 10")
        time.sleep(1)
        print("Hackney - Economics - 11")
        time.sleep(1)
        print("Hackney - Politics - 12")
        time.sleep(1)
        print("Please Have all Historical Excel Data Sheets stored in the folder 'Data' in Program Files")
        time.sleep(1)
        print("The Forecast Produced Files will be stored in the 'Forecasted File Directory' in Program Files")
        time.sleep(1)
        print()
        time.sleep(1)
        print("If you would like the program to process a New Department or a New College Please Contact the Developer")
        time.sleep(1)

    # Method that allows user to input historical Excel spreadsheet data to the SQL Database
    @staticmethod
    def Option2(data):
        data.ImportExceltoSQL()

    # Method that allows user to visualise spreadsheet data
    def Option3(self, data):
        query = "Please enter the filename of the Spreadsheet you would like to be used to visualise values? "
        self.SetSpreadsheet(data.GetFilenameChoice(query, True))
        time.sleep(1)
        print("Data Accepted")
        data.PlotGraph(self.GetSpreadsheeet())

    # This Method calls the Facebook Prophet Module. This module is a Machine Learning Algorithm that uses Time Series
    # Forecasting.It calls the EvaluateFBProphet Method which shows the performance of the algorithm on the specific
    # Dataset and outputs the MAE. Then the OutofSampleFBProphet method then conducts the forecast for the specific
    # time period
    def MLChoice1(self, data, Tdata):
        amountofyearsforecastedfor = self.GetYear()
        # raw_data is dataframe
        raw_data = Tdata.iloc[:, 2:11]
        time.sleep(1)
        time.sleep(1)
        # This Method Evaluates the model and provides MAE Number. This Number will be able to tell Dev How accurate the
        # model is at forecasting when using the testing dataset
        # This will be commented out in order to hide this details from End-User to prevent Confusion (Abstraction)
        # data.EvaluateFBProphetModel(raw_data, self.CheckPayDict(1), amountofyearsforecastedfor) # This is used to test the Model
        print()
        print()
        # This Method Actually uses the model that is Evaluated and is able to produce the Forecast and Excel File
        data.OutOfSampleFBProphetForecast(raw_data, self.CheckPayDict(1), True, amountofyearsforecastedfor)
        for x in range(2, 9):
            time.sleep(1)
            # This Method Evaluates the model and provides MAE Number. This Number will be able to tell Dev How accurate the
            # model is at forecasting when using the testing dataset
            # This will be commented out in order to hide this details from End-User to prevent Confusion (Abstraction)
            # data.EvaluateFBProphetModel(raw_data, self.CheckPayDict(x), amountofyearsforecastedfor) # This is used to test the Model
            print()
            print()
            data.OutOfSampleFBProphetForecast(raw_data, self.CheckPayDict(x), False, amountofyearsforecastedfor)

    # This Method is the 'Custom Algorithm'. It uses Mathematical functions, mainly Percentage Change and Moving Averages
    # In order to produce a forecast. The Method first of all checks if the historical data in the database for the
    # Chosen Department and College is minimum three years otherwise the forecast won't be conducted and user will be
    # Returned to the Main Menu. If there is three years or more historical data then the program is able to proceed
    # and will Create a new Object for each type of Pay and Call the CUstomML method from the Process class (that's
    # all the processing is). Then it will add the newly forecasted data to the dataframe ready for it to be used in the
    # Next years Forecast. This is all in a while loop until the value year has reached 0. Then the Final Dataframe
    # is printed to the user, the Dataframe is plotted on a Graph and then the ExporttoExcel method from the Output
    # Class is called in order to deal with the user Saving the File.
    def MLChoice2(self, data, Tdata):
        year = self.GetYear()
        amountofyearsforecastedfor = self.GetYear()
        originalyear = self.GetOriginalYear()
        raw_data = Tdata
        year1 = raw_data['Year'].iloc[0]
        lastrow = raw_data.shape[0] - 1
        year2 = raw_data['Year'].iloc[lastrow]
        times = (year2 - year1)
        if times < 2:
            print()
            time.sleep(1)
            print(
                f"More Data is required to produce a Forecast, minimum of 3 years worth of data needed you currently have {times + 1}")
            time.sleep(1)
            print("You will be redirected to the Main Menu...")
            return
        while year != 0:
            Department = Process()
            for x in range(1, 9):
                time.sleep(1)
                Department.CustomML(raw_data, self.CheckPayDict(x), data.GetDepartment())
            Department.CustomMLFinalOutput()
            raw_data = Department.AddForecastValuestoDF(raw_data)
            year = year - 1
        raw_data['Date'] = pd.to_datetime(raw_data['Date']).dt.normalize()
        print()
        time.sleep(1)
        print(raw_data)
        datarange = Department.times + 1
        Department.SetYear(amountofyearsforecastedfor)
        Department.SetOriginalYear(originalyear)
        Department.PlotDataframe(raw_data)
        Department.ExporttoExcel(raw_data, datarange, data)

    # Method that allows the user to trigger the Forecasting part of the program. It gets the Campus,Department and
    # Year choices by calling the respective Validation Checking function (Get-----Choice). Dictionaries are utilised
    # here to match the user entered Campus and returns the options for the Campus since there are specific departments
    # available to certain campuses (e.g:if Redbridge then the Politics Department can't be shown).Then the Dataframe
    # will be checked to see if it's empty meaning there is no historical_data for the chosen campus and department.This
    # now redirects them and ask whether they have Historical Data to input into the Program, if they reply No then it
    # will be explained to them that they are required to populate the historical data table with historical data from
    # their Excel Sheets otherwise they will not be able to Forecast and then are Redirected to the Main Menu.If the
    # Dataframe isn't empty then its checked whether it has at least 3 years worth of historical data in the database as
    # that is minimum amount of data required in order to run the program. If they dont have at least three years then
    # they are told how many years they do have and then are re-directed to the main menu. If they have three years then
    # The User is able to pick a Choice of ML Algorithm and The Validation Checking Function is once again called to
    # ensure No incorrect inputs are passed and that the user wont be able to break the program.Once the Algorithm is
    # Chosen the specific Method for that Algorithm is called
    def Option4(self, data):
        campus = self.GetCampusChoice()
        if not campus:
            return
        data.SetCampus(campus)
        campus = self.CheckCampusDict(data.GetCampus())
        department = self.GetDepartmentChoice(campus)
        if not department:
            return
        data.SetDepartment(department)
        year = self.GetYearChoice()
        if not year:
            return
        data.SetYear(int(year))
        self.SetYear(int(year))
        dataframe_check = data.CollectTestData()
        if not dataframe_check:
            self.MissingDataMenu()
            MissingDataChoice = self.GetMissingDataChoice()
            if MissingDataChoice == 1 or not MissingDataChoice:
                data.SetCampus("")
                data.SetDepartment("")
                data.SetYear(0)
                return
            if MissingDataChoice == 2:
                time.sleep(1)
                check = input("Do you have Historical Data in the form of Excel Sheets to input into the Program Y/N "
                              "(Default is N): ")
                if check == "y" or check == "Y":
                    time.sleep(1)
                    print("You will now be redirected to Importing Historical Data...")
                    time.sleep(1)
                    self.Option2(data)
                else:
                    time.sleep(1)
                    print("Sorry, You need Data in the Database for this Campus and Department or have Excel Sheets "
                          "with Historical Data for this Campus and Department in order to use this Program")
                    time.sleep(1)
                    print("You will now be redirected to the Main Menu...")
                    data.SetCampus("")
                    data.SetDepartment("")
                    data.SetYear(0)
                    return
        else:
            Tdata = data.LoadData()
            lastrow = Tdata.shape[0] - 1
            y2 = Tdata['Year'].iloc[lastrow]
            self.SetOriginalYear(y2)
            year1 = Tdata['Year'].iloc[0]
            lastrow = Tdata.shape[0] - 1
            year2 = Tdata['Year'].iloc[lastrow]
            checktimes = (year2 - year1)
            if checktimes < 2:
                print()
                time.sleep(1)
                print(
                    f"More Data is required to produce a Forecast, minimum of 3 years worth of data needed you currently have {checktimes + 1}")
                time.sleep(1)
                print("You will be redirected to the Main Menu...")
                time.sleep(1)
                print()
                return
            self.DisplayMLMenu()
            MLChoice = self.GetMLChoice()
            if MLChoice == 1:
                self.MLChoice1(data, Tdata)
            if MLChoice == 2:
                self.MLChoice2(data, Tdata)
            if not MLChoice:
                return

    # Method that allows the user to exit the program
    @staticmethod
    def Option6():
        print("Goodbye")
        sys.exit()

    # This Method is the core of the program and is triggered when the program starts. This Method calls the Methods for
    # the different functionalities of the program depending on the user choice. This user Choice is picked up by the
    # GetMainMenuChoice method which also has Validation to ensure Program isn't broken. If Option6 is called then
    # the program will call the method that quits
    def Run(self):
        print()
        print("-----WELCOME TO THE FINANCIAL FORECASTING PROGRAM-----")
        MenuOption = 0
        data = Process()
        self.StartupCheck(data)
        while not MenuOption == 5:
            self.DisplayMenu()
            MenuOption = self.GetMainMenuChoice()
            if MenuOption == 1:
                self.Option1()
            if MenuOption == 2:
                self.Option2(data)
            if MenuOption == 3:
                self.Option3(data)
            if MenuOption == 4:
                self.Option4(data)
        if MenuOption == 5:
            self.Option6()


# This class deals with preparing the file to be saved and have anything else applied to it
# This class Inherits from the Main Class
class Output(Main):
    NewSavePath: str

    def __init__(self):
        super().__init__()
        self.OutputFilename = ""
        self.NewSavePath = ""
        self.outFoldername = ""
        self.trange = 0

    # Getters and Setters Methods
    def GetoutFoldername(self):
        return self.outFoldername

    def GetNewSavePath(self):
        return self.NewSavePath

    def GetOutputFilename(self):
        return self.OutputFilename

    def Gettrange(self):
        return self.trange

    def SetOutputFilename(self, OutputFilename):
        self.OutputFilename = OutputFilename

    def SetNewSavePath(self, SavePath):
        self.NewSavePath = SavePath

    def SetoutFolderName(self, outfoldername):
        self.outFoldername = outfoldername

    def Settrange(self, trange):
        self.trange = trange

    # This Method is called By the ExporttoExcel Method and Asks the User whether they want the Excel File to have all
    # data from the dataframe or whether they should just store the targeted year data to the excel sheet. Depending on
    # the option the whole dataframe is exported or the dataframe called dfcopy which is the same as the original
    # dataframe only consist of values from the targeted year. A message is then written to the user in order to signify
    # that the saving to the Excel File was Successful
    def Export(self, dfCopy, dataframe):
        time.sleep(1)
        targetyear = int(self.GetOriginalYear()) + int(self.GetYear())
        Choice = input(
            f"Would you like just data from just the targeted forecasted year ({targetyear}) or data from every year enter Y "
            "(Default is Every Year): ")
        if Choice == "Y":
            with pd.ExcelWriter(self.GetNewSavePath(), mode="w", engine="openpyxl") as writer:
                dfCopy.to_excel(writer, index=False)
            time.sleep(1)
            print("Successfully Exported To Excel")
        else:
            with pd.ExcelWriter(self.GetNewSavePath(), mode="w", engine="openpyxl") as writer:
                dataframe.to_excel(writer, index=False)
            time.sleep(1)
            print("Successfully Exported To Excel")

    # This Method is called by the MLOption2 and first sets the NewSavePath to the ForecastedFileDirectory which
    # is where the Forecasted Excel Files will be stored. Then there is another dataframe created that only consist data
    # for the targeted year (this is called dfcopy).Then the user is asked to enter the filename you want the exported
    # file to have
    def ExporttoExcel(self, dataframe, trange, data):
        self.SetNewSavePath(data.Getdftpath() + "ForecastedFileDirectory")
        x = 0
        dfCopy = dataframe.copy()
        self.Settrange(trange * 12)
        dfCopy = dfCopy.drop(dfCopy.index[x:self.Gettrange()])
        print()
        if os.path.isdir(self.NewSavePath) is True:
            time.sleep(1)
            self.SetOutputFilename(input("Please Enter the Filename you want this exported Excel file to have: "))
            self.SetNewSavePath(self.NewSavePath + "/" + self.GetOutputFilename() + ".xlsx")
            self.Export(dfCopy, dataframe)
        else:
            time.sleep(1)
            self.SetOutputFilename(input("Please Enter the Filename you want the exported file to have: "))
            self.Export(dfCopy, dataframe)


# This class inherits from Output
class Initialise(Output):
    # This Class checks for the Connection to the SQL server and will not allow the program to run if server is
    # unavailable as well as putting the credentials in to allow the SQL DB to be written to
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.mydb = None
        self.engine = None

    # Checks Credentials provided by user or in config file to see if connection can be established
    def InitialiseSQL(self):
        try:
            self.mydb = mysql.connector.connect(host=self.Gethostname(), port=self.Getport(),
                                                user=self.Getusername(),
                                                password=self.Getpassword(), database=self.Getdbname(), autocommit=True)
            if self.mydb.is_connected():
                self.cursor = self.mydb.cursor()
                return True
        except:
            try:
                self.mydb = mysql.connector.connect(host=self.Gethostname(), port=self.Getport(),
                                                    user=self.Getusername(),
                                                    password=self.Getpassword(), autocommit=True)
                if self.mydb.is_connected():
                    self.cursor = self.mydb.cursor()
                    self.cursor.execute("CREATE DATABASE ncc")
                    self.InitialiseSQL()
                    return True
            except:
                return False

    # Creates engine for sqlalchemy library to allow for communication between dataframe, excel files and SQL DB
    def CreateEngine(self):
        self.engine = create_engine(self.MYSQLPath())

    # Path of MYSQL DB
    def MYSQLPath(self):
        return f"mysql://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.dbname}"

    # Method Used to pass Query/commands to SQL DB using the cursor
    def Query(self, query, wanttoquery):
        self.cursor = self.mydb.cursor()
        try:
            self.cursor.execute(query)
            if wanttoquery:
                return self.cursor.fetchall()
        except EnvironmentError:
            return False

    # Method that validates whether Engine config is corrected
    def InitialiseEngine(self):
        if self.engine.connect():
            return True

    # Method that takes in SQL DDL File and splits the file dy the delimeter.Then each line is passed into Query Method
    def SQL_TO_Python(self, filename):
        file = open(filename, 'r')
        sql = file.read()
        file.close()
        sqlSCRIPT = sql.split(';')
        for c in sqlSCRIPT:
            self.Query(c, False)


# This class many handles converting Excel spreadsheet data into the SQL database as well as outputting graphs
# This class inherits from Initialise
class Input(Initialise):
    # Class handles all the major Inputs from the User
    def __init__(self):
        super().__init__()
        self.filename = ""
        self.path = ""
        self.dftpath = ""

    # Getters and Setters Method
    def Setdftpath(self, dftpath):
        self.dftpath = dftpath

    def Getdftpath(self):
        return self.dftpath

    def Setpath(self, path):
        self.path = path

    def Getpath(self):
        return self.path

    def Setfilename(self, filename):
        self.filename = filename

    def Getfilename(self):
        return self.filename

    # Method That Gets File Name Choice. This is called in different cases such as visualising spreadsheets whcih would
    # set pathbool to true as it requires the path whereas getting filename for the historicalData is not needing a path
    # hence pathbool in that instance is false
    def GetFilenameChoice(self, query, pathbool):
        while True:
            print()
            time.sleep(1)
            print(query)
            self.Setfilename(input())
            self.Setpath(self.Getdftpath() + 'Data/' + self.Getfilename() + '.xls')
            if os.path.isfile(self.Getpath()) is True:
                if pathbool:
                    return self.Getpath()
                else:
                    return self.Getfilename()
            else:
                print()
                time.sleep(1)
                print('No such file.  Check file name and PATH and try again.')
                self.Setpath(self.Getdftpath())

    # First GetFilenameChoice called to ask User to enter Filename of the Excel File they want to enter and checks
    # whether file exists inside the Data folder and if passed all Validation then returns Filename. The Method
    # Takes Data from Excel File and Converts into dataframe format allowing for it to be imported into SQL through
    # SQLAlchemy Library. Before Excel File is pushed to SQL Database a couple of checks are conducted first. Firstly it
    # check whether the file is empty and if it is it explains to end user the problem and calls the method again
    # showing that this is a recursive algorithm.Then the Method checks Whether this file has already been inputted
    # before by passing a SQL statement in to check whether the for that specific Campus,Department and Year already has
    # data in the databases. If this return True then the end user is told what the problem is and is redirected to the
    # Main Menu.Once bypassing all Validation Checks then the Excel File is formatted as a SQL Query and then is
    # submitted to the SQL Database.Try and Except will catch any EnvironmentErrors and will be re-directed to Main Menu
    def ImportExceltoSQL(self):
        query = "Please enter the filename of the Historical Data (Spreadsheet) you would like to Input into " \
                "the SQL Database: "
        self.Setpath(self.Getdftpath())
        inputdata = self.GetFilenameChoice(query, False)
        self.SetHistoricalData(inputdata)
        PATH = self.Getpath()
        df = pd.read_excel(PATH)
        if df.empty:
            time.sleep(1)
            print("You Have Provided an Empty Excel File. Please Try Again....")
            self.ImportExceltoSQL()  # Recursion
            return
        Year = df['Year'].iloc[1]
        DIndex = df['DepartmentCode'].iloc[1]
        CIndex = df['CampusCode'].iloc[1]
        Query = (" SELECT * FROM historical_data WHERE DepartmentCode = (%s) AND CampusCode = (%s) AND Year = (%s) " % (
            DIndex, CIndex, Year))
        querycheck = self.Query(Query, True)
        if querycheck:
            print()
            time.sleep(1)
            print("Data Insertion Unsuccessful - Duplicate Records Detected")
            time.sleep(1)
            print("You will be redirected to the Main Menu...")
            return
        try:
            df.to_sql('historical_data', con=self.engine, if_exists='append', index=False,
                      dtype={'CampusCode': Integer, 'DepartmentCode': Integer, 'Year': Integer, 'Months': String,
                             'Date': String,
                             'Income': Float, 'EstablishmentPay': Float, 'VariablePay': Float, 'AgencyPay': Float,
                             'OtherPay': Float, 'TotalPay': Float, 'SurplusDeficit': Float, 'NoOfStudents': Integer})
            print()
            time.sleep(1)
            print("Data Insertion Successful")
        except EnvironmentError:
            print()
            time.sleep(1)
            print("Data Insertion Unsuccessful - Environment Error")
            time.sleep(1)
            print("You will be redirected to the Main Menu...")

    # Plots Data from Excel File onto the Graph using matplotlib library
    def PlotGraph(self, PATH):
        sheet = pd.read_excel(PATH)
        plt.figure(figsize=(15, 15))
        x1 = list(sheet['Months'])
        y1 = list(sheet['Income'])
        plt.plot(x1, y1, label="Income")
        y2 = list(sheet['EstablishmentPay'])
        plt.plot(x1, y2, label="EstablishmentPay")
        y3 = list(sheet['VariablePay'])
        plt.plot(x1, y3, label="VariablePay")
        y4 = list(sheet['AgencyPay'])
        plt.plot(x1, y4, label="AgencyPay")
        y5 = list(sheet['OtherPay'])
        plt.plot(x1, y5, label="OtherPay")
        y6 = list(sheet['TotalPay'])
        plt.plot(x1, y6, label="TotalPay")
        y7 = list(sheet['NonPay'])
        plt.plot(x1, y7, label="NonPay")
        y8 = list(sheet['SurplusDeficit'])
        plt.plot(x1, y8, label="Surplus/Deficit")
        plt.xlabel('Months')
        plt.ylabel('Value')
        title = self.Getfilename()
        plt.title(title)
        plt.legend()
        time.sleep(1)
        plt.show()

    # Plots Dataframe and uses Different lines for actual and forecasted values. The Library plotly also nicely displays
    # separate graphs on one web page allowing for clear correlation and trends to be seen
    def PlotDataframe(self, dataframe):
        pd.options.plotting.backend = "plotly"
        # # data
        # df_wide = dataframe
        # df_long = pd.melt(df_wide, id_vars=['Date'],
        #                   value_vars=['Income', 'EstablishmentPay', 'VariablePay', 'AgencyPay', 'OtherPay', 'TotalPay', 'NonPay', 'SurplusDeficit', 'NoOfStudents'])
        # # plotly
        # fig = px.line(df_long, x='Date', y='value', color='variable')
        # # Show plot
        # fig.show()

        # Set Dataframe Index to the date Column
        df = dataframe.set_index('Date')

        # split data
        df_predict = df.loc[str(self.GetOriginalYear()) + '-12-01':]
        df_actual = df[~df.isin(df_predict)].dropna()

        # plotly setup
        fig = make_subplots(rows=9,
                            cols=1,
                            subplot_titles=(
                                'Income', 'EstablishmentPay', 'VariablePay', 'AgencyPay', 'OtherPay', 'TotalPay',
                                'NonPay',
                                'SurplusDeficit', 'NoOfStudents'))

        for x in range(1, 10):
            fig.add_trace(go.Scatter(x=df_actual.index, y=df_actual[self.CheckPayDict(x)],
                                     name=self.CheckPayDict(x),
                                     mode='lines',
                                     line=dict(color='steelblue', width=2)), row=x, col=1)

            fig.add_trace(go.Scatter(x=df_predict.index, y=df_predict[self.CheckPayDict(x)],
                                     name=self.CheckPayDict(x) + ' Forecasted',
                                     mode='lines',
                                     line=dict(color='firebrick', width=2, dash='dash')), row=x, col=1)
        fig.update_layout(height=6000, width=1400)
        fig.show()


# This class inherits from Input
class Process(Input):
    # This Class contains all the Key Processing of the Program - Stack,Queue,ML Algorithms,Dictionaries,Lists,
    # Mathematical Algorithms
    def __init__(self):
        super().__init__()
        self.times = 0
        self.Top = 0
        self.Front = 0
        self.Rear = 0
        self.FinalQFront = 0
        self.FinalQRear = 0
        self.QueueMath = []
        self.QueueEnglish = []
        self.QueueScience = []
        self.QueueMedia = []
        self.QueueConstruction = []
        self.QueueEngineering = []
        self.QueueNestedPC = []
        self.QueuePhysics = []
        self.QueueBroadcasting = []
        self.QueueHistory = []
        self.QueueGeography = []
        self.QueueEconomics = []
        self.QueuePolitics = []
        self.FinalQueueIncome = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueEstablishmentPay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueAgencyPay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueOtherPay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueVariablePay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueTotalPay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueNonPay = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.FinalQueueSurplusDeficit = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.NewYearColumnQueue = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.MonthsQueue = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                            "October", "November", "December"]
        self.DateQueue = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.NoOfStudentsQueue = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.MAStack = ["", "", "", "", "", "", "", "", "", "", ""]
        self.HashDataStore = ["", "", "", "", "", "", "", "", "", "", "", ""]
        self.Key = ""
        self.Index = 0
        self.DPDict = {
            "Math": 1,
            "English": 2,
            "Science": 3,
            "Media": 4,
            "Construction": 5,
            "Engineering": 6,
            "Physics": 7,
            "Broadcasting": 8,
            "History": 9,
            "Geography": 10,
            "Economics": 11,
            "Politics": 12
        }
        self.CPDict = {
            "Redbridge": 1,
            "Epping": 2,
            "Hackney": 3
        }
        self.dataframe = 0
        self.DepartmentDict = {
            "Math": self.QueueMath,
            "English": self.QueueEnglish,
            "Science": self.QueueScience,
            "Media": self.QueueMedia,
            "Construction": self.QueueConstruction,
            "Engineering": self.QueueEngineering,
            "Physics": self.QueuePhysics,
            "Broadcasting": self.QueueBroadcasting,
            "History": self.QueueHistory,
            "Geography": self.QueueGeography,
            "Economics": self.QueueEconomics,
            "Politics": self.QueuePolitics
        }
        self.ValueDict = {
            "Income": self.FinalQueueIncome,
            "EstablishmentPay": self.FinalQueueEstablishmentPay,
            "AgencyPay": self.FinalQueueAgencyPay,
            "OtherPay": self.FinalQueueOtherPay,
            "TotalPay": self.FinalQueueTotalPay,
            "NonPay": self.FinalQueueNonPay,
            "SurplusDeficit": self.FinalQueueSurplusDeficit,
            "VariablePay": self.FinalQueueVariablePay
        }

    # Methods to check values in the specified Dictionary
    def CheckDepartment(self, Department):
        return self.DepartmentDict[Department]

    def CheckValue(self, value):
        return self.ValueDict[value]

    def CheckDPDict(self, DPDict):
        return self.DPDict[DPDict]

    def CheckCPDict(self, CPDict):
        return self.CPDict[CPDict]

    # Getters and Setters Methods
    def Settimes(self, times):
        self.times = times

    def Gettimes(self):
        return self.times

    # Method that determines the starting value for January for that Forecasted Year. Takes in values for every
    # Historical year and Pushes onto a temp array. Then the array values will be added toa variable called
    # FinalInitialValue
    @staticmethod
    def DetermineStartingValue(subjqueue, times):
        temp = []
        c = 0
        FinalInitialValue = 0
        for x in range(times):
            temp.append(subjqueue[x][0])
            FinalInitialValue = FinalInitialValue + temp[c]
            c = c + 1
        FinalInitialValue = FinalInitialValue / times
        return FinalInitialValue

    # Start of Queue Methods
    @staticmethod
    # This Method creates the Multi-Dimensional Array. The amount of elements in the array is created dependant on the
    # amount of data available in the dataframe
    def CreateQueue(subjqueue, times):
        for x in range(times):
            innerqueue = []
            for y in range(12):
                innerqueue.append("")
            subjqueue.append(innerqueue)

    # This Method works by creating a Queue that size is depndant on the amount of years that the dataframe has
    # data for. This Queue is used to get all the January Values next to each other then all the February Values etc.
    # This is done to make it easy for the Percentage Change algorithm to easily calculate the Percentage Change for the
    # values
    def CreateDifferencesQueue(self, times):
        for x in range((times * 11)):
            self.QueueNestedPC.append("")

    # This Method Populates the queue with values from the dataframe and iterates until thje value time = 0
    def PopulateQueue(self, subjqueue, raw_data, value, times):
        a = 12
        b = 24
        i = 0
        for y in range(13):
            y1 = int(raw_data[value].iloc[y])
            self.AddQueue(subjqueue, y1, 0)
        times = times - 1
        i = i + 1
        while times != 0:
            for y in range(a, b):
                y1 = int(raw_data[value].iloc[y])
                self.AddQueue(subjqueue, y1, i)
            times = times - 1
            a = a + 12
            b = b + 12
            i = i + 1
        print(subjqueue)

    # This Method adds to the specified Queue using the Rear Pointer
    def AddQueue(self, subjqueue, uinput, index):
        if self.Rear == 12:
            self.Rear = 0
            if subjqueue[int(index)][int(self.Rear)] == "":
                subjqueue[int(index)][int(self.Rear)] = int(uinput)
                self.Rear = self.Rear + 1
        else:
            subjqueue[int(index)][int(self.Rear)] = int(uinput)
            self.Rear = self.Rear + 1

    # This Method removes from the specified Queue using the Front Pointer
    def RemoveQueue(self, subjqueue, index):
        if self.Front == 12:
            self.Front = 0
        elif subjqueue[0] == "" and self.Front == self.Rear:
            print("Empty Queue")
        else:
            subjqueue[index, self.Front] = ""
            self.Front = self.Front + 1

    # This Method Populates the Differences Queue. It calculates the Percentage Change for the values between the values
    # for the specific month and stores in a separate array using the Front pointer
    def DifferencesQueue(self, subjqueue, times):
        DQFront = 0
        for y in range(11):
            for x in range(times):
                if int(subjqueue[x][y]) == 0:
                    result = 0
                else:
                    result = (((int(subjqueue[x][y + 1]) - int(subjqueue[x][y])) / int(subjqueue[x][y])) * 100)
                # print(result)
                self.QueueNestedPC[DQFront] = result
                DQFront = DQFront + 1
                # print(DQFront)
        print(self.QueueNestedPC)

    # Start of Stack Methods
    # This Method pushes to the Stack using the Top Pointer
    def PushStack(self, uinput):
        # Pushes the value on to the stack
        if self.Top == len(self.MAStack):
            self.Top = 0
        else:
            self.MAStack[self.Top] = uinput
            self.Top = self.Top + 1

    # This Method Pops from the Stack using the Top Pointer
    def PopStack(self):
        # Removes an item off the stack
        if self.Top == 0:
            print("Unable to Pop, Reached Bottom of Stack")
            return
        self.Top = self.Top - 1
        v = self.MAStack[self.Top]
        self.MAStack[self.Top] = " "
        return v

    # This Method Calculates the Moving Average of the Percentage Changes for the specific month. Then the value is
    # pushed to the the Stack
    def MovingAverage(self, periods):
        counter = periods * 11
        minus = 0
        while counter != 0:
            FinalPCMA = 0
            c = 0
            temp = []
            for x in range((len(self.QueueNestedPC) - periods) - minus, len(self.QueueNestedPC) - minus):
                temp.append(self.QueueNestedPC[x])
                FinalPCMA = FinalPCMA + temp[c]
                c = c + 1
            FinalPCMA = FinalPCMA / periods
            self.PushStack(FinalPCMA)
            counter = counter - periods
            minus = minus + periods
        print(self.MAStack)

    # This Method Pops from the Stack containing the Averages for the Percentage Change and then Apply the Value to the
    # previous Month. This is a recursive Algorithm as it calls itself.The final value is stored in the FinalValueQueue
    def ApplyMAPercentPrevValue(self, FinalValueQueue, subjqueue, times):
        if self.FinalQFront == 12:
            self.FinalQFront = 0
            self.ApplyMAPercentPrevValue(FinalValueQueue, subjqueue, times)  # Recursive Algorithm
        else:
            FinalValueQueue[self.FinalQFront] = self.DetermineStartingValue(subjqueue, (times + 1))
            self.FinalQFront = self.FinalQFront + 1
            for x in range(11):
                FinalValueQueue[self.FinalQFront] = FinalValueQueue[x] * (1 + ((self.PopStack()) / 100))
                self.FinalQFront = self.FinalQFront + 1

    # This class collects the test data for the ML Model from the SQL database
    def CollectTestData(self):
        # This class collects the Test data required from the SQL database and puts it into the panda dataframe
        # ready to be manipulated
        Department = self.GetDepartment()
        Campus = self.GetCampus()
        DIndex = self.CheckDPDict(Department)
        CIndex = self.CheckCPDict(Campus)
        Query = (" SELECT * FROM historical_data WHERE DepartmentCode = (%s) AND CampusCode = (%s) " % (DIndex, CIndex))
        Path = self.MYSQLPath()
        self.dataframe = pd.read_sql_query(Query, con=Path)
        self.dataframe = self.dataframe.drop(columns=['CampusCode', 'DepartmentCode'])
        if self.dataframe.empty:
            return False
        else:
            return True

    # Methods that prepares the training test data for the ML Model
    def LoadData(self):
        dataframe = self.dataframe.fillna(0.0)
        #    dataframe.set_index('Date', inplace=True)
        #    Rdata = dataframe.to_numpy()
        Rdata = dataframe
        Rdata = Rdata.sort_values(by='Date')
        Rdata = Rdata.reset_index(drop=True)
        Rdata['Date'] = pd.to_datetime(Rdata['Date']).dt.normalize()
        print()
        time.sleep(1)
        print(Rdata)
        return Rdata

    # Method that Plots Graph for Dataframe
    @staticmethod
    def PlotSQLGraph(raw_data):
        raw_data = raw_data.rename(columns={"Date": "ds", "Income": "y"})
        print(raw_data)
        raw_data.plot()
        pyplot.show()

    # Facebook Open Source Machine learning Algorithm
    def EvaluateFBProphetModel(self, raw_data, value, years):
        raw_data = raw_data.rename(columns={"Date": "ds", value: "y"})
        model = Prophet()
        model.fit(raw_data)
        # define the period for which we want a prediction
        future = list()
        for i in range(1, 13):
            date = '2014-%02d' % i
            future.append([date])
        future = DataFrame(future)
        future.columns = ['ds']
        future['ds'] = to_datetime(future['ds'])
        # use the model to make a forecast
        forecast = model.predict(future)
        # calculate MAE between expected and predicted values for december
        y_true = raw_data['y'][-12:].values
        y_pred = forecast['yhat'].values
        mae = mean_absolute_error(y_true, y_pred)
        print('MAE: %.3f' % mae)
        # plot expected vs actual
        pyplot.plot(y_true, label='Actual')
        pyplot.plot(y_pred, label='Predicted')
        pyplot.legend()
        pyplot.show()

    def OutOfSampleFBProphetForecast(self, raw_data, value, firsttime, years):
        if firsttime:
            self.SetoutFolderName(self.Getdftpath() + "ForecastedFileDirectory/FBModelValues.csv")
            # outFolderName is the Path
            if os.path.isfile(self.GetoutFoldername()) is True:
                # opening the file with w+ mode truncates the file
                f = open(self.GetoutFoldername(), "w+")
                f.close()
            else:
                file1 = open(self.GetoutFoldername(), "w")
                file1.close()
        raw_data = raw_data.rename(columns={"Date": "ds", value: "y"})
        model = Prophet()
        # fit the model
        model.fit(raw_data)
        # define the period for which we want a prediction
        future = model.make_future_dataframe(periods=(12 * years), freq='MS')
        # use the model to make a forecast
        forecast = model.predict(future)
        # summarize the forecast
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
        try:
            forecast.to_csv(self.GetoutFoldername(), mode='a')
            print("Final Values saved to CSV File in Program Folder")
        except:
            print("Error with exporting data to csv")
        # plot forecast
        model.plot(forecast)
        pyplot.show()

    # This is the Custom ML Algorithm. First it gets the year for the first and last row in the dataframe and then
    # minuses them and then adds 1 to calculate how many years of data entry does the dataframe have. Then the dataframe
    # passes in the Department the user wants to forecast for into the method that matches the user requested Department
    # to the specific Queue using Dictionaries. Once completed the Final Queue for that specific value will also be
    # matched with forecasted values using Dictionaries. The a Queue is created and the size of the Queue is dependant
    # on the amount of years of historical data there is. After the Queue is Populated from the dataframe and then a
    # separate queue is created containing the values for the specific month next to each other making it easier for
    # the Differences Method to calculate the Percentage Change between values. Then the Moving Average method is called
    # to gain the moving average of the percentage changes and then the Recursive Method is called to apply the Calulated
    # value for the average percentage change to be applied.Then the algorithm is repeated again.
    def CustomML(self, raw_data, value, Department):
        print()
        y1 = raw_data['Year'].iloc[0]
        lastrow = raw_data.shape[0] - 1
        y2 = raw_data['Year'].iloc[lastrow]
        self.Settimes(y2 - y1)
        times = self.Gettimes()
        subjqueue = self.CheckDepartment(Department)
        FinalValueQueue = self.CheckValue(value)
        self.CreateQueue(subjqueue, times + 1)
        self.PopulateQueue(subjqueue, raw_data, value, times + 1)
        self.CreateDifferencesQueue((times + 1))
        self.DifferencesQueue(subjqueue, (times + 1))
        self.MovingAverage(times + 1)
        self.ApplyMAPercentPrevValue(FinalValueQueue, subjqueue, times)
        print(FinalValueQueue)
        subjqueue.clear()
        self.QueueNestedPC.clear()
        print()
        print()

    # Method that prints final Output to the User stating what the Final Forecasted Values Are
    def CustomMLFinalOutput(self):
        print()
        time.sleep(1)
        print("Final Values for the next forecasted Year")
        time.sleep(1)
        print("Final Income: ", self.FinalQueueIncome)
        time.sleep(1)
        print("Final EstablishmentPay: ", self.FinalQueueEstablishmentPay)
        time.sleep(1)
        print("Final AgencyPay: ", self.FinalQueueAgencyPay)
        time.sleep(1)
        print("Final OtherPay: ", self.FinalQueueOtherPay)
        time.sleep(1)
        print("Final VariablePay: ", self.FinalQueueVariablePay)
        time.sleep(1)
        print("Final TotalPay: ", self.FinalQueueTotalPay)
        time.sleep(1)
        print("Final NonPay: ", self.FinalQueueNonPay)
        time.sleep(1)
        print("Final Surplus/Deficit: ", self.FinalQueueSurplusDeficit)
        time.sleep(1)
        print()

    # This Method adds the forecasted values from the machine learning/custom algorithm to the dataframe using The
    # pointer to traverse through each array to form a row which is added to the Dataframe
    def AddForecastValuestoDF(self, dataframe):
        Front = 0
        m1 = 0
        lastrow = dataframe.shape[0] - 1
        lastyear = int(dataframe['Year'].iloc[lastrow])
        newyear = int(lastyear + 1)
        students = int(dataframe['NoOfStudents'].iloc[lastrow])
        for i in range(12):
            self.NewYearColumnQueue[Front] = newyear
            self.NoOfStudentsQueue[Front] = students
            date = datetime.date(newyear, m1 + 1, 1)
            self.DateQueue[Front] = date
            Front = Front + 1
            m1 = m1 + 1
        for Rear in range(12):
            row_to_append = [self.NewYearColumnQueue[Rear], self.MonthsQueue[Rear], self.DateQueue[Rear],
                             self.FinalQueueIncome[Rear], self.FinalQueueEstablishmentPay[Rear],
                             self.FinalQueueVariablePay[Rear],
                             self.FinalQueueAgencyPay[Rear], self.FinalQueueOtherPay[Rear],
                             self.FinalQueueTotalPay[Rear],
                             self.FinalQueueNonPay[Rear], self.FinalQueueSurplusDeficit[Rear],
                             self.NoOfStudentsQueue[Rear]]
            dataframe_length = len(dataframe)
            dataframe.loc[dataframe_length] = row_to_append
        return dataframe
