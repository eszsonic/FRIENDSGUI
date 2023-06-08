import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import threading
import math
import matplotlib.pyplot as plt
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
        self.cb_com.current(0)
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
            width=36)
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
            values=["Stem","Step","Line"],
            width=25)
        self.cb_plot.current(0)
        self.cb_plot.pack(expand=False, side="left")

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

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Start Data Collection",
            command=self.send_text_btn_sdc,
            state="enable")
        self.btn_send.pack(expand=False, side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Read Data",
            command=self.send_text_btn_r,
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
            width=90,
            state="normal")
        self.lb_rx.pack(expand=False)

        self.btn_rxexp = ttk.Button(
            lf_rx,
            text="Clear",
            command=self.clear_text,
            state="enable")
        self.btn_rxexp.pack(expand=False, side="right")


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

    def _serial_read(self):
        while self.serialcom.serial.is_open:
            try:
                _recv_data = self.serialcom.serial.readline()
                if _recv_data != b'':
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

    def send_text_btn(self):
        _send_data = self.en_send.get()
        self.serialcom.serial.write(_send_data.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data)
        self.en_send.delete(0, tk.END)

    def send_text_btn_sdc(self):
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

    def send_text_btn_r(self):

        self.lb_rx.delete(0, 'end')
        time.sleep(0.3)

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

        current_time = DT.datetime.now()

        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode("utf-8"))

        time.sleep(1)

        _send_data_r = "r"
        self.serialcom.serial.write(_send_data_r.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_r)

        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname:
            _fname += ".txt"
            # file_name1 = _fname.split("/")[-1]
            file_name2 = _fname.split(".")[0] + "_converted.txt"
            file_name3 = _fname.split(".")[0] + "_duration.txt"
            # file_name1.split(".")[0]

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

        time.sleep(0.4)
        # if _fname_c:
        # _fname_c += "_converted.txt"
        with open(file_name2, 'w') as f2:
            df = pd.DataFrame(columns=["Timestamps:"])

            def datetime_from_utc_to_local(utc_datetime):
                now_timestamp = time.time()
                offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
                return utc_datetime + offset

            f2.write(str("Local Time: " + str(current_time) + "\n"))

            for i in range(self.lb_rx.size()):

                if ((str(self.lb_rx.get(i))[0:8]) == "Internal"):
                    tm = self.lb_rx.get(i)[0:40]
                    # f.write(str(self.lb_rx.get(i)) + "\n")

                if (((str(self.lb_rx.get(i))[0:5]) != "Input") and
                        ((str(self.lb_rx.get(i))[0:7]) != "Erasing") and
                        ((str(self.lb_rx.get(i))[0:11]) != "Timestamps:") and
                        ((str(self.lb_rx.get(i))[0:8]) != "Finished") and
                        ((str(self.lb_rx.get(i))[0:5]) != "Erase") and
                        ((str(self.lb_rx.get(i))[0:6]) != "Number") and
                        ((str(self.lb_rx.get(i))[0:3]) != "Set") and
                        ((str(self.lb_rx.get(i))[0:8]) != "Internal")):

                    line2 = str(self.lb_rx.get(i))
                    timestamp_hex = line2[4:8] + line2[8:12] + line2[12:16]  # formatting
                    # line2 = line4.rjust(30, '2')
                    # timestamp_hex = line2[0:4] + line2[12:16] + line2[4:8]  # formatting

                    for hexstamp in timestamp_hex.split():
                        gmt_time = DT.datetime.utcfromtimestamp(
                            float(int(hexstamp, 16)) / 16 ** 4)  # UNIX hex to GMT converter
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

                    df.loc[len(df)] = [event]
            f2.write(str(tm) + "\n")
            f2.write(df.to_string(index=False) + "\n")

        with open(file_name3, 'w') as f3:
            df["Timestamps:"] = df["Timestamps:"].apply(lambda x: add_comma_if_words(x))
            df[["Event", "Time"]] = df["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
            df.drop("Timestamps:", axis=1, inplace=True)
            df["Time"] = df['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
            df[["Date", "Time"]] = df["Time"].apply(lambda x: pd.Series(str(x).split(", ")))
            format_time_column(df, "Time")
            df["Time_subseconds"] = df['Time'].apply(time_to_seconds_subseconds)
            df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"])

            duration = 0

            string1 = 'PUFF_ON'
            string2 = 'PUFF_OFF'
            string3 = 'TOUCH_ON'
            string4 = 'TOUCH_OFF'

            for index, row in df.iterrows():
                if index + 1 < len(df) and row["Event"] == string3 and df.loc[index + 1, 'Event'] == string4:
                    new_row = pd.Series({'Event': "Touch", 'Date': row["Date"],
                                         'Range': str(row["Time"]) + "-" + str(df.loc[index + 1, 'Time']),
                                         'Duration_in_seconds': str(
                                             df.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                    df_v2.loc[df_v2.index.max() + 1] = new_row

                if index + 1 < len(df) and row["Event"] == string1 and df.loc[index + 1, 'Event'] == string2:
                    new_row = pd.Series({'Event': "PUFF", 'Date': row["Date"],
                                         'Range': str(row["Time"]) + "-" + str(df.loc[index + 1, 'Time']),
                                         'Duration_in_seconds': str(
                                             df.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                    df_v2.loc[df_v2.index.max() + 1] = new_row

            df_v2 = df_v2.iloc[1:].reset_index(drop=True)
            f3.write(df_v2.to_string(index=False) + "\n")

        df["Time_round"] = df['Time'].apply(round_to_nearest_second)
        df['Time_in_seconds'] = df['Time_round'].apply(convert_to_seconds)
        self.btn_erase.config(state="normal")
        plot_type=self.cb_plot.get()
        if plot_type=="Stem":
            def generate_graph(df):

                unique_dates = df['Date'].unique()

                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    # Get the rows with the current date
                    rows = df[df['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df) and row['Event'] == string1 and df.loc[index + 1, 'Event'] == string2:
                            duration = df.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                start_index = row["Time_in_seconds"]
                                end_index = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df) and row['Event'] == string3 and df.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    total_duration = f"{total_duration:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

                    markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ', basefmt=' ',
                                                              linefmt='g', label='PUFF> {}'.format(puff_duration+"s"))
                    stemline.set_linewidth(10)
                    # ax1.bar(np.arange(86400), time_matrix1, align='center', width=1, color='red', label='Puff')
                    # ax1.plot(np.arange(86400), time_matrix1, linewidth=1, color='red', label='Puff')
                    ax1.stem(np.arange(86400), time_matrix11, markerfmt=' ',basefmt=' ', linefmt='r', label='PUFF< {}'.format(puff_duration+"s"))
                    ax1.set_ylabel(date)
                    ax1.legend()
                    ax1.set_title("Total puffing time: " + str(total_duration) + 's')
                    fig.set_size_inches(15, 3)

                    # ax2.bar(np.arange(86400), time_matrix2, align='center', width=1, color='blue', label='Touch')
                    # ax2.plot(np.arange(86400), time_matrix2, linewidth=1, color='blue', label='Touch')
                    ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    ax2.legend()
                    plt.tight_layout()
                    # plt.show()


                return ax1, ax2

            ax1, ax2 = generate_graph(df=df)
            plt.show()

        if plot_type == "Step":
            def generate_graph(df):

                unique_dates = df['Date'].unique()

                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    # Get the rows with the current date
                    rows = df[df['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df) and row['Event'] == string1 and df.loc[index + 1, 'Event'] == string2:
                            duration = df.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                start_index = row["Time_in_seconds"]
                                end_index = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df) and row['Event'] == string3 and df.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    total_duration = f"{total_duration:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

                    ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                    ax1.step(np.arange(86400), time_matrix11, where='post', color="red", label='PUFF< {}'.format(puff_duration + "s"))
                    ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)
                    ax1.fill_between(np.arange(86400), time_matrix11, step="post", color='red', alpha=0.5)
                    ax1.set_ylim(0, 1.1)

                    ax1.set_xlabel("Time")
                    ax1.legend()
                    ax1.set_ylabel(date)
                    fig.set_size_inches(15, 3)

                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                return ax1, ax2
            ax1, ax2 = generate_graph(df=df)
            plt.show()

        if plot_type == "Line":
            def generate_graph(df):

                unique_dates = df['Date'].unique()

                x_ticks = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800,
                           50400, 54000,
                           57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400]
                x_labels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                            "10:00",
                            "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                            "21:00",
                            "22:00", "23:00", "24:00"]
                puff_duration = 0
                puff_duration = self.en_puff.get()
                for date in unique_dates:
                    print(date)
                    total_duration = 0
                    # Get the rows with the current date
                    rows = df[df['Date'] == date]

                    time_matrix1 = np.zeros((86400,), dtype=int)
                    time_matrix11 = np.zeros((86400,), dtype=int)
                    time_matrix2 = np.zeros((86400,), dtype=int)

                    string1 = 'PUFF_ON'
                    string2 = 'PUFF_OFF'
                    string3 = 'TOUCH_ON'
                    string4 = 'TOUCH_OFF'
                    for index, row in rows.iterrows():
                        if index + 1 < len(df) and row['Event'] == string1 and df.loc[index + 1, 'Event'] == string2:
                            duration = df.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration):
                                start_index = row["Time_in_seconds"]
                                end_index = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        if index + 1 < len(df) and row['Event'] == string3 and df.loc[index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                    total_duration = f"{total_duration:.4f}"
                    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

                    ax1.plot(np.arange(86400), time_matrix1, color="green", label='PUFF> {}'.format(puff_duration + "s"))
                    ax1.plot(np.arange(86400), time_matrix11, color="red", label='PUFF< {}'.format(puff_duration + "s"))
                    ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                    ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.set_ylabel(date)

                    fig.set_size_inches(15, 3)

                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)
                    ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                return ax1, ax2
            ax1, ax2 = generate_graph(df=df)
            plt.show()


        

    def send_text_btn_e(self):
        _send_data_e = "e"
        self.serialcom.serial.write(_send_data_e.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_e)
        self.btn_yes.config(state="normal")

    def send_text_btn_y(self):
        _send_data_y = "y"
        self.serialcom.serial.write(_send_data_y.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_y)

    def send_text_btn_s(self):
        current_time = DT.datetime.now()
        unix_timestamp = (DT.datetime.timestamp(current_time))
        frac, whole = math.modf(unix_timestamp)
        unix_1 = hex(int(str(whole)[0:-2]))[2:]
        unix_2 = hex(int(str(frac)[2:]))[2:]
        _send_data_s = "s" + str(unix_1) + str(unix_2)
        self.serialcom.serial.write(_send_data_s.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_s)

    def send_text_btn_t(self):
        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_t)




if __name__ == "__main__":
    global t2
    root = tk.Tk()
    root.title("FRIENDS Serial Communication")

    Application(master=root)

    root.mainloop()
