import webbrowser
import subprocess
import pyautogui
import time
import psutil
import datetime
import socket
import mysql.connector 


class joiner:
    def __init__(self):
        self.current_time = datetime.datetime.today().strftime("%H:%M:%S")
    #checks if there is internet connection or not
    def is_connected(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False
        
    #Confirmation
    def check_for_confirmation(self,pic):
        while pyautogui.locateCenterOnScreen(pic ,grayscale= True, confidence= .6)==None:
            print(pyautogui.locateCenterOnScreen(pic ,grayscale= True, confidence= .5))
            time.sleep(0.5)

    def lec_no(self):
        lec=0
        current_time = datetime.datetime.today().strftime("%H:%M:%S")
        self.mydb= mysql.connector.connect(host="localhost", user="root", passwd="akash123#",database="akash")
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute(f"SELECT from_time FROM zoom")
        from_times= self.mycursor.fetchall()
        self.mycursor.execute(f"SELECT to_time FROM zoom")
        to_times= self.mycursor.fetchall()
        self.mycursor.execute(f"SELECT sno FROM zoom")
        periods= self.mycursor.fetchall()
        for period,from_time,to_time in zip(periods,from_times,to_times):
            if from_time[0] <= current_time and to_time[0] >= current_time:
                return period[0]
        return("no lecture for now")
    def ID_Password_Extractor(self):
        lec = self.lec_no()
        if type(lec)!= str:
            try:
                self.mydb= mysql.connector.connect(host="localhost", user="root", passwd="akash123#",database="akash")
                self.mycursor = self.mydb.cursor(buffered=True)
                self.mycursor.execute(f"SELECT * FROM zoom WHERE sno='{lec}'")
                print(lec)
                record= self.mycursor.fetchone()
                if record==None:
                    print("No class for now")
                    input()
                    return
                else:
                    Id= record[2]
                    password= record[3]
                    link= record[4]
            except:
                print("something went wrong")
                input()
            if password!="" and Id!="":
                self.join_in_class(Id,password)
            else:
                self.join_in_class_by_link(link)
        else:
            print(lec)
            input()

    def join_in_class_by_link(self,link):
        pyautogui.hotkey("win", "d")
        webbrowser.open_new(link)
        self.check_for_confirmation("Link_open.png")
        pyautogui.press("left")
        pyautogui.press("Enter")
    def join_in_class(self,Id,password):
        print("We are about to join a class so, please stop whatever u were doing")
        time.sleep(5)
        pyautogui.hotkey("win", "d")
        try:
            subprocess.Popen('"%USERPROFILE%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"',shell=True)
        except:
            print("please Install zoom in your computer")
            input()
            exit()
        while True:
            if pyautogui.locateCenterOnScreen("zoom_sign_in.png",grayscale= True, confidence= .5)!= None:
                break
            elif pyautogui.locateCenterOnScreen("zoom_sign_in_2.png",grayscale= True, confidence= .5)!= None:
                break
            else:
                time.sleep(0.5)
        join_button= pyautogui.locateCenterOnScreen("join_button.png",grayscale= True, confidence= .5)
        if join_button== None:
            join_button= pyautogui.locateCenterOnScreen("join_button_2.png",grayscale= True, confidence= .5)
        pyautogui.moveTo(join_button)
        pyautogui.click()
        self.check_for_confirmation("join_meeting.png")
        pyautogui.typewrite(Id)
        pyautogui.press("Enter")
        self.check_for_confirmation("passcode.png")
        pyautogui.typewrite(password)
        pyautogui.press("Enter")


if __name__ == "__main__":
    join = joiner()
    # while join.is_connected() == False:
    #     print("wating for internet access.....")
    #     time.sleep(2)
    join.ID_Password_Extractor()

    