import tkinter as tk#library for tkinter

def main():
    MainWindow = tk.Tk()
    OutputBox1 = tk.Text(MainWindow,bg='gray', width=5, height=5).grid(row=0, column=0)
    OutputBox2 = tk.Text(MainWindow,bg='gray', width=5, height=5).grid(row=1, column=0)
    EntryBox1 = tk.Entry(MainWindow,bg='gray').grid(row=2, column=0)
    
    tk.mainloop()

main()