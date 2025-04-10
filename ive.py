#Income vs Expense Python module
#Designed by tazrog
#2025
import pandas as pd
import os
import time
from os import system, name
import shutil
import numpy as np
import matplotlib.pyplot as plt
import sys

again =0
def center_text(lines):
    # Get the terminal size
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns
    # Center each line and store in a new list
    centered_lines = [line.center(terminal_width) for line in lines]
    return centered_lines

def Exit_Program():
    os.remove("in.txt")
    os.remove("out.txt")
    os.remove("cat.txt")
    os.remove("date.txt")
    os.remove("year.txt")
    os.remove("pin.txt")
    os.remove("pout.txt")
    if os.path.exists("pcat.txt"):
        os.remove("pcat.txt")    
    print ("Files Deleted")
    sys.exit()
    
def Disk_Location():
    # Check if the disk.txt file exists
    if os.path.isfile("disk.txt"):
        # Read the disk location from the file
        with open("disk.txt", "r") as f:
            disk = f.read().strip()        
        return disk
   
    # Check if the IVE.DSK file exists in the directory
    if os.path.isfile("disk/IVE.DSK"):
        print("IVE.DSK file found in disk directory.")
        return "disk"
    # If the file does not exist, prompt the user for the location
    print("IVE.DSK file not found in disk directory.")
    print("Please enter the location of the IVE.DSK file.")
    print("Example: /home/user/IVE.DSK")
    disk=input("Enter the location of the IVE.DSK file: ")
    # Check if the file exists  
    if os.path.isfile(disk+"/IVE.DSK"):
        #Save disk loacation to txt file
        with open("disk.txt", "w") as f:
            f.write(disk)
        f.close()
        print("IVE.DSK file found in the specified location.")
    else:
        print("IVE.DSK file not found in the specified location.")
        print("Please check the location and try again.")
        # Prompt the user for the location of the IVE.DSK file
        disk=input("Enter the location of the IVE.DSK file: ")
        # Check if the file exists
        if os.path.isfile(disk+"/IVE.DSK"):
            #Save disk loacation to txt file
            with open("disk.txt", "w") as f:
                f.write(disk)
            f.close()
            print("IVE.DSK file found in the specified location.")     
    return disk

def Get_Files():
    disk = Disk_Location()
    command = "decb copy "+disk+"/IVE.DSK,OUT.DAT out.txt"
    os.system(command)
    command = "decb copy "+disk+"/IVE.DSK,IN.DAT in.txt"
    os.system(command)
    command = "decb copy "+disk+"/IVE.DSK,CAT.DAT cat.txt"
    os.system(command)
    command = "decb copy "+disk+"/IVE.DSK,DATE.DAT date.txt"
    os.system(command)
    command = "decb copy "+disk+"/IVE.DSK,YEAR.DAT year.txt"
    os.system(command)

def add_new_line_after_chars(input_file, output_file, cat):
    char_val=30
    if cat == 1:
        char_val=10
    with open(input_file, 'r') as file:
        content = file.read()
    new_content = ''
    char_count = 0
    for char in content:
        new_content += char
        char_count += 1
        if char_count == char_val:
            new_content += '\n'
            char_count = 0
    with open(output_file, 'w') as file:
        file.write(new_content)

def Monthly_IVE():
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    print("Income vs Expense")
    dfin = pd.read_fwf("pin.txt",header=None, names =["Date","Cat","Amt"])
    dfin['Month']=dfin['Date'].str[:2]
    dfout = pd.read_fwf("pout.txt",header=None, names =["Date","Cat","Amt"])
    dfout['Month']=dfout['Date'].str[:2]
    print ("M          Income         Expense          Diff")
    print ("-----------------------------------------------------")
    for i in range(1,13):
        if i==1:
            a="01"
        if i==2:
            a="02"
        if i==3:
            a="03"
        if i==4:
            a="04"
        if i==5:
            a="05"
        if i==6:
            a="06"
        if i==7:
            a="07"
        if i==8:
            a="08"
        if i==9:
            a="09"
        if i==10:
            a="10"
        if i==11:
            a="11"
        if i==12:
            a="12"        
        Search_Month= (dfin[dfin['Month'].str.contains(a, case = False)]['Amt'].sum())
        Search_Month_Exp= (dfout[dfout['Month'].str.contains(a, case = False)]['Amt'].sum())
        print (f"Month {a}      ${Search_Month:,.2f}     ${Search_Month_Exp:,.2f}         ${Search_Month-Search_Month_Exp:,.2f}")   
    print ("-----------------------------------------------------")
    print(f"${dfin['Amt'].sum():,.2f}   ${dfout['Amt'].sum():,.2f}         ${dfin['Amt'].sum()-dfout['Amt'].sum():,.2f}")
    print ("Press [M]enu - [Q]uit")
    a=input()
    if a=="m":
        main_menu()
    if a=="q":
        Exit_Program()

