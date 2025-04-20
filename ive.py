#Income vs Expense Python module
#Designed by tazrog
#2025
#For Windows and Linux
#Needs Drivewire4 to sync with coco

import pandas as pd
import os
import time
from os import system, name
import shutil
import matplotlib.pyplot as plt
import sys
import termios
import tty

# Import msvcrt only if the system is Windows
if os.name == 'nt':  # Windows
    import msvcrt  # Import for listening to keypresses on Windows

def get_keypress():
    """
    Cross-platform function to get a single keypress.
    Uses msvcrt for Windows and termios/tty for Linux.
    """
    if os.name == 'nt':  # Windows
        return msvcrt.getch().decode('utf-8').lower()
    else:  # Linux/Unix
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

again =0
def center_text(lines):

    # Get the terminal size
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns

    # Center each line and store in a new list
    centered_lines = [line.center(terminal_width) for line in lines]
    return centered_lines

def set_screen_color():
    if name == 'nt':  # Windows
        os.system('color 20')  # Set background to green and text to black
        system('cls')
    else:  # Linux/Unix
        print("\033[102m\033[30m", end="")  # Set background to bright green and text to black
        system('clear')

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
    if name == 'nt':  # Windows
        system('cls')
    else:  # Linux/Unix        
        system('clear')
    sys.exit()
    
def Disk_Location():
    # Check if the disk.txt file exists
    if os.path.isfile("disk.txt"):

        # Read the disk location from the file
        with open("disk.txt", "r") as f:
            disk = f.read().strip()        
        return disk   
    
    # Check if the IVE.DSK file exists in the directory
    if name == 'nt':  # Windows
        if os.path.isfile("disk\\IVE.DSK"):
            print("IVE.DSK file found in disk directory.")
            return "disk"
    else:
        if os.path.isfile("disk/IVE.DSK"):
            print("IVE.DSK file found in disk directory.")
            return "disk"

    # If the file does not exist, prompt the user for the location
    print("IVE.DSK file not found in disk directory.")
    print("Please enter the location of the IVE.DSK file.")
    print("Example: /home/user/IVE.DSK")
    disk=input("Enter the location of the IVE.DSK file: ")

    # Check if the file exists 
    if name == 'nt':  # Windows
        if os.path.isfile(disk+"\\IVE.DSK"):

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
            if os.path.isfile(disk+"\\IVE.DSK"):
                #Save disk loacation to txt file
                with open("disk.txt", "w") as f:
                    f.write(disk)
                f.close()
                print("IVE.DSK file found in the specified location.")  
    else:
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
                with open("disk.txt", "w") as f:
                    f.write(disk)
                f.close()
                print("IVE.DSK file found in the specified location.")   
    return disk

def Get_Files():
    if os.name == 'nt':  # Windows
        disk = Disk_Location()
        command = "decb copy "+disk+"\\IVE.DSK,OUT.DAT out.txt"
        os.system(command)
        command = "decb copy "+disk+"\\IVE.DSK,IN.DAT in.txt"
        os.system(command)
        command = "decb copy "+disk+"\\IVE.DSK,CAT.DAT cat.txt"
        os.system(command)
        command = "decb copy "+disk+"\\IVE.DSK,DATE.DAT date.txt"
        os.system(command)
        command = "decb copy "+disk+"\\IVE.DSK,YEAR.DAT year.txt"
        os.system(command)
    else:
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
    set_screen_color()   
    print("INCOME vs EXPENSE")
    dfin = pd.read_fwf("pin.txt", header=None, names=["Date", "Cat", "Amt"])
    dfin['Month'] = dfin['Date'].str[:2]
    dfout = pd.read_fwf("pout.txt", header=None, names=["Date", "Cat", "Amt"])
    dfout['Month'] = dfout['Date'].str[:2]
    
    # Print header with right-aligned columns
    print(f"{'M':>5} {'Income':>15} {'Expense':>15} {'Diff':>15}")
    print("-" * 50)

    # Iterate through each month and calculate totals
    for i in range(1, 13):
        a = f"{i:02}"  # Format month as two digits (e.g., "01", "02", ..., "12")
        Search_Month = dfin[dfin['Month'].str.contains(a, case=False)]['Amt'].sum()
        Search_Month_Exp = dfout[dfout['Month'].str.contains(a, case=False)]['Amt'].sum()
        print(f"{a:>5} {f'${Search_Month:,.2f}':>15} {f'${Search_Month_Exp:,.2f}':>15} {f'${Search_Month-Search_Month_Exp:,.2f}':>15}")

    # Print totals
    print("-" * 50)
    print(f"{'Total':>5} {f'${dfin['Amt'].sum():,.2f}':>15} {f'${dfout['Amt'].sum():,.2f}':>15} {f'${dfin['Amt'].sum()-dfout['Amt'].sum():,.2f}':>15}")
    print("Press [M]enu - [Q]uit")
    a = input()
    if a == "m" or a == "M":
        main_menu()
    if a == "q" or a == "Q":
        Exit_Program()

