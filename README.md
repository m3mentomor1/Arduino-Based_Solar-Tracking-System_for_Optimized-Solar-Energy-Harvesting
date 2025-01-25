<div align="center">
  <h1>Arduino-Based Solar Tracking System for Optimized Solar Energy Harvesting</h1>
</div>

### 🧐 I. Overview

This project demonstrates the development of an Arduino-based solar tracking system designed to optimize the energy capture efficiency of solar panels. The system adjusts the panel's orientation in real-time, following the brightest light source, ensuring the solar panel remains aligned with the optimal sunlight direction for maximum energy absorption.
<br><br>
##

### ⛓️ II. Features

#### ✅ Real-Time Solar Panel Adjustment
The system uses photoresistive sensors to track light intensity and adjust the solar panel’s orientation (both vertically and horizontally).
<br><br><br>

#### ✅ Energy Efficiency
The system improves solar panel energy capture by dynamically adjusting to follow the sun, resulting in more efficient energy harvesting compared to static panels.
<br><br><br>

#### ✅ Arduino-based Control
The system utilizes an Arduino UNO microcontroller to process sensor data and control servo motors for panel orientation.
<br><br><br>

#### ✅ Application Software
A user-friendly dashboard displays real-time sensor readings, panel orientation, and power consumption. The software also provides an interface to monitor the solar tracking system and track the performance of the solar panel, including its real-time light intensity and adjustments.
<br><br>
##

### ⚙️ III. Hardware Components

- **1x Arduino UNO R3 (CH340)**: Central controller to manage sensors, servos, and the tracking algorithm.<br>
- **4x Photo Resistive Sensor Modules**: Used to measure the light intensity at four different positions (Top Left, Top Right, Bottom Left, and Bottom Right).<br>
- **2x SG90 Servo Motors**: Used to adjust the horizontal and vertical angles of the solar panel.<br>
- **1x 6V 3W Monocrystalline Solar Panel**: Harvests solar energy.<br>
- **4x 18650 Lithium-Ion Batteries**: Stores energy harvested by the solar panel for system operation.

| **Component**                          | **What it looks like**             |
|----------------------------------------|------------------------------------|
| **1x Arduino UNO R3 (CH340)**          | <img src="[arduino_image_link](https://github.com/user-attachments/assets/12b00573-a18d-44c7-aaea-52e0c09ddd75)" width="50"> |
| **4x Photo Resistive Sensor Modules**  | ![LDR](ldr_image_link)             |
| **2x SG90 Servo Motors**               | ![SG90 Servo](servo_image_link)    |
| **1x 6V 3W Monocrystalline Solar Panel** | ![Solar Panel](solar_image_link)  |
| **4x 18650 Lithium-Ion Batteries**     | ![18650 Battery](battery_image_link) |

<br><br>
##

### 💻 IV. Software Components

**Tech Stack**: ``C/C++ (Arduino Framework)`` ``Python`` ``Tkinter`` ``pySerial``
<br><br>
##