def Monthly_Graph():
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    print("Income vs Expense")
    print("Close Graph to continue") 
    
    # Load data
    dfin = pd.read_fwf("pin.txt", header=None, names=["Date", "Cat", "Amt"])
    dfin['Month'] = dfin['Date'].str[:2]
    dfout = pd.read_fwf("pout.txt", header=None, names=["Date", "Cat", "Amt"])
    dfout['Month'] = dfout['Date'].str[:2]

    months = []
    income_values = []
    expense_values = []

    # Collect data for each month
    for i in range(1, 13):
        a = f"{i:02}"  # Format month as two digits (e.g., "01", "02", ..., "12")
        Search_Month = dfin[dfin['Month'].str.contains(a, case=False)]['Amt'].sum()
        Search_Month_Exp = dfout[dfout['Month'].str.contains(a, case=False)]['Amt'].sum()
        months.append(a)
        income_values.append(Search_Month)
        expense_values.append(Search_Month_Exp)

    # Reverse the order of months, income, and expense for top-to-bottom display
    months.reverse()
    income_values.reverse()
    expense_values.reverse()

    # Create a horizontal bar graph with dynamic drawing order
    plt.figure(figsize=(10, 6))
    y_positions = range(len(months))

    for i, (income, expense) in enumerate(zip(income_values, expense_values)):
        if income >= expense:
            # Draw income first, then expense
            plt.barh(i, income, color='green', label='Income' if i == 0 else "", edgecolor='black')
            plt.barh(i, expense, color='red', label='Expense' if i == 0 else "", edgecolor='black')
        else:
            # Draw expense first, then income
            plt.barh(i, expense, color='red', label='Expense' if i == 0 else "", edgecolor='black')
            plt.barh(i, income, color='green', label='Income' if i == 0 else "", edgecolor='black')

        # Add text annotations for income and expense values
        # Move the highest value annotation further to the right but inside the bar
        if income >= expense:
            plt.text(income - (income * 0.1), i, f"${income:,.2f}", va='center', ha='right', color='white', fontsize=8)
            plt.text(expense / 2, i, f"${expense:,.2f}", va='center', ha='center', color='white', fontsize=8)
        else:
            plt.text(expense - (expense * 0.1), i, f"${expense:,.2f}", va='center', ha='right', color='white', fontsize=8)
            plt.text(income / 2, i, f"${income:,.2f}", va='center', ha='center', color='white', fontsize=8)

    # Set labels and title
    plt.yticks(y_positions, months)
    plt.title('Income vs Expense (Dynamic Drawing Order)')
    plt.xlabel('Amount')
    plt.ylabel('Month')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')  # Add a vertical line at 0
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()      
    main_menu()    
    
def Get_Cat():
    disk = Disk_Location()
    input_file = 'cat.txt'
    output_file = 'pcat.txt'
    add_new_line_after_chars(input_file, output_file,1)
    dfcat = pd.read_fwf("pcat.txt",header=None, names =["Cat"])
    dfcat.index +=1
    return dfcat
    