def Monthly_Graph():
    set_screen_color()    
    print("INCOME vs EXPENSE")
    print("CLOSE GRAPH TO RETURN")   

    # Load data
    dfin = pd.read_fwf("pin.txt", header=None, names=["Date", "Cat", "Amt"])
    dfin['Month'] = dfin['Date'].str[:2]
    dfout = pd.read_fwf("pout.txt", header=None, names=["Date", "Cat", "Amt"])
    dfout['Month'] = dfout['Date'].str[:2]

    # Map numeric months to their respective abbreviations
    month_labels = {
        "01": "JAN", "02": "FEB", "03": "MAR", "04": "APR",
        "05": "MAY", "06": "JUN", "07": "JUL", "08": "AUG",
        "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"
    }
    months = [f"{i:02}" for i in range(1, 13)]  # Ensure all months (01-12) are included
    income_values = []
    expense_values = []

    # Collect data for each month
    for a in months:
        Search_Month = dfin[dfin['Month'].str.contains(a, case=False)]['Amt'].sum()
        Search_Month_Exp = dfout[dfout['Month'].str.contains(a, case=False)]['Amt'].sum()
        income_values.append(Search_Month)
        expense_values.append(Search_Month_Exp)

    # Reverse the order of months, income, and expense for top-to-bottom display
    months.reverse()
    income_values.reverse()
    expense_values.reverse()

    # Create a horizontal bar graph with dynamic drawing order
    plt.figure(figsize=(10, 6), facecolor='black')  # Set figure background to black
    ax = plt.gca()
    ax.set_facecolor('black')  # Set axes background to black
    y_positions = range(len(months))

    for i, (income, expense) in enumerate(zip(income_values, expense_values)):
        if income > 0 or expense > 0:  # Only plot bars if income or expense is greater than 0
            if income >= expense:

                # Draw income first, then expense
                plt.barh(i, income, color='green', label='Income' if i == 0 else "", edgecolor='black')
                plt.barh(i, expense, color='red', label='Expense' if i == 0 else "", edgecolor='black')
            else:

                # Draw expense first, then income
                plt.barh(i, expense, color='red', label='Expense' if i == 0 else "", edgecolor='black')
                plt.barh(i, income, color='green', label='Income' if i == 0 else "", edgecolor='black')

            # Add text annotations for income and expense values
            if income >= expense:
                plt.text(income - (income * 0.1), i, f"${income:,.2f}", va='center', ha='right', color='white', fontsize=8)
                plt.text(expense / 2, i, f"${expense:,.2f}", va='center', ha='center', color='white', fontsize=8)
            else:
                plt.text(expense - (expense * 0.1), i, f"${expense:,.2f}", va='center', ha='right', color='white', fontsize=8)
                plt.text(income / 2, i, f"${income:,.2f}", va='center', ha='center', color='white', fontsize=8)

    # Set labels and title
    month_abbreviations = [month_labels[m] for m in months]  # Map numeric months to abbreviations
    plt.yticks(y_positions, month_abbreviations, color='white')  # Set y-tick labels to month abbreviations
    plt.title('INCOME vs EXPENSE', color='white')  # Set title color to white
    plt.xlabel('Amount', color='white')  # Set x-axis label color to white
    plt.ylabel('Month', color='white')  # Set y-axis label color to white
    plt.axvline(0, color='white', linewidth=0.8, linestyle='--')  # Add a vertical line at 0
    #plt.legend(facecolor='black', edgecolor='white', labelcolor='white')  # Set legend background and text colors
    plt.grid(axis='x', linestyle='--', alpha=0.7, color='white')  # Set grid color to white

    # Adjust x-axis ticks to exclude zero
    x_ticks = ax.get_xticks()
    x_ticks = [tick for tick in x_ticks if tick != 0]  # Exclude zero
    ax.set_xticks(x_ticks)
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
    print (f"INCOME   >>>           ${Income_total:,.2f}")
    print (f"EXPENSE  >>>           ${Expense_total:,.2f}")
    if diff >0:
        d="+"
    else:
        d="-"
    print (d,f"$FLOW  >>>           ${diff:,.2f}")
    
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
    print("     INCOME vs EXPENSE     ")
    print("       CREATED BY")
    print("         TAZROG")
    print("          2025")
    print("")
    print("         FOR THE")
    print("   TANDY COLOR COMPUTER")
    print("     DESKTOP COMPANION")
    print("")
    print("         LOADING")  
    Get_Files()
    time.sleep(2)
    date = Get_Date()  
    set_screen_color() 

    #Date Screen
    print("     INCOME vs EXPENSE")
    print("")
    print("")
    print("        DATE", date)
    print("")
    print("      PRESS [C]HANGE")
    print("  PRESS ANY KEY TO CONTINUE")       

    while True:
        key = get_keypress()  # Use the cross-platform function
        if key == "c":
            Change_Date()
            break
        else:
            if name == 'nt':
                system('cls')
            else:
                system('clear') 
            break
    main_menu()

