# setting connection between python and postgres
import psycopg
import os
from dotenv import load_dotenv
load_dotenv()

from decimal import Decimal
from datetime import date,datetime

connection=psycopg.connect(

    host="localhost",
    dbname="expense_tracker",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port=5432
)
cursor=connection.cursor()

print("connected to postgreSQL successfully")


while True:
#asking user what they want
    print("YOU HAVE MULTIPLE CHOICES :-")
    print(" 1.Add your new expense")
    print(" 2.View your expense")
    print(" 3.Delete existing expense")
    print(" 4.Edit en existing expense")
    print(" 5.Monthly spending summary")
    print(" 6.Category wise summary")
    print(" 7.Search expenses by date") 
    print(" 8.Custom expense range") 
    print(" 9.Exit")
    choice=input("enter your choice :")


    if choice =="1":
        print("Add your new expense")
        amount=Decimal(input("enter amount :"))
        category=input("enter category :")
        description=input("enter description :")
        while True:
            try:
                date_text=input("enter the date (YYYY-MM-DD):")
                expense_date=datetime.strptime(date_text,"%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date! Please try again.")

        
        
        print(amount)
        print(category)
        print(description)
        print(expense_date)
    #this code is basically entering the data into postgresql
        # cursor=connection.cursor()
        cursor.execute(
        """
        INSERT INTO EXPENSES(amount,category,description,expense_date)
         VALUES(%s,%s,%s,%s)
        """,
        (amount,category,description,expense_date)
        )
        connection.commit()
        print("EXPENSE HAS BEEN SUCCESSFULLY ADDED!")

    elif choice =="2":
        print("View your expense")
        # cursor=connection.cursor()
        cursor.execute("SELECT * FROM expenses") #sends the select command to postgres and ask for all expenses
        expenses=cursor.fetchall() #take all the rows from postgres (returns)and add them in python variable(expenses)
    
        for one_row in expenses:
            expense_id,amount,category,description,expense_date = one_row
            print("ID :",expense_id)
            print("amount :",amount)
            print("category :",category)
            print("description :",description)
            print("date :",expense_date)
            print("------------------------------------")

    elif choice =="3":
        print("Delete existing expense")
        expense_id=int(input("Enter Expense ID to Delete : "))
        # cursor=connection.cursor()
        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id=%s
            """,
            (expense_id,)
        )
        print(cursor.rowcount)
        connection.commit()
        if cursor.rowcount >0:
            print("YOUR EXPENSE HAS BEEN SUCCESSFULLY DELETED!")
        else :
            print("OOPS!,NO EXPENSE WAS FOUND")

    elif choice=="4":
        print("Edit en existing expense")
        expense_id=int(input("Choose ID number to Edit the Expense : "))
        new_amount=Decimal(input("enter new amount : "))
        # cursor=connection.cursor()
        cursor.execute(
            """
            UPDATE expenses
            SET amount=%s
            WHERE id=%s
            """,
            (new_amount,expense_id)
        )
        print(cursor.rowcount)
        connection.commit()
        if cursor.rowcount >0:
            print("YOUR AMOUNT HAS BEEN SUCCESSFULLY UPDATED!")
        else:
            print("OOPS!THE ID DOESN'T EXIST \n PLEASE ENTER THE EXISTING ID!")
    
    elif choice=="5":
        print("Monthly spending summary")
        
        # cursor=connection.cursor()
        month=int(input("Enter Month(1-12):"))
        year=int(input("Enter Year:"))
        
        if month >=1 and month <=12:
            print("VALID MONTH")
        
           
            cursor.execute(
                """
                SELECT COUNT(*),SUM(amount)
                FROM expenses
                WHERE EXTRACT (MONTH FROM expense_date)=%s
                AND EXTRACT (YEAR FROM expense_date)=%s;
                """,(month,year)
            )
        
            result=cursor.fetchone()
            print("total number of expenses:",result[0])
            print("total spending is:",result[1])
        else:
            print("INVALID MONTH")  

    elif choice =="6":
        print("Category wise summary")
        print("YOU HAVE 2 CHOICES :-")
        print("1.View all categories")
        print("2.View specific spending category")
        category_choice=input("enter your choice :")

        if category_choice=="1":

            # cursor=connection.cursor()
            cursor.execute(
            """
            SELECT category,SUM (amount)
            FROM expenses
            GROUP BY category;
            """
            )  
            results=cursor.fetchall()
            for row in results:
                print("category :",row[0])
                print("total spending is :",row[1])
        
        
        elif category_choice=="2":
            category=input("Enter category you want to see :")
            # cursor=connection.cursor()
            cursor.execute(
            """
            SELECT category,SUM(amount)
            FROM expenses
            WHERE category=%s
            GROUP BY category;
            """,(category,))

            results =cursor.fetchone()

            if results is None:
                print("Category not found")
            else:
                print("category :",results[0])
                print("Total spending is :",results[1])

        else:
            print("Invalid choice! please select 1 or 2.")

            
    elif choice=="7":
        print("Search expenses by date")
        while True:
            try:
                date_text=input("enter date(YYYY-MM-DD):")
                expense_date=datetime.strptime(date_text,"%Y-%m-%d").date()
                
                break 
            except ValueError:
                print("Invalid date!please enter correct date.")

                
        cursor.execute(
            """
            SELECT *FROM expenses
            WHERE expense_date=%s
            """,(expense_date,)
        )

        results=cursor.fetchall()
        if not results:
            print("No expenses found on this date")

        else:
            for row in results:
                print(row)
    

    elif choice=="8":
        start_date=input("enter start date(YYYY-MM-DD) :")
        end_date=input("enter end date(YYYY-MM-DD) :")

        start_date=datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date=datetime.strptime(end_date,"%Y-%m-%d").date()
        if start_date > end_date:
            print("Start date can not be greater than end date")
        else:
            cursor.execute(
                """
                SELECT * FROM expenses
                WHERE expense_date BETWEEN %s and %s                                        
                 """,(start_date,end_date)
            )
            results=cursor.fetchall()

        if not results:
            print("No expense found!")

        else:
           for row in results:
            print("ID :",row[0])
            print("Amount :",row[1])
            print("Category :",row[2])
            print("Description :",row[3])
            print("Expense date :",row[4])
            
            


          
       


    elif choice =="9":
        print("you have successfully exited")
        connection.close()
        break

    else:
        print("Invalid choice.Please try again!")