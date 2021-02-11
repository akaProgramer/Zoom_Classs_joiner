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
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
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
        if len(inp)>20:
            return False
        elif inp.isalpha() or " " in inp or "+" in inp:

            return True
        elif inp == "":
            return True
        else:
            return False

    def check_time_field(self,inp):
        if len(inp)>12:
            return False
        elif inp.isnumeric() or ":" in inp:
            return True
        elif inp == "":
            return True
        else:
            return False

    def check_zoom_id_field(self,inp):
        if len(inp)>15:
            return False
        elif inp.isnumeric() or " " in inp:
            return True
        elif inp == "":
            return True
        else:
            return False
        
    def check_zoom_password_field(self,inp):
        if len(inp)>15:
            return False
        elif inp.isalnum() or " " in inp:

            return True
        elif inp == "":
            return True
        else:
            return False
        
    
    
    def feed(self):
        subject= self.subject_name_Entry.get()
        zoom_id= self.zoom_id_Entry.get()
        zoom_password= self.zoom_password_Entry.get()
        zoom_link= self.zoom_link_Entry.get()
        From_time= self.zoom_from_entry.get()
        To_time= self.zoom_to_entry.get()
        print(subject,zoom_id,zoom_link,zoom_password,subject,From_time,To_time)
        if ((zoom_id !="" and zoom_password!="" and subject!="") or (subject!="" and zoom_link!="")):
            try:
                self.mycursor.execute("INSERT INTO ZOOM (subject,class_id,class_password,class_link,from_time,to_time) VALUES(%s,%s,%s,%s,%s,%s)",(subject,zoom_id,zoom_password,zoom_link,From_time,To_time))
                self.mydb.commit()
                self.table_data.insert('',"end",text="",values=(subject,zoom_id,zoom_password,zoom_link,From_time,To_time))
                tkm.showinfo("Insert Status","inserted successfully")
                self.subject_name_Entry.delete(0,'end')
                self.zoom_id_Entry.delete(0,'end')
                self.zoom_password_Entry.delete(0,'end')
                self.zoom_link_Entry.delete(0,'end')
                self.zoom_from_entry.delete(0,'end')
                self.zoom_to_entry.delete(0,'end')
                self.subject_name_Entry.focus()
            except:
                tkm.showerror("Error","Duplicate Entry")
                return
        else:
            tkm.showinfo("Insertion failed","either Subject, Zoom ID and Zoom Password or Subject, Zoom link should be filled")
            
    def insert(self):
        self.table_data.config(selectmode="none")
        self.insert_frame= tk.Frame(self.main_frame,bg="#ffffff")
        subject_name_label= tk.Label(self.insert_frame,text="Subject Name : ",font="arialblack 12",bg="#ffffff")
        subject_name_label.grid(column=0,row=0,padx=(200,10),pady=10)
        self.subject_name_Entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.subject_name_Entry.grid(column=2,row=0,padx=(20,10),pady=10,ipady=3)
        self.subject_name_Entry.focus()
        reg1= self.insert_frame.register(self.check_subject_field)
        self.subject_name_Entry.config(validate="key",validatecommand=(reg1,'%P'))
        zoom_id_label= tk.Label(self.insert_frame,text="Zoom ID : ",bg="#ffffff",font="arialblack 12")
        zoom_id_label.grid(column=0,row=1,padx=(200,10),pady=10)
        self.zoom_id_Entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.zoom_id_Entry.grid(column=2,row=1,padx=(20,10),pady=10,ipady=3)
        reg2= self.insert_frame.register(self.check_zoom_id_field)
        self.zoom_id_Entry.config(validate="key",validatecommand=(reg2,'%P'))
        zoom_password_label= tk.Label(self.insert_frame,text="Zoom Password :",bg="#ffffff",font="arialblack 12")
        zoom_password_label.grid(column=0,row=2,padx=(200,10),pady=10)
        self.zoom_password_Entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.zoom_password_Entry.grid(column=2,row=2,padx=(20,10),pady=10,ipady=3)
        reg3= self.insert_frame.register(self.check_zoom_password_field)
        self.zoom_password_Entry.config(validate="key",validatecommand=(reg3,'%P'))
        zoom_link_label= tk.Label(self.insert_frame,text="Zoom Link : ",bg="#ffffff",font="arialblack 12")
        zoom_link_label.grid(column=0,row=3,padx=(200,10),pady=10)
        self.zoom_link_Entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.zoom_link_Entry.grid(column=2,row=3,padx=(20,10),pady=10,ipady=3)

        zoom_timing_label = tk.Label(self.insert_frame, text="Timings (hh:mm:ss)",bg="#ffffff",font="arialblack 12")
        zoom_timing_label.grid(column=3,row=0,padx=(200,10),pady=10)
        zoom_from= tk.Label(self.insert_frame,text="From : ",bg="#ffffff",font="arialblack 12")
        zoom_from.grid(column=3,row=1,pady=10)
        self.zoom_from_entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.zoom_from_entry.grid(column=4,row=1,pady=10,ipady=3)
        regt= self.insert_frame.register(self.check_time_field)
        self.zoom_from_entry.config(validate="key",validatecommand=(regt,'%P'))
        zoom_to= tk.Label(self.insert_frame,text="To : ",bg="#ffffff",font="arialblack 12")
        zoom_to.grid(column=3,row=2,pady=10)
        self.zoom_to_entry= tk.Entry(self.insert_frame,font="arialblack 12")
        self.zoom_to_entry.grid(column=4,row=2,pady=10,ipady=3)
        regtt= self.insert_frame.register(self.check_time_field)
        self.zoom_to_entry.config(validate="key",validatecommand=(regtt,'%P'))
        submit_button= tk.Button(self.insert_frame,text="Submit",command=self.feed,font="arialblack 15",bg="#ffffff",cursor="hand2")
        submit_button.grid(row=5,column=1,pady=10)
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
        delete_button= tk.Button(self.delete_frame,text="Delete",cursor="hand2", font="arialblack 20 bold",borderwidth=4 ,relief="raised",bg="#ffffff", command=lambda :self.delete_record(self.table_data))
        delete_button.pack(ipadx=40,ipady=2,pady=20)
        return self.delete_frame
        
    def updated(self):
        self.mycursor.execute("SELECT sno FROM ZOOM WHERE subject='"+self.values[0]+"'")
        no= self.mycursor.fetchone()
        subject= self.subject_name_Entry.get()
        zoom_id= self.zoom_id_Entry.get()
        zoom_password= self.zoom_password_Entry.get()
        zoom_link= self.zoom_link_Entry.get()
        From_time= self.zoom_from_entry.get()
        To_time= self.zoom_to_entry.get()
        try:
            self.mycursor.execute("UPDATE ZOOM SET subject=%s,class_id=%s, class_password=%s, class_link=%s,from_time=%s,to_time=%s WHERE sno=%s",(subject,zoom_id,zoom_password,zoom_link,From_time,To_time,no[0]))
            self.mydb.commit()
            tkm.showinfo("Success","Successfully updated")
            self.table_data.item(self.current_record,values=(subject,zoom_id,zoom_password,zoom_link,From_time,To_time))
            self.subject_name_Entry.delete(0,'end')
            self.zoom_id_Entry.delete(0,'end')
            self.zoom_password_Entry.delete(0,'end')
            self.zoom_link_Entry.delete(0,'end')
            self.zoom_from_entry.delete(0,'end')
            self.zoom_to_entry.delete(0,'end')
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
        self.zoom_from_entry.delete(0,'end')
        self.zoom_to_entry.delete(0,'end')
        self.subject_name_Entry.insert(0,self.values[0])
        self.zoom_id_Entry.insert(0,self.values[1])
        self.zoom_password_Entry.insert(0,self.values[2])
        self.zoom_link_Entry.insert(0,self.values[3])
        self.zoom_from_entry.insert(0,self.values[4])
        self.zoom_to_entry.insert(0,self.values[5])

    def update(self):
        self.update_frame= tk.Frame(self.main_frame,bg="#ffffff")
        self.table_data.config(selectmode="browse")
        subject_name_label= tk.Label(self.update_frame,text="Subject Name : ",font="arialblack 12",bg="#ffffff")
        subject_name_label.grid(column=0,row=0,padx=(200,10),pady=10)
        self.subject_name_Entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.subject_name_Entry.grid(column=2,row=0,padx=(20,10),pady=10,ipady=3)
        self.subject_name_Entry.focus()
        reg1= self.update_frame.register(self.check_subject_field)
        self.subject_name_Entry.config(validate="key",validatecommand=(reg1,'%P'))
        zoom_id_label= tk.Label(self.update_frame,text="Zoom ID : ",bg="#ffffff",font="arialblack 12")
        zoom_id_label.grid(column=0,row=1,padx=(200,10),pady=10)
        self.zoom_id_Entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.zoom_id_Entry.grid(column=2,row=1,padx=(20,10),pady=10,ipady=3)
        reg2= self.update_frame.register(self.check_zoom_id_field)
        self.zoom_id_Entry.config(validate="key",validatecommand=(reg2,'%P'))
        zoom_password_label= tk.Label(self.update_frame,text="Zoom Password :",bg="#ffffff",font="arialblack 12")
        zoom_password_label.grid(column=0,row=2,padx=(200,10),pady=10)
        self.zoom_password_Entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.zoom_password_Entry.grid(column=2,row=2,padx=(20,10),pady=10,ipady=3)
        reg3= self.update_frame.register(self.check_zoom_password_field)
        self.zoom_password_Entry.config(validate="key",validatecommand=(reg3,'%P'))
        zoom_link_label= tk.Label(self.update_frame,text="Zoom Link :",bg="#ffffff",font="arialblack 12")
        zoom_link_label.grid(column=0,row=3,padx=(200,10),pady=10)
        self.zoom_link_Entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.zoom_link_Entry.grid(column=2,row=3,padx=(20,10),pady=10,ipady=3)
        
        zoom_timing_label = tk.Label(self.update_frame, text="Timings (hh:mm:ss)",bg="#ffffff",font="arialblack 12")
        zoom_timing_label.grid(column=3,row=0,padx=(200,10),pady=10)
        zoom_from= tk.Label(self.update_frame,text="From : ",bg="#ffffff",font="arialblack 12")
        zoom_from.grid(column=3,row=1,pady=10)
        self.zoom_from_entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.zoom_from_entry.grid(column=4,row=1,pady=10,ipady=3)
        regt= self.update_frame.register(self.check_time_field)
        self.zoom_from_entry.config(validate="key",validatecommand=(regt,'%P'))
        zoom_to= tk.Label(self.update_frame,text="To : ",bg="#ffffff",font="arialblack 12")
        zoom_to.grid(column=3,row=2,pady=10)
        self.zoom_to_entry= tk.Entry(self.update_frame,font="arialblack 12")
        self.zoom_to_entry.grid(column=4,row=2,pady=10,ipady=3)
        regtt= self.update_frame.register(self.check_time_field)
        self.zoom_to_entry.config(validate="key",validatecommand=(regtt,'%P'))

        self.retrieve_button= tk.Button(self.update_frame,text="Retrieve",command=self.extracted,bg="#ffffff",font="arialblack 15",cursor="hand2")
        self.retrieve_button.grid(column=1,row=4)
        
        self.Update_button= tk.Button(self.update_frame,text="Update",command=self.updated,state="disabled",bg="#ffffff",font="arialblack 15",cursor="hand2")
        self.Update_button.grid(column=2,row=4)
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
        self.schedule_frame= tk.Frame(self.main_frame,bg="#ffffff")
        self.mycursor.execute("SELECT pno FROM zoom")
        lec_no= self.mycursor.fetchall()
        print(lec_no)
        self.mycursor.execute("SELECT subject FROM zoom")
        subjects= self.mycursor.fetchall()
        entries= []
        row=0
        for subject,lec in zip(subjects,lec_no):
            subject_name_label= tk.Label(self.schedule_frame,text=subject,bg="#ffffff",font="arialblack 10")
            subject_name_label.grid(row=row,column=0,pady=7,padx=100)
            self.subject_seq_Entry= tk.Entry(self.schedule_frame)
            self.subject_seq_Entry.grid(row=row,column=2)
            reg3= self.schedule_frame.register(self.check_seq_field)
            self.subject_seq_Entry.config(validate="key",validatecommand=(reg3,'%P'))
            self.subject_seq_Entry.insert(0,lec)
            entries.append(self.subject_seq_Entry)
            row=row+1
        submit_button= tk.Button(self.schedule_frame,text="Submit",cursor="hand2",font="arialblack 15",command=lambda:self.insert_seq(subjects,entries))
        submit_button.grid(row=row+1,column=1,pady=10)
        return self.schedule_frame
    def GUI_window(self):
        self.main_frame= tk.Frame(self,borderwidth=6,bg="#ffffff")
        head_frame= tk.Frame(self.main_frame)
        main_heading= tk.Label(head_frame, text="Online Class Automation",font="arialblack 40 bold",bg="#2962FF",fg="white")
        main_heading.pack(fill=tk.BOTH)
        head_frame.pack(fill=tk.BOTH,pady=(10,20))

        buttons_frame= tk.Frame(self.main_frame,bg="#ffffff")
        modify_button= tk.Button(buttons_frame,text="Update",font="black 20 bold",cursor="hand2",command=lambda:self.swap_frame(self.update()))
        modify_button.grid(ipadx=40,pady=10,padx=20,row=0,column=0)
        add_button= tk.Button(buttons_frame,text= "+Add",font="black 20 bold",bg="#2deb69",cursor="hand2",command=lambda:self.swap_frame(self.insert()))
        add_button.grid(ipadx=40,pady=10,padx=20,row=0,column=1)
        delete_button= tk.Button(buttons_frame, text="Delete",bg="#ff1414",font="black 20 bold",cursor="hand2",command=lambda: self.swap_frame(self.delete()))
        delete_button.grid(ipadx=40,pady=10,padx=20,row=0,column=2)
        delete_button= tk.Button(buttons_frame, text="Schedule",font="black 20 bold",cursor="hand2",command=lambda: self.swap_frame(self.schedule()))
        delete_button.grid(ipadx=40,pady=10,padx=20,row=0,column=3)
        buttons_frame.pack(pady=(10,10),fill=tk.X)
        
        
        table_frame= tk.Frame(self.main_frame)
        table_scrollbar=tk.Scrollbar(table_frame)
        table_scrollbar.pack(side="right",fill="y")
        table_xscrollbar=tk.Scrollbar(table_frame,orient="horizontal")
        table_xscrollbar.pack(side="bottom",fill="x")
        style= tk.ttk.Style(table_frame)
        style.theme_use("clam")
        style.configure(".",font="helvetica 10",borderwidth=4,padding=5, relief="groove",rowheight=25)
        style.configure("Treeview.Heading",font="arialblack 13 bold",padding=6, relief="groove")
        self.mycursor.execute("select * from zoom")
        self.table_data = tk.ttk.Treeview(table_frame,selectmode="none",yscrollcommand= table_scrollbar.set ,xscrollcommand=table_xscrollbar.set)
        table_scrollbar.config(command=self.table_data.yview)
        table_scrollbar.config(command=self.table_data.xview)
        self.table_data["show"]="headings"
        self.table_data["columns"]= ("subject","class_id","class_password","class_link","From","To")
        self.table_data.column("subject",width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_id", width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_password", width=50,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("class_link", width=400,minwidth=50, anchor=tk.CENTER)
        self.table_data.column("From", width=50,minwidth=50, anchor=tk.CENTER)   
        self.table_data.column("To", width=50,minwidth=50, anchor=tk.CENTER)    
        self.table_data.heading("subject", text="Sub Name",anchor= tk.CENTER) 
        self.table_data.heading("class_id", text="Zoom ID",anchor= tk.CENTER) 
        self.table_data.heading("class_password", text="Zoom Password",anchor= tk.CENTER) 
        self.table_data.heading("class_link", text="Zoom Link",anchor= tk.CENTER)
        self.table_data.heading("From", text="From",anchor= tk.CENTER)
        self.table_data.heading("To", text="To",anchor= tk.CENTER)
        self.table_data.pack(fill=tk.BOTH)
        self.table_data.tag_configure("oddrow",background="#DFDFDF")
        self.table_data.tag_configure("evenrow",background="lightblue")
        i=0
        for row in self.mycursor:
            self.table_data.insert('',i,text="",values=(row[1],row[2],row[3],row[4],row[5],row[6]),tags=("evenrow",))
            i+=1
        table_frame.pack(fill="x")
        self.table_data.pack(fill=tk.BOTH)
        self.main_frame.pack(expand=True,fill=tk.BOTH)

    

if __name__ == "__main__":
    window= GUI()
    window.GUI_window()
    window.mainloop()