def Change_Date():
    disk= Disk_Location()
    print ("NEW DATE")
    month=input("MONTH ")
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
    day=input("DAY ")
    date = month+"/"+day
    print (date)
    with open("date.txt", "w") as file:
            file.write(date)
            file.close()
    if name == 'nt':  # Windows
        command="decb copy date.txt "+disk+"\\IVE.DSK,DATE.DAT -r"
        os.system(command)
    else:
        command="decb copy date.txt "+disk+"/IVE.DSK,DATE.DAT -r"
        os.system(command)
    set_screen_color()
    main_menu()
    
def Cat_Expense():
    set_screen_color()
    print ("[M]ENU OR MONTH(1-12): ")
    month = input("LEAVE BLANK FOR YEAR: ")  
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
    if month == "m" or month =="M":  
        main_menu()
        
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
        month = "YEAR"
    print(f"CAT TOTAL FOR THE MONTH {month}:")
    print(category_totals.to_string())
    print("\nPRESS [M] FOR MENEU.")
    choice = input()
    if choice.lower() == 'm':
        main_menu()

def Cat_Income():
    set_screen_color()
    print ("[M]ENU OR MONTH(1-12): ")
    month = input("LEAVE BLANK FOR YEAR: ")    
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
    if month == "m" or month =="M":  
        main_menu()

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
    print(f"CAT TOTAL FOR MONTH {month}:")
    print(category_totals.to_string())
    print("\nPRESS [M] FOR MENU.")
    choice = input()
    if choice.lower() == 'm':
        main_menu()