def total():
    input_file = 'in.txt'
    output_file = 'pin.txt'
    add_new_line_after_chars(input_file, output_file,0)
    dfin = pd.read_fwf("pin.txt",header=None, names =["Date","Cat","Amt"])
    Income_total = (dfin["Amt"].sum())
    input_file = 'out.txt'
    output_file = 'pout.txt'
    add_new_line_after_chars(input_file, output_file,0)
    dfout = pd.read_fwf("pout.txt",header=None, names =["Date","Cat","Amt"])
    Income_total =(dfin["Amt"].sum())
    Expense_total =(dfout["Amt"].sum())
    diff = Income_total-Expense_total 
    print (f"Income   >>>           ${Income_total:,.2f}")
    print (f"Expense  >>>           ${Expense_total:,.2f}")
    if diff >0:
        d="+"
    else:
        d="-"
    print (d,f"$Flow  >>>           ${diff:,.2f}")
    
def Get_Date():
        with open("date.txt", "r") as file:
            lines = file.readlines()
            date = lines
        date=str(date)
        date = date.replace('[', '')
        date = date.replace(']', '')
        date = date.replace("'", "")
        file.close()
        return date

def intro():
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    # List of lines to center
    lines_to_center = [
        "Income vs Expense",
        "",
        "Created by",
        "TAZROG",
        "2025",
        "",
        "For the",
        "Tandy Color Computer",
        "Linux System",
        "",
        "",
        "Loading",
    ]
    # Center the lines
    centered = center_text(lines_to_center)
    # Print each centered line
    for line in centered:
        print(line)
    Get_Files()
    time.sleep(1)
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    #Check Date
    date=Get_Date()
# List of lines to center
    lines_to_center = [
        "Income vs Expesne",
        "",
        "",
        "Date",date,
        "",
        "Press [c] and [enter] to change",
        "Press any other key to start"
    ]
    # Center the lines
    centered = center_text(lines_to_center)
    # Print each centered line
    for line in centered:
        print(line)
    x=input()
    if x== "c":
       Change_Date()
    if x == " ":
        if name == 'nt':
            system('cls')
        else:
            system('clear') 
    with open("date.txt", "r") as file:
            lines = file.readlines()   
    main_menu()

def Change_Date():
    disk= Disk_Location()
    print ("new Date")
    month=input("Month ")
    day=input("Day ")
    date = month+"/"+day
    print (date)
    with open("date.txt", "w") as file:
            file.write(date)
            file.close()
    command="decb copy date.txt "+disk+"/IVE.DSK,DATE.DAT -r"
    os.system(command)
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    main_menu()
    
def Cat_Expense():
    print ("Select a month (MM): ")
    month = input("Leave blank to show year: ")  
    if month == "1":
        month = "01"
    if month == "2":
        month = "02"
    if month == "3":
        month = "03"
    if month == "4":
        month = "04"
    if month == "5":
        month = "05"
    if month == "6":
        month = "06"
    if month == "7":
        month = "07"
    if month == "8":
        month = "08"
    if month == "9":
        month = "09"    
        
    # Add all category amounts based on the selected month
    pd.set_option('display.max_rows', None)
    system('clear')
    df = pd.read_fwf("pout.txt", header=None, names=["Date", "Cat", "Amt"])
    df.index += 1
    # Filter rows based on the selected month
    filtered_df = df[df['Date'].str.startswith(month)]   
    if filtered_df.empty:
        print(f"No data found for the month {month}.")
        return
    # Group by category and sum amounts
    category_totals = filtered_df.groupby('Cat')['Amt'].sum()
    if month == "":
        month = "Year"
    print(f"Category totals for the month {month}:")
    print(category_totals.to_string())
    print("\nPress [M]enu to return.")
    choice = input()
    if choice.lower() == 'm':
        main_menu()

def Cat_Income():
    print ("Select a month (MM): ")
    month = input("Leave blank to show year: ")    
    if month == "1":
        month = "01"
    if month == "2":
        month = "02"
    if month == "3":
        month = "03"
    if month == "4":
        month = "04"
    if month == "5":
        month = "05"
    if month == "6":
        month = "06"
    if month == "7":
        month = "07"
    if month == "8":
        month = "08"
    if month == "9":
        month = "09"    
    # Add all category amounts based on the selected month
    pd.set_option('display.max_rows', None)
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    df = pd.read_fwf("pin.txt", header=None, names=["Date", "Cat", "Amt"])
    df.index += 1
    # Filter rows based on the selected month
    filtered_df = df[df['Date'].str.startswith(month)]
    if filtered_df.empty:
        print(f"No data found for the month {month}.")
        return
    # Group by category and sum amounts
    category_totals = filtered_df.groupby('Cat')['Amt'].sum()
    if month == "":
        month = "Year"
    print(f"Category totals for the month {month}:")
    print(category_totals.to_string())
    print("\nPress [M]enu to return.")
    choice = input()
    if choice.lower() == 'm':
        main_menu()

