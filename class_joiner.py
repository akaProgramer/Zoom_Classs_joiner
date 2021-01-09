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
        while pyautogui.locateCenterOnScreen(pic ,grayscale= True, confidence= .5)==None:
            time.sleep(0.5)

    def lec_no(self):
        current_time = datetime.datetime.today().strftime("%H:%M:%S")
        # print(current_time)
        if current_time <= "10:30:00" and current_time >= "09:55:00":
            return 1
        elif current_time <= "11:05:00" and current_time >= "10:32:00":
            return 2
        elif current_time <= "11:40:00" and current_time >= "11:07:00":
            return 3
        elif current_time <= "12:15:00" and current_time >= "11:42:00":
            return 4
        elif current_time <= "12:50:00" and current_time >= "12:17:00":
            return 5
        else:
            return "No class for now"
    def ID_Password_Extractor(self):
        lec = self.lec_no()
        if type(lec)!= str:
            try:
                self.mydb= mysql.connector.connect(host="localhost", user="root", passwd="akash123#",database="akash")
                self.mycursor = self.mydb.cursor(buffered=True)
                self.mycursor.execute(f"SELECT * FROM zoom WHERE pno='{lec}'")
                print(lec)
                record= self.mycursor.fetchone()
                if record==None:
                    print("No class for now")
                    return
                else:
                    Id= record[2]
                    password= record[3]
                    link= record[4]
                print(record)
            except:
                print("something went wrong")
            if password!="" and Id!="":
                    self.join_in_class(Id,password)
            else:
                self.join_in_class_by_link(link)
        else:
            print(lec)

    def join_in_class_by_link(self,link):
        pyautogui.hotkey("win", "d")
        webbrowser.open_new(link)
        self.check_for_confirmation("Link_open.png")
        pyautogui.press("left")
        pyautogui.press("Enter")
    # ALL joining operatoins C:\Users\%USERPROFILE%\AppData\Roaming\Zoom\bin\Zoom.exe
    def join_in_class(self,Id,password):
        print("We are about to join a class so, please stop whatever u were doing")
        # time.sleep(5)
        pyautogui.hotkey("win", "d")
        subprocess.Popen('"%USERPROFILE%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"',shell=True)
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
    while join.is_connected() == False:
        print("wating for internet access.....")
        time.sleep(2)
    # join.join_in_class()
    # join.join_in_class_by_link()
    join.ID_Password_Extractor()

    