def Backup_DSK():
    disk = Disk_Location()  # Get the current disk location
    dsk_file = os.path.join(disk, "IVE.DSK")  # Path to the .DSK file

    # Check if the .DSK file exists
    if not os.path.isfile(dsk_file):
        print("IVE.DSK file not found in the specified location.")
        print("Please check the disk location and try again.")
        time.sleep(3)
        return

    # Prompt the user for the backup folder
    print("Enter the path to the backup folder:")
    backup_folder = input("Backup Folder: ").strip()

    # Ensure the backup folder exists
    if not os.path.exists(backup_folder):
        try:
            os.makedirs(backup_folder)
            print(f"Backup folder '{backup_folder}' created.")
        except Exception as e:
            print(f"Error creating backup folder: {e}")
            time.sleep(3)
            return

    # Copy the .DSK file to the backup folder
    try:
        shutil.copy(dsk_file, backup_folder)
        print(f"IVE.DSK file successfully backed up to '{backup_folder}'.")
    except Exception as e:
        print(f"Error backing up file: {e}")
    time.sleep(3)
    main_menu()

def Settings():
    set_screen_color()    
    print("           Settings")
    print("      1- CHANGE DATE")
    print("      2- CHANGE DISK LOCATION")
    print("      3- CHANGE CATEGORIES")
    print("      4- BACKUP DSK")
    print("      5- BACK TO MAIN MENU")
    print("Press the respective key for your choice:")

    while True:        
            key = get_keypress()  # Get the key and convert to lowercase
            if key == "1":
                Change_Date()
                break
            elif key == "2":
                Disk_Location()
                break
            elif key == "3":
                if name == 'nt':
                    system('cls')
                else:
                    system('clear') 
                print("Please use CoCo to add and or change Categories.")
                time.sleep(3)
                Settings()  # Return to the settings menu
                break
            elif key == "4":
                Backup_DSK()
                break
            elif key == "5":
                main_menu()
                break
            elif key == "q":
                Exit_Program()
                break

def main_menu():
    set_screen_color()
    Get_Files()
    Get_Cat()
    date = Get_Date()
    print("")
    print("")
    print("          --> DATE " + date + " <--")
    print("       ***INCOME VS EXPENSE***")
    print("          1- ENTER INCOME")
    print("          2- ENTER EXPENSE")
    print("          3- LIST/FIND INCOME")
    print("          4- LIST/FIND EXPENSE")
    print("          5- MONTHLY IVE")
    print("          6- IVE GRAPH")
    print("          7- CAT. INCOME")
    print("          8- CAT. EXPENSE")
    print("          9- SETTINGS")
    print("-------------------------------------")
    total()
    print("")

    while True:
        key = get_keypress()  # Use the cross-platform function
        if key == "1":
            Enter_Income()
            break
        elif key == "2":
            Enter_Expense()
            break
        elif key == "3":
            List_Income()
            break
        elif key == "4":
            List_Expense()
            break
        elif key == "5":
            Monthly_IVE()
            break
        elif key == "6":
            Monthly_Graph()
            break
        elif key == "7":
            Cat_Income()
            break
        elif key == "8":
            Cat_Expense()
            break
        elif key == "9":
            Settings()
            break
        elif key == "q":
            Exit_Program()
            break

