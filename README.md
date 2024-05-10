
# FRIENDS GUI

FRIENDS (Flexible Robust Instrumentation of Electronic Nicotine Delivery Systems) GUI is created using the Tkinter toolkit in Python to monitor the vaping behaviour of ENDS users. The software establishes serial communication between a hardware sensor-based FRIENDS device and a computer, and also offers users the flexibility to control parameters for data collection, extraction, conversion into a human-readable format, and visualization of vaping metrics such as puff frequency and duration over an entire day for better interpretation.



![App Screenshot](https://github.com/eszsonic/FRIENDSGUI/blob/master/Screenshots/main_window.png?raw=true)




## Functionalities

- Status Bar: It shows the connectivity status between the computer and the FRIENDS device. It turns into “green” and shows “connected” when the connection between the two devices have been established after selecting the appropriate COM port and baud rate (115200).

- COM Port: Appropriate COM port should have been selected for establishing the connection for a particular FRIENDS device.

- Baudrate: For the FRIENDS device, the baud rate will be 115200.

- COM Port: If the appropriate com port for the device doesn’t show up in the options, reload button should be pressed to get the appropriate com port.

- Reload: If the appropriate com port for the device doesn’t show up in the options, reload button should be pressed to get the appropriate com port.

- Connect: After setting the com port and baud rate, connect button should be pressed to establish the connection between the computer and the FRIENDS device.

- Disconnect: To turn off the connection, disconnect button should be pressed.

- Minimum puffing duration: By setting the threshold (minimum puffing duration) , user can separate the puffing events in the plots based on this threshold. By default, the value of this entry is 0.0. There are two options to show the puffing events in the plot based on the threshold.

        - Display all puffing events
        - Display puffs that exceed the threshold
  1st option will show all the puffing events in the plots.
          Example: For minimum puffing duration 1.0 s:
![App Screenshot](https://github.com/eszsonic/FRIENDSGUI/blob/master/Screenshots/graph_1.png?raw=true)
   2nd option will show the puffing events that only exceed the specified minimum puffing duration, 
           Example: For minimum puffing duration 1.0s
![App Screenshot](https://github.com/eszsonic/FRIENDSGUI/blob/master/Screenshots/graph_2.png?raw=true)

- Plot types: Three types of plot (Line, Stem, and Step) are available for user selection to generate the plots.

- Read Time: This button returns the device’s actual time in extended POSIX format. It shows the timestamps in the Rx monitor of the GUI. 

- Set Time: This button set the local time in POSIX format to the device. 

- Erase flash: This button will erase the device’s flash memory. It requires a confirmation (YES) and “Yes” button will be enabled after pressing “Erase” button. 

- Start Data Collection: This button should be pressed before start collecting the data. It will set the local time in POSIX format to the device and erase the flash memory of the device and make it ready to start the data collection. 

- Read Data: After pressing the “Read Data” button, the data from the device will be read in the RX monitor.

- File Conversion: This button converts the original timestamps to human-readable time, extracts vaping metrices, and generates the plots. It creates two text files.

         - File 1: It contains the local time in human readable format (e.g., Local Time: 2023-06-05 13:06:47.836938), and event’s timestamps in human readable format (converted) 
         - File 2: It contains a data table with four columns (Event, Date, Range, Duration(ms)). One can find each complete event’s occurring date, time range and duration from this table. Example:
    ![App Screenshot](https://github.com/eszsonic/FRIENDSGUI/blob/master/Screenshots/file_3.png?raw=true)

- Clear: This button will clear all the text in RX monitor

- Save data and generate plots:  After pressing the “Read Data” button, the data from the device will be read in the RX monitor. For saving those data, user should click on “Save data and generate plots” button. The raw data will be saved in a text file and converted ones will also be generated.
The system will generate the plots from the data. The number of plots depends on the number of days in the data (one plot for one day). Time from 00:00 to 24:00 represents the horizontal x-axis.

- Data Status Bar: It shows the status while performing the functionality of “Read Data”, “File Conversion”, and “Save data and generate plots” button.

## Dependencies
The Graphical user interface was created with the [Tkinter](https://docs.python.org/3/library/tkinter.html) framework.

Dependencies for Python program:
- [Python](https://www.python.org/) version 3.9+
- [matplotlib](https://pypi.org/project/matplotlib/)==3.7.1
- [numpy](https://pypi.org/project/numpy/)==1.24.3
- [pandas](https://pypi.org/project/pandas/)==2.0.1
- [pyserial](https://pypi.org/project/pyserial/)==3.5
- [datetime](https://pypi.org/project/DateTime/)==5.5











## Run Locally

Clone the project

```bash
  https://github.com/eszsonic/FRIENDSGUI.git
```

Go to the project directory

```bash
  cd FRIENDSGUI\FRIENDS Serial Monitor
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the application

```bash
  python main_gui.py
```


## Authors and Acknowledgements

- [Shehan Irteza Pranto](https://sites.google.com/view/shehanirteza/)
- [Dr. Larry Hawk](https://arts-sciences.buffalo.edu/psychology/faculty/faculty-directory/hawk.html)
- [Dr. Edward Sazonov](https://eng.ua.edu/eng-directory/dr-edward-sazonov/)

Shehan Irteza Pranto was responsible for the programming aspects in creating the original software. Dr. Edward Sazonov was the primary supervisor over this project, with Dr. Larry Hawk as secondary supervisor. 


## License

FRIENDS_GUI is released under the [MIT License](https://opensource.org/license/mit) 


## FAQ

#### What to do before giving the device to any participant?
Answer:
-	Connect the device to the computer via USB
-	Open FRIENDS serial communication app.
-	Select appropriate COM port and baud rate (115200) and press connect
-	Press “Start Data Collection Button”. It will set the internal time to the device and put a request to erase the storage (flash)
-	Press “Yes” button to erase the flash.


#### Is it required to install python programming language to use this software?

Answer: Yes, you need to have Python installed on your computer, preferably version 3.11. Please check the [Python installation process](https://www.geeksforgeeks.org/how-to-install-python-on-windows/).


