import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime

# Calibration constant for converting ADC to lux (adjust as per your sensor)
K_CONSTANT = 200000  # Example value, replace with your calibrated constant

class SolarTrackingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar Tracking Dashboard")
        self.root.geometry("1200x600")  # Adjusted for more space
        self.root.state("zoomed")  # Start maximized with the taskbar visible

        # Serial connection
        self.serial_connection = None
        self.is_reading = False
        self.serial_monitor_open = False

        # Create GUI components
        self.create_widgets()

        # Start the real-time clock
        self.update_clock()

    def create_widgets(self):
        # Port selection
        port_frame = ttk.LabelFrame(self.root, text="Connect to Arduino", padding=(10, 10))
        port_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(port_frame, text="Select Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_combobox = ttk.Combobox(port_frame, state="readonly", width=30)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.connect_button = ttk.Button(port_frame, text="Connect", command=self.connect_arduino)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        self.disconnect_button = ttk.Button(port_frame, text="Disconnect", state="disabled", command=self.disconnect_arduino)
        self.disconnect_button.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(port_frame, text="Refresh Ports", command=self.refresh_ports).grid(row=0, column=4, padx=5, pady=5)

        # Open/Close Serial Monitor button
        self.open_serial_button = ttk.Button(port_frame, text="Open Serial Monitor", command=self.toggle_serial_monitor)
        self.open_serial_button.grid(row=0, column=5, padx=5, pady=5)

        # Status Indicator (split into two parts for dynamic coloring)
        status_frame = tk.Frame(port_frame)
        status_frame.grid(row=0, column=6, padx=15, pady=5, sticky="e")

        self.status_text_label = ttk.Label(status_frame, text="Status: ", foreground="black")
        self.status_text_label.pack(side="left")

        self.status_value_label = ttk.Label(status_frame, text="Arduino Disconnected", foreground="red")
        self.status_value_label.pack(side="left")

        # Main content frame
        main_content_frame = tk.Frame(self.root)
        main_content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Section: Sensors and Power Distribution
        left_section = tk.Frame(main_content_frame)
        left_section.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Data display for photo resistive sensors
        sensor_frame = ttk.LabelFrame(left_section, text="Photo Resistive Sensors (Illuminance)", padding=(10, 10))
        sensor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.sensor_labels = {}
        sensor_names = [
            "Top Left (lt)",
            "Top Right (rt)",
            "Bottom Left (ld)",
            "Bottom Right (rd)",
            "Overall Average Light Intensity (veg)"
        ]
        for i, name in enumerate(sensor_names):
            ttk.Label(sensor_frame, text=f"  {name}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            self.sensor_labels[name] = ttk.Label(sensor_frame, text="0.00 Lx", font=("Arial", 12), foreground="blue")
            self.sensor_labels[name].grid(row=i, column=1, sticky="w", padx=5, pady=5)

        # Data display for servo motors
        servo_frame = ttk.LabelFrame(left_section, text="Servo Motors (Current Angle)", padding=(10, 10))
        servo_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.servo_labels = {}
        servo_names = [
            "Horizontal (servoh)",
            "Vertical (servov)"
        ]
        for i, name in enumerate(servo_names):
            ttk.Label(servo_frame, text=f"  {name}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            self.servo_labels[name] = ttk.Label(servo_frame, text="0°", font=("Arial", 12), foreground="blue")
            self.servo_labels[name].grid(row=i, column=1, sticky="w", padx=5, pady=5)

        # Data display for power distribution
        power_frame = ttk.LabelFrame(left_section, text="Power Distribution", padding=(10, 10))
        power_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.power_labels = {}
        power_names = [
            "Photo Resistive Sensor (Top Left)",
            "Photo Resistive Sensor (Top Right)",
            "Photo Resistive Sensor (Bottom Left)",
            "Photo Resistive Sensor (Bottom Right)",
            "Servo Motor (Horizontal)",
            "Servo Motor (Vertical)"
        ]
        for i, name in enumerate(power_names):
            ttk.Label(power_frame, text=f"  {name}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            self.power_labels[name] = ttk.Label(power_frame, text="0.00 V", font=("Arial", 12), foreground="blue")
            self.power_labels[name].grid(row=i, column=1, sticky="w", padx=5, pady=5)

        # Right Section: Clock and Serial Monitor
        right_section = tk.Frame(main_content_frame)
        right_section.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Clock Section
        clock_frame = tk.Frame(right_section, bg="black", width=300, height=200)
        clock_frame.pack_propagate(False)
        clock_frame.pack(fill="x", padx=10, pady=10)

        # Center-align clock content
        clock_content = tk.Frame(clock_frame, bg="black")
        clock_content.place(relx=0.5, rely=0.5, anchor="center")

        # Date label (smaller font size)
        self.date_label = tk.Label(clock_content, text="", font=("Arial", 16), fg="white", bg="black", anchor="center")
        self.date_label.pack(pady=5)

        # Time label (larger font size, dandelion color, 7-segment style)
        self.time_label = tk.Label(clock_content, text="", font=("Courier", 48, "bold"), fg="#FFD700", bg="black", anchor="center")
        self.time_label.pack(pady=5)

        # Timezone label
        self.timezone_label = tk.Label(clock_content, text="", font=("Arial", 16), fg="white", bg="black", anchor="center")
        self.timezone_label.pack(pady=5)

        # Serial Monitor Section
        self.serial_monitor_frame = ttk.LabelFrame(right_section, text="Serial Monitor", padding=(10, 10))
        self.serial_monitor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.serial_monitor_frame.pack_forget()  # Initially hidden

        self.serial_monitor_text = scrolledtext.ScrolledText(self.serial_monitor_frame, wrap=tk.WORD, state="disabled", font=("Courier", 10))
        self.serial_monitor_text.pack(fill="both", expand=True, padx=5, pady=5)

    def update_clock(self):
        """Update the real-time clock."""
        now = datetime.now()
        local_timezone = time.localtime().tm_gmtoff // 3600  # Get the offset in hours from UTC
        timezone_offset = f"(UTC{'+' if local_timezone >= 0 else ''}{local_timezone:02}:00)"

        # Date and time formatting
        date_text = now.strftime("%A | %B %d, %Y")
        time_text = now.strftime("%I:%M:%S %p")

        # Update labels
        self.date_label.config(text=date_text)
        self.time_label.config(text=time_text)
        self.timezone_label.config(text=timezone_offset)

        self.root.after(1000, self.update_clock)  # Refresh every 1 second

    def toggle_serial_monitor(self):
        """Toggle the visibility of the serial monitor and change button text."""
        if self.serial_monitor_open:
            self.serial_monitor_frame.pack_forget()
            self.open_serial_button.config(text="Open Serial Monitor")
            self.serial_monitor_open = False
        else:
            self.serial_monitor_frame.pack(fill="both", expand=True, padx=10, pady=10)
            self.open_serial_button.config(text="Close Serial Monitor")
            self.serial_monitor_open = True

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_combobox['values'] = [port.device for port in ports]
        if ports:
            self.port_combobox.current(0)

    def connect_arduino(self):
        selected_port = self.port_combobox.get()
        if not selected_port:
            messagebox.showerror("Error", "No port selected. Please select a port to connect.")
            return

        try:
            self.serial_connection = serial.Serial(selected_port, 9600, timeout=1)
            self.is_reading = True
            self.update_status("Connected", "green")
            threading.Thread(target=self.read_from_arduino, daemon=True).start()
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
            messagebox.showinfo("Success", f"Connected to {selected_port}")
        except serial.SerialException as e:
            self.update_status("Disconnected", "red")
            messagebox.showerror("Error", f"Failed to connect to {selected_port}: {e}")

    def disconnect_arduino(self):
        self.is_reading = False
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        self.update_status("Disconnected", "red")
        self.connect_button.config(state="normal")
        self.disconnect_button.config(state="disabled")
        messagebox.showinfo("Disconnected", "Arduino has been disconnected.")

    def update_status(self, status, color):
        """Update the status label text and dynamic color for the value."""
        self.status_value_label.config(text=f"Arduino {status}", foreground=color)

    def read_from_arduino(self):
        while self.is_reading and self.serial_connection.is_open:
            try:
                line = self.serial_connection.readline().decode("utf-8").strip()
                if line:
                    self.update_serial_monitor(line)
                    self.parse_and_update_data(line)
            except Exception as e:
                print(f"Error reading from Arduino: {e}")
                self.is_reading = False

    def update_serial_monitor(self, line):
        """Update the serial monitor with new data."""
        self.serial_monitor_text.config(state="normal")
        self.serial_monitor_text.insert(tk.END, line + "\n")
        self.serial_monitor_text.yview(tk.END)  # Auto-scroll to the bottom
        self.serial_monitor_text.config(state="disabled")

    def parse_and_update_data(self, line):
        try:
            data = {}
            items = line.split()  # Split line into key-value pairs
            for item in items:
                if ":" in item:  # Only process items containing ':'
                    key, value = item.split(":")
                    try:
                        data[key] = float(value) if "voltage" in key else int(value)
                    except ValueError:
                        continue

            # Update sensor labels
            if "lt" in data:
                lux = self.convert_to_lux(data["lt"])
                self.sensor_labels["Top Left (lt)"].config(text=f"{lux:.2f} Lx")
            if "rt" in data:
                lux = self.convert_to_lux(data["rt"])
                self.sensor_labels["Top Right (rt)"].config(text=f"{lux:.2f} Lx")
            if "ld" in data:
                lux = self.convert_to_lux(data["ld"])
                self.sensor_labels["Bottom Left (ld)"].config(text=f"{lux:.2f} Lx")
            if "rd" in data:
                lux = self.convert_to_lux(data["rd"])
                self.sensor_labels["Bottom Right (rd)"].config(text=f"{lux:.2f} Lx")
            if "lt" in data and "rt" in data and "ld" in data and "rd" in data:
                veg = (data["lt"] + data["rt"] + data["ld"] + data["rd"]) // 4
                veg_lux = self.convert_to_lux(veg)
                self.sensor_labels["Overall Average Light Intensity (veg)"].config(text=f"{veg_lux:.2f} Lx")

            # Update servo labels
            if "servoh" in data:
                self.servo_labels["Horizontal (servoh)"].config(text=f"{data['servoh']}°")
            if "servov" in data:
                self.servo_labels["Vertical (servov)"].config(text=f"{data['servov']}°")

            # Update power labels
            if "voltageLt" in data:
                self.power_labels["Photo Resistive Sensor (Top Left)"].config(text=f"{data['voltageLt']:.2f} V")
            if "voltageRt" in data:
                self.power_labels["Photo Resistive Sensor (Top Right)"].config(text=f"{data['voltageRt']:.2f} V")
            if "voltageLd" in data:
                self.power_labels["Photo Resistive Sensor (Bottom Left)"].config(text=f"{data['voltageLd']:.2f} V")
            if "voltageRd" in data:
                self.power_labels["Photo Resistive Sensor (Bottom Right)"].config(text=f"{data['voltageRd']:.2f} V")
            if "voltageServoH" in data:
                self.power_labels["Servo Motor (Horizontal)"].config(text=f"{data['voltageServoH']:.2f} V")
            if "voltageServoV" in data:
                self.power_labels["Servo Motor (Vertical)"].config(text=f"{data['voltageServoV']:.2f} V")
        except Exception as e:
            print(f"Error parsing data: {e}")

    def convert_to_lux(self, adc_value):
        """Convert ADC value to lux using the calibration constant."""
        if adc_value == 0:
            return 0
        return K_CONSTANT / adc_value


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SolarTrackingDashboard(root)
    root.mainloop()
