import RPi.GPIO as GPIO
import time
from datetime import datetime
from python.HR8825 import HR8825
from guizero import App, Text, PushButton, Combo, info, Window, TextBox
import serial

# Initialize motors
Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor1.SetMicroStep('hardward', 'fullstep')

# GPIO setup for valves
VENT_VALVE_PIN = 18       # Vent to outside
VACUUM_VALVE_PIN = 23     # Vacuum line to clear chamber
CHAMBER_VALVE_PIN = 24    # Access to chamber
VAPE_VALVE_PIN = 25       # Access to vape
GPIO.setmode(GPIO.BCM)
GPIO.setup(VENT_VALVE_PIN, GPIO.OUT)
GPIO.setup(VACUUM_VALVE_PIN, GPIO.OUT)
GPIO.setup(CHAMBER_VALVE_PIN, GPIO.OUT)
GPIO.setup(VAPE_VALVE_PIN, GPIO.OUT)

# Initialize all valves to closed state
GPIO.output(VENT_VALVE_PIN, GPIO.LOW)
GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)
GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW)
GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)

# Default values
volume = 120  # Volume of puffs in mL
inhale_time = 3  # Time of inhale in seconds
exhale_time = 3  # Time of exhale in seconds
in_flowrate = volume / inhale_time
out_flowrate = volume / exhale_time
chamber_interpuff_time = 0  # Time between puffs sent to the chamber
chamber_number_puffs = 1  # Number of puffs sent to the chamber
free_interpuff_time = 18  # Time between puffs with vent valve open
free_number_puffs = 24  # Number of puffs with vent valve open
num_chambered_seq = 5  # Number of chambered puff sequences performed (with free puffs in between)

# Timing parameters
hold_time = 0.5  # Hold time between inhale/exhale in seconds
vent_open_time = 10 # Time vent valve will remain open for first puff
chamber_hold_time = 120  # Time aerosol will be trapped in chamber before clearing
chamber_clear_time = 720  # Time vacuum valve will be open for to clear chamber - CHANGE IF NEEDED
line_clear_time = 5 # Time after chamber clear to ensure no residual aerosol in tubimg

# Constraints
max_volume = 450  # Max volume of syringe

# Motor control functions
def inhale(motor, steps, speed):
    """Forward motion = inhale"""
    motor.TurnStep(Dir='forward', steps=steps, stepdelay=speed)

def hold(duration):
    """Pause for the specified duration."""
    time.sleep(duration)

def exhale(motor, steps, speed):
    """Backward motion = exhale"""
    motor.TurnStep(Dir='backward', steps=steps, stepdelay=speed)

def initialize_scale(port="/dev/ttyUSB0"):
    scale = serial.Serial(port, baudrate=9600, timeout=0.5)
    time.sleep(2.0)  # let serial connection settle
    scale.reset_input_buffer()
    return scale

def parse_mass_line(line):
    """
    Convert a raw balance string into a float mass in grams.

    Example inputs:
        "+   84.413g"
        "84.413g"
        "-   0.002g"

    Returns:
        float mass in grams, or None if the line is invalid/partial.
    """
    line = line.strip()

    # Must contain grams
    if "g" not in line.lower():
        return None

    # Remove unit and extra spaces
    mass_part = line.lower().replace("g", "").strip()

    # Remove internal spaces, e.g. "+   84.413" -> "+84.413"
    mass_part = mass_part.replace(" ", "")

    try:
        return float(mass_part)
    except ValueError:
        return None

def read_scale_latest(scale, duration=2.0):
    # Flush stale data, then collect fresh readings
    scale.reset_input_buffer()
    time.sleep(0.5)
    scale.reset_input_buffer() # Flush again to start clean

    readings = []
    end_time = time.time() + duration

    while time.time() < end_time:
        raw = scale.readline()
        line = raw.decode("utf-8", errors="ignore").strip()
        mass = parse_mass_line(line)
        if mass is not None:
            readings.append((line, mass))
    if not readings:
        return None, None

    return readings[-1]