def List_Expense():
    disk = Disk_Location()
    set_screen_color()
    pd.set_option('display.max_rows', None)
   
    df = pd.read_fwf("pout.txt",header=None, names =["Date","Cat","Amt"])
    df.index +=1
    rows_per_page = 14
    a=input ("SEARCH [D]ATE, [C]AT, [A]MT, [M]ENU: ")
    
    if a=="a" or a=="A":  
        a=input("AMOUNT $?")        
        Search = df[df['Amt'].astype(str).str.startswith(a)]
        if name == 'nt':
            system('cls')
        else:
          system('clear') 
        for i in range(0, len(Search), rows_per_page):

    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]

    # Print the current chunk
            chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
            print(chunk)

    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                if name == 'nt':
                    system('cls')
                else:
                    system('clear') 
            Search_Sum= (df[df['Amt'].astype(str).str.startswith(a)]['Amt'].sum())
            print("")

            #print(f"Total for search Amt-{a} is ${Search_Sum:,.2f}")
            a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")
            
            if a=="m" or a=="M":
                main_menu()
            if a=="r" or a=="R":
                i=0
                List_Expense()
            if a=="a" or a=="A":
                Enter_Expense()
    if a=="c":
            a=input("CATEGORY? ")
            Search=(df[df['Cat'].str.startswith(a.upper())])
            if name == 'nt':
                system('cls')
            else:
                system('clear') 
            for i in range(0, len(Search), rows_per_page):

    # Get the current chunk of rows
                chunk = Search.iloc[i:i + rows_per_page]

    # Print the current chunk
                chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
                print(chunk)

    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                system('clear')
            Search_Sum= (df[df['Cat'].str.startswith(a.upper())]['Amt'].sum())
            print ("")
            print(f"TOTAL ? CAT-{a} ${Search_Sum:,.2f}")
            a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")                   
            if a=="m" or a=="M":
                main_menu()
            elif a=="r" or a=="R":
                i=0
                List_Expense()
            elif a=="a" or a=="A":
                Enter_Expense()
            elif a.isdigit():
                num=int(a)
                tbl="pout.txt"
                ptble="out.txt"
                dat="OUT.DAT"
                print ("ARE YOU SURE YOU WANT TO DELETE")
                print (df.loc[num])
                b=input()
                if b =="y" or b=="Y":
                    Delete(tbl,num,ptble,dat)                                        
                else:
                    List_Expense()
    if a=="d":
        a=input("DATE? ##/##. NEED AT LEAST DIGITS ")
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
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                system('clear')
            Search_Sum= (df[df['Date'].str.contains(a)]['Amt'].sum())
            print("")
            print(f"TOTAL ? DATE-{a} ${Search_Sum:,.2f}")                 
        a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")                
        if a=="m" or a=="M":
            main_menu()
        elif a=="r" or a=="R":
            List_Expense()
        elif a=="a" or a=="A":
            Enter_Expense()
        elif a.isdigit():
            num=int(a)
            tbl="pout.txt"
            ptble="out.txt"
            dat="OUT.DAT"
            print ("ARE YOU SURE YOU WANT TO DELETE")
            print (df.loc[num])
            b=input()
            if b =="y" or b=="Y":
                Delete(tbl,num,ptble,dat)                               
            else:
                List_Expense()        
        elif a =="q" or a=="Q":
            Exit_Program()
        main_menu()

def List_Income():
    set_screen_color()
    disk = Disk_Location()
    pd.set_option('display.max_rows', None)
    system('clear') 
    dfin = pd.read_fwf("pin.txt",header=None, names =["Date","Cat","Amt"])
    dfin.index +=1
    rows_per_page = 14
    a=input("SEARCH [D]ATE, [C]AT, [A]MT, [M]ENU: ")     
    if a=="a" or a =="A":  
        a=input("AMT? ")        
        Search = dfin[dfin['Amt'].astype(str).str.contains(a)]
        if name == 'nt':
            system('cls')
        else:
          system('clear') 
        for i in range(0, len(Search), rows_per_page):

    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]

    # Print the current chunk
            chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
            print(chunk)

    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                if name == 'nt':
                    system('cls')
                else:
                    system('clear') 
            Search_Sum= (dfin[dfin['Amt'].astype(str).str.startswith(a)]['Amt'].sum())
            print("")

            #print(f"Total for search Amt-{a} is ${Search_Sum:,.2f}")
            a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")            
            if a=="m" or a=="M":
                main_menu()
            if a=="r" or a=="R":
                i=0
                List_Income()
            if a=="a" or a=="A":
                Enter_Income()  
    if a=="c" or a=="C":
        a=input("CATEGORY? ")
        Search=(dfin[dfin['Cat'].str.startswith(a.upper())])
        if name == 'nt':
            system('cls')
        else:
            system('clear') 
        for i in range(0, len(Search), rows_per_page):

# Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]

# Print the current chunk
            chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
            print(chunk)

# Pause and wait for user input to continue
        if i + rows_per_page < len(Search):
            x= input("ENTER CONT [M]ENU? ")
            if x == "m" or x == "M":
                main_menu()
            if name == 'nt':
                system('cls')
            else:
                system('clear') 
        Search_Sum= (dfin[dfin['Cat'].str.startswith(a.upper())]['Amt'].sum())
        print ("")
        print(f"TOTAL CAT-{a} ${Search_Sum:,.2f}")
        a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")               
        if a=="m" or a=="M":
            main_menu()
        elif a=="r" or a=="R":
            i=0
            List_Income()
        elif a=="a" or a=="A":
            Enter_Income()
        elif a.isdigit():
            num=int(a)
            tbl="pin.txt"
            ptble="in.txt"
            dat="IN.DAT"
            print ("ARE YOU SURE YOU WANT TO DELETE")
            print (dfin.loc[num])
            b=input()
            if b =="y" or b=="Y":
                Delete(tbl,num,ptble,dat)
                if name == 'nt':  # Windows
                    command="decb copy "+ptble+" "+disk+"\\IVE.DSK,"+dat+" -r"
                    os.system(command)
                else:
                    command="decb copy "+ptble+" "+disk+"/IVE.DSK,"+dat+" -r"
                    os.system(command)
            else:
                List_Income() 
    if a=="d":
        a=input("DATE? ##/##. NEED AT LEAST 2 DIGITS ")
        Search=(dfin[dfin['Date'].str.startswith(a)])
        if name == 'nt':
            system('cls')
        else:
         system('clear')        
        for i in range(0, len(Search), rows_per_page):

    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]

    # Print the current chunk
            chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
            print(chunk)

    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                system('clear')
            Search_Sum= (dfin[dfin['Date'].str.contains(a)]['Amt'].sum())
            print("")
            print(f"TOTAL DATE-{a} ${Search_Sum:,.2f}") 
            a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")
            
            if a=="m" or a=="M":
                main_menu()
            if a=="r" or a=="R":
                List_Income()
            if a=="a" or a=="A":
                Enter_Income()
    if a=="c":
        a=input("CATEGORY? ")
        Search=(dfin[dfin['Cat'].str.startswith(a.upper())])
        if name == 'nt':
            system('cls')
        else:
            system('clear') 
        for i in range(0, len(Search), rows_per_page):

    # Get the current chunk of rows
            chunk = Search.iloc[i:i + rows_per_page]

    # Print the current chunk
            chunk['Amt'] = chunk['Amt'].apply(lambda x: f"${x:,.2f}")
            print(chunk)

    # Pause and wait for user input to continue
            if i + rows_per_page < len(Search):
                x= input("ENTER CONT [M]ENU? ")
                if x == "m" or x == "M":
                    main_menu()
                system('clear')
            Search_Sum= (dfin[dfin['Cat'].str.startswith(a.upper())]['Amt'].sum())
            print ("")
            print(f"TOTAL CAT-{a} ${Search_Sum:,.2f}")
            a=input ("[M]ENU -[R]EDO -[A]DD -DEL# ")              
            if a=="a" or a=="A":
                Enter_Income()                
            elif a=="m" or a=="M":
                main_menu()
            elif a=="r" or a=="R":
                List_Income()
            elif a=="a" or a=="A":
                Enter_Income()
            elif a.isdigit():
                num=int(a)
                tbl="pin.txt"
                ptble="in.txt"
                dat="IN.DAT"
                print ("ARE YOU SURE YOU WANT TO DELETE")
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
    if name == 'nt':  # Windows
        command="decb copy "+ptble+" "+disk+"\\IVE.DSK,"+dat+" -r"    
        os.system(command)
    else:
        command="decb copy "+ptble+" "+disk+"/IVE.DSK,"+dat+" -r"    
        os.system(command)
    if name == 'nt':
        system('cls')
    else:
        system('clear')     
    return