def Settings():
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    lines_to_center = [
        "Settings",
        "",
        "1- Change Date",
        "2- Change Disk Location",
        "3- Change Category",
        "4- Back to Main Menu",
        "",
    ]
    # Center the lines
    centered = center_text(lines_to_center)
    # Print each centered line
    for line in centered:
        print(line)
    a=input("Your Choice: ")
    if a=="1":
        Change_Date()
    if a=="2":
        Disk_Location()
    if a=="3":
        Get_Cat()
    if a=="4":
        main_menu()
    if a=="q":
        Exit_Program()    

def main_menu():
    # List of lines to center
    Get_Files()
    date=Get_Date()
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    lines_to_center = [
        "-->"+date+"<--",
        "***Income vs Expense***",
         "1 - Enter Income",
         "2 - Enter Expense",
         "3 - List/Find Income",
         "4 - List/Find Expense",
         "5 - Monthly IVE",
         "6 - IVE Graph",
         "7 - Cat. Income",
         "8 - Cat. Expense",
         "9 - Settings",
    ]
    # Center the lines
    centered = center_text(lines_to_center)
    # Print each centered line
    for line in centered:
        print(line)
    total()
    print ("")
    x=input("Your Choice: ")
    if x=="1":
        Enter_Income()
    if x=="2":
        Enter_Expense()
    if x=="3":
        List_Income()
    if x=="4":
        List_Expense()
    if x=="5":
        Monthly_IVE()
    if x=="6":
        Monthly_Graph()
    if x=="7":
        Cat_Income()
    if x=="8":
        Cat_Expense()
    if x=="9":
        Settings()
    if x=="q":
        Exit_Program()

def List_Expense():
    pd.set_option('display.max_rows', None)
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    df = pd.read_fwf("pout.txt",header=None, names =["Date","Cat","Amt"])
    df.index +=1
    rows_per_page = 32 
    print ("Search [D]ate, [C]at, [A]mt, [M]enu:")
    a=input()
    if a=="a":  
        a=input("What Amount? ")        
        Search = df[df['Amt'].astype(str).str.startswith(a)]
        if name == 'nt':
            system('cls')
        else:
          system('clear') 
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                if name == 'nt':
                    system('cls')
                else:
                    system('clear') 
            Search_Sum= (df[df['Amt'].astype(str).str.startswith(a)]['Amt'].sum())
            print("")
            #print(f"Total for search Amt-{a} is ${Search_Sum:,.2f}")
            print ("[M]enu -[R]edo -[A]dd -Del#")
            a=input()
            if a=="m":
                main_menu()
            if a=="r":
                List_Expense()
            if a=="a":
                Enter_Expense()
    if a=="d":
        a=input("What date? ##/## format. Need at lest 2 digits")
        Search=(df[df['Date'].str.startswith(a)])
        if name == 'nt':
            system('cls')
        else:
         system('clear') 
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                system('clear')
            Search_Sum= (df[df['Date'].str.contains(a)]['Amt'].sum())
            print("")
            print(f"Total for search date-{a} is ${Search_Sum:,.2f}") 
        print ("[M]enu -[R]edo -[A]dd -Del#")
        a=input()
        if a=="m":
            main_menu()
        if a=="r":
            List_Expense()
        if a=="a":
            Enter_Expense()
        if a=="c":
            a=input("What Category? ")
            Search=(df[df['Cat'].str.startswith(a.upper())])
            if name == 'nt':
                system('cls')
            else:
                system('clear') 
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                system('clear')
            Search_Sum= (df[df['Cat'].str.contains(a, case = False)]['Amt'].sum())
            print ("")
            print(f"Total for search Cat-{a} is ${Search_Sum:,.2f}")
        print ("[M]enu -[R]edo -[A]dd -Del#")
        a=input()        
        if a=="m":
            main_menu()
        elif a=="r":
            List_Expense()
        elif a=="a":
            Enter_Expense()
        elif a.isdigit():
            num=int(a)
            tbl="pout.txt"
            ptble="out.txt"
            dat="OUT.DAT"
            print ("Are you sure you want to delete")
            print (df.loc[num])
            b=input()
            if b =="y":
                Delete(tbl,num,ptble,dat)
            else:
                List_Expense()
        
        elif a =="q":
            Exit_Program()
        main_menu()

