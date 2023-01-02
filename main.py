import datetime
from datetime import *
from customtkinter import *

set_appearance_mode("dark")

root = CTk()
root.geometry("500x500")

months = ["JAN", "FEB", "MAR", "APR", "MAY",
          "JUN", "JUL", "AUG", "SEP", "OCT",
          "NOV", "DEC"]
dates = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
         "13", "14", "15", "16", "17", "18", "19", "20", "21", "22",
         "23", "24", "25", "26", "27", "28", "29", "30", "31"]

label1 = CTkLabel(root, text="insert date of last period")
label1.pack()

months = CTkComboBox(root, values=months)
months.pack()

dates = CTkComboBox(root, values=dates)
dates.pack()

print(datetime.today())

root.mainloop()


