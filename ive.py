#Income vs Expense Python module
#Designed by tazrog
#2025
import pandas as pd
import os
import time
from os import system, name
import shutil

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
    quit()
    
    

def Get_Files():
    command = "decb copy IVE25.DSK,OUT.DAT out.txt"
    os.system(command)
    command = "decb copy IVE25.DSK,IN.DAT in.txt"
    os.system(command)
    command = "decb copy IVE25.DSK,CAT.DAT cat.txt"
    os.system(command)
    command = "decb copy IVE25.DSK,DATE.DAT date.txt"
    os.system(command)
    command = "decb copy IVE25.DSK,YEAR.DAT year.txt"
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

def Get_Cat():
    input_file = 'cat.txt'
    output_file = 'pcat.txt'
    add_new_line_after_chars(input_file, output_file,1)
    dfcat = pd.read_fwf("pcat.txt",header=None, names =["Cat"])
    dfcat.index +=1
    return dfcat
    with open("in.txt", "r") as file:
            lines = file.readlines()
    lines[line_number-1] = lines[line_number-1].rstrip('\n') + income
    with open("in.txt", 'w') as file:
           file.writelines(lines)
    file.close()
    command = "decb copy in.txt IVE25.DSK,IN.DAT -r"
    os.system(command)

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
       system('clear')
    with open("date.txt", "r") as file:
            lines = file.readlines()   
    main_menu()

def Change_Date():
    print ("new Date")
    month=input("Month ")
    day=input("Day ")
    date = month+"/"+day
    print (date)
    with open("date.txt", "w") as file:
            file.write(date)
            file.close()
    command="decb copy date.txt IVE25.DSK,DATE.DAT -r"
    os.system(command)
    main_menu()

def main_menu():
    # List of lines to center
    Get_Files()
    date=Get_Date()
    system('clear') 
    lines_to_center = [
        "-->"+date+"<--",
        "***Income vs Expense***",
        "1- Enter Income",
        "2- Enter Expense",
        "3- List/Find Income",
        "4- List/Find Expense",
        "5- Monthly IVE",
        "6- IVE Graph",
        "7- Cat. Income",
        "8- Cat Expense",
        "9- Settings",
        "",
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
    if x=="q":
        Exit_Program()

def List_Expense():
    pd.set_option('display.max_rows', None)
    system('clear') 
    df = pd.read_fwf("pout.txt",header=None, names =["Date","Cat","Amt"])
    df.index +=1
    rows_per_page = 32 
    print ("Search [D]ate, [C]at, [A]mt, [M]enu:")
    a=input()
    if a=="d":
        a=input("What date? ")
        Search=(df[df['Date'].str.contains(a)])
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
        List_Income()
    if a=="a":
        Enter_Income()
    if a=="c":
        a=input("What Category? ")
        Search=(df[df['Cat'].str.contains(a, case=False)])
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
        
    elif a=="m":
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
    if a=="d":
        a=input("What date? ")
        Search=(dfin[dfin['Date'].str.contains(a)])
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
        Search=(dfin[dfin['Cat'].str.contains(a, case=False)])
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
    command="decb copy "+ptble+" IVE25.DSK,"+dat+" -r"
    os.system(command)
    main_menu()

def Enter_Income():
       again =0
       system('clear')
       date=Get_Date()
       i=input("Amount ")
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
       line_number=1
       with open("in.txt", "r") as file:
            lines = file.readlines()
       lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
       with open("in.txt", 'w') as file:
           file.writelines(lines)
       file.close()  
       command = "decb copy in.txt IVE25.DSK,IN/DAT -r"
       os.system(command)
       main_menu()

def Enter_Expense():
       again =0
       date=Get_Date()
       system('clear')
       print ("Expense Transaction")
       i=input("Amount ")
       if i =="":
            print ("Please enter a valid option")
            time.sleep(3)
            Enter_Expense()
       if i.isdigit() ==  False:
            print ("Please enter a number option")
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
       amtlen =len(amt)
       amt=amt+" "*(9-amtlen)
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
       line_number=1
       with open("out.txt", "r") as file:
            lines = file.readlines()
       lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + income
       with open("out.txt", 'w') as file:
            file.writelines(lines)
       file.close()
       command = "decb copy out.txt IVE25.DSK,OUT/DAT -r"
       os.system(command)
       if again == 1:
            again =0
            Enter_Expense()
       main_menu()

def main():
    system('clear') 
    intro()

main()


