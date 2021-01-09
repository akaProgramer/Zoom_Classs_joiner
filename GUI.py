import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm
import mysql.connector

from time import sleep
import itertools
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mydb= mysql.connector.connect(host="localhost", user="root", passwd="akash123#",database="akash")
        self.mycursor = self.mydb.cursor(buffered=True)
        self.geometry("1200x750")
        self.title("Zoom Automation and Stuff")
        # self.attributes("-alpha",0.8)
        self.frame= None
    def swap_frame(self,new_frame):
        for item in self.table_data.selection():
            self.table_data.selection_remove(item)
        if self.frame is not None:
            self.frame.destroy()
        self.frame= new_frame
        self.frame.pack(expand=True,fill=tk.BOTH)

    def check_subject_field(self,inp):
        self.output_display.config(text="",bg="orange")
        if len(inp)>20:
            self.output_display.config(text="*Character limit exceed",fg="#d62d20",bg="#ffffff")
            return False
        elif inp.isalpha() or " " in inp or "+" in inp:
            self.output_display.config(text="",bg="orange")
            return True
        elif inp == "":
            return True
        else:
            self.output_display.config(text="*Aphabets are allowed only!!",fg="#d62d20",bg="#ffffff")
            return False

    def check_zoom_id_field(self,inp):
        self.output_display.config(text="",bg="orange")
        if len(inp)>15:
            self.output_display.config(text="*Character limit exceed",fg="#d62d20",bg="#ffffff")
            return False
        elif inp.isnumeric() or " " in inp:
            self.output_display.config(text="",bg="orange")
            return True
        elif inp == "":
            return True
        else:
            self.output_display.config(text="*Numbers are allowed only!!",fg="#d62d20",bg="#ffffff")
            return False
        
    def check_zoom_password_field(self,inp):
        self.output_display.config(text="",bg="orange")
        if len(inp)>15:
            return False
        elif inp.isalnum() or " " in inp:
            self.output_display.config(text="",bg="orange")
            return True
        elif inp == "":
            return True
        else:
            self.output_display.config(text="*Character not allowed",fg="#d62d20",bg="#ffffff")
            return False
        
    
    
    def feed(self):
        subject= self.subject_name_Entry.get()
        zoom_id= self.zoom_id_Entry.get()
        zoom_password= self.zoom_password_Entry.get()
        zoom_link= self.zoom_link_Entry.get()
        if ((zoom_id !="" and zoom_password!="" and subject!="") or (subject!="" and zoom_link!="")):
            try:
                self.mycursor.execute("INSERT INTO ZOOM (subject,class_id,class_password,class_link) VALUES(%s,%s,%s,%s)",(subject,zoom_id,zoom_password,zoom_link))
                self.mydb.commit()
                self.table_data.insert('',"end",text="",values=(subject,zoom_id,zoom_password,zoom_link))
                tkm.showinfo("Insert Status","inserted successfully")
                self.subject_name_Entry.delete(0,'end')
                self.zoom_id_Entry.delete(0,'end')
                self.zoom_password_Entry.delete(0,'end')
                self.zoom_link_Entry.delete(0,'end')
                self.subject_name_Entry.focus()
            except:
                tkm.showerror("Error","Duplicate Entry")
                return
        else:
            tkm.showinfo("Insertion failed","either Subject, Zoom ID and Zoom Password or Subject, Zoom link should be filled")
            
    def insert(self):
        self.table_data.config(selectmode="none")
        self.insert_frame= tk.Frame(self.main_frame,bg="#ffffff")
        subject_name_label= tk.Label(self.insert_frame,text="Subject Name",font="arialblack 15")
        subject_name_label.place(x=40,y=20)
        self.subject_name_Entry= tk.Entry(self.insert_frame,font="arialblack 15")
        self.subject_name_Entry.place(x=220,y=20,height=33,width=400)
        self.subject_name_Entry.focus()
        reg1= self.insert_frame.register(self.check_subject_field)
        self.subject_name_Entry.config(validate="key",validatecommand=(reg1,'%P'))
        zoom_id_label= tk.Label(self.insert_frame,text="Zoom ID")
        zoom_id_label.pack()
        self.zoom_id_Entry= tk.Entry(self.insert_frame)
        self.zoom_id_Entry.pack()
        reg2= self.insert_frame.register(self.check_zoom_id_field)
        self.zoom_id_Entry.config(validate="key",validatecommand=(reg2,'%P'))
        zoom_password_label= tk.Label(self.insert_frame,text="Zoom Password")
        zoom_password_label.pack()
        self.zoom_password_Entry= tk.Entry(self.insert_frame)
        self.zoom_password_Entry.pack()
        reg3= self.insert_frame.register(self.check_zoom_password_field)
        self.zoom_password_Entry.config(validate="key",validatecommand=(reg3,'%P'))
        zoom_link_label= tk.Label(self.insert_frame,text="Zoom Link")
        zoom_link_label.pack()
        self.zoom_link_Entry= tk.Entry(self.insert_frame)
        self.zoom_link_Entry.pack()
        self.output_display= tk.Label(self.insert_frame)
        self.output_display.pack()
        submit_button= tk.Button(self.insert_frame,text="Submit",command=self.feed)
        submit_button.pack()
        return self.insert_frame

    def delete_record(self,table_data):
        selected_records= table_data.selection()
        print(selected_records)
        for record in selected_records:
            print(table_data.item(record)["values"])  
            sid= table_data.item(record)["values"][0]
            del_query= "DELETE FROM ZOOM WHERE subject=%s"
            sel_data=(sid,)
            self.mycursor.execute(del_query,sel_data)
            self.mydb.commit()
            self.table_data.delete(record)
        if selected_records==():
            tkm.showerror("Failed","No record selected")
        else:
            tkm.showinfo("Success","Selected items deleted")
    def delete(self):
        self.delete_frame= tk.Frame(self.main_frame,bg="#ffffff")
        self.table_data.config(selectmode="extended")
        self.table_data.pack(fill=tk.BOTH)
        delete_button= tk.Button(self.delete_frame,text="Delete", font="arialblack 20 bold",borderwidth=4 ,relief="raised",bg="#ffffff", command=lambda :self.delete_record(self.table_data))
        delete_button.pack(ipadx=40,ipady=2,pady=20)
        return self.delete_frame
        
    def updated(self):
        self.mycursor.execute("SELECT sno FROM ZOOM WHERE subject='"+self.values[0]+"'")
        no= self.mycursor.fetchone()
        subject= self.subject_name_Entry.get()
        print(subject)
        zoom_id= self.zoom_id_Entry.get()
        zoom_password= self.zoom_password_Entry.get()
        zoom_link= self.zoom_link_Entry.get()
        try:
            self.mycursor.execute("UPDATE ZOOM SET subject=%s,class_id=%s, class_password=%s, class_link=%s WHERE sno=%s",(subject,zoom_id,zoom_password,zoom_link,no[0]))
            self.mydb.commit()
            tkm.showinfo("Success","Successfully updated")
            self.table_data.item(self.current_record,values=(subject,zoom_id,zoom_password,zoom_link))
            self.subject_name_Entry.delete(0,'end')
            self.zoom_id_Entry.delete(0,'end')
            self.zoom_password_Entry.delete(0,'end')
            self.zoom_link_Entry.delete(0,'end')
            self.Update_button.config(state="disabled")
        except:
            tkm.showerror("Error","Duplicate Entry")
    def extracted(self):
        self.current_record= self.table_data.focus()
        self.values= self.table_data.item(self.current_record,"values")
        if self.values=="":
            tkm.showerror("selection error","no record selected, please select a record from the table")
            return
        else:
            self.Update_button.config(state="normal")
        self.subject_name_Entry.delete(0,'end')
        self.zoom_id_Entry.delete(0,'end')
        self.zoom_password_Entry.delete(0,'end')
        self.zoom_link_Entry.delete(0,'end')
        self.subject_name_Entry.insert(0,self.values[0])
        self.zoom_id_Entry.insert(0,self.values[1])
        self.zoom_password_Entry.insert(0,self.values[2])
        self.zoom_link_Entry.insert(0,self.values[3])

    def update(self):
        self.update_frame= tk.Frame(self.main_frame,bg="#ffffff")
        self.table_data.config(selectmode="browse")
        subject_name_label= tk.Label(self.update_frame,text="Subject Name")
        subject_name_label.pack()
        self.subject_name_Entry= tk.Entry(self.update_frame)
        self.subject_name_Entry.pack()
        self.subject_name_Entry.focus()
        reg1= self.update_frame.register(self.check_subject_field)
        self.subject_name_Entry.config(validate="key",validatecommand=(reg1,'%P'))
        zoom_id_label= tk.Label(self.update_frame,text="Zoom ID")
        zoom_id_label.pack()
        self.zoom_id_Entry= tk.Entry(self.update_frame)
        self.zoom_id_Entry.pack()
        reg2= self.update_frame.register(self.check_zoom_id_field)
        self.zoom_id_Entry.config(validate="key",validatecommand=(reg2,'%P'))
        zoom_password_label= tk.Label(self.update_frame,text="Zoom Password")
        zoom_password_label.pack()
        self.zoom_password_Entry= tk.Entry(self.update_frame)
        self.zoom_password_Entry.pack()
        reg3= self.update_frame.register(self.check_zoom_password_field)
        self.zoom_password_Entry.config(validate="key",validatecommand=(reg3,'%P'))
        zoom_link_label= tk.Label(self.update_frame,text="Zoom Link")
        zoom_link_label.pack()
        self.zoom_link_Entry= tk.Entry(self.update_frame)
        self.zoom_link_Entry.pack()
        self.output_display= tk.Label(self.update_frame)
        self.output_display.pack()
        
        self.retrieve_button= tk.Button(self.update_frame,text="Retrieve",command=self.extracted)
        self.retrieve_button.pack()
        
        self.Update_button= tk.Button(self.update_frame,text="Update",command=self.updated,state="disabled")
        self.Update_button.pack()
        return self.update_frame
    def check_seq_field(self,inp):
        if len(inp)>5:
            return False
        elif inp.isnumeric() or " " in inp:
            return True
        elif inp == "":
            return True
        else:
            return False
    def insert_seq(self,subjects,entries):
        for entry,subject in zip(entries,subjects):
            print(entry.get())
            print(subject)
            self.mycursor.execute("UPDATE ZOOM SET pno=%s WHERE subject=%s",(entry.get(),subject[0]))
            self.mydb.commit()
        tkm.showinfo("Success","Successfully updated")
    def schedule(self):
        self.schedule_frame= tk.Frame(self.main_frame)
        self.mycursor.execute("SELECT pno FROM zoom")
        lec_no= self.mycursor.fetchall()
        print(lec_no)
        self.mycursor.execute("SELECT subject FROM zoom")
        subjects= self.mycursor.fetchall()
        entries= []
        for subject,lec in zip(subjects,lec_no):
            subject_name_label= tk.Label(self.schedule_frame,text=subject)
            subject_name_label.pack()
            self.subject_seq_Entry= tk.Entry(self.schedule_frame)
            self.subject_seq_Entry.pack()
            reg3= self.schedule_frame.register(self.check_seq_field)
            self.subject_seq_Entry.config(validate="key",validatecommand=(reg3,'%P'))
            self.subject_seq_Entry.insert(0,lec)
            entries.append(self.subject_seq_Entry)
        submit_button= tk.Button(self.schedule_frame,text="Submit",command=lambda:self.insert_seq(subjects,entries))
        submit_button.pack()
        return self.schedule_frame
    def GUI_window(self):
        self.main_frame= tk.Frame(self,borderwidth=6,bg="#ffffff")
        head_frame= tk.Frame(self.main_frame)
        main_heading= tk.Label(head_frame, text="Online Class Automation",font="arialblack 40 bold",bg="#2962FF",fg="white")
        main_heading.pack(fill=tk.BOTH)
        head_frame.pack(fill=tk.BOTH,pady=(10,20))

        buttons_frame= tk.Frame(self.main_frame,bg="#ffffff")
        modify_button= tk.Button(buttons_frame,text="Update",font="black 20 bold",command=lambda:self.swap_frame(self.update()))
        modify_button.grid(ipadx=40,pady=10,padx=20,row=0,column=0)
        add_button= tk.Button(buttons_frame,text= "+Add",font="black 20 bold",bg="#2deb69",command=lambda:self.swap_frame(self.insert()))
        add_button.grid(ipadx=40,pady=10,padx=20,row=0,column=1)
        delete_button= tk.Button(buttons_frame, text="Delete",bg="#ff1414",font="black 20 bold",command=lambda: self.swap_frame(self.delete()))
        delete_button.grid(ipadx=40,pady=10,padx=20,row=0,column=2)
        delete_button= tk.Button(buttons_frame, text="Schedule",font="black 20 bold",command=lambda: self.swap_frame(self.schedule()))
        delete_button.grid(ipadx=40,pady=10,padx=20,row=0,column=3)
        buttons_frame.pack(pady=(10,10),fill=tk.X)
        
        
        table_frame= tk.Frame(self.main_frame)
        table_scrollbar=tk.Scrollbar(table_frame)
        table_scrollbar.pack(side="right",fill="y")
        table_xscrollbar=tk.Scrollbar(table_frame,orient="horizontal")
        table_xscrollbar.pack(side="bottom",fill="x")
        style= tk.ttk.Style(table_frame)
        style.theme_use("clam")
        style.configure(".",font="helvetica 10",borderwidth=4,padding=5, relief="groove")
        style.configure("Treeview.Heading",font="arialblack 13 bold",padding=6, relief="groove")
        self.mycursor.execute("select * from zoom")
        self.table_data = tk.ttk.Treeview(table_frame,selectmode="none",yscrollcommand= table_scrollbar.set ,xscrollcommand=table_xscrollbar.set)
        table_scrollbar.config(command=self.table_data.yview)
        table_scrollbar.config(command=self.table_data.xview)
        self.table_data["show"]="headings"
        self.table_data["columns"]= ("subject","class_id","class_password","class_link")
        self.table_data.column("subject", width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_id", width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_password", width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_link", width=400,minwidth=50, anchor=tk.CENTER)       
        self.table_data.heading("subject", text="Sub Name",anchor= tk.CENTER) 
        self.table_data.heading("class_id", text="Zoom ID",anchor= tk.CENTER) 
        self.table_data.heading("class_password", text="Zoom Password",anchor= tk.CENTER) 
        self.table_data.heading("class_link", text="Zoom Link",anchor= tk.CENTER)
        self.table_data.pack(fill=tk.BOTH)
        self.table_data.tag_configure("oddrow",background="#DFDFDF")
        self.table_data.tag_configure("evenrow",background="lightblue")
        i=0
        for row in self.mycursor:
            self.table_data.insert('',i,text="",values=(row[1],row[2],row[3],row[4]),tags=("evenrow",))
            i+=1
        table_frame.pack(fill="x")
        self.table_data.pack(fill=tk.BOTH)
        self.main_frame.pack(expand=True,fill=tk.BOTH)

    

if __name__ == "__main__":
    window= GUI()
    window.GUI_window()
    window.mainloop()
