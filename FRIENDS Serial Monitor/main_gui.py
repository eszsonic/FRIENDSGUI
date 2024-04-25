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
import matplotlib
matplotlib.use('TkAgg')

import numpy as np

from serialcompy import SerialCom
import serial


from datetime import datetime, timedelta
import datetime as DT

import time
from tkinter import filedialog, Tk
import pandas as pd



class Application(ttk.Frame):
    time_duration = 0
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
        self._widget_read()


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

    def _widget_read(self):
        # StatusBar
        lf_read = ttk.LabelFrame(self.master, text="Data Status Bar")
        lf_read.pack(expand=False, side="top")

        self.read_status = ttk.Label(
            master=lf_read,
            width=90,
            text="Ready",
            background="lightgray")
        self.read_status.pack(expand=False, side="left")

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

        self.btn_time = ttk.Button(
            master=lf_send,
            text="Read Time",
            command=self.send_text_btn_t,
            state="disable")
        self.btn_time.pack(expand=False, side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Set time",
            command=self.send_text_btn_s,
            state="disable")
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

        self.btn_cgp = ttk.Button(
            master=lf_send,
            text="File Conversion",
            command=self.send_text_btn_conv,
            state="enable")
        self.btn_cgp.pack(expand=False, side="left")

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

        self.btn_save = ttk.Button(
            lf_rx,
            text="Save data and generate plots",
            command=self.save_data,
            state="disable")
        self.btn_save.pack(expand=False, side="right")

        self.btn_rxexp = ttk.Button(
            lf_rx,
            text="Clear",
            command=self.clear_text,
            state="enable")
        self.btn_rxexp.pack(expand=False, side="right")

        self.instruction_label = ttk.Label(
            lf_rx,
            text="Please click 'Clear' button to clear the monitor & enable 'Read Data' button")
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
            self.btn_read.config(state="normal")
            self.btn_time.config(state="normal")
            self.btn_close.config(state="normal")
            self.btn_sdc.config(state="normal")

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
        """
        if self.serialcom.serial.in_waiting:
            received_data = self.serialcom.serial.read(self.serialcom.serial.in_waiting).decode()  # Read the received data from the serial connection
            if received_data != b'':
               self.lb_rx.insert(tk.END, received_data)

        root.after(100, self._serial_read)
        """

        buffer = b''
        num=0
        while self.serialcom.serial.is_open:
            _recv_data = self.serialcom.serial.readline()
            if _recv_data != b'':
                buffer += _recv_data
                while b'\r\n' in buffer:
                    self.read_status.config(text="Reading Data from device. Please wait ......", background="orange")
                    num=1
                    line, buffer = buffer.split(b'\r\n', 1)
                    try:
                        self.lb_rx.insert(tk.END, line.strip().decode("utf-8"))
                        # _recv_data = self.serialcom.serial_read()
                    except (TypeError, AttributeError):
                        print("Comport disconnected while reading")
            if num==1 and _recv_data == b'':
               self.read_status.config(text="Reading Data Done", background="lightgreen")
               num=0


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
        self.btn_time.config(state="disable")
        self.btn_sdc.config(state="disable")
        self.btn_read.config(state="disable")
        self.btn_yes.config(state="disable")
        self.lb_rx.config(state="disable")
        self.btn_rxexp.config(state="disable")

    def clear_text(self):
        self.lb_rx.delete(0, 'end')
        self.btn_read.config(state="normal")
        self.read_status.config(text="Ready", background="lightgray")

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

        #time.sleep(1)
        #_send_data_y = "y"
        #self.serialcom.serial.write(_send_data_y.encode("utf-8"))

        self.btn_read.config(state="disabled")
        self.btn_yes.config(state="normal")


    def send_text_btn_r(self):
        self.read_status.config(text="Reading Data from the Device. Please wait .....", background="lightgreen")
        #self.lb_rx.delete(0, 'end')
        #time.sleep(0.3)



        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode())

        _send_data_r = "r"
        self.serialcom.serial.write(_send_data_r.encode())

        # self.lb_tx.insert(tk.END, _send_data_r)
        self.btn_save.config(state="normal")
        self.btn_read.config(state="disabled")


    def save_data(self):
        self.read_status.config(text="Save Data and Generating plots", background="orange")
        current_time = DT.datetime.now()
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname:
            _fname += ".txt"
            file_name2 = _fname.split(".")[0] + "_converted.txt"
            file_name3 = _fname.split(".")[0] + "_duration.txt"


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
                        ((str(self.lb_rx.get(i))[0:4]) != "Puff") and
                        ((str(self.lb_rx.get(i))[0:5]) != "Touch") and
                        ((str(self.lb_rx.get(i))[0:5]) != "Read") and
                        ((str(self.lb_rx.get(i))[0:3]) != "Set")):
                    df2.loc[len(df2)] = [str(self.lb_rx.get(i))]
                    # f.write(str(self.lb_rx.get(i)) + "\n")
            f1.write(str(tm2) + "\n")
            f1.write(df2.to_string(index=False) + "\n")

        self.btn_erase.config(state="normal")
        self.btn_read.config(state="disabled")
        self.btn_sdc.config(state="normal")
        self.btn_save.config(state="disabled")



        def add_comma_if_words(string):
            words_to_replace = ["SET_TIME", "TOUCH_ON", "TOUCH_OFF", "PUFF_ON", "PUFF_OFF", "READ_TIME","TEMPERATURE_ON","TEMPERATURE_OFF", "UNEXPECTED_TIMESTAMP"]
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

        def seconds_to_milliseconds(seconds):
            milliseconds = float(seconds) * 1000
            return "{:.4f}".format(milliseconds)

        def format_column(value):
            value_str = str(value)
            left_aligned = value_str[:15]
            right_aligned = value_str[15:]
            return f"{left_aligned:<8}{right_aligned:>}"

        def format_time(input_time):
            try:
                # Parse the input time
                time_obj = datetime.strptime(input_time, "%H:%M:%S.%f")

                formatted_time = time_obj.strftime("%H:%M:%S.%f")[:-3]

                return formatted_time
            except ValueError:
                # Handle the case where the input time format is invalid
                return "Invalid Time Format"


        with open(file_name2, 'w') as f2:
            df=df2.copy()
            df2 = pd.DataFrame(columns=["Timestamps:"])
            def datetime_from_utc_to_local(utc_datetime):
                now_timestamp = time.time()
                offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
                return utc_datetime + offset

            f2.write(str("Local Time: " + str(current_time) + "\n"))

            prefix = [1, 2, 3, 4, 5, 6, "E", "F"]
            for index, row in df.iterrows():
                #line2= str(row)
                #line2=line2[15:31]
                line = str(row[0])
                line2 = line[-16:]
                count_before_16 = 0
                for char in line[:-16]:
                    if char.isdigit() or (char.isalpha() and char.isupper()):
                       count_before_16 += 1
                if count_before_16 == 0 and line2[0] in "123456EF":
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
                        hex_number=str(line2[4:16])
                        decimal_number = int(hex_number, 16)
                        event = "TEMPERATURE_ON" + " " + str(decimal_number)
                    elif (line2[0] == "6"):
                        hex_number = str(line2[4:16])
                        decimal_number = int(hex_number, 16)
                        event = "TEMPERATURE_OFF" + " " + str(decimal_number)
                    elif (line2[0] == "E"):
                        event = "READ_TIME" + " " + str(local_time)
                    elif (line2[0] == "F"):
                        event = "SET_TIME" + " " + str(local_time)
                    else:
                        event = "Time"
                        print("issue")
                    df2.loc[len(df2)] = [event]
                else:
                    event = "UNEXPECTED_TIMESTAMP" + " " + str(line)
                    df2.loc[len(df2)] = [event]

            df2_n = df2.copy()
            df2_new_temp = df2.copy()
            df2_n["Timestamps:"] = df2_n["Timestamps:"].apply(lambda x: add_comma_if_words(x))
            df2_n[["Event", "Information"]] = df2_n["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
            df2_n.drop("Timestamps:", axis=1, inplace=True)
            f2.write(df2_n.to_string(index=False) + "\n")

        with open(file_name3, 'w') as f3:
            #df2_new_temp = df2_new.copy()
            df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
            df2 = df2[~df2['Timestamps:'].str.startswith('UNEXPECTED')]

            df2["Timestamps:"] = df2["Timestamps:"].apply(lambda x: add_comma_if_words(x))
            df2[["Event", "Time"]] = df2["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
            df2.drop("Timestamps:", axis=1, inplace=True)
            df2["Time"] = df2['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
            df2[["Date", "Time"]] = df2["Time"].apply(lambda x: pd.Series(str(x).split(", ")))
            format_time_column(df2, "Time")
            df2["Time_subseconds"] = df2['Time'].apply(time_to_seconds_subseconds)

            #for temperature graph

            df2_new_temp["Timestamps:"] = df2_new_temp["Timestamps:"].apply(lambda x: add_comma_if_words(x))
            df2_new_temp[["Event", "Time"]] = df2_new_temp["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
            df2_new_temp = df2_new_temp[df2_new_temp['Event'] != 'READ_TIME']
            df2_new_temp = df2_new_temp[df2_new_temp['Event'] != 'SET_TIME']
            df2_new_temp.drop("Timestamps:", axis=1, inplace=True)

            df2_new_temp["Time"] = df2_new_temp['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
            df2_new_temp[["Temperature", "Time"]] = df2_new_temp["Time"].apply(lambda x: pd.Series(str(x).split(", ")))

            rows_to_delete = []
            for index, row in df2_new_temp.iterrows():

                if row['Event'] == 'UNEXPECTED_TIMESTAMP':
                    # Check previous row

                    if index > 0:
                        prev_row = df2_new_temp.loc[index - 1]
                        if prev_row['Event'] in ['PUFF_ON', 'TOUCH_ON', 'TEMPERATURE_ON']:
                            rows_to_delete.append(index - 1)

                    # Check following row
                    if index < len(df) - 1:
                        next_row = df2_new_temp.loc[index + 1]
                        if next_row['Event'] in ['PUFF_OFF', 'TOUCH_OFF', 'TEMPERATURE_OFF']:
                            rows_to_delete.append(index + 1)

                    rows_to_delete.append(index)

            df2_new_temp.drop(index=rows_to_delete, inplace=True)
            df2_new_temp = df2_new_temp.reset_index(drop=True)

            # Find the NaN values in the 'Time' column of 'TEMPERATURE_ON' row
            for index, row in df2_new_temp.iterrows():
                if (row['Event'] == 'TEMPERATURE_ON') and pd.isna(row['Time']):
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index-2, 'Time']
                if (row['Event'] == 'TEMPERATURE_OFF') and pd.isna(row['Time']):
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index-2, 'Time']


            format_time_column(df2_new_temp, "Time")
            df2_new_temp["Time_subseconds"] = df2_new_temp['Time'].apply(time_to_seconds_subseconds)
            df2_new_temp['Date'] = pd.to_datetime(df2_new_temp['Temperature'], errors='coerce')

            for index, row in df2_new_temp.iterrows():
                if (row['Event'] == 'TEMPERATURE_ON' and pd.isna(row['Date'])):
                    df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
                if (row['Event'] == 'TEMPERATURE_OFF' and pd.isna(row['Date'])):
                    df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']

            df2_new_temp['Temperature'] = df2_new_temp['Temperature'].apply(lambda x: 0 if pd.to_datetime(x, errors='coerce') is not pd.NaT else x)
            df2_new_temp['Time'] = df2_new_temp['Time'].apply(lambda x: format_time(x))
            df2_new_temp["Time_round"] = df2_new_temp['Time'].apply(round_to_nearest_second)
            df2_new_temp['Time_in_seconds'] = df2_new_temp['Time_round'].apply(convert_to_seconds)


            df2['Time'] = df2['Time'].apply(lambda x: format_time(x))

            df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"])

            duration = 0

            string1 = 'PUFF_ON'
            string2 = 'PUFF_OFF'
            string3 = 'TOUCH_ON'
            string4 = 'TOUCH_OFF'
            df2.reset_index(drop=True, inplace=True)

            for index, row in df2.iterrows():
                if index + 1 < len(df2) and row["Event"] == string3 and df2.loc[index + 1, 'Event'] == string4:
                    new_row = pd.Series({'Event': "TOUCH", 'Date': row["Date"],
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
            df_v2['Duration(ms)'] = df_v2['Duration_in_seconds'].apply(seconds_to_milliseconds)
            df_v2['Duration(ms)'] = df_v2['Duration(ms)'].astype(float).round(1)
            df_v2 = df_v2.drop('Duration_in_seconds', axis=1)

            f3.write(df_v2.to_string(index=False) + "\n")

        df2["Time_round"] = df2['Time'].apply(round_to_nearest_second)
        df2['Time_in_seconds'] = df2['Time_round'].apply(convert_to_seconds)
        #df2=df2_new.copy()
        #take the dataframe from 2nd file df2_n and find time in seconds for each event





        plot_type = self.cb_plot.get()

        if plot_type=="Stem":
            def generate_graph(df2_new_temp):
                unique_dates = df2_new_temp['Date'].unique()
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
                    date= str(date)[:10]
                    print(date)
                    total_duration = 0
                    dur_gth = 0
                    number_of_puff = 0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        """
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                            time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                        """

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})

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

                    #ax1.set_ylabel(date)
                    ax1.legend()
                    ax1.set_title("Date: "+ str(date) + " ,Total puffing time above threshold: " + str(dur_gth) + 's'+ ","+"Num of Puffs above threshold: "+str(number_of_puff))
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

                    fig.set_size_inches(17, 7)


                    markerline, stemline, baseline = ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    stemline.set_linewidth(10)
                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    ax2.legend()

                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()


                return ax1, ax3, ax2, ax4

            ax1, ax3, ax2, ax4, = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Step":
            def generate_graph(df2_new_temp):

                unique_dates = df2_new_temp['Date'].unique()
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
                    date = str(date)[:10]
                    print(date)
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        """
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                            time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                        """

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})
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
                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
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

                    fig.set_size_inches(17, 7)


                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()

                return ax1,ax3,ax2,ax4
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Line":
            def generate_graph(df2_new_temp):

                unique_dates = df2_new_temp['Date'].unique()

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
                    date = str(date)[:10]
                    print(date)
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        """
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                            time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                        """

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    #fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,gridspec_kw={'height_ratios': [1, 1, 5]})
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    option = self.cb_plot_puff.get()
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.plot(np.arange(86400), time_matrix11, color="red",
                                 label='PUFF< {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                        ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    if option == "Display puffs that exceed the threshold":
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str( dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
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


                    fig.set_size_inches(17, 7)


                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()

                return ax1, ax3, ax2, ax4
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        self.read_status.config(text="Ready", background="lightgray")




    def send_text_btn_conv(self):

        self.lb_rx.delete(0, 'end')
        time.sleep(0.3)

        #_send_data_t = "t"
        #self.serialcom.serial.write(_send_data_t.encode("utf-8"))


        def add_comma_if_words(string):
            words_to_replace = ["SET_TIME", "TOUCH_ON", "TOUCH_OFF", "PUFF_ON", "PUFF_OFF", "READ_TIME","TEMPERATURE_ON","TEMPERATURE_OFF","UNEXPECTED_TIMESTAMP"]
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

        def seconds_to_milliseconds(seconds):
            milliseconds = float(seconds) * 1000
            return "{:.4f}".format(milliseconds)

        self.read_status.config(text="Converting timestamps", background="lightgreen")
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
        prefix = [1, 2, 3, 4, 5, 6, "E", "F"]

        for index, row in df.iterrows():
            line= str(row[0])
            line2 = line[-16:]
            count_before_16 = 0
            #line2=line2[15:31]
            for char in line[:-16]:
                if char.isdigit() or (char.isalpha() and char.isupper()):
                    count_before_16 += 1
            if count_before_16 == 0 and line2[0] in "123456EF":
                timestamp_hex = line2[4:8] + line2[8:12] + line2[12:16]
                for hexstamp in timestamp_hex.split():
                    gmt_time = DT.datetime.utcfromtimestamp(
                        float(int(hexstamp, 16)) / 16 ** 4)  # UNIX hex to GMT converter
                    local_time = datetime_from_utc_to_local(gmt_time)  # GMT to local time converter
                if (line2[0] == "1"):
                    event = "PUFF_ON" + " " + str(local_time)
                elif (line2[0] == "2"):
                    event = "PUFF_OFF" + " " + str(local_time)
                elif (line2[0] == "3"):
                    event = "TOUCH_ON" + " " + str(local_time)
                elif (line2[0] == "4"):
                    event = "TOUCH_OFF" + " " + str(local_time)
                elif (line2[0] == "5"):
                    hex_number = str(line2[4:16])
                    decimal_number = int(hex_number, 16)
                    event = "TEMPERATURE_ON" + " " + str(decimal_number)
                elif (line2[0] == "6"):
                    hex_number = str(line2[4:16])
                    decimal_number = int(hex_number, 16)
                    event = "TEMPERATURE_OFF" + " " + str(decimal_number)
                elif (line2[0] == "E"):
                    event = "READ_TIME" + " " + str(local_time)
                elif (line2[0] == "F"):
                    event = "SET_TIME" + " " + str(local_time)
                else:
                    event = "Time"
                    print("issue")

                df2.loc[len(df2)] = [event]
            else:
                event = "UNEXPECTED_TIMESTAMP" + " " + str(line)
                df2.loc[len(df2)] = [event]
        #f2.write(str(tm) + "\n")
        #df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
        df2_new_temp = df2.copy()
        df3=df2.copy()

        df3["Timestamps:"] = df3["Timestamps:"].apply(lambda x: add_comma_if_words(x))
        df3[["Event", "Information"]] = df3["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
        df3.drop("Timestamps:", axis=1, inplace=True)

        df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
        df2 = df2[~df2['Timestamps:'].str.startswith('UNEXPECTED')]
        df2["Timestamps:"] = df2["Timestamps:"].apply(lambda x: add_comma_if_words(x))
        df2[["Event", "Time"]] = df2["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
        df2.drop("Timestamps:", axis=1, inplace=True)
        df2["Time"] = df2['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
        df2[["Date", "Time"]] = df2["Time"].apply(lambda x: pd.Series(str(x).split(", ")))
        format_time_column(df2, "Time")
        df2["Time_subseconds"] = df2['Time'].apply(time_to_seconds_subseconds)

        def format_time(input_time):
            try:
                # Parse the input time
                time_obj = datetime.strptime(input_time, "%H:%M:%S.%f")

                # Format the time with two digits for hours, minutes, and seconds, and six decimal points
                formatted_time = time_obj.strftime("%H:%M:%S.%f")[:-3]

                return formatted_time
            except ValueError:
                # Handle the case where the input time format is invalid
                return "Invalid Time Format"

        #For temperature graph

        #print(df2_new_temp.head())
        df2_new_temp["Timestamps:"] = df2_new_temp["Timestamps:"].apply(lambda x: add_comma_if_words(x))
        df2_new_temp[["Event", "Time"]] = df2_new_temp["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
        df2_new_temp.drop("Timestamps:", axis=1, inplace=True)
        df2_new_temp["Time"] = df2_new_temp['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
        df2_new_temp[["Temperature", "Time"]] = df2_new_temp["Time"].apply(lambda x: pd.Series(str(x).split(", ")))

        rows_to_delete = []
        for index, row in df2_new_temp.iterrows():

            if row['Event'] == 'UNEXPECTED_TIMESTAMP':
                # Check previous row

                if index > 0:
                    prev_row = df2_new_temp.loc[index - 1]
                    if prev_row['Event'] in ['PUFF_ON', 'TOUCH_ON', 'TEMPERATURE_ON']:
                        rows_to_delete.append(index - 1)

                # Check following row
                if index < len(df) - 1:
                    next_row = df2_new_temp.loc[index + 1]
                    if next_row['Event'] in ['PUFF_OFF', 'TOUCH_OFF', 'TEMPERATURE_OFF']:
                        rows_to_delete.append(index + 1)

                rows_to_delete.append(index)

        df2_new_temp.drop(index=rows_to_delete, inplace=True)
        df2_new_temp = df2_new_temp.reset_index(drop=True)

        for index, row in df2_new_temp.iterrows():
            if (row['Event'] == 'TEMPERATURE_ON') and pd.isna(row['Time']):
                if not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index - 2, 'Time']
            if (row['Event'] == 'TEMPERATURE_OFF') and pd.isna(row['Time']):
                if not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index - 2, 'Time']

        format_time_column(df2_new_temp, "Time")
        df2_new_temp["Time_subseconds"] = df2_new_temp['Time'].apply(time_to_seconds_subseconds)
        df2_new_temp['Date'] = pd.to_datetime(df2_new_temp['Temperature'], errors='coerce')
        for index, row in df2_new_temp.iterrows():
            if (row['Event'] == 'TEMPERATURE_ON' and pd.isna(row['Date'])):
                df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
            if (row['Event'] == 'TEMPERATURE_OFF' and pd.isna(row['Date'])):
                df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
        df2_new_temp['Temperature'] = df2_new_temp['Temperature'].apply(lambda x: 0 if pd.to_datetime(x, errors='coerce') is not pd.NaT else x)
        df2_new_temp['Time'] = df2_new_temp['Time'].apply(lambda x: format_time(x))
        df2_new_temp["Time_round"] = df2_new_temp['Time'].apply(round_to_nearest_second)
        df2_new_temp['Time_in_seconds'] = df2_new_temp['Time_round'].apply(convert_to_seconds)


        df2['Time'] = df2['Time'].apply(lambda x: format_time(x))
        df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"])
        duration = 0



        string1 = 'PUFF_ON'
        string2 = 'PUFF_OFF'
        string3 = 'TOUCH_ON'
        string4 = 'TOUCH_OFF'
        df2.reset_index(drop=True, inplace=True)
        for index, row in df2.iterrows():
            if index + 1 < len(df2) and row["Event"] == string3 and df2.loc[index + 1, 'Event'] == string4:
                new_row = pd.Series({'Event': "TOUCH", 'Date': row["Date"],
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
        df_v2['Duration(ms)'] = df_v2['Duration_in_seconds'].apply(seconds_to_milliseconds)
        df_v2['Duration(ms)'] = df_v2['Duration(ms)'].astype(float).round(1)
        df_v2 = df_v2.drop('Duration_in_seconds', axis=1)

        self.read_status.config(text="Save timestamps and generating plots", background="lightgreen")
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname:
            _fname = _fname.split(".")[0]+"_converted.txt"
            file_name3=_fname.split(".")[0]+"_duration.txt"



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
            def generate_graph(df2_new_temp):

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
                    date = str(date)[:10]
                    total_duration = 0
                    dur_gth = 0
                    number_of_puff = 0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})

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

                    #ax1.set_ylabel(date)
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
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

                    fig.set_size_inches(17, 7)
                    ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.set_ylim(0, 1.1)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()


                return ax1, ax3, ax2, ax4

            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Step":
            def generate_graph(df2_new_temp):

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
                    date = str(date)[:10]
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                       ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                       ax1.step(np.arange(86400), time_matrix11, where='post', color="red", label='PUFF< {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)
                       ax1.fill_between(np.arange(86400), time_matrix11, step="post", color='red', alpha=0.5)

                    if option=="Display puffs that exceed the threshold":
                        ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)

                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")

                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
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

                    fig.set_size_inches(17, 7)


                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()
                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()

                return ax1, ax3, ax2, ax4
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Line":
            def generate_graph(df2_new_temp):

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
                    #print(date)
                    date = str(date)[:10]
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)
                    time_matrix3 = np.zeros((86400,), dtype=int)
                    time_matrix31 = np.zeros((86400,), dtype=int)
                    time_matrix4 = np.zeros((86400,), dtype=int)
                    time_matrix41 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    string5 = 'TEMPERATURE_ON'
                    string6 = 'TEMPERATURE_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[index + 1, 'Event'] == string2:
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                dur_gth += duration
                                number_of_puff += 1
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[ index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        """
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                            time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                        """

                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    dur_gth = f"{dur_gth:.4f}"
                    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,gridspec_kw={'height_ratios': [1, 1, 5]})
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.plot(np.arange(86400), time_matrix11, color="red",
                                 label='PUFF< {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                        ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    if option == "Display puffs that exceed the threshold":
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    # ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
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

                    fig.set_size_inches(17, 7)

                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.legend()
                    # ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Create stem plots
                    stem3 = ax3.stem(np.arange(86400), time_matrix3, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem31 = ax3.stem(np.arange(86400), time_matrix31, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    stem4 = ax4.stem(np.arange(86400), time_matrix4, linefmt='blue', markerfmt=' ',
                                     basefmt=" ",
                                     label="Temperature ON")
                    stem41 = ax4.stem(np.arange(86400), time_matrix41, linefmt='red', markerfmt=' ',
                                      basefmt=" ",
                                      label="Temperature OFF")

                    for i, yval in enumerate(time_matrix3):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix31):
                        if yval > 0:
                            ax3.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix4):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')

                    for i, yval in enumerate(time_matrix41):
                        if yval > 0:
                            ax4.annotate(round(yval, 2), (i, yval), textcoords="offset points",
                                         xytext=(0, 5),
                                         ha='center', va='bottom', rotation='vertical')
                    """
                    bars = ax3.bar(np.arange(86400), time_matrix3,color='blue',label="Temperature ON")
                    bars1 = ax3.bar(np.arange(86400), time_matrix31,color='red',label="Temperature OFF",bottom=time_matrix3)

                    for bar, yval in zip(bars, time_matrix3):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')

                    # Add values on top of each bar in the second set, arrange text vertically above the bars
                    for bar, yval in zip(bars1, time_matrix31):
                        if yval > 0:
                            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height(), round(yval, 2),
                                     ha='center', va='bottom', rotation='vertical')
                    """

                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    min_matrix3 = min(non_zero_values3)
                    min_matrix31 = min(non_zero_values31)

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    min_matrix4 = min(non_zero_values4)
                    min_matrix41 = min(non_zero_values41)

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    plt.tight_layout()
                    plt.show()

                return ax1, ax3, ax2, ax4
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        self.read_status.config(text="Ready", background="lightgray")
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
    root.title("FRIENDS GUI")
    Application(master=root)

    root.mainloop()
