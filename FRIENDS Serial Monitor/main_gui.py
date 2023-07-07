import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import threading
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import AutoLocator, NullFormatter

import numpy as np

from serialcompy import SerialCom
import serial


from datetime import datetime, timedelta
import datetime as DT

import time
from tkinter import filedialog, Tk
import pandas as pd


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.serialcom = SerialCom(baudrate=115200, timeout=0.1, writemode=True)
        self.create_wedgets()

    def create_wedgets(self):
        self._wedget_statusbar()
        self._wedget_com()
        self._wedget_bps()
        self._wedget_puff()
        self._wedget_send()
        self._wedget_txrx()


    def _wedget_statusbar(self):
        # StatusBar
        lf_status = ttk.LabelFrame(self.master, text="Status Bar")
        lf_status.pack(expand=False, side="top")

        self.la_status = ttk.Label(
            master=lf_status,
            width=85,
            text="No Connection",
            background="lightgray")
        self.la_status.pack(expand=False, side="left")

    def _wedget_com(self):
        # COM list pulldown, Reload button
        lf_com = ttk.LabelFrame(self.master, text="COM")
        lf_com.pack(expand=False, side="top")

        self.cb_com = ttk.Combobox(
            master=lf_com,
            state="readonly",
            values=self.serialcom.find_comports(),
            width=69)
        self.cb_com.pack(expand=False, side="left")

        self.btn_reload = ttk.Button(
            master=lf_com,
            text="Reload",
            command=self.reload_com_btn)
        self.btn_reload.pack(expand=False, side="left")

    def _wedget_bps(self):
        # Baudrate list pulldown, Open button, Close button
        lf_bps = ttk.LabelFrame(self.master, text="Baudrate (bps)")
        lf_bps.pack(expand=False, side="top")

        self.en_bps = ttk.Entry(
            master=lf_bps,
            width=41)
        self.en_bps.insert(0, "115200")
        self.en_bps.pack(expand=False, side="left")

        self.btn_open = ttk.Button(
            master=lf_bps,
            text="Connect",
            command=self.open_com_btn)
        self.btn_open.pack(expand=False, side="left")

        self.btn_close = ttk.Button(
            master=lf_bps,
            text="Disconnect",
            command=self.close_com_btn,
            state="disable")
        self.btn_close.pack(expand=False, side="left")

    def _wedget_puff(self):
        # Baudrate list pulldown, Open button, Close button
        lf_bps = ttk.LabelFrame(self.master, text="Minimum puffing duration (s) and plot type")
        lf_bps.pack(expand=False, side="top")

        self.en_puff = ttk.Entry(
            master=lf_bps,
            width=25)
        self.en_puff.insert(0, "0.0")
        self.en_puff.pack(expand=False, side="left")

        self.cb_plot = ttk.Combobox(
            master=lf_bps,
            values=["Line","Stem","Step"],
            width=25)
        self.cb_plot.current(0)
        self.cb_plot.pack(expand=False, side="left")

        self.cb_plot_puff = ttk.Combobox(
            master=lf_bps,
            values=["Display all puffing events", "Display puffs that exceed the threshold"],
            width=35)
        self.cb_plot_puff.current(0)
        self.cb_plot_puff.pack(expand=False, side="left")

        self.btn_puff = ttk.Button(
            master=lf_bps,
            text="send",
            command=self.open_puff)
        self.btn_puff.pack(expand=False, side="left")



    def _wedget_send(self):
        # String entry
        lf_send = ttk.LabelFrame(self.master, text="Input")
        lf_send.pack(expand=False, side="top")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Read Time",
            command=self.send_text_btn_t,
            state="enable")
        self.btn_send.pack(expand=False, side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Set time",
            command=self.send_text_btn_s,
            state="enable")
        self.btn_send.pack(expand=False, side="left")

        self.btn_erase = ttk.Button(
            master=lf_send,
            text="Erase Flash",
            command=self.send_text_btn_e,
            state="disable")
        self.btn_erase.pack(expand=False, side="left")

        self.btn_sdc = ttk.Button(
            master=lf_send,
            text="Start Data Collection",
            command=self.send_text_btn_sdc,
            state="disable")
        self.btn_sdc.pack(expand=False, side="left")

        self.btn_read = ttk.Button(
            master=lf_send,
            text="Read Data",
            command=self.send_text_btn_r,
            state="disable")
        self.btn_read.pack(expand=False, side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Conversion & Generate Plots",
            command=self.send_text_btn_conv,
            state="enable")
        self.btn_send.pack(expand=False, side="left")

        self.btn_yes = ttk.Button(
            master=lf_send,
            text="Yes",
            command=self.send_text_btn_y,
            state="disable")
        self.btn_yes.pack(expand=False, side="left")

    def _wedget_txrx(self):
        # TX RX
        pw_txrx = ttk.PanedWindow(self.master, orient="horizontal")
        pw_txrx.pack(expand=False, side="top")

        ## TX
        lf_tx = ttk.LabelFrame(pw_txrx, text="TX")
        lf_tx.pack(expand=False, side="left")

        ## RX
        lf_rx = ttk.LabelFrame(pw_txrx, text="RX")
        lf_rx.pack(expand=False, side="right")

        self.lb_rx = tk.Listbox(
            lf_rx,
            height=20,
            width=110,
            state="normal")
        self.lb_rx.pack(expand=False)

        self.btn_rxexp = ttk.Button(
            lf_rx,
            text="Clear",
            command=self.clear_text,
            state="enable")
        self.btn_rxexp.pack(expand=False, side="right")

        self.instruction_label = ttk.Label(
            lf_rx,
            text="Please click 'Clear' button to enable 'Read Data' button")
        self.instruction_label.pack(expand=False, side="left")

    def reload_com_btn(self):
        self.cb_com.config(values=self.serialcom.find_comports())

    def open_com_btn(self):
        _device = self.serialcom.devices[self.cb_com.current()].device
        _baudrate = self.en_bps.get()
        if not self.serialcom.register_comport(device=_device):
            print("Cannot specify the comport. Please try again.")
        elif _baudrate.isdecimal() or _baudrate == "":
            if _baudrate.isdecimal():
                self.serialcom.serial.baudrate = int(_baudrate)

            self.serialcom.serial.open()
            self.la_status.config(text="Connected", background="lightgreen")
            # self.en_send.config(state="normal")
            self.btn_send.config(state="normal")
            self.btn_close.config(state="normal")

            self.lb_rx.config(state="normal")
            self.btn_rxexp.config(state="normal")
            self.cb_com.config(state="disable")
            self.btn_reload.config(state="disable")
            self.en_bps.config(state="disable")
            self.btn_open.config(state="disable")

            self._start_serialread()

        else:
            print("Text in the baudrate entry is not a number.")

    def _start_serialread(self):
        self._th_sread = threading.Thread(target=self._serial_read)
        # self._th_sread.daemon = True
        self._th_sread.start()
        

        """
            _recv_data = self.serialcom.serial.readline()
            if _recv_data != b'':
                try: 
                    self.lb_rx.insert(tk.END, _recv_data.strip().decode("utf-8"))
                    # _recv_data = self.serialcom.serial_read()
                except (TypeError, AttributeError):
                    print("Comport disconnected while reading")
        """ 
    def _serial_read(self):
        buffer = b''
        while self.serialcom.serial.is_open:
            _recv_data = self.serialcom.serial.readline()
            if _recv_data != b'':
                buffer += _recv_data
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    try:
                        self.lb_rx.insert(tk.END, _recv_data.strip().decode("utf-8"))
                        # _recv_data = self.serialcom.serial_read()
                    except (TypeError, AttributeError):
                        print("Comport disconnected while reading")
            
   
    def open_puff(self):
        puff_duration=0
        puff_duration=self.en_puff.get()

    def close_com_btn(self):
        self.serialcom.close_comport()
        self._th_sread.join()
        self.cb_com.config(state="readonly")
        self.btn_reload.config(state="normal")
        self.en_bps.config(state="normal")
        self.btn_open.config(state="normal")
        self.la_status.config(text="Disconnected", background="lightgray")
        # self.en_send.config(state="disable")
        self.btn_send.config(state="disable")
        self.btn_close.config(state="disable")
        self.btn_erase.config(state="disable")
        self.btn_yes.config(state="disable")
        self.lb_rx.config(state="disable")
        self.btn_rxexp.config(state="disable")

    def clear_text(self):
        self.lb_rx.delete(0, 'end')
        self.btn_read.config(state="normal")

    def send_text_btn(self):
        _send_data = self.en_send.get()
        self.serialcom.serial.write(_send_data.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data)
        self.en_send.delete(0, tk.END)

    def send_text_btn_sdc(self):
        self.lb_rx.delete(0, 'end')
        current_time = DT.datetime.now()
        unix_timestamp = (DT.datetime.timestamp(current_time))
        frac, whole = math.modf(unix_timestamp)
        unix_1 = hex(int(str(whole)[0:-2]))[2:]
        unix_2 = hex(int(str(frac)[2:]))[2:]

        _send_data_sdc2 = "s" + str(unix_1) + str(unix_2)
        self.serialcom.serial.write(_send_data_sdc2.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_sdc2[0:13])

        time.sleep(1)
        _send_data_sdc1 = "e"
        self.serialcom.serial.write(_send_data_sdc1.encode("utf-8"))

        time.sleep(1)
        _send_data_y = "y"
        self.serialcom.serial.write(_send_data_y.encode("utf-8"))

        self.btn_read.config(state="disabled")

    def send_text_btn_r(self):

        #self.lb_rx.delete(0, 'end')
        #time.sleep(0.3)

        current_time = DT.datetime.now()

        _send_data_r = "r"
        self.serialcom.serial.write(_send_data_r.encode("utf-8"))

        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode("utf-8"))

        # self.lb_tx.insert(tk.END, _send_data_r)

        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname:
            _fname += ".txt"



        with open(_fname, 'w') as f1:
            df2 = pd.DataFrame(columns=["Timestamps:"])

            f1.write(str("Local Time: " + str(current_time) + "\n"))

            for i in range(self.lb_rx.size()):
                if ((str(self.lb_rx.get(i))[0:8]) == "Internal"):
                    tm2 = self.lb_rx.get(i)[0:40]

                # if (str(self.lb_rx.get(i))[0:8]) == "Internal":
                # f.write(str(self.lb_rx.get(i)) + "\n")

                if (((str(self.lb_rx.get(i))[0:5]) != "Input") and
                        ((str(self.lb_rx.get(i))[0:7]) != "Erasing") and
                        ((str(self.lb_rx.get(i))[0:8]) != "Finished") and
                        ((str(self.lb_rx.get(i))[0:5]) != "Erase") and
                        ((str(self.lb_rx.get(i))[0:6]) != "Number") and
                        ((str(self.lb_rx.get(i))[0:11]) != "Timestamps:") and
                        ((str(self.lb_rx.get(i))[0:8]) != "Internal") and
                        ((str(self.lb_rx.get(i))[0:3]) != "Set")):
                    df2.loc[len(df2)] = [str(self.lb_rx.get(i))]
                    # f.write(str(self.lb_rx.get(i)) + "\n")
            f1.write(str(tm2) + "\n")
            f1.write(df2.to_string(index=False) + "\n")
        
        self.btn_erase.config(state="normal")
        self.btn_read.config(state="disabled")
        self.btn_sdc.config(state="normal")


    def send_text_btn_conv(self):

        self.lb_rx.delete(0, 'end')
        time.sleep(0.3)

        #_send_data_t = "t"
        #self.serialcom.serial.write(_send_data_t.encode("utf-8"))
        
        
        def add_comma_if_words(string):
            words_to_replace = ["SET_TIME", "TOUCH_ON", "TOUCH_OFF", "PUFF_ON", "PUFF_OFF", "READ_TIME"]
            for word in words_to_replace:
                string = string.replace(word, f"{word},")
            return string

        def format_time_column(df, column_name):
            # Convert the column to string
            df[column_name] = df[column_name].astype(str)

            # Split the column into hours, minutes, seconds, and milliseconds
            time_parts = df[column_name].str.split(':', expand=True)
            hours = time_parts[0].astype(int)
            minutes = time_parts[1].astype(int)
            seconds = time_parts[2].astype(float).round(10).astype(str)

            # Format the seconds column
            seconds = seconds.apply(lambda s: s if '.' in s else s + '.00')

            # Combine the formatted parts into a new column
            df[column_name] = hours.map("{:02d}".format) + ':' + \
                              minutes.map("{:02d}".format) + ':' + \
                              seconds
            return df

        def time_to_seconds_subseconds(time_str):
            # Convert the time string to a datetime object
            time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")

            # Extract the hours, minutes, seconds, and microseconds
            hours = time_obj.hour
            minutes = time_obj.minute
            seconds = time_obj.second
            microseconds = time_obj.microsecond

            # Calculate the total seconds including subseconds
            total_seconds = (hours * 3600) + (minutes * 60) + seconds + (microseconds / 1e6)

            return total_seconds

        def round_to_nearest_second(time_str):
            # Parse the input time string to a datetime object
            time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")

            # Calculate the microsecond fraction and the rounded microsecond value
            microsecond_fraction = time_obj.microsecond / 1000000.0
            rounded_microsecond = round(microsecond_fraction)

            # Add the rounded microsecond value to the original time
            rounded_time = time_obj + timedelta(microseconds=rounded_microsecond * 1000000)

            # Format the rounded time as a string
            rounded_time_str = rounded_time.strftime("%H:%M:%S")

            return rounded_time_str

        def convert_to_seconds(time_string):
            time_parts = time_string.split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        
        
        
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        df = pd.read_csv(file_path)
        df2 = pd.DataFrame(columns=["Timestamps:"])

        def datetime_from_utc_to_local(utc_datetime):
            now_timestamp = time.time()
            offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
            return utc_datetime + offset
        
        df.columns=["Timestamps:"]
        df = df.drop(df.index[:2])
        df = df.reset_index(drop=True)
        for index, row in df.iterrows():
            line2= str(row)
            line2=line2[15:31]
            timestamp_hex = line2[4:8] + line2[8:12] + line2[12:16]
            
            for hexstamp in timestamp_hex.split():
                gmt_time = DT.datetime.utcfromtimestamp(float(int(hexstamp, 16)) / 16 ** 4)  # UNIX hex to GMT converter
                local_time = datetime_from_utc_to_local(gmt_time)  # GMT to local time converter
                    # Event separation
            if (line2[0] == "1"):
                event = "PUFF_ON" + " " + str(local_time)
            elif (line2[0] == "2"):
                event = "PUFF_OFF" + " " + str(local_time)
            elif (line2[0] == "3"):
                event = "TOUCH_ON" + " " + str(local_time)
            elif (line2[0] == "4"):
                event = "TOUCH_OFF" + " " + str(local_time)
            elif (line2[0] == "5"):
                event = "TEMPERATURE_ON" + " " + str(local_time)
            elif (line2[0] == "6"):
                event = "TEMPERATURE_OFF" + " " + str(local_time)
            elif (line2[0] == "E"):
                event = "READ_TIME" + " " + str(local_time)
            elif (line2[0] == "F"):
                event = "SET_TIME" + " " + str(local_time)
            else:
                event = "Time"
                print("issue")

            df2.loc[len(df2)] = [event]
        #f2.write(str(tm) + "\n")
        
        df3=df2.copy()
        
        df2["Timestamps:"] = df2["Timestamps:"].apply(lambda x: add_comma_if_words(x))
        df2[["Event", "Time"]] = df2["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
        df2.drop("Timestamps:", axis=1, inplace=True)
        df2["Time"] = df2['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
        df2[["Date", "Time"]] = df2["Time"].apply(lambda x: pd.Series(str(x).split(", ")))
        format_time_column(df2, "Time")
        df2["Time_subseconds"] = df2['Time'].apply(time_to_seconds_subseconds)
        df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"])

        duration = 0

        string1 = 'PUFF_ON'
        string2 = 'PUFF_OFF'
        string3 = 'TOUCH_ON'
        string4 = 'TOUCH_OFF'

        for index, row in df2.iterrows():
            if index + 1 < len(df2) and row["Event"] == string3 and df2.loc[index + 1, 'Event'] == string4:
                new_row = pd.Series({'Event': "Touch", 'Date': row["Date"],
                                        'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                        'Duration_in_seconds': str(
                                            df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                df_v2.loc[df_v2.index.max() + 1] = new_row

            if index + 1 < len(df2) and row["Event"] == string1 and df2.loc[index + 1, 'Event'] == string2:
                new_row = pd.Series({'Event': "PUFF", 'Date': row["Date"],
                                        'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                        'Duration_in_seconds': str(
                                            df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                df_v2.loc[df_v2.index.max() + 1] = new_row

        df_v2 = df_v2.iloc[1:].reset_index(drop=True)
    
        self.lb_rx.insert(tk.END, "Conversion is Done. After saving the converted files, plot generation will be started")
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])
        if _fname:
            _fname = file_path.split(".")[0]+"_converted.txt"
            file_name3=file_path.split(".")[0]+"_duration.txt"
        current_time = DT.datetime.now()
        
        with open(_fname, 'w') as f2:
            for i in range(self.lb_rx.size()):
                if ((str(self.lb_rx.get(i))[0:8]) == "Internal"):
                    tm2 = self.lb_rx.get(i)[0:40]
            #f2.write(str(tm2) + "\n")
            f2.write(str("Local Time: " + str(current_time) + "\n"))
            f2.write(df3.to_string(index=False) + "\n")

        with open(file_name3, 'w') as f3:
            f3.write(df_v2.to_string(index=False) + "\n")        
        
        
        df2["Time_round"] = df2['Time'].apply(round_to_nearest_second)
        df2['Time_in_seconds'] = df2['Time_round'].apply(convert_to_seconds)
        plot_type=self.cb_plot.get()
        if plot_type=="Stem":
            def generate_graph(df2):

                unique_dates = df2['Date'].unique()
                """
                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                """
                x_ticks = [0, 1800, 3600, 5400, 7200, 9000, 10800, 12600, 14400, 16200, 18000, 19800, 21600, 23400,
                           25200, 27000, 28800, 30600, 32400, 34200,
                           36000, 37800, 39600, 41400, 43200, 45000, 46800, 48600, 50400, 52200, 54000, 55800, 57600,
                           59400, 61200, 63000, 64800, 66600, 68400, 70200, 72000, 73800, 75600, 77400, 79200, 81000,
                           82800, 84600, 86400, 86460]
                x_labels = ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30",
                            "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
                            "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                            "20:00", "20:30",
                            "21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "24:00", "24:01"]
                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    dur_gth = 0
                    number_of_puff = 0
                    # Get the rows with the current date
                    rows = df2[df2['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2) and row['Event'] == string1 and df2.loc[index + 1, 'Event'] == string2:
                            duration = df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff+=1
                                start_index = row["Time_in_seconds"]
                                end_index = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2) and row['Event'] == string3 and df2.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ', basefmt=' ',
                                                              linefmt='g', label='PUFF> {}'.format(puff_duration+"s"))
                        stemline.set_linewidth(10)
                        # ax1.bar(np.arange(86400), time_matrix1, align='center', width=1, color='red', label='Puff')
                        # ax1.plot(np.arange(86400), time_matrix1, linewidth=1, color='red', label='Puff')
                        ax1.stem(np.arange(86400), time_matrix11, markerfmt=' ',basefmt=' ', linefmt='r', label='PUFF< {}'.format(puff_duration+"s"))

                    if option == "Display puffs that exceed the threshold":
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ',
                                                                  basefmt=' ',
                                                                  linefmt='g',
                                                                  label='PUFF> {}'.format(puff_duration + "s"))
                        stemline.set_linewidth(10)

                    ax1.set_ylabel(date)
                    ax1.legend()
                    ax1.set_title("Total puffing time above threshold: " + str(dur_gth) + 's'+ ","+"Num of Puffs above threshold: "+str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    minor_ticks = []
                    minor_labels = []
                    for i in range(len(x_ticks) - 1):
                        start_tick = x_ticks[i]
                        end_tick = x_ticks[i + 1]
                        for tick in range(start_tick, end_tick, 300):
                            minor_ticks.append(tick)
                            minutes = tick // 60
                            hours = minutes // 60
                            minutes %= 60
                            minor_labels.append(f"{hours:02d}:{minutes:02d}")
                    plt.xticks(x_ticks, x_labels)
                    # plt.minorticks_on()
                    plt.xticks(minor_ticks, rotation=90)
                    plt.tick_params(axis='x', which="both", width=1, length=4)

                    fig.set_size_inches(17, 3)


                    ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    ax2.legend()
                    plt.tight_layout()
                    # plt.show()


                return ax1, ax2

            ax1, ax2 = generate_graph(df2=df2)
            self.lb_rx.insert(tk.END, "Plot generation Done")
            plt.show()

        if plot_type == "Step":
            def generate_graph(df2):

                unique_dates = df2['Date'].unique()
                """
                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                """
                x_ticks = [0, 1800, 3600, 5400, 7200, 9000, 10800, 12600, 14400, 16200, 18000, 19800, 21600, 23400,
                           25200, 27000, 28800, 30600, 32400, 34200,
                           36000, 37800, 39600, 41400, 43200, 45000, 46800, 48600, 50400, 52200, 54000, 55800, 57600,
                           59400, 61200, 63000, 64800, 66600, 68400, 70200, 72000, 73800, 75600, 77400, 79200, 81000,
                           82800, 84600, 86400, 86460]
                x_labels = ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30",
                            "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
                            "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                            "20:00", "20:30",
                            "21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "24:00", "24:01"]
                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2[df2['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2) and row['Event'] == string1 and df2.loc[index + 1, 'Event'] == string2:
                            duration = df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff+=1
                                start_index = row["Time_in_seconds"]
                                end_index = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2) and row['Event'] == string3 and df2.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                       ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                       ax1.step(np.arange(86400), time_matrix11, where='post', color="red", label='PUFF< {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)
                       ax1.fill_between(np.arange(86400), time_matrix11, step="post", color='red', alpha=0.5)

                    if option=="Display puffs that exceed the threshold":
                        ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)

                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.legend()
                    ax1.set_ylabel(date)
                    ax1.set_title("Total puffing time above threshold: " + str(dur_gth) + 's'+ ","+" Num of Puffs above threshold: "+str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    minor_ticks = []
                    minor_labels = []
                    for i in range(len(x_ticks) - 1):
                        start_tick = x_ticks[i]
                        end_tick = x_ticks[i + 1]
                        for tick in range(start_tick, end_tick, 300):
                            minor_ticks.append(tick)
                            minutes = tick // 60
                            hours = minutes // 60
                            minutes %= 60
                            minor_labels.append(f"{hours:02d}:{minutes:02d}")
                    plt.xticks(x_ticks, x_labels)
                    # plt.minorticks_on()
                    plt.xticks(minor_ticks, rotation=90)
                    plt.tick_params(axis='x', which="both", width=1, length=4)

                    fig.set_size_inches(17, 3)


                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                return ax1, ax2
            ax1, ax2 = generate_graph(df2=df2)
            self.lb_rx.insert(tk.END, "Plot generation Done")
            plt.show()

        if plot_type == "Line":
            def generate_graph(df2):

                unique_dates = df2['Date'].unique()
                """
                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                """

                x_ticks = [0,1800, 3600,5400,7200,9000,10800,12600,14400,16200,18000,19800,21600,23400,25200,27000,28800,30600,32400,34200,
                           36000,37800,39600,41400,43200,45000,46800,48600,50400,52200,54000,55800,57600,59400,61200,63000,64800,66600,68400,70200,72000,73800,75600,77400,79200,81000,82800,84600,86400,86460]
                x_labels = ["00:00","00:30", "01:00","01:30", "02:00","02:30","03:00","03:30","04:00","04:30", "05:00","05:30", "06:00", "06:30","07:00","07:30", "08:00","08:30","09:00","09:30",
                            "10:00","10:30","11:00","11:30", "12:00","12:30","13:00", "13:30", "14:00","14:30", "15:00","15:30", "16:00","16:30" ,"17:00","17:30", "18:00","18:30", "19:00","19:30", "20:00","20:30",
                            "21:00","21:30","22:00","22:30", "23:00","23:30","24:00","24:01"]

                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2[df2['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2) and row['Event'] == string1 and df2.loc[index + 1, 'Event'] == string2:
                            duration = df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff+=1
                                start_index = row["Time_in_seconds"]
                                end_index = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2) and row['Event'] == string3 and df2.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
                    option = self.cb_plot_puff.get()
                    if option=="Display all puffing events":
                       ax1.plot(np.arange(86400), time_matrix1, color="green", label='PUFF> {}'.format(puff_duration + "s"))
                       ax1.plot(np.arange(86400), time_matrix11, color="red", label='PUFF< {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                       ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    if option=="Display puffs that exceed the threshold":
                       ax1.plot(np.arange(86400), time_matrix1, color="green",label='PUFF> {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.set_ylabel(date)
                    ax1.set_title("Total puffing time above threshold: " + str(dur_gth) + 's'+ ","+" Num of Puffs above threshold: "+str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    minor_ticks = []
                    minor_labels = []
                    for i in range(len(x_ticks) - 1):
                        start_tick = x_ticks[i]
                        end_tick = x_ticks[i + 1]
                        for tick in range(start_tick, end_tick, 300):
                            minor_ticks.append(tick)
                            minutes = tick // 60
                            hours = minutes // 60
                            minutes %= 60
                            minor_labels.append(f"{hours:02d}:{minutes:02d}")
                    plt.xticks(x_ticks, x_labels)
                    #plt.minorticks_on()
                    plt.xticks(minor_ticks, rotation=90)
                    plt.tick_params(axis='x', which="both", width=1, length=4)


                    fig.set_size_inches(17, 3)


                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.legend()
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                return ax1, ax2
            ax1, ax2 = generate_graph(df2=df2)
            self.lb_rx.insert(tk.END, "Plot generation Done")
            plt.show()

        self.btn_read.config(state="disabled")

    def send_text_btn_e(self):
        _send_data_e = "e"
        self.serialcom.serial.write(_send_data_e.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_e)
        self.btn_yes.config(state="normal")
        self.btn_read.config(state="disabled")

    def send_text_btn_y(self):
        _send_data_y = "y"
        self.serialcom.serial.write(_send_data_y.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_y)
        self.btn_read.config(state="disabled")

    def send_text_btn_s(self):
        current_time = DT.datetime.now()
        unix_timestamp = (DT.datetime.timestamp(current_time))
        frac, whole = math.modf(unix_timestamp)
        unix_1 = hex(int(str(whole)[0:-2]))[2:]
        unix_2 = hex(int(str(frac)[2:]))[2:]
        _send_data_s = "s" + str(unix_1) + str(unix_2)
        self.serialcom.serial.write(_send_data_s.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_s)
        self.btn_read.config(state="disabled")

    def send_text_btn_t(self):
        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_t)
        self.btn_read.config(state="disabled")




if __name__ == "__main__":
    global t2
    root = tk.Tk()
    root.title("FRIENDS Serial Communication")
    Application(master=root)

    root.mainloop()