def log_mass(scale, log_file, puff_number, puff_type, timing_label, retries=2, retry_delay=2.0):

    for attempt in range(retries):
        line, mass = read_scale_latest(scale)
        if mass is not None:
            break
        print(f"WARNING: Read attempt {attempt + 1}/{retries} got None - retrying in {retry_delay}s")
        time.sleep(retry_delay)
        try:
            scale.close()
            time.sleep(0.5)
            scale = initialize_scale(scale.port)
            print(f"Scale reinitialized on attempt {attempt+1}")
        except Exception as e:
            print(f"Warning: Failed to reset scale connection: {e}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if mass is not None:
        log_file.write(f"{timestamp},{puff_number},{puff_type},{timing_label},{mass:.3f},{line}\n")
        log_file.flush()
        print(f"{timestamp},{puff_number},{puff_type},{timing_label},{mass:.3f},{line}")
    else:
        log_file.write(f"{timestamp},{puff_number},{puff_type},{timing_label},NONE,NONE\n")
        log_file.flush()
        print(f"WARNING: All {retries} read attempts failed for puff {puff_number} ({timing_label})")
        
    return scale

def puff_sequence(motor, steps_forward, steps_backward, inhale_delay, exhale_delay, hold_time,
                  chamber_interpuff_time, chamber_number_puffs, free_interpuff_time, free_number_puffs, num_chambered_seq):
    """Performs puff sequence with chambered and free puffs"""
    # First puff: clear with vent valve open (not included in programmed puffs)
    print("Performing first puff (Vent valve open)")
    status_text.value = "Performing first puff (Vent valve open)"
    app.update()
   
    # First puff - only vent valve will open for puffs
    # Initialize with all vents closed
    GPIO.output(VENT_VALVE_PIN, GPIO.LOW)
    GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW)
    GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)
    GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)

    # Initialize the scale
    scale = initialize_scale(port="/dev/ttyUSB0")
    log_name = datetime.now().strftime("mass_log_%m%d%Y_%H%M%S.csv")
    log_file = open(log_name, "w", newline="")
    log_file.write("timestamp,puff_number,puff_type,timing_label,mass_g,raw_mass\n")
    log_file.flush()

    puff_counter = 0

    GPIO.output(VAPE_VALVE_PIN, GPIO.HIGH)  # Open vape valve
    inhale(motor, steps_forward, inhale_delay)
    GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)   # Close vape valve
    GPIO.output(VENT_VALVE_PIN, GPIO.HIGH)  # Open vent valve
    hold(hold_time)
    exhale(motor, steps_backward, exhale_delay)
    time.sleep(vent_open_time)
    GPIO.output(VENT_VALVE_PIN, GPIO.LOW)  # Close vent valve
    GPIO.output(VACUUM_VALVE_PIN, GPIO.HIGH) # Open vacuum line to clear residual
    time.sleep(line_clear_time)
    GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW) # Close vacuum valve
   
    time.sleep(vent_open_time)
   
    num_chambered_seq_remaining = num_chambered_seq

    # Cycle between chambered puffs and free puffs
    for cycle in range(num_chambered_seq):
        print(f"Starting sequence {cycle + 1} of {num_chambered_seq}")
        status_text.value = f"Starting sequence {cycle + 1} of {num_chambered_seq}"
        app.update()

        # Chambered puffs - only chamber valve will open
        # Initialize with all vents closed
        GPIO.output(VENT_VALVE_PIN, GPIO.LOW)
        GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW)
        GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)
        GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)
       
        for i in range(chamber_number_puffs):
            print(f"Performing chambered puff {i + 1} of {chamber_number_puffs}")
            status_text.value = f"Chambered puff {i + 1} of {chamber_number_puffs} (Cycle {cycle + 1}/{num_chambered_seq})"
            app.update()
           
            GPIO.output(VAPE_VALVE_PIN, GPIO.HIGH)  # Open vape valve
            inhale(motor, steps_forward, inhale_delay)
            GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)  # Close vape valve
            GPIO.output(CHAMBER_VALVE_PIN, GPIO.HIGH) # Open chamber valve
            hold(hold_time)
            exhale(motor, steps_backward, exhale_delay)
           
            # Keep chamber valve open while clearing
            time.sleep(chamber_hold_time)
            GPIO.output(VACUUM_VALVE_PIN, GPIO.HIGH)  # Open vacuum valve (chamber valve remains open)
            time.sleep(chamber_clear_time)
            GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW) # Close chamber valve
            hold(line_clear_time)
            GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)  # Close vacuum valve

        num_chambered_seq_remaining = num_chambered_seq_remaining - 1
       
        # Free puffs - only vent valve will open
        if num_chambered_seq_remaining > 0:

            # Initialize with all vents closed
            GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW)
            GPIO.output(VENT_VALVE_PIN, GPIO.LOW)
            GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)
            GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)

           
            for i in range(free_number_puffs):
                print(f"Performing free puff {i + 1} of {free_number_puffs}")
                status_text.value = f"Free puff {i + 1} of {free_number_puffs} (Cycle {cycle + 1}/{num_chambered_seq})"
                app.update()

                # log mass here 
                puff_counter += 1
                scale = log_mass(scale, log_file, puff_counter, "free", "pre_puff") 

                GPIO.output(VAPE_VALVE_PIN, GPIO.HIGH)  # Open vape valve
                inhale(motor, steps_forward, inhale_delay)
                GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)  # Close vape valve

                GPIO.output(VENT_VALVE_PIN, GPIO.HIGH)  # Open vent valve
                hold(hold_time)
                exhale(motor, steps_backward, exhale_delay)
                GPIO.output(VENT_VALVE_PIN, GPIO.LOW)  # Close vent valve

                hold(5.0)
                scale = log_mass(scale, log_file, puff_counter, "free", "post_puff") # Log mass here for post puff
                hold(free_interpuff_time)

            GPIO.output(VENT_VALVE_PIN, GPIO.LOW) # Close vent valve
            GPIO.output(VACUUM_VALVE_PIN, GPIO.HIGH) # Open vacuum to clear residual
            hold(line_clear_time)
            GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW) # Close vacuum valve
            hold(35)    # Wait before starting more puffs

    print("Puff sequence complete")
    status_text.value = "Puff sequence complete"
    log_file.close()
    scale.close()
    app.update()

    # Ensure all valves are closed and cleanup
    GPIO.output(VENT_VALVE_PIN, GPIO.LOW)
    GPIO.output(CHAMBER_VALVE_PIN, GPIO.LOW)
    GPIO.output(VACUUM_VALVE_PIN, GPIO.LOW)
    GPIO.output(VAPE_VALVE_PIN, GPIO.LOW)
    motor.Stop()
    GPIO.cleanup()