def Enter_Income():
        set_screen_color()
        disk=Disk_Location()
        again =0
        
        date=Get_Date()
        i=input("Amount $")
        if i =="m":
            main_menu()
        if i =="":
            print ("PLEASE ENTER A VALID OPTION")
            time.sleep(3)
            Enter_Income()
        if i.isdecimal() ==  True:
            print ("ENTER A AMOUNT #.##")
            time.sleep(3)
            Enter_Expense()
        
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
        amt=amt.replace(",", "")
        amtlen =len(amt)-1
        amt=amt+" "*(9-amtlen)
        if name == 'nt':
            system('cls')
        else:
            system('clear') 

    # List of lines to center
        lines_to_center = [
        "INCOME TRANSACTION",
        "",
        "",
        date+cat+"$"+amt,
        "",
        "PRESS [C]HANGE",
        "",
        "PRESS [A]DD",
        "PRESS [ENTER] TO ADD"
    ]
    # Center the lines
        centered = center_text(lines_to_center)

    # Print each centered line
        for line in centered:
            print(line)
        income=date+cat+amt
        a=input()
        if a =="c" or a =="C":
            Enter_Income()
        if a =="a" or a=="A":
            again =1
        else:
            line_number=1
            with open("in.txt", "r") as file:
                lines = file.readlines()
            lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
            with open("in.txt", 'w') as file:
                file.writelines(lines)
            file.close()
            if name == 'nt':  # Windows
                command = "decb copy in.txt "+disk+"\\IVE.DSK,IN.DAT -r"
                os.system(command)
            else:
                command = "decb copy in.txt "+disk+"/IVE.DSK,IN.DAT -r"
                os.system(command)           
        if again == 1:
            again =0
            Enter_Income()
        main_menu()

def Enter_Expense():
       set_screen_color()
       disk=Disk_Location()
       again =0
       date=Get_Date()       
       print ("EXPENSE TRANSACTION")
       i=input("AMOUNT $")
       if i =="m":
            main_menu()
       if i =="":
            print ("ENTER A VALID OPTION")
            time.sleep(3)
            Enter_Expense()
       if i.isdecimal() ==  True:
            print ("ENTER A AMOUNT #.##")
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
       amt=amt.replace(",", "")
       amtlen =len(amt)
       amt=amt+" "*(9-amtlen)       
       if name == 'nt':
            system('cls')
       else:
            system('clear') 

    # List of lines to center
       lines_to_center = [
       "EXPENSE TRANSACTION",
       "",
       "",
       date+cat+"$"+amt,
       "",
       "PRESS [C]HANGE",
       "",
       "PRESS [A]DD",
       "PRESS [ENTER] TO ADD"
    ]
    # Center the lines
       centered = center_text(lines_to_center)

    # Print each centered line
       for line in centered:
           print(line)
       income=date+cat+amt
       a=input()
       if a =="c" or a =="C":
            Enter_Expense()
       if a =="a" or a=="A":
            again =1
       line_number=1
       with open("out.txt", "r") as file:
            lines = file.readlines()
       lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
       with open("out.txt", 'w') as file:
            file.writelines(lines)
       file.close()
       if name == 'nt':  # Windows
            command = "decb copy out.txt "+disk+"\\IVE.DSK,OUT.DAT -r"
            os.system(command)
       else:
            command = "decb copy out.txt "+disk+"/IVE.DSK,OUT.DAT -r"
            os.system(command)          
       if again == 1:
            again =0
            Enter_Expense()       
       main_menu()             

def main():   
    set_screen_color()    
    intro()

main()


