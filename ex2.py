import logging
import platform
import subprocess
from threading import Thread
from time import sleep
from last_mo import *
import psutil
import chose_date


class monitor:

    def __init__(self):
        self.runServ = []  # services running
        self.stpServ = []  # services stopped
        self.runServ2 = []  # services running
        self.stpServ2 = []  # services stopped
        self.servList = []
        self.servList2 = []
        self.time_int = 0
        self.logger1 = logging.getLogger('serviceList')
        self.logger2 = logging.getLogger('Status_Log.txt')
        self.firstloop = True
        self.bol = False
        self. my_os = platform.system()

    def set_logger(self):
        self.logger1.setLevel(level=20)
        self.logger2.setLevel(level=20)
        fh1 = logging.FileHandler('serviceList')
        fh2 = logging.FileHandler('Status_Log.txt')
        ch2 = logging.StreamHandler()                                                               # the lines in logger2 wll print to the screen
        formatter = logging.Formatter('%(asctime)s ~ %(message)s', datefmt='%d-%m-%Y-%H-%M-%S')     # time format that print to the log file with the message
        fh1.setFormatter(formatter)
        fh2.setFormatter(formatter)
        ch2.setFormatter(formatter)
        self.logger1.addHandler(fh1)
        self.logger2.addHandler(fh2)
        self.logger2.addHandler(ch2)
        return True

    def monitor(self):
        if self.my_os == "Linux":
            # print(" My OS is Linux!")
            pythonServices = subprocess.check_output('service --status-all', shell=True).decode()
            self.servList = pythonServices.split('\n')
            # first running, is statuse is running, we append the service to the runServ list and to the logger1 file
            # first running, is statuse is stopped, we append the service to the stpServ list
            if self.firstloop:
                for i in range(len(self.servList)):
                    if '[ + ]' in self.servList[i]:
                        self.runServ.append(self.servList[i][7:])
                        self.logger1.info(self.servList[i][7:])
                    elif '[ - ]' in self.servList[i]:
                        self.stpServ.append(self.servList[i][7:])
                self.firstloop = False
            # this happend after the first loop
            else:
                for i in range(len(self.servList)):
                    if '[ + ]' in self.servList[i]:
                        self.runServ2.append(self.servList[i][7:])
                        self.logger1.info(self.servList[i][7:])
                    elif '[ - ]' in self.servList[i]:
                        self.stpServ2.append(self.servList[i][7:])
                for i in range(len(self.servList)):
                    if self.servList[i][7:] in self.stpServ and self.servList[i][7:] in self.runServ2:  # fasfadgadgag
                        self.logger2.info(f"New service: {self.servList[i][7:]}")
                    elif self.servList[i][7:] in self.runServ and self.servList[i][7:] in self.stpServ2:  # fasfadgadgag
                        self.logger2.info(f"Service stopped: {self.servList[i][7:]}")
                # We clear the previous lists and update them with the current lists
                self.runServ.clear()
                self.runServ = self.runServ2.copy()
                self.runServ2.clear()
                self.stpServ.clear()
                self.stpServ = self.stpServ2.copy()
                self.stpServ2.clear()
            # we clear the service lists before we start another loop
            self.servList.clear()
            # servList = servList2.copy()
            # servList2.clear()
            sleep(self.time_int)
        elif self.my_os == "Windows":

            # while True:
            s = psutil.win_service_iter()
            # in this proc_name contain the name and display_name of current service.
            # in this proc_status contain the statuse and the name and display_name of current service.
            for i in s:
                proc_name = {"name": i.name(), "display name": i.display_name()}
                proc_status = {"status": i.status(), "name": i.name(), "display name": i.display_name()}
                self.servList.append(proc_name)
                self.servList2.append(proc_status)
            # first running, is statuse is running, we append the service to the runServ list and to the logger1 file
            # first running, is statuse is stopped, we append the service to the stpServ list
            if self.firstloop:
                # print(" My OS is Windows!")

                for i in range(len(self.servList2)):
                    if self.servList2[i]['status'] == 'running':
                        self.runServ.append(self.servList[i])
                        self.logger1.info(self.servList[i])
                    if self.servList2[i]['status'] == 'stopped':
                        self.stpServ.append(self.servList[i])
                self.firstloop = False
            # this happend after the first loop
            else:
                for i in range(len(self.servList2)):
                    if self.servList2[i]['status'] == 'running':
                        self.runServ2.append(self.servList[i])
                        self.logger1.info(self.servList[i])
                    if self.servList2[i]['status'] == 'stopped':
                        self.stpServ2.append(self.servList[i])
                for i in range(len(self.servList2)):
                    if self.servList2[i]['status'] == 'running' and self.servList[i] in self.stpServ:
                        self.logger2.info(f"New service: {self.servList[i]}")
                    elif self.servList2[i]['status'] == 'stopped' and self.servList[i] in self.runServ:
                        self.logger2.info(f"Service stopped: {self.servList[i]}")
                # We clear the previous lists and update them with the current lists
                self.runServ.clear()
                self.runServ = self.runServ2.copy()
                self.runServ2.clear()
                self.stpServ.clear()
                self.stpServ = self.stpServ2.copy()
                self.stpServ2.clear()
            # we clear the service lists before we start another loop
            self.servList.clear()
            self.servList2.clear()

            sleep(self.time_int)
        else:
            print("This monitor isn't support your OS")

    def manual(self):
        t1 = str(input("Choose the first date in this format -  DD-MM-YYYY-HH-MM-SS"))
        GB = chose_date.time(t1)
        while not GB:
            print("you entered bad input")
            t1 = str(input("Choose the first date in this format -  DD-MM-YYYY-HH-MM-SS"))
            GB = chose_date.time(t1)
        list1 = []
        with open('serviceList', 'r') as CD:
            lines = CD.readlines()
        testDate = ""
        date, Name = lines[-1].split('~')
        if date < t1:
            testDate = date
        for line in lines:
            date, Name = line.split('~')
            if date < t1 and testDate == "":
                pass
            elif date >= t1 and testDate == "":
                testDate = date
                list1.append(Name)
            elif date == testDate:
                list1.append(Name)
        t2 = str(input("Choose the second date in this format -  DD-MM-YYYY-HH-MM-SS"))
        GB = chose_date.time(t2)
        while not GB:
            print("you entered bad input")
            t2 = str(input("Choose the second date in this format -  DD-MM-YYYY-HH-MM-SS"))
        list2 = []
        testDate = ""
        date, Name = lines[-1].split('~')
        if date < t2:
            testDate = date
        for line in lines:
            date, Name = line.split('~')
            if date < t2 and testDate == "":
                pass
            elif date >= t2 and testDate == "":
                testDate = date
                list2.append(Name)
            elif date == testDate:
                list2.append(Name)
        if list1 == list2:
            print(f"There is no changes between {t1} and {t2}")
        elif t1 < t2:
            print(f"Changes between {t1} and {t2}:\n")
            self.list_compare(list1, list2)
        else:
            print(f"Changes between {t2} and {t1}:\n")
            self.list_compare(list2, list1)

    def list_compare(self, list1, list2):
        for ser in range(len(list1)):
            if list1[ser] not in list2:
                print(f"Service stopped - {list1[ser]}")
        for ser in range(len(list2)):
            if list2[ser] not in list1:
                print(f"New Service - {list2[ser]}")

    def ui(self):
        menu = "~~Welcome to the Service Monitor Tool.~~\n ~For manual mode type 'manual'.\n"\
               " ~For monitor mode type 'monitor'.\n ~For Exit type 'Ex'.\n ~For this menu type 'MENU'."
        print(menu)
        while True:
            if not self.bol:
                mode = input("Enter the mode you want to oprate:")
                if mode == "monitor":
                    self.time_int=0
                    scan_time = input(
                        "How often do you want the program to sample data? Enter numbers of seconds only.")
                    try:
                        self.time_int = int(scan_time)
                    except:
                        print("bad input")
                    while self.time_int <= 0:
                        scan_time = input(
                            "How often do you want the program to sample data? Enter numbers of seconds only.")
                        try:
                            self.time_int = int(scan_time)
                        except:
                            print("bad input")
                    self.bol = True
                if mode == "manual":
                    self.bol = False
                    self.manual()
                if mode == "MENU":
                    print(menu)
                if mode == "Ex":
                    break
            else:
                mode = input("to exit from monitor press any bottum")
                self.bol = False


if __name__ == '__main__':
    if main_changes():
        my_monitor = monitor()
        my_monitor.set_logger()
        Thread(target=my_monitor.ui).start()
        while True:
            if my_monitor.bol:
                my_monitor.monitor()