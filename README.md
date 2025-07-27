# -OIBSIP_domain_taskno.3
Project  3 of Oasis Intern
This is a **simple, user-friendly BMI (Body Mass Index) Calculator** built with **Python** , using
Tkinter for the GUI, SQLite for storing user history, and matplotlib for showing BMI trend graphs.

The app allows you to:

```
➢ Calculate your BMI based on weight and height
➢ See your BMI category (e.g., Normal, Overweight)
➢ Save entries automatically under your username
➢ View your complete BMI history
➢ Visualize changes in your BMI over time with a graph
```
**Features**

```
➢ Clean and modern GUI using ttk widgets and dark theme
```
```
➢ BMI calculated and categorized instantly
```
```
➢ Smart validation for weight (20–300kg) and height (80–250cm)
```
```
➢ History saved locally using SQLite database
```
```
➢ Trend graph using matplotlib if 2+ records exist
```
```
➢ Each user has separate data entries based on username
```
**Requirements**

```
➢ Python 3.x
➢ Tkinter (comes pre-installed with Python)
➢ matplotlib
➢ No internet needed; works completely offline
➢ Install matplotlib if you haven’t:
pip install matplotlib
```

**How to Run**

```
➢ Make sure all required libraries are installed.
➢ Run the app:
➢ python bmi_calculator.py
```
**Screenshots**



**Files Overview**

```
File Description
```
```
bmi_calculator.py Main script containing the complete application
```
```
bmi_data.db SQLite database file (auto-created after running the app)
```
```
README.md This file – contains instructions and project overview
```
**How It Works**

```
➢ Input your username , weight (kg) , and height (cm)
➢ Click "Calculate BMI"
➢ The app will:
o Show your BMI value
o Highlight your BMI category in color
o Save the record in a local database
➢ Click "Show History & Trends" to:
o View your past records
o See a BMI trend graph if more than one entry exists
```
**BMI Categories**

```
Category BMI Range Color
```
```
Underweight Below 18.5 Sky Blue
```
```
Normal 18.5 – 24.9 Light Green
```
```
Overweight 25 – 29.9 Gold
```
```
Obese 30 and above Red
```

# Author :)

# Muhammad Ali

**License**

Feel free to use or modify this project for learning or personal use.

**Thank you.**