# GUI Functions
def calculate_parameters():
    global volume, inhale_time, exhale_time, in_flowrate, out_flowrate

    selected_option = param_combo.value

    if selected_option == "Volume and Flowrate":
        volume = float(volume_input.value)
        in_flowrate = float(in_flowrate_input.value)
        out_flowrate = float(out_flowrate_input.value)
        inhale_time = volume / in_flowrate
        exhale_time = volume / out_flowrate

        inhale_time_input.value = round(inhale_time, 2)
        exhale_time_input.value = round(exhale_time, 2)

    elif selected_option == "Volume and Duration":
        volume = float(volume_input.value)
        inhale_time = float(inhale_time_input.value)
        exhale_time = float(exhale_time_input.value)
        in_flowrate = volume / inhale_time
        out_flowrate = volume / exhale_time

        in_flowrate_input.value = round(in_flowrate, 2)
        out_flowrate_input.value = round(out_flowrate, 2)

    elif selected_option == "Flowrate and Duration":
        in_flowrate = float(in_flowrate_input.value)
        out_flowrate = float(out_flowrate_input.value)
        inhale_time = float(inhale_time_input.value)
        exhale_time = float(exhale_time_input.value)

        inhale_volume = in_flowrate * inhale_time
        exhale_volume = out_flowrate * exhale_time

        if round(inhale_volume, 2) != round(exhale_volume, 2):
            info("Error", "Inhale and exhale volumes must match. Adjust flow rates or times")
            return None

        volume = inhale_volume
        volume_input.value = round(volume, 2)

    # Recalculate motor steps and delays
    revolutions_forward = volume * (1 / 23.077)
    revolutions_backward = volume * (1 / 23.077)
    steps_forward = int(revolutions_forward * 200)
    steps_backward = int(revolutions_backward * 200)
    inhale_delay = (inhale_time / 2) / steps_forward
    exhale_delay = (exhale_time / 2) / steps_backward

    return steps_forward, steps_backward, inhale_delay, exhale_delay