def List_Income():
    pd.set_option('display.max_rows', None)
    system('clear') 
    dfin = pd.read_fwf("pin.txt",header=None, names =["Date","Cat","Amt"])
    dfin.index +=1
    rows_per_page = 32 
    print ("Search [D]ate, [C]at, [A]mt, [M]enu:")
    a=input()   
    if a=="a":  
        a=input("What Amount? ")        
        Search = dfin[dfin['Amt'].astype(str).str.contains(a)]
        if name == 'nt':
            system('cls')
        else:
          system('clear') 
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                if name == 'nt':
                    system('cls')
                else:
                    system('clear') 
            Search_Sum= (dfin[dfin['Amt'].astype(str).str.startswith(a)]['Amt'].sum())
            print("")
            #print(f"Total for search Amt-{a} is ${Search_Sum:,.2f}")
            print ("[M]enu -[R]edo -[A]dd -Del#")
            a=input()
            if a=="m":
                main_menu()
            if a=="r":
                List_Income()
            if a=="a":
                Enter_Income()   
    if a=="d":
        a=input("What date? ##/## format. Need at lest 2 digits")
        Search=(dfin[dfin['Date'].str.startswith(a)])
        if name == 'nt':
            system('cls')
        else:
         system('clear')        
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                system('clear')
            Search_Sum= (dfin[dfin['Date'].str.contains(a)]['Amt'].sum())
            print("")
            print(f"Total for search date-{a} is ${Search_Sum:,.2f}") 
            print ("[M]enu -[R]edo -[A]dd -Del#")
            a=input()
            if a=="m":
                main_menu()
            if a=="r":
                List_Income()
            if a=="a":
                Enter_Income()
    if a=="c":
        a=input("What Category? ")
        Search=(dfin[dfin['Cat'].str.startswith(a.upper())])

        if name == 'nt':
            system('cls')
        else:
            system('clear') 
        for i in range(0, len(Search), rows_per_page):
    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]
    # Print the current chunk
            print(chunk)
    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                input("Press Enter to continue...")
                system('clear')
            Search_Sum= (dfin[dfin['Cat'].str.contains(a, case = False)]['Amt'].sum())
            print ("")
            print(f"Total for search Cat-{a} is ${Search_Sum:,.2f}")
            print ("[M]enu -[R]edo -[A]dd -Del#")
            a=input()    
            if a=="a":
                pass
            elif a=="m":
                main_menu()
            elif a=="r":
                List_Income()
            elif a=="a":
                Enter_Income()
            elif a.isdigit():
                num=int(a)
                tbl="pin.txt"
                ptble="in.txt"
                dat="IN.DAT"
                print ("Are you sure you want to delete")
                print (dfin.loc[num])
                b=input()
                if b =="y":
                    Delete(tbl,num,ptble,dat)
                else:
                    List_Income()
    main_menu()

def Delete(tbl,num,ptble,dat):
    disk =Disk_Location()
    df= pd.read_fwf(tbl,header=None, names =["Date","Cat","Amt"])
    df.index +=1
    df=df.drop(index=num)
    continuous_row = []
    for index, row in df.iterrows():
    # For each row, iterate through each column
        for value in row:
            continuous_row.append(f"{str(value):<10}")  # Format values to be 10 characters wide
# Join the list into a single string with a single space between each formatted entry
    continuous_row_string = ''.join(continuous_row)
