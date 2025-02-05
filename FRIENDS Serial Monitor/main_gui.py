#Importing libraries
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
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
import re
import os


class Application(ttk.Frame):
    #variable to store time duration
    time_duration = 0
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack() # Pack the frame into the master widget
        self.serialcom = SerialCom(baudrate=115200, timeout=0.1, writemode=True) # Initialize SerialCom object with specified parameters
        self.create_wedgets() # Call method to create widgets

    def create_wedgets(self):
        # Method to create various widgets
        self._wedget_statusbar()
        self._wedget_com()
        self._wedget_bps()
        self._wedget_puff()
        self._wedget_send()
        self._wedget_txrx()
        self._widget_read()


    def _wedget_statusbar(self):
        # Create a label frame for the status bar
        lf_status = ttk.LabelFrame(self.master, text="Status Bar")
        lf_status.pack(expand=False, side="top") # Pack the label frame


        # Create label for status information
        self.la_status = ttk.Label(
            master=lf_status,
            width=85,
            text="No Connection",
            background="lightgray")
        self.la_status.pack(expand=False, side="left") # Pack the label

    def _widget_read(self):
        # Create a label frame for the data status bar
        lf_read = ttk.LabelFrame(self.master, text="Data Status Bar")
        lf_read.pack(expand=False, side="top") # Pack the label frame

        # Create label for read status information
        self.read_status = ttk.Label(
            master=lf_read,
            width=90,
            text="Ready",
            background="lightgray")
        self.read_status.pack(expand=False, side="left")  # Pack the label

    def _wedget_com(self):
        # Create a label frame for COM settings
        lf_com = ttk.LabelFrame(self.master, text="COM")
        lf_com.pack(expand=False, side="top")

        # Combobox for selecting COM port
        self.cb_com = ttk.Combobox(
            master=lf_com,
            state="readonly",
            values=self.serialcom.find_comports(),  # Populate values from available COM ports
            width=69)
        self.cb_com.pack(expand=False, side="left")

        # Button to reload available COM ports
        self.btn_reload = ttk.Button(
            master=lf_com,
            text="Reload",
            command=self.reload_com_btn)
        self.btn_reload.pack(expand=False, side="left")

    def _wedget_bps(self):
        # Create a label frame for Baudrate settin
        lf_bps = ttk.LabelFrame(self.master, text="Baudrate (bps)")
        lf_bps.pack(expand=False, side="top")

        # Entry widget for entering baudrate
        self.en_bps = ttk.Entry(
            master=lf_bps,
            width=41)
        self.en_bps.insert(0, "115200") # Default baudrate
        self.en_bps.pack(expand=False, side="left")

        # Button to connect to COM port
        self.btn_open = ttk.Button(
            master=lf_bps,
            text="Connect",
            command=self.open_com_btn)  #Call open_com_btn method on click
        self.btn_open.pack(expand=False, side="left")

        # Button to disconnect from COM port
        self.btn_close = ttk.Button(
            master=lf_bps,
            text="Disconnect",
            command=self.close_com_btn, # Call close_com_btn method on click
            state="disable")
        self.btn_close.pack(expand=False, side="left")

    def _wedget_puff(self):
        # Create a label frame for puffing settings
        lf_bps = ttk.LabelFrame(self.master, text="Minimum puffing duration (s) and plot type")
        lf_bps.pack(expand=False, side="top")

        # Entry widget for entering minimum puffing duration
        self.en_puff = ttk.Entry(
            master=lf_bps,
            width=25)
        self.en_puff.insert(0, "0.0")
        self.en_puff.pack(expand=False, side="left")

        # Combobox for selecting plot type
        self.cb_plot = ttk.Combobox(
            master=lf_bps,
            values=["Line","Stem","Step"],
            width=25)
        self.cb_plot.current(0)
        self.cb_plot.pack(expand=False, side="left")

        # Combobox for selecting puffing display option
        self.cb_plot_puff = ttk.Combobox(
            master=lf_bps,
            values=["Display all puffing events", "Display puffs that exceed the threshold"],
            width=35)
        self.cb_plot_puff.current(0)
        self.cb_plot_puff.pack(expand=False, side="left")

        # Button to send puffing settings
        self.btn_puff = ttk.Button(
            master=lf_bps,
            text="send",
            command=self.open_puff)
        self.btn_puff.pack(expand=False, side="left")


    def _wedget_send(self):
        # Create a label frame for controlling data collection
        lf_send = ttk.LabelFrame(self.master, text="Input")
        lf_send.pack(expand=False, side="top")

        # Button to read time
        self.btn_time = ttk.Button(
            master=lf_send,
            text="Read Time",
            command=self.send_text_btn_t,  #Call send_text_btn_t method on click
            state="disable") # Initially disabled
        self.btn_time.pack(expand=False, side="left")

        # Button to set time
        self.btn_send = ttk.Button(
            master=lf_send,
            text="Set time",
            command=self.send_text_btn_s, # Call send_text_btn_s method on click
            state="disable") # Initially disabled
        self.btn_send.pack(expand=False, side="left")

        # Button to erase flash
        self.btn_erase = ttk.Button(
            master=lf_send,
            text="Erase Flash",
            command=self.send_text_btn_e,  # Call send_text_btn_e method on click
            state="disable") # Initially disabled
        self.btn_erase.pack(expand=False, side="left")

        # Button to start data collection
        self.btn_sdc = ttk.Button(
            master=lf_send,
            text="Start Data Collection",
            command=self.send_text_btn_sdc,  # Call send_text_btn_sdc method on click
            state="disable") # Initially disabled
        self.btn_sdc.pack(expand=False, side="left")

        # Button to read data
        self.btn_read = ttk.Button(
            master=lf_send,
            text="Read Data",
            command=self.send_text_btn_r, # Call send_text_btn_r method on click
            state="disable") # Initially disabled
        self.btn_read.pack(expand=False, side="left")

        # Button for file conversion
        self.btn_cgp = ttk.Button(
            master=lf_send,
            text="File Conversion",
            command=self.send_text_btn_conv, # Call send_text_btn_conv method on click
            state="enable") # Initially enabled
        self.btn_cgp.pack(expand=False, side="left")

        # Button to confirm "Yes"
        self.btn_yes = ttk.Button(
            master=lf_send,
            text="Yes",
            command=self.send_text_btn_y, # Call send_text_btn_y method on click
            state="disable") # Initially disabled
        self.btn_yes.pack(expand=False, side="left")

    def _wedget_txrx(self):
        # Create a PanedWindow for TX and RX sections
        pw_txrx = ttk.PanedWindow(self.master, orient="horizontal")
        pw_txrx.pack(expand=False, side="top")

        ## TX
        lf_tx = ttk.LabelFrame(pw_txrx, text="TX")
        lf_tx.pack(expand=False, side="left")

        ## RX
        lf_rx = ttk.LabelFrame(pw_txrx, text="RX")
        lf_rx.pack(expand=False, side="right")

        # Listbox to display received data
        self.lb_rx = tk.Listbox(
            lf_rx,
            height=20,
            width=110,
            state="normal") # Set initial state to normal
        self.lb_rx.pack(expand=False)

        # Button to save data and generate plots
        self.btn_save = ttk.Button(
            lf_rx,
            text="Save data and generate plots",
            command=self.save_data, # Call save_data method on click
            state="disable") # Initially disabled
        self.btn_save.pack(expand=False, side="right")

        # Button to clear received data
        self.btn_rxexp = ttk.Button(
            lf_rx,
            text="Clear",
            command=self.clear_text, # Call clear_text method on click
            state="enable") # Initially enabled
        self.btn_rxexp.pack(expand=False, side="right")

        # Label providing instruction
        self.instruction_label = ttk.Label(
            lf_rx,
            text="Please click 'Clear' button to clear the monitor & enable 'Read Data' button")
        self.instruction_label.pack(expand=False, side="left")

    def reload_com_btn(self):
        self.cb_com.config(values=self.serialcom.find_comports()) # Reload available COM ports in the combobox

    def open_com_btn(self):
        # Get selected COM port and baudrate
        _device = self.serialcom.devices[self.cb_com.current()].device
        _baudrate = self.en_bps.get()
        # Try to register the COM port
        if not self.serialcom.register_comport(device=_device): # Check if the COM port registration failed
            print("Cannot specify the comport. Please try again.") # Print error message if registration failed
        elif _baudrate.isdecimal() or _baudrate == "":  #Check if the entered baudrate is a decimal number or empty
            if _baudrate.isdecimal(): # If the entered baudrate is a decimal number
                self.serialcom.serial.baudrate = int(_baudrate) # Set the baudrate of the serial connection to the entered value
            # Open the COM port
            self.serialcom.serial.open()
            # Update status label to show connection status
            self.la_status.config(text="Connected", background="lightgreen")
            # self.en_send.config(state="normal")
            # Enable buttons and disable certain widgets
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

            # Start reading data from the serial port
            self._start_serialread()

        else:
            print("Text in the baudrate entry is not a number.")

    def _start_serialread(self):
        # Start a new thread to continuously read data from the serial port
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
        # Continuously read data from the serial port and update the listbox
        buffer = b'' # Initialize an empty byte buffer to store received data
        num=0 # Initialize a flag to track whether data reading is in progress
        while self.serialcom.serial.is_open: # Continuously read data from the serial port while it's open
            _recv_data = self.serialcom.serial.readline() # Read a line of data from the serial port
            # Check if any data is received
            if _recv_data != b'':
                # Append received data to the buffer
                buffer += _recv_data
                # Process data in the buffer as long as there are complete lines terminated by \r\n
                while b'\r\n' in buffer:
                    self.read_status.config(text="Reading Data from device. Please wait ......", background="orange") # Update status label to indicate reading status
                    num=1 # Set the flag to indicate data reading is in progress
                    line, buffer = buffer.split(b'\r\n', 1) # Split the buffer into lines delimited by \r\n, extracting the first line
                    try:
                        self.lb_rx.insert(tk.END, line.strip().decode("utf-8")) # Insert received data into the listbox after decoding it
                        # _recv_data = self.serialcom.serial_read()
                    except (TypeError, AttributeError):
                        print("Comport disconnected while reading") # Handle exceptions if the comport gets disconnected during reading
            if num==1 and _recv_data == b'':
                # Update status label to indicate reading completion
               self.read_status.config(text="Reading Data Done", background="lightgreen")
               num=0 # Reset the flag to indicate reading completion


    def open_puff(self):
        puff_duration=0
        puff_duration=self.en_puff.get() # Get the specified puff duration from the entry widget

    def close_com_btn(self):
        self.serialcom.close_comport() # Close the COM port
        self._th_sread.join() # Wait for the serial read thread to finish
        # Enable/disable widgets and update status after closing the COM port
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
        # Clear the text in the listbox and enable the read button
        self.lb_rx.delete(0, 'end')
        self.btn_read.config(state="normal")
        # Reset the read status label
        self.read_status.config(text="Ready", background="lightgray")

    def send_text_btn(self):
        _send_data = self.en_send.get() # Get the text to send from the entry widget
        self.serialcom.serial.write(_send_data.encode("utf-8"))  # Send the text over the serial connection
        # self.lb_tx.insert(tk.END, _send_data)
        self.en_send.delete(0, tk.END) # Clear the entry widget after sending the text

    def send_text_btn_sdc(self):
        self.lb_rx.delete(0, 'end') # Clear the listbox
        current_time = DT.datetime.now() # Get the current time
        # Get the UNIX timestamp and split it into integer and fractional parts
        unix_timestamp = (DT.datetime.timestamp(current_time))
        frac, whole = math.modf(unix_timestamp)
        # Convert integer and fractional parts of UNIX timestamp to hexadecimal
        unix_1 = hex(int(whole))[2:] #unix_1 = hex(int(str(whole)[0:-2]))[2:]
        unix_2 = hex(int(frac * 1_000_000))[2:] #unix_2 = hex(int(str(frac)[2:]))[2:]

        #send message to the device for setting time in it
        _send_data_sdc2 = "s" + str(unix_1) + str(unix_2)
        self.serialcom.serial.write(_send_data_sdc2.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_sdc2[0:13])

        # Wait for 1 second
        time.sleep(1)
        #Send message to the device for earising flash
        _send_data_sdc1 = "e"
        self.serialcom.serial.write(_send_data_sdc1.encode("utf-8"))

        #time.sleep(1)
        #_send_data_y = "y"
        #self.serialcom.serial.write(_send_data_y.encode("utf-8"))

        # Disable the read button and enable the yes button
        self.btn_read.config(state="disabled")
        self.btn_yes.config(state="normal")


    def send_text_btn_r(self):
        # Update status label to indicate reading data from the device
        self.read_status.config(text="Reading Data from the Device. Please wait .....", background="lightgreen")
        #self.lb_rx.delete(0, 'end')
        #time.sleep(0.3)


        #send command to request device time
        _send_data_t = "t"
        self.serialcom.serial.write(_send_data_t.encode())

        # Send command to request data from the device
        _send_data_r = "r"
        self.serialcom.serial.write(_send_data_r.encode())

        # Disable the save button and enable the read button
        # self.lb_tx.insert(tk.END, _send_data_r)
        self.btn_save.config(state="normal")
        self.btn_read.config(state="disabled")


    def save_data(self):
        # Update status label to indicate saving data and generating plots
        self.read_status.config(text="Save Data and Generating plots", background="orange")
        # Get the current time
        current_time = DT.datetime.now()
        # Ask user for the file name and location to save the data
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname:
            _fname += ".txt" # Append .txt extension to the file name
            # Generate file names for converted and duration data files
            file_name2 = _fname.split(".")[0] + "_converted.txt"
            file_name3 = _fname.split(".")[0] + "_duration.txt"

        # Write data to the file
        with open(_fname, 'w') as f1:
            df2 = pd.DataFrame(columns=["Timestamps:"])
            # Write local time to the file
            f1.write(str("Local Time: " + str(current_time) + "\n"))
            # Iterate through data in the listbox
            for i in range(self.lb_rx.size()):
                if ((str(self.lb_rx.get(i))[0:8]) == "Internal"): #To grab the internal timestamps of the device, it will find "Internal" in first 8 characters
                    tm2 = self.lb_rx.get(i)[0:40] ##take characters from 0 to 40 that includes the whole line (internal timestamps)

                # if (str(self.lb_rx.get(i))[0:8]) == "Internal":
                # f.write(str(self.lb_rx.get(i)) + "\n")
                ## Take only the saved timestamps in the flash.  Algotithm : Include all the lines from the RX monitor except those that started from some specified word given below.
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
            # Write data to the file
            f1.write(str(tm2) + "\n")
            f1.write(df2.to_string(index=False) + "\n")
        # Enable/disable buttons after saving data
        self.btn_erase.config(state="normal")
        self.btn_read.config(state="disabled")
        self.btn_sdc.config(state="normal")
        self.btn_save.config(state="disabled")



        def add_comma_if_words(string):
            # List of words to replace with word + comma
            words_to_replace = ["SET_TIME", "TOUCH_ON", "TOUCH_OFF", "PUFF_ON", "PUFF_OFF", "READ_TIME","TEMPERATURE_ON","TEMPERATURE_OFF", "UNEXPECTED_TIMESTAMP"]
            # Iterate through each word in the list
            for word in words_to_replace:
                string = string.replace(word, f"{word},") # Replace each word with the word followed by a comma
            # Return the modified string
            return string

        def format_time_column(df, column_name):
            # Convert the column to string
            df[column_name] = df[column_name].astype(str)

            # Split the column into hours, minutes, seconds, and milliseconds
            time_parts = df[column_name].str.split(':', expand=True)
            hours = time_parts[0].astype(int)
            minutes = time_parts[1].astype(int)
            ############################################### Edit started ##############################################################
            #seconds = time_parts[2].astype(float).round(10).astype(str)
            # Convert seconds to float, round to 10 decimal places, and prevent scientific notation
            seconds = time_parts[2].astype(float).apply(lambda x: f"{x:.6f}")
            ############################################### Edit started ##############################################################


            # Format the seconds column
            seconds = seconds.apply(lambda s: s if '.' in s else s + '.00')

            # Combine the formatted parts into a new column
            df[column_name] = hours.map("{:02d}".format) + ':' + \
                              minutes.map("{:02d}".format) + ':' + \
                              seconds
            return df
        ############################################### Edit started ##############################################################

        def clean_invalid_time_rows(df):

            to_drop = []

            for index, row in df[df['Time'] == "Invalid Time Format"].iterrows():
                event = row['Event']
                if event in ["PUFF_ON", "TOUCH_ON", "TEMPERATURE_ON"]:
                    to_drop.extend([index, index + 1] if index + 1 in df.index else [index])
                elif event in ["PUFF_OFF", "TOUCH_OFF", "TEMPERATURE_OFF"]:
                    to_drop.extend([index - 1, index] if index - 1 in df.index else [index])

            return df.drop(to_drop).reset_index(drop=True)

        ############################################### Edit Ended ##############################################################

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
            # Split the time string into its components
            time_parts = time_string.split(':')
            # Convert hours, minutes, and seconds to integers
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            # Calculate total seconds
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds

        def seconds_to_milliseconds(seconds):
            milliseconds = float(seconds) * 1000 # Convert seconds to milliseconds
            return "{:.4f}".format(milliseconds) # Format the result to four decimal places

        def format_column(value):
            value_str = str(value)
            # Left-align the first 15 characters, right-align the remaining characters
            left_aligned = value_str[:15]
            right_aligned = value_str[15:]
            return f"{left_aligned:<8}{right_aligned:>}"

        def format_time(input_time):
            try:
                # Parse the input time into a datetime object
                time_obj = datetime.strptime(input_time, "%H:%M:%S.%f")
                # Format the time as HH:MM:SS.mmm
                formatted_time = time_obj.strftime("%H:%M:%S.%f")[:-3]

                return formatted_time
            except ValueError:
                # Handle the case where the input time format is invalid
                return "Invalid Time Format"


        with open(file_name2, 'w') as f2:
            df=df2.copy()
            df2 = pd.DataFrame(columns=["Timestamps:"]) # Define df2 as an empty DataFrame

            # Function to convert UTC datetime to local datetime
            def datetime_from_utc_to_local(utc_datetime):
                now_timestamp = time.time()
                offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
                return utc_datetime + offset

            # Write local time to the file
            f2.write(str("Local Time: " + str(current_time) + "\n"))
            # List of prefixes indicating different types of events
            valid_prefixes = {"1", "2", "3", "4", "5", "6", "E", "F"}
            for index, row in df.iterrows():
                #line2= str(row)
                #line2=line2[15:31]
                # Extract the last 16 characters of the line
                line = str(row[0])
                line2 = re.sub(r"\s+", "", line)  # Remove all whitespace (spaces, tabs, newlines, etc.) line.replace(" ", "")
                if len(line2) == 16 and line2.isalnum() and (line2.isupper() or line2.isdigit()) and line2[0] in valid_prefixes:
                    timestamp_hex = line2[4:8] + line2[8:12]
                    subsecond_hex = line2[12:16]
                    for hexstamp in timestamp_hex.split():
                        gmt_time = DT.datetime.utcfromtimestamp(int(hexstamp, 16)) + DT.timedelta(seconds=(int(subsecond_hex, 16) / 65536))  # UNIX hex to GMT converter
                        # gmt_time = DT.datetime.utcfromtimestamp(float(int(hexstamp, 16) // 16**4)) \
                        #            + DT.timedelta(microseconds=int(hexstamp, 16) % 16**4)
                        local_time = datetime_from_utc_to_local(gmt_time)  # GMT to local time converter
                            # Event separation
                    # Determine the event type based on the first character of line2
                    if (line2[0] == "1"):
                        event = "PUFF_ON" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time) #isoformat
                    elif (line2[0] == "2"):
                        event = "PUFF_OFF" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                    elif (line2[0] == "3"):
                        event = "TOUCH_ON" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                    elif (line2[0] == "4"):
                        event = "TOUCH_OFF" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                    elif (line2[0] == "5"):
                        hex_number = str(line2[4:16])
                        decimal_number = int(hex_number, 16)
                        event = "TEMPERATURE_ON" + " " + str(decimal_number)
                    elif (line2[0] == "6"):
                        hex_number = str(line2[4:16])
                        decimal_number = int(hex_number, 16)
                        event = "TEMPERATURE_OFF" + " " + str(decimal_number)
                    elif (line2[0] == "E"):
                        event = "READ_TIME" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                    elif (line2[0] == "F"):
                        event = "SET_TIME" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                    else:
                        event = "Time"
                        print("issue")
                    # Add the event to df2 DataFrame
                    df2.loc[len(df2)] = [event]
                else:  ##for invalid/corrupt timestamps
                    event = "UNEXPECTED_TIMESTAMP" + " " + str(line)
                    df2.loc[len(df2)] = [event]

            df2_n = df2.copy()
            df2_new_temp = df2.copy()
            df2_n["Timestamps:"] = df2_n["Timestamps:"].apply(lambda x: add_comma_if_words(x))  # Add comma after specific words in "Timestamps:" column
            df2_n[["Event", "Information"]] = df2_n["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", "))) # Split "Timestamps:" column into "Event" and "Information" columns
            df2_n.drop("Timestamps:", axis=1, inplace=True)
            # Write the formatted DataFrame to the file
            f2.write(df2_n.to_string(index=False) + "\n")

        with open(file_name3, 'w') as f3:
            #df2_new_temp = df2_new.copy()
            # Remove rows from df2 where 'Timestamps:' column starts with 'TEMP' or 'UNEXPECTED'
            df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
            df2 = df2[~df2['Timestamps:'].str.startswith('UNEXPECTED')]

            df2["Timestamps:"] = df2["Timestamps:"].apply(lambda x: add_comma_if_words(x))  # Add commas after specific words in 'Timestamps:' column
            df2[["Event", "Time"]] = df2["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", "))) # Split 'Timestamps:' column into 'Event' and 'Time' columns
            df2.drop("Timestamps:", axis=1, inplace=True)
            df2["Time"] = df2['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True) # Replace date format in 'Time' column
            df2[["Date", "Time"]] = df2["Time"].apply(lambda x: pd.Series(str(x).split(", "))) # Split 'Time' column into 'Date' and 'Time' columns
            format_time_column(df2, "Time") # Format 'Time' column
            df2["Time_subseconds"] = df2['Time'].apply(time_to_seconds_subseconds) # Convert 'Time' to seconds and subseconds

            #for temperature graph
            # Filter rows in df2_new_temp to exclude 'READ_TIME' and 'SET_TIME' events
            df2_new_temp["Timestamps:"] = df2_new_temp["Timestamps:"].apply(lambda x: add_comma_if_words(x))
            df2_new_temp[["Event", "Time"]] = df2_new_temp["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
            df2_new_temp = df2_new_temp[df2_new_temp['Event'] != 'READ_TIME']
            df2_new_temp = df2_new_temp[df2_new_temp['Event'] != 'SET_TIME']
            df2_new_temp.drop("Timestamps:", axis=1, inplace=True)

            df2_new_temp["Time"] = df2_new_temp['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
            df2_new_temp[["Temperature", "Time"]] = df2_new_temp["Time"].apply(lambda x: pd.Series(str(x).split(", ")))

            # Initialize list to store rows to delete
            ## Handling unexpected timestamps
            rows_to_delete = []
            for index, row in df2_new_temp.iterrows():

                if row['Event'] == 'UNEXPECTED_TIMESTAMP':
                    # Check previous row for related event types
                    if index > 0:
                        prev_row = df2_new_temp.loc[index - 1]
                        # If the previous row has a related event type, add its index to the list
                        if prev_row['Event'] in ['PUFF_ON', 'TOUCH_ON', 'TEMPERATURE_ON']:
                            rows_to_delete.append(index - 1)

                    # Check following row for related event types
                    if index < len(df) - 1:
                        next_row = df2_new_temp.loc[index + 1]
                        # If the following row has a related event type, add its index to the list
                        if next_row['Event'] in ['PUFF_OFF', 'TOUCH_OFF', 'TEMPERATURE_OFF']:
                            rows_to_delete.append(index + 1)

                    rows_to_delete.append(index)
            # Drop rows identified for deletion
            df2_new_temp.drop(index=rows_to_delete, inplace=True)
            df2_new_temp = df2_new_temp.reset_index(drop=True)

            # Find the NaN values in the 'Time' column of 'TEMPERATURE_ON' row
            for index, row in df2_new_temp.iterrows():
                # Check if the value in the 'Event' column of the current row is 'TEMPERATURE_ON'
                # and if the 'Time' value in the current row is NaN (missing)
                if (row['Event'] == 'TEMPERATURE_ON') and pd.isna(row['Time']):
                    # If conditions are met, set the 'Time' value of the current row to the 'Time' value
                    # from the row two positions above (using index-2)
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index-2, 'Time']
                # Check if the value in the 'Event' column of the current row is 'TEMPERATURE_OFF'
                # and if the 'Time' value in the current row is NaN (missing)
                if (row['Event'] == 'TEMPERATURE_OFF') and pd.isna(row['Time']):
                    # If conditions are met, set the 'Time' value of the current row to the 'Time' value
                    # from the row two positions above (using index-2)
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index-2, 'Time']


            format_time_column(df2_new_temp, "Time") # Format the 'Time' column of the DataFrame df2_new_temp
            df2_new_temp["Time_subseconds"] = df2_new_temp['Time'].apply(time_to_seconds_subseconds) # Convert the 'Time' column to seconds with subseconds
            df2_new_temp['Date'] = pd.to_datetime(df2_new_temp['Temperature'], errors='coerce')
            # Iterate over each row in the DataFrame df2_new_temp
            for index, row in df2_new_temp.iterrows():
                # Check if the 'Event' is 'TEMPERATURE_ON' and 'Date' is NaN
                if (row['Event'] == 'TEMPERATURE_ON' and pd.isna(row['Date'])):
                    # If conditions are met, set the 'Date' value of the current row to
                    # the 'Date' value from two positions above (using index - 2)
                    df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
                # Check if the 'Event' is 'TEMPERATURE_OFF' and 'Date' is NaN
                if (row['Event'] == 'TEMPERATURE_OFF' and pd.isna(row['Date'])):
                    # If conditions are met, set the 'Date' value of the current row to
                    # the 'Date' value from two positions above (using index - 2)
                    df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']

            df2_new_temp['Temperature'] = df2_new_temp['Temperature'].apply(lambda x: 0 if pd.to_datetime(x, errors='coerce') is not pd.NaT else x) # Convert 'Temperature' column to 0 if it cannot be converted to datetime
            df2_new_temp['Time'] = df2_new_temp['Time'].apply(lambda x: format_time(x))
            ################################################### Edit Started ##############################################################
            # Drop rows where 'Time' contains "Invalid Time Format"
            df2_new_temp = clean_invalid_time_rows(df2_new_temp)
            ################################################### Edit Ended ##############################################################

            df2_new_temp["Time_round"] = df2_new_temp['Time'].apply(round_to_nearest_second) # Round 'Time' values to the nearest second
            df2_new_temp['Time_in_seconds'] = df2_new_temp['Time_round'].apply(convert_to_seconds) # Convert 'Time_round' values to seconds


            df2['Time'] = df2['Time'].apply(lambda x: format_time(x))
            ################################################### Edit Started ##############################################################
            # Drop rows where 'Time' contains "Invalid Time Format"
            df2 = clean_invalid_time_rows(df2)
            ################################################### Edit Ended ##############################################################

            df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"]) #initialize dataframe for generating event information file

            duration = 0
            # Define event strings
            string1 = 'PUFF_ON'
            string2 = 'PUFF_OFF'
            string3 = 'TOUCH_ON'
            string4 = 'TOUCH_OFF'
            df2.reset_index(drop=True, inplace=True) # Reset index of DataFrame df
            # Iterate over each row in DataFrame df2
            for index, row in df2.iterrows():
                # Check if the current row is the event of "TOUCH_ON" and the next row is the event of "TOUCH_OFF"
                if index + 1 < len(df2) and row["Event"] == string3 and df2.loc[index + 1, 'Event'] == string4:
                    # Define the new row with event type, date, time range, and duration in seconds of that event
                    new_row = pd.Series({'Event': "TOUCH", 'Date': row["Date"],
                                         'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                         'Duration_in_seconds': str(
                                             df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                    # Append the new row to DataFrame df_v2
                    df_v2.loc[df_v2.index.max() + 1] = new_row
                # Check if the current row is the event of "PUFF_ON" and the next row is the event of "PUFF_OFF"
                if index + 1 < len(df2) and row["Event"] == string1 and df2.loc[index + 1, 'Event'] == string2:
                    # Define the new row with event type, date, time range, and duration in seconds of that event
                    new_row = pd.Series({'Event': "PUFF", 'Date': row["Date"],
                                         'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                         'Duration_in_seconds': str(
                                             df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                    # Append the new row to DataFrame df_v2
                    df_v2.loc[df_v2.index.max() + 1] = new_row
            df_v2 = df_v2.iloc[1:].reset_index(drop=True)
            # Convert 'Duration_in_seconds' to milliseconds and round to one decimal place
            df_v2['Duration(ms)'] = df_v2['Duration_in_seconds'].apply(seconds_to_milliseconds)
            df_v2['Duration(ms)'] = df_v2['Duration(ms)'].astype(float).round(1)
            # Drop the 'Duration_in_seconds' column from DataFrame df_v2
            df_v2 = df_v2.drop('Duration_in_seconds', axis=1)

            f3.write(df_v2.to_string(index=False) + "\n") # Write the DataFrame df_v2 to file f3

        df2["Time_round"] = df2['Time'].apply(round_to_nearest_second)
        df2['Time_in_seconds'] = df2['Time_round'].apply(convert_to_seconds)
        #df2=df2_new.copy()
        #take the dataframe from 2nd file df2_n and find time in seconds for each event





        plot_type = self.cb_plot.get() # Get the selected plot type from the plot type combo box
        # Check if the selected plot type is "Stem"
        if plot_type=="Stem":
            # Define a function to generate the stem plot graph
            def generate_graph(df2_new_temp):
                unique_dates = df2_new_temp['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame

                # Define x-axis ticks and labels for a 24-hour time span
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
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    date= str(date)[:10] # Extract date part from datetime
                    print(date)
                    # Initialize variables for total duration, duration above threshold, and number of puffs
                    total_duration = 0
                    dur_gth = 0
                    number_of_puff = 0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]
                    # Initialize arrays to store time matrix for different events
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
                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): ## if any puff duration is greater or equal that the specified puff duration
                                dur_gth += duration # calculate the duration within the condition
                                number_of_puff += 1 # calculate puff frequency within the condition
                                # Mark the time range of PUFF events on the time matrix
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            # Mark the time range of TOUCH events on the time matrix
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF event
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        # Stem plot for puffing events exceeding the threshold duration
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ', basefmt=' ',
                                                              linefmt='g', label='PUFF> {}'.format(puff_duration+"s"))
                        stemline.set_linewidth(10)
                        # ax1.bar(np.arange(86400), time_matrix1, align='center', width=1, color='red', label='Puff')
                        # ax1.plot(np.arange(86400), time_matrix1, linewidth=1, color='red', label='Puff')
                        # Stem plot for puffing events below the threshold duration
                        ax1.stem(np.arange(86400), time_matrix11, markerfmt=' ',basefmt=' ', linefmt='r', label='PUFF< {}'.format(puff_duration+"s"))

                    if option == "Display puffs that exceed the threshold":
                        # Stem plot for puffing events exceeding the threshold duration
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ',
                                                                  basefmt=' ',
                                                                  linefmt='g',
                                                                  label='PUFF> {}'.format(puff_duration + "s"))
                        stemline.set_linewidth(10)

                    #ax1.set_ylabel(date)
                    # Set title and labels for the subplot
                    ax1.legend()
                    ax1.set_title("Date: "+ str(date) + " ,Total puffing time above threshold: " + str(dur_gth) + 's'+ ","+"Num of Puffs above threshold: "+str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Stem plot for TOUCH events on another subplot
                    markerline, stemline, baseline = ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    stemline.set_linewidth(10)
                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    ax2.legend()

                    # Stem plots for temperature on other subplots

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

                    # Annotate temperature values on the plots
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


                    ## find the maximum and minimum value for setting y axis
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3 =0
                    if len(non_zero_values31) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                        min_matrix4 = min(non_zero_values4)
                    else:
                        min_matrix4 = 0
                    if len(non_zero_values41) != 0:
                        min_matrix41 = min(non_zero_values41)
                    else:
                        min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()

                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)

                # Return the created subplots
                return ax1, ax3, ax2, ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4, = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Step": # Check if the selected plot type is "Step"
            # Define a function to generate the step plot graph
            def generate_graph(df2_new_temp):

                unique_dates = df2_new_temp['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame

                # Define x-axis ticks and labels for a 24-hour time span
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
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    date = str(date)[:10] # Extract date part from datetime
                    print(date)
                    # Initialize variables for total duration, duration above threshold, and number of puffs
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    # Initialize arrays to store time matrix for different events
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
                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): ## if any puff duration is greater or equal than the specified minimum puff duration
                                dur_gth += duration  # calculate the duration within the condition
                                number_of_puff += 1  # calculate puff frequency within the condition
                                # Mark the time range of PUFF events on the time matrix
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1
                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF event
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                       # Step plot for puffing events exceeding the threshold duration
                       ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                       # Step plot for puffing events below the threshold duration
                       ax1.step(np.arange(86400), time_matrix11, where='post', color="red", label='PUFF< {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)
                       ax1.fill_between(np.arange(86400), time_matrix11, step="post", color='red', alpha=0.5)

                    if option=="Display puffs that exceed the threshold":
                        # Step plot for puffing events exceeding the threshold duration
                        ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)

                    # Set title and labels for the subplot
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.legend()
                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Step plot for TOUCH events on another subplot
                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Stem plots for temperature on other subplots
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

                    # Annotate temperature values on the plots
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

                    ## find the maximum and minimum value for setting y axis for temperature
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3 =0
                    if len(non_zero_values31) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                        min_matrix4 = min(non_zero_values4)
                    else:
                        min_matrix4 = 0
                    if len(non_zero_values41) != 0:
                        min_matrix41 = min(non_zero_values41)
                    else:
                        min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)
                # Return the created subplots
                return ax1,ax3,ax2,ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        # Check if the selected plot type is "Line"
        if plot_type == "Line":
            # Define a function to generate the line plot graph
            def generate_graph(df2_new_temp):

                unique_dates = df2_new_temp['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame

                # Define x-axis ticks and labels for a 24-hour time span
                x_ticks = [0,1800, 3600,5400,7200,9000,10800,12600,14400,16200,18000,19800,21600,23400,25200,27000,28800,30600,32400,34200,
                           36000,37800,39600,41400,43200,45000,46800,48600,50400,52200,54000,55800,57600,59400,61200,63000,64800,66600,68400,70200,72000,73800,75600,77400,79200,81000,82800,84600,86400,86460]
                x_labels = ["00:00","00:30", "01:00","01:30", "02:00","02:30","03:00","03:30","04:00","04:30", "05:00","05:30", "06:00", "06:30","07:00","07:30", "08:00","08:30","09:00","09:30",
                            "10:00","10:30","11:00","11:30", "12:00","12:30","13:00", "13:30", "14:00","14:30", "15:00","15:30", "16:00","16:30" ,"17:00","17:30", "18:00","18:30", "19:00","19:30", "20:00","20:30",
                            "21:00","21:30","22:00","22:30", "23:00","23:30","24:00","24:01"]

                puff_duration = 0
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    date = str(date)[:10] # Extract date part from datetime
                    print(date)
                    # Initialize variables for total duration, duration above threshold, and number of puffs
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    # Initialize arrays to store time matrix for different events
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
                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): # if any puff duration is greater or equal that the specified puff duration
                                dur_gth += duration # calculate the duration within the condition
                                number_of_puff += 1 # calculate puff frequency within the condition
                                # Mark the time range of PUFF events on the time matrix
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            # Mark the time range of TOUCH events on the time matrix
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF event
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    #fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,gridspec_kw={'height_ratios': [1, 1, 5]})
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        # Line plot for puffing events exceeding the threshold duration
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        # Line plot for puffing events below the threshold duration
                        ax1.plot(np.arange(86400), time_matrix11, color="red",
                                 label='PUFF< {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                        ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    if option == "Display puffs that exceed the threshold":
                        # Line plot for puffing events exceeding the threshold duration
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)

                    # Set title and labels for the subplot
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str( dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Line plot for TOUCH events on another subplot
                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Stem plots for temperature on other subplots
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

                    # Annotate temperature values on the plots
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

                    ## find the maximum and minimum value for setting y axis in temperature graph
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3 =0
                    if len(non_zero_values31) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                        min_matrix4 = min(non_zero_values4)
                    else:
                        min_matrix4 = 0
                    if len(non_zero_values41) != 0:
                        min_matrix41 = min(non_zero_values41)
                    else:
                        min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()

                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)

                # Return the created subplots
                return ax1, ax3, ax2, ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        self.read_status.config(text="Ready", background="lightgray")




    def send_text_btn_conv(self):

        self.lb_rx.delete(0, 'end') # delete everything from RX monitor
        time.sleep(0.3) # Introduce a small delay to avoid overwhelming the system with rapid execution


        def add_comma_if_words(string):
            # List of words to replace with word + comma
            words_to_replace = ["SET_TIME", "TOUCH_ON", "TOUCH_OFF", "PUFF_ON", "PUFF_OFF", "READ_TIME","TEMPERATURE_ON","TEMPERATURE_OFF","UNEXPECTED_TIMESTAMP"]
            # Iterate through each word in the list
            for word in words_to_replace:
                string = string.replace(word, f"{word},")
            # Return the modified string
            return string

        def format_time_column(df, column_name):
            # Convert the column to string
            df[column_name] = df[column_name].astype(str)

            # Split the column into hours, minutes, seconds, and milliseconds
            time_parts = df[column_name].str.split(':', expand=True)

            hours = time_parts[0].astype(int)
            minutes = time_parts[1].astype(int)
        ############################################### Edit started ##############################################################
            #seconds = time_parts[2].astype(float).round(10).astype(str)
            # Convert seconds to float, round to 10 decimal places, and prevent scientific notation
            seconds = time_parts[2].astype(float).apply(lambda x: f"{x:.6f}")
        ############################################### Edit ended ##############################################################

            # Format the seconds column
            seconds = seconds.apply(lambda s: s if '.' in s else s + '.00')

            # Combine the formatted parts into a new column
            df[column_name] = hours.map("{:02d}".format) + ':' + \
                              minutes.map("{:02d}".format) + ':' + \
                              seconds
            return df
        ############################################### Edit started ##############################################################

        def clean_invalid_time_rows(df):
            to_drop = []

            for index, row in df[df['Time'] == "Invalid Time Format"].iterrows():
                event = row['Event']
                if event in ["PUFF_ON", "TOUCH_ON", "TEMPERATURE_ON"]:
                    to_drop.extend([index, index + 1] if index + 1 in df.index else [index])
                elif event in ["PUFF_OFF", "TOUCH_OFF", "TEMPERATURE_OFF"]:
                    to_drop.extend([index - 1, index] if index - 1 in df.index else [index])

            return df.drop(to_drop).reset_index(drop=True)

        def process_file(file_path):
            """
            Reads a text file, removes all lines before the last occurrence of "Timestamps:",
            and saves the result in a new file with '_temp' appended to the original name.

            If multiple occurrences of "Timestamps:" are found, it alerts the user via a pop-up message
            and stops execution. Otherwise, it proceeds to clean the file.

            Args:
                file_path (str): Path to the input text file.

            Returns:
                str or None: Path to the new file if processing is successful, else None.
            """
            try:
                # Read the file content
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                # Find all occurrences of "Timestamps:"
                timestamp_indices = [i for i, line in enumerate(lines) if "Timestamps:" in line]

                if not timestamp_indices:
                    print("Error: 'Timestamps:' not found in the file.")
                    return None

                if len(timestamp_indices) > 1:
                    # Create a pop-up alert for multiple "Timestamps:" occurrences
                    root = tk.Tk()
                    root.withdraw()  # Hide the main Tkinter window
                    messagebox.showwarning(
                        "Multiple Timestamps Detected",
                        "The data was read and saved multiple times in the text file.\n"
                        "Please remove unwanted/unnecessary data from the text file and read it again."
                    )
                    print("Execution stopped due to multiple 'Timestamps:' occurrences.")
                    return None  # Stop execution and ask the user to clean the file

                # If only one "Timestamps:" is found, proceed with cleaning
                last_index = timestamp_indices[-1]
                filtered_lines = lines[last_index:]

                # Construct new file name with "_temp"
                base_name, ext = os.path.splitext(file_path)
                new_file_path = f"{base_name}_temp{ext}"

                # Write back the filtered content to the new file
                with open(new_file_path, "w", encoding="utf-8") as file:
                    file.writelines(filtered_lines)

                print(f"File has been processed and saved as: {new_file_path}")

                # Update file_path variable
                return new_file_path

            except FileNotFoundError:
                print(f"Error: The file at '{file_path}' was not found.")
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

# def check_for_e_in_column(df_column, input_integer):
        #     # Iterate through each row in the specified DataFrame column
        #     for index, value in df_column.iteritems():
        #         # Check if 'e' or 'E' is present in the string
        #         if 'e' in str(value) in str(value):
        #             # Print the index where 'e' was found
        #             print(f"'e' found in row index: {index}")
        #
        #             # Print the entire row where 'e' was found
        #             # print(f"Row: {df_column.iloc[index]}")
        #
        #             # Print the integer that was passed as input
        #             print(f"Case Location: {input_integer}")
        #
        #             # Stop execution and return "e found"
        #             return index
        #
        #     # If 'e' was not found in any string, return no 'e' found
        #     return "No e was found"

############################################### Edit Ended ##############################################################

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
            # Split the time string into its components
            time_parts = time_string.split(':')
            # Convert hours, minutes, and seconds to integers
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            # Calculate total seconds
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds

        def seconds_to_milliseconds(seconds):
            milliseconds = float(seconds) * 1000 # Convert seconds to milliseconds
            return "{:.4f}".format(milliseconds) # Format the result to four decimal places

        ##Update status bar
        self.read_status.config(text="Converting timestamps", background="lightgreen")
        #ask for a text file with original timestamps
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])

        # remove any line starts with "Input Command"
        # remove_lines_from_file(file_path)

        # Remove all the lines before "timestamp:" and rename file_path variable to originalName_temp
        file_path = process_file(file_path)

        ## convert the file into a dataframe
        df = pd.read_csv(file_path)
        ##create a new dataframe df2
        df2 = pd.DataFrame(columns=["Timestamps:"])

        # Function to convert UTC datetime to local datetime
        def datetime_from_utc_to_local(utc_datetime):
            now_timestamp = time.time()
            offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
            return utc_datetime + offset
        
        df.columns=["Timestamps:"]
        #delete the headers
        df = df.drop(df.index[:0])
        df = df.reset_index(drop=True)
        # List of prefixes indicating different types of events
        valid_prefixes = {"1", "2", "3", "4", "5", "6", "E", "F"}
        for index, row in df.iterrows():
            # Extract the last 16 characters of the line
            line = str(row[0])
            line2 = re.sub(r"\s+", "", line)  # Remove all whitespace (spaces, tabs, newlines, etc.) line.replace(" ", "")
            if len(line2) == 16 and line2.isalnum() and (line2.isupper() or line2.isdigit()) and line2[0] in valid_prefixes:
                timestamp_hex = line2[4:8] + line2[8:12]
                subsecond_hex = line2[12:16]
                for hexstamp in timestamp_hex.split():
                    gmt_time = DT.datetime.utcfromtimestamp(int(hexstamp, 16)) + DT.timedelta(seconds=(int(subsecond_hex, 16) / 65536))  # UNIX hex to GMT converter
                    local_time = datetime_from_utc_to_local(gmt_time)  # GMT to local time converter

                if (line2[0] == "1"):
                    event = "PUFF_ON" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                elif (line2[0] == "2"):
                    event = "PUFF_OFF" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                elif (line2[0] == "3"):
                    event = "TOUCH_ON" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                elif (line2[0] == "4"):
                    event = "TOUCH_OFF" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                elif (line2[0] == "5"):
                    hex_number = str(line2[4:16])
                    decimal_number = int(hex_number, 16)
                    event = "TEMPERATURE_ON" + " " + str(decimal_number)
                elif (line2[0] == "6"):
                    hex_number = str(line2[4:16])
                    decimal_number = int(hex_number, 16)
                    event = "TEMPERATURE_OFF" + " " + str(decimal_number)
                elif (line2[0] == "E"):
                    event = "READ_TIME" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                elif (line2[0] == "F"):
                    event = "SET_TIME" + " " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f") #str(local_time)
                else:
                    event = "Time"
                    print("issue")
                # Add the event to df2 DataFrame
                df2.loc[len(df2)] = [event]
            else:
                event = "UNEXPECTED_TIMESTAMP" + " " + str(line)
                df2.loc[len(df2)] = [event]
        #f2.write(str(tm) + "\n")
        #df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
        df2_new_temp = df2.copy()
        df3 = df2.copy()

        df3["Timestamps:"] = df3["Timestamps:"].apply(lambda x: add_comma_if_words(x))  # Add comma after specific words in "Timestamps:" column
        df3[["Event", "Information"]] = df3["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", "))) # Split "Timestamps:" column into "Event" and "Information" columns
        df3.drop("Timestamps:", axis=1, inplace=True)

        # Remove rows from df2 where 'Timestamps:' column starts with 'TEMP' or 'UNEXPECTED'
        df2 = df2[~df2['Timestamps:'].str.startswith('TEMP')]
        df2 = df2[~df2['Timestamps:'].str.startswith('UNEXPECTED')]
        df2["Timestamps:"] = df2["Timestamps:"].apply(lambda x: add_comma_if_words(x)) # Add commas after specific words in 'Timestamps:' column

        df2[["Event", "Time"]] = df2["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", "))) # Split 'Timestamps:' column into 'Event' and 'Time' columns
        df2.drop("Timestamps:", axis=1, inplace=True)
        df2["Time"] = df2['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True) # Replace date format in 'Time' column
        df2[["Date", "Time"]] = df2["Time"].apply(lambda x: pd.Series(str(x).split(", "))) # Split 'Time' column into 'Date' and 'Time' columns
        format_time_column(df2, "Time")

        # Check for e in time
        # result = check_for_e_in_column(df2['Time'], 7)
        # if isinstance(result, int):
        #     print(df2[result])

        df2["Time_subseconds"] = df2['Time'].apply(time_to_seconds_subseconds) # Convert 'Time' to seconds and subsecond

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

        # For temperature graph
        # Filter rows in df2_new_temp to exclude 'READ_TIME' and 'SET_TIME' events
        df2_new_temp["Timestamps:"] = df2_new_temp["Timestamps:"].apply(lambda x: add_comma_if_words(x))
        df2_new_temp[["Event", "Time"]] = df2_new_temp["Timestamps:"].apply(lambda x: pd.Series(str(x).split(", ")))
        df2_new_temp.drop("Timestamps:", axis=1, inplace=True)
        df2_new_temp["Time"] = df2_new_temp['Time'].str.replace(r'(\d{4}-\d{2}-\d{2})', r'\1,', regex=True)
        df2_new_temp[["Temperature", "Time"]] = df2_new_temp["Time"].apply(lambda x: pd.Series(str(x).split(", ")))

        # Initialize list to store rows to delete
        ## Handling unexpected timestamps
        rows_to_delete = []
        for index, row in df2_new_temp.iterrows():

            if row['Event'] == "UNEXPECTED_TIMESTAMP":
                # Check previous row for related event types

                if index > 0:
                    prev_row = df2_new_temp.loc[index - 1]
                    # If the previous row has a related event type, add its index to the list
                    if prev_row['Event'] in ['PUFF_ON', 'TOUCH_ON', 'TEMPERATURE_ON']:
                        rows_to_delete.append(index - 1)

                # Check following row for related event types
                if index < len(df) - 1:
                    next_row = df2_new_temp.loc[index + 1]
                    # If the following row has a related event type, add its index to the list
                    if next_row['Event'] in ['PUFF_OFF', 'TOUCH_OFF', 'TEMPERATURE_OFF']:
                        rows_to_delete.append(index + 1)

                rows_to_delete.append(index)

        # Drop rows identified for deletion
        df2_new_temp.drop(index=rows_to_delete, inplace=True)
        df2_new_temp = df2_new_temp.reset_index(drop=True)

        # Find the NaN values in the 'Time' column of 'TEMPERATURE_ON' row
        for index, row in df2_new_temp.iterrows():
            # Check if the current row's event is 'TEMPERATURE_ON' and the time is NaN
            if (row['Event'] == 'TEMPERATURE_ON') and pd.isna(row['Time']):
                # Check if the time value two rows above the current row is not NaN
                # if not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                if index >= 2 and not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                    # If the condition is met, fill the NaN time with the time from two rows above
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index - 2, 'Time']
            # Check if the current row's event is 'TEMPERATURE_OFF' and the time is NaN
            if (row['Event'] == 'TEMPERATURE_OFF') and pd.isna(row['Time']):
                # Check if the time value two rows above the current row is not NaN
                # if not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                if index >= 2 and not pd.isna(df2_new_temp.at[index - 2, 'Time']):
                    # If the condition is met, fill the NaN time with the time from two rows above
                    df2_new_temp.at[index, 'Time'] = df2_new_temp.at[index - 2, 'Time']

        format_time_column(df2_new_temp, "Time") # Format the 'Time' column of the DataFrame df2_new_temp
        df2_new_temp["Time_subseconds"] = df2_new_temp['Time'].apply(time_to_seconds_subseconds) # Convert the 'Time' column to seconds with subseconds
        df2_new_temp['Date'] = pd.to_datetime(df2_new_temp['Temperature'], errors='coerce')
        # Iterate over each row in the DataFrame df2_new_temp
        for index, row in df2_new_temp.iterrows():
            # Check if the 'Event' is 'TEMPERATURE_ON' and 'Date' is NaN
            if (row['Event'] == 'TEMPERATURE_ON' and pd.isna(row['Date'])):
                # If conditions are met, set the 'Date' value of the current row to
                # the 'Date' value from two positions above (using index - 2)
                df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
            # Check if the 'Event' is 'TEMPERATURE_OFF' and 'Date' is NaN
            if (row['Event'] == 'TEMPERATURE_OFF' and pd.isna(row['Date'])):
                # If conditions are met, set the 'Date' value of the current row to
                # the 'Date' value from two positions above (using index - 2)
                df2_new_temp.at[index, 'Date'] = df2_new_temp.at[index - 2, 'Date']
        df2_new_temp['Temperature'] = df2_new_temp['Temperature'].apply(lambda x: 0 if pd.to_datetime(x, errors='coerce') is not pd.NaT else x)
        df2_new_temp['Time'] = df2_new_temp['Time'].apply(lambda x: format_time(x))
        # Drop rows where 'Time' contains "Invalid Time Format"
        df2_new_temp = clean_invalid_time_rows(df2_new_temp)

        df2_new_temp["Time_round"] = df2_new_temp['Time'].apply(round_to_nearest_second) # Round 'Time' values to the nearest second
        df2_new_temp['Time_in_seconds'] = df2_new_temp['Time_round'].apply(convert_to_seconds) # Convert 'Time_round' values to seconds

        df2['Time'] = df2['Time'].apply(lambda x: format_time(x))
        # Drop rows where 'Time' contains "Invalid Time Format"
        df2 = clean_invalid_time_rows(df2)

        df_v2 = pd.DataFrame(data=[["0", "0", "0", "0"]], columns=["Event", "Date", "Range", "Duration_in_seconds"])
        duration = 0



        string1 = 'PUFF_ON'
        string2 = 'PUFF_OFF'
        string3 = 'TOUCH_ON'
        string4 = 'TOUCH_OFF'
        df2.reset_index(drop=True, inplace=True) # Reset index of DataFrame df2
        for index, row in df2.iterrows():
            # Check if the current row is the event of "TOUCH_ON" and the next row is the event of "TOUCH_OFF"
            if index + 1 < len(df2) and row["Event"] == string3 and df2.loc[index + 1, 'Event'] == string4:
                # Define the new row with event type, date, time range, and duration in seconds of that event
                new_row = pd.Series({'Event': "TOUCH", 'Date': row["Date"],
                                        'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                        'Duration_in_seconds': str(
                                            df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                # Append the new row to DataFrame df_v2
                df_v2.loc[df_v2.index.max() + 1] = new_row
            # Check if the current row is the event of "PUFF_ON" and the next row is the event of "PUFF_OFF"
            if index + 1 < len(df2) and row["Event"] == string1 and df2.loc[index + 1, 'Event'] == string2:
                # Define the new row with event type, date, time range, and duration in seconds of that event
                new_row = pd.Series({'Event': "PUFF", 'Date': row["Date"],
                                        'Range': str(row["Time"]) + "-" + str(df2.loc[index + 1, 'Time']),
                                        'Duration_in_seconds': str(
                                            df2.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"])})
                # Append the new row to DataFrame df_v2
                df_v2.loc[df_v2.index.max() + 1] = new_row

        df_v2 = df_v2.iloc[1:].reset_index(drop=True)
        # Convert 'Duration_in_seconds' to milliseconds and round to one decimal place
        df_v2['Duration(ms)'] = df_v2['Duration_in_seconds'].apply(seconds_to_milliseconds)
        df_v2['Duration(ms)'] = df_v2['Duration(ms)'].astype(float).round(1)
        # Drop the 'Duration_in_seconds' column from DataFrame df_v2
        df_v2 = df_v2.drop('Duration_in_seconds', axis=1)

        ##Update the status bar
        self.read_status.config(text="Save timestamps and generating plots", background="lightgreen")
        ## ask for the location to save the converted file 1
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])
        ##add postfixes with the file name
        if _fname:
            _fname = _fname.split(".")[0]+"_converted.txt"
            file_name3=_fname.split(".")[0]+"_duration.txt"


        ##Write dataframes into files
        current_time = DT.datetime.now()

        with open(_fname, 'w') as f2:
            for i in range(self.lb_rx.size()):
                ## add internal timestamps into the files to write
                if ((str(self.lb_rx.get(i))[0:8]) == "Internal"):
                    tm2 = self.lb_rx.get(i)[0:40]
            #f2.write(str(tm2) + "\n")
            f2.write(str("Local Time: " + str(current_time) + "\n"))
            f2.write(df3.to_string(index=False) + "\n")
        with open(file_name3, 'w') as f3:
            f3.write(df_v2.to_string(index=False) + "\n")        
        
        
        df2["Time_round"] = df2['Time'].apply(round_to_nearest_second)
        df2['Time_in_seconds'] = df2['Time_round'].apply(convert_to_seconds)



        plot_type=self.cb_plot.get() # Get the selected plot type from the plot type combo box
        # Check if the selected plot type is "Stem"
        if plot_type=="Stem":
            # Define a function to generate the stem plot graph
            def generate_graph(df2_new_temp):

                unique_dates = df2['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame
                # Define x-axis ticks and labels for a 24-hour time span
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
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    print(date)
                    date = str(date)[:10] # Extract date part from datetime
                    total_duration = 0
                    dur_gth = 0
                    number_of_puff = 0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]
                    # Initialize arrays to store time matrix for different events
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
                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): ## if any puff duration is greater or equal that the specified minimum puff duration
                                dur_gth += duration # calculate the duration within the condition
                                number_of_puff += 1 # calculate puff frequency within the condition
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            # Mark the time range of TOUCH events on the time matrix
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF event
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})

                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        # Stem plot for puffing events exceeding the threshold duration
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ', basefmt=' ',
                                                              linefmt='g', label='PUFF> {}'.format(puff_duration+"s"))
                        stemline.set_linewidth(10)
                        # ax1.bar(np.arange(86400), time_matrix1, align='center', width=1, color='red', label='Puff')
                        # ax1.plot(np.arange(86400), time_matrix1, linewidth=1, color='red', label='Puff')
                        # Stem plot for puffing events below the threshold duration
                        ax1.stem(np.arange(86400), time_matrix11, markerfmt=' ',basefmt=' ', linefmt='r', label='PUFF< {}'.format(puff_duration+"s"))

                    if option == "Display puffs that exceed the threshold":
                        # Stem plot for puffing events exceeding the threshold duration
                        markerline, stemline, baseline = ax1.stem(np.arange(86400), time_matrix1, markerfmt=' ',
                                                                  basefmt=' ',
                                                                  linefmt='g',
                                                                  label='PUFF> {}'.format(puff_duration + "s"))
                        stemline.set_linewidth(10)

                    #ax1.set_ylabel(date)
                    # Set title and labels for the subplot
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Stem plot for TOUCH events on another subplot
                    ax2.stem(np.arange(86400), time_matrix2, markerfmt=' ',basefmt=' ', linefmt='b', label="TOUCH")
                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.set_ylim(0, 1.1)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()

                    # Stem plots for temperature on other subplots
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

                    # Annotate temperature values on the plots
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


                    ## find the maximum and minimum value for setting y axis in temparature graph
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3 =0
                    if len(non_zero_values31) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                        min_matrix4 = min(non_zero_values4)
                    else:
                        min_matrix4 = 0
                    if len(non_zero_values41) != 0:
                        min_matrix41 = min(non_zero_values41)
                    else:
                        min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()

                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)


                return ax1, ax3, ax2, ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        if plot_type == "Step": # Check if the selected plot type is "Step"
            # Define a function to generate the step plot graph
            def generate_graph(df2_new_temp):

                unique_dates = df2['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame

                # Define x-axis ticks and labels for a 24-hour time span
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
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    print(date)
                    date = str(date)[:10] # Extract date part from datetime
                    # Initialize variables for total duration, duration above threshold, and number of puffs
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    # Initialize arrays to store time matrix for different events
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
                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[
                            index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): ## if any puff duration is greater or equal than the specified minimum puff duration
                                dur_gth += duration # calculate the duration within the condition
                                number_of_puff += 1 # calculate puff frequency within the condition
                                # Mark the time range of PUFF events on the time matrix
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[
                            index + 1, 'Event'] == string4:
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[
                            index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF event
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                       # Step plot for puffing events exceeding the threshold duration
                       ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                       # Step plot for puffing events below the threshold duration
                       ax1.step(np.arange(86400), time_matrix11, where='post', color="red", label='PUFF< {}'.format(puff_duration + "s"))
                       ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)
                       ax1.fill_between(np.arange(86400), time_matrix11, step="post", color='red', alpha=0.5)

                    if option=="Display puffs that exceed the threshold":
                        # Step plot for puffing events exceeding the threshold duration
                        ax1.step(np.arange(86400), time_matrix1, where='post', color="green", label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, step="post", color='green', alpha=0.5)

                    # Set title and labels for the subplot
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")

                    #ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Step plot for TOUCH events on another subplot
                    ax2.step(np.arange(86400), time_matrix2, where='post', label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, step="post", color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    #ax2.set_xticks(np.array(x_ticks), np.array(x_labels), fontsize=10)
                    ax2.legend()
                    #ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")
                    plt.tight_layout()
                    # Stem plots for temperature on other subplots
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

                    # Annotate temperature values on the plots
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

                    ## find the maximum and minimum value for setting y axis for temperature
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3 =0
                    if len(non_zero_values31) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                        min_matrix4 = min(non_zero_values4)
                    else:
                        min_matrix4 = 0
                    if len(non_zero_values41) != 0:
                        min_matrix41 = min(non_zero_values41)
                    else:
                        min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)

                # Return the created subplots
                return ax1, ax3, ax2, ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        # Check if the selected plot type is "Line"
        if plot_type == "Line":
            # Define a function to generate the line plot graph
            def generate_graph(df2_new_temp):

                unique_dates = df2['Date'].unique() # Get unique dates from the 'Date' column of the DataFrame

                # Define x-axis ticks and labels for a 24-hour time span
                x_ticks = [0,1800, 3600,5400,7200,9000,10800,12600,14400,16200,18000,19800,21600,23400,25200,27000,28800,30600,32400,34200,
                           36000,37800,39600,41400,43200,45000,46800,48600,50400,52200,54000,55800,57600,59400,61200,63000,64800,66600,68400,70200,72000,73800,75600,77400,79200,81000,82800,84600,86400,86460]
                x_labels = ["00:00","00:30", "01:00","01:30", "02:00","02:30","03:00","03:30","04:00","04:30", "05:00","05:30", "06:00", "06:30","07:00","07:30", "08:00","08:30","09:00","09:30",
                            "10:00","10:30","11:00","11:30", "12:00","12:30","13:00", "13:30", "14:00","14:30", "15:00","15:30", "16:00","16:30" ,"17:00","17:30", "18:00","18:30", "19:00","19:30", "20:00","20:30",
                            "21:00","21:30","22:00","22:30", "23:00","23:30","24:00","24:01"]

                puff_duration = 0
                # Get puff duration from the entry widget
                puff_duration = self.en_puff.get()
                # Iterate over each unique date
                for date in unique_dates:
                    #print(date)
                    date = str(date)[:10] # Extract date part from datetime
                    # Initialize variables for total duration, duration above threshold, and number of puffs
                    total_duration = 0
                    dur_gth=0
                    number_of_puff=0
                    # Get the rows with the current date
                    rows = df2_new_temp[df2_new_temp['Date'] == date]

                    # Initialize arrays to store time matrix for different events
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

                    # Iterate over each row in the filtered DataFrame
                    for index, row in rows.iterrows():
                        # Check if the current row and the next row form a PUFF event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string1 and df2_new_temp.loc[index + 1, 'Event'] == string2:
                            # Calculate duration between PUFF_ON and PUFF_OFF events
                            duration = df2_new_temp.loc[index + 1, 'Time_subseconds'] - row["Time_subseconds"]
                            total_duration += duration
                            if float(duration) >= float(puff_duration): # if any puff duration is greater or equal that the specified puff duration
                                dur_gth += duration # calculate the duration within the condition
                                number_of_puff += 1 # calculate puff frequency within the condition
                                # Mark the time range of PUFF events on the time matrix
                                start_index = row["Time_in_seconds"]
                                end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix1[start_index:end_index + 1] = 1
                            else:
                                # Mark the time range of PUFF events below threshold on the time matrix
                                start_index11 = row["Time_in_seconds"]
                                end_index11 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                                time_matrix11[start_index11:end_index11 + 1] = 1
                        # Check if the current row and the next row form a TOUCH event
                        if index + 1 < len(df2_new_temp) and row['Event'] == string3 and df2_new_temp.loc[ index + 1, 'Event'] == string4:
                            # Mark the time range of TOUCH events on the time matrix
                            start_index = row["Time_in_seconds"]
                            end_index = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            time_matrix2[start_index:end_index + 1] = 1

                        # Check if the current row and the next row form a TEMPERATURE_ON and TEMPERATURE_OFF event pair
                        if index + 1 <= len(df2_new_temp) and row['Event'] == string5 and df2_new_temp.loc[index + 1, 'Event'] == string6:
                            # Get the start and end time indices for the temperature event pair
                            start_index3 = row["Time_in_seconds"]
                            end_index3 = df2_new_temp.loc[index + 1, 'Time_in_seconds']
                            # handling corrupt timestamps in graph. Check the preceding event before setting temperature values
                            if df2_new_temp.loc[index - 1, 'Event'] == "PUFF_OFF":
                                # Set temperature values in time matrix for PUFF_OFF even
                                time_matrix3[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix31[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']
                            if df2_new_temp.loc[index - 1, 'Event'] == "TOUCH_OFF":
                                # Set temperature values in time matrix for TOUCH_OFF event
                                time_matrix4[start_index3] = df2_new_temp.loc[index, 'Temperature']
                                time_matrix41[end_index3] = df2_new_temp.loc[index + 1, 'Temperature']

                    # Convert total duration above threshold to string format with 4 decimal places
                    dur_gth = f"{dur_gth:.4f}"
                    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,gridspec_kw={'height_ratios': [1, 1, 5]})
                    # Create a figure with subplots for each type of event
                    fig, (ax1, ax3, ax2, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 2]})
                    # Display puffing events on the first subplot
                    option = self.cb_plot_puff.get()
                    if option == "Display all puffing events":
                        # Line plot for puffing events exceeding the threshold duration
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        # Line plot for puffing events below the threshold duration
                        ax1.plot(np.arange(86400), time_matrix11, color="red",
                                 label='PUFF< {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                        ax1.fill_between(np.arange(86400), time_matrix11, color='red', alpha=0.5)
                    if option == "Display puffs that exceed the threshold":
                        # Line plot for puffing events exceeding the threshold duration
                        ax1.plot(np.arange(86400), time_matrix1, color="green",
                                 label='PUFF> {}'.format(puff_duration + "s"))
                        ax1.fill_between(np.arange(86400), time_matrix1, color='green', alpha=0.5)
                    # Set title and labels for the subplot
                    ax1.legend()
                    ax1.set_ylim(0, 1.1)
                    ax1.set_xlabel("Time")
                    # ax1.set_ylabel(date)
                    ax1.set_title("Date: " + str(date) + " ,Total puffing time above threshold: " + str(
                        dur_gth) + 's' + "," + "Num of Puffs above threshold: " + str(number_of_puff))
                    ax2.set_xticks(x_ticks)
                    ax2.set_xticklabels(x_labels)

                    # Set minor ticks and labels
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

                    # Set the size of the figure
                    fig.set_size_inches(17, 7)

                    # Line plot for TOUCH events on another subplot
                    ax2.plot(np.arange(86400), time_matrix2, color="blue", label="TOUCH")
                    ax2.fill_between(np.arange(86400), time_matrix2, color='blue', alpha=0.5)
                    ax2.set_ylim(0, 1.1)

                    ax2.legend()
                    # ax2.set_ylabel(date)
                    ax2.set_xlabel("Time")

                    # Stem plots for temperature on other subplots
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

                    # Annotate temperature values on the plots
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


                    ## find the maximum and minimum value for setting y axis in temperature graph
                    max_matrix3 = max(time_matrix3)
                    max_matrix31 = max(time_matrix31)

                    non_zero_values3 = [x for x in time_matrix3 if x != 0]
                    non_zero_values31 = [x for x in time_matrix31 if x != 0]

                    if len(non_zero_values3) != 0:
                        min_matrix3 = min(non_zero_values3)
                    else:
                        min_matrix3=0
                    if len(non_zero_values3) != 0:
                        min_matrix31 = min(non_zero_values31)
                    else:
                        min_matrix31=0

                    max_combined3 = max(max_matrix3, max_matrix31)
                    min_combined3 = min(min_matrix3, min_matrix31)

                    max_matrix4 = max(time_matrix4)
                    max_matrix41 = max(time_matrix41)

                    non_zero_values4 = [x for x in time_matrix4 if x != 0]
                    non_zero_values41 = [x for x in time_matrix41 if x != 0]

                    if len(non_zero_values4) != 0:
                       min_matrix4 = min(non_zero_values4)
                    else:
                       min_matrix4=0
                    if len(non_zero_values41) != 0:
                       min_matrix41 = min(non_zero_values41)
                    else:
                       min_matrix41=0

                    max_combined4 = max(max_matrix4, max_matrix41)
                    min_combined4 = min(min_matrix4, min_matrix41)

                    # Set y-axis labels and limits for temperature subplots
                    ax3.set_ylabel("Temp for puff")
                    ax3.set_ylim(min_combined3 - 10, max_combined3 + 10)
                    ax3.legend()

                    ax4.set_ylabel("Temp for touch")
                    ax4.set_ylim(min_combined4 - 10, max_combined4 + 10)
                    ax4.legend()
                    # Adjust layout and display the plots
                    plt.tight_layout()
                    plt.show(block=False)

                # Return the created subplots
                return ax1, ax3, ax2, ax4

            # Generate the graph using the provided DataFrame
            ax1, ax3, ax2, ax4 = generate_graph(df2_new_temp=df2_new_temp)
            # Update status text to indicate plot generation completion
            self.read_status.config(text="Plot generation Done", background="lightgreen")
            plt.show()

        self.read_status.config(text="Ready", background="lightgray")

    # Define a method to send the character 'e' to the serial port
    def send_text_btn_e(self):
        _send_data_e = "e"
        # Encode the character 'e' and send it to the serial port
        self.serialcom.serial.write(_send_data_e.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_e)
        self.btn_yes.config(state="normal")
        self.btn_read.config(state="disabled")

    # Define a method to send the character 'y' to the serial port
    def send_text_btn_y(self):
        _send_data_y = "y"
        # Encode the character 'y' and send it to the serial port
        self.serialcom.serial.write(_send_data_y.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_y)
        self.btn_read.config(state="disabled")

    def send_text_btn_s(self):
        # Get the current time and convert it to a Unix timestamp
        current_time = DT.datetime.now()
        unix_timestamp = (DT.datetime.timestamp(current_time))
        # Separate the integer and fractional parts of the Unix timestamp
        frac, whole = math.modf(unix_timestamp)
        # Convert the integer part to hexadecimal and extract the relevant portion
        unix_1 = hex(int(whole))[2:]  # unix_1 = hex(int(str(whole)[0:-2]))[2:]

        # Convert the fractional part to hexadecimal and extract the relevant portion
        unix_2 = hex(int(frac * 1_000_000))[2:]  # unix_2 = hex(int(str(frac)[2:]))[2:]
        # Construct the data to be sent ('s' + first part of Unix timestamp + second part of Unix timestamp)
        _send_data_s = "s" + str(unix_1) + str(unix_2)
        # Encode the data and send it to the serial port
        self.serialcom.serial.write(_send_data_s.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_s)
        self.btn_read.config(state="disabled")

    # Define a method to send the character 't' to the serial port
    def send_text_btn_t(self):
        _send_data_t = "t"
        # Encode the character 't' and send it to the serial port
        self.serialcom.serial.write(_send_data_t.encode("utf-8"))
        # self.lb_tx.insert(tk.END, _send_data_t)
        self.btn_read.config(state="disabled")




if __name__ == "__main__":
    global t2
    root = tk.Tk()
    root.title("FRIENDS GUI")
    Application(master=root)

    root.mainloop()

#%%

#%%

#%%

#%%