def start_puffing():
    global chamber_interpuff_time, chamber_number_puffs, free_interpuff_time, free_number_puffs, num_chambered_seq

    # Read values from sliders
    chamber_interpuff_time = float(chamber_interpuff_input.value)
    chamber_number_puffs = int(chamber_number_puffs_input.value)
    free_interpuff_time = float(free_interpuff_input.value)
    free_number_puffs = int(free_number_puffs_input.value)
    num_chambered_seq = int(num_chambered_seq_input.value)

    # Calculate the parameters based on user inputs
    steps_forward, steps_backward, inhale_delay, exhale_delay = calculate_parameters()

    if volume > max_volume:
        info("Error", f"Volume cannot exceed {max_volume} mL. Please select a lower volume.")
        return

    try:
        # Perform puff sequence
        puff_sequence(Motor1, steps_forward, steps_backward, inhale_delay, exhale_delay, hold_time,
                      chamber_interpuff_time, chamber_number_puffs, free_interpuff_time, free_number_puffs, num_chambered_seq)
        info("Success", "Puff sequence complete.")
    except Exception as e:
        info("Error", f"An error occurred: {e}")
        Motor1.Stop()
        GPIO.cleanup()

def update_input_fields():
    """Update the visible input fields based on the selected parameter combination."""
    selected_option = param_combo.value

    # Hide or show fields based on the selected option
    if selected_option == "Volume and Duration":
        in_flowrate_input.disable()
        out_flowrate_input.disable()
        volume_input.enable()
        inhale_time_input.enable()
        exhale_time_input.enable()
   
    elif selected_option == "Volume and Flowrate":
        inhale_time_input.disable()
        exhale_time_input.disable()
        volume_input.enable()
        in_flowrate_input.enable()
        out_flowrate_input.enable()

    elif selected_option == "Flowrate and Duration":
        volume_input.disable()
        in_flowrate_input.enable()
        out_flowrate_input.enable()
        inhale_time_input.enable()
        exhale_time_input.enable()
       
    calculate_parameters()
   
def real_time_update():
    #real time update
    calculate_parameters()

# GUI Setup
app = App(title="VMFRIENDS GUI", width=400, height=550)

Text(app, "Select input parameters")
param_combo = Combo(app, options=["Volume and Duration", "Volume and Flowrate", "Flowrate and Duration"], command=update_input_fields)

Text(app, "Volume (mL)")
volume_input = TextBox(app, text=str(volume))

Text(app, "Inhale Flowrate (mL/s)")
in_flowrate_input = TextBox(app, text=str(in_flowrate))

Text(app, "Exhale Flowrate (mL/s)")
out_flowrate_input = TextBox(app, text=str(out_flowrate))

Text(app, "Inhale Time (s)")
inhale_time_input = TextBox(app, text=str(inhale_time))

Text(app, "Exhale Time (s)")
exhale_time_input = TextBox(app, text=str(exhale_time))

Text(app, "Interpuff Time - Chambered (s)")
chamber_interpuff_input = TextBox(app, text=str(chamber_interpuff_time))

Text(app, "Number of Chamber Puffs")
chamber_number_puffs_input = TextBox(app, text=str(chamber_number_puffs))

Text(app, "Interpuff Time - Free (s)")
free_interpuff_input = TextBox(app, text=str(free_interpuff_time))

Text(app, "Number of Free Puffs")
free_number_puffs_input = TextBox(app, text=str(free_number_puffs))

Text(app, "Number of Chambered Sequences")
num_chambered_seq_input = TextBox(app, text=str(num_chambered_seq))

PushButton(app, text="Start Puffing", command=start_puffing)

status_text = Text(app, text="",size=11)

# Initially disable irrelevant inputs
update_input_fields()

app.display()