# Save the continuous row to a text file
    with open(ptble, 'w') as f:
        f.write(continuous_row_string)
    command="decb copy "+ptble+" "+disk+"/IVE.DSK,"+dat+" -r"
    if name == 'nt':
        system('cls')
    else:
        system('clear')     
    main_menu()

def Enter_Income():
        disk=Disk_Location()
        again =0
        system('clear')
        date=Get_Date()
        i=input("Amount ")
        if i =="m":
            main_menu()
        if i =="":
            print ("Please enter a valid option")
            time.sleep(3)
            Enter_Income()
        if i.isdecimal() ==  True:
            print ("Please enter a dolar amount i.e. 1.00 -include the cents.")
            time.sleep(3)
            Enter_Expense()
        system('clear')
        dfcat=Get_Cat()
        print (dfcat)
        c=input()
        c=int(c)
        cat = dfcat.loc[c, 'Cat']
        print(date+"  "+cat+"  "+i)
        date=date+" "*5
        catlen=len(cat)-1
        cat=cat+" "*(10-catlen)
        i=float(i)
        amt = f"{i:,.2f}"
        amtlen =len(amt)-1
        amt=amt+" "*(9-amtlen)
        if name == 'nt':
            system('cls')
        else:
            system('clear') 
    # List of lines to center
        lines_to_center = [
        "Income Transaction",
        "",
        "",
        date+cat+"$"+amt,
        "",
        "Press [C]hange",
        "",
        "Press [A] another",
        "Press [Enter] to add"
    ]
    # Center the lines
        centered = center_text(lines_to_center)
    # Print each centered line
        for line in centered:
            print(line)
        income=date+cat+amt
        a=input()
        if a =="c":
            Enter_Expense()
        if a =="a":
            again =1
        else:
            line_number=1
            with open("out.txt", "r") as file:
                lines = file.readlines()
            lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
            with open("out.txt", 'w') as file:
                file.writelines(lines)
            file.close()
            command = "decb copy in.txt "+disk+"/IVE.DSK,IN.DAT -r"
            os.system(command)           
            if again == 1:
                again =0
                Enter_Income()
            main_menu()

def Enter_Expense():
       disk=Disk_Location()
       again =0
       date=Get_Date()
       system('clear')
       print ("Expense Transaction")
       i=input("Amount ")
       if i =="m":
            main_menu()
       if i =="":
            print ("Please enter a valid option")
            time.sleep(3)
            Enter_Expense()
       if i.isdecimal() ==  True:
            print ("Please enter a dolar amount i.e. 1.00 -include the cents.")
            time.sleep(3)
            Enter_Expense()        
       if name == 'nt':
         system('cls')
       else:
         system('clear') 
       dfcat=Get_Cat()
       print (dfcat)
       c=input()
       c=int(c)
       cat = dfcat.loc[c, 'Cat']
       print(date+"  "+cat+"  "+i)
       date=date+" "*5
       catlen=len(cat)-1
       cat=cat+" "*(10-catlen)
       i=float(i)
       amt = f"{i:,.2f}"
       amtlen =len(amt)
       amt=amt+" "*(9-amtlen)       
       if name == 'nt':
            system('cls')
       else:
            system('clear') 
    # List of lines to center
       lines_to_center = [
       "Expense Transaction",
       "",
       "",
       date+cat+"$"+amt,
       "",
       "Press [C]hange",
       "",
       "Press [A] another",
       "Press [Enter] to add"
    ]
    # Center the lines
       centered = center_text(lines_to_center)
    # Print each centered line
       for line in centered:
           print(line)
       income=date+cat+amt
       a=input()
       if a =="c":
            Enter_Expense()
       if a =="a":
            again =1
       else:
           line_number=1
           with open("out.txt", "r") as file:
               lines = file.readlines()
           lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
           with open("out.txt", 'w') as file:
               file.writelines(lines)
           file.close()
           command = "decb copy out.txt "+disk+"/IVE.DSK,OUT.DAT -r"
           os.system(command)          
           if again == 1:
                again =0
                Enter_Expense()       
           main_menu()             

def main():
    #check to see if user is on windows or linux
    if name == 'nt':
        system('cls')
    else:
        system('clear') 
    intro()

main()


