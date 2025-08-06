# 🏥 Medical Appointments Dashboard

An interactive data visualization dashboard built with **Dash** and **Plotly** to analyze medical appointment no-show patterns from a real-world Brazilian healthcare dataset.

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Interactive-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Dash](https://img.shields.io/badge/Dash-2.17.1-orange)
![Plotly](https://img.shields.io/badge/Plotly-5.17.0-red)

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Information](#dataset-information)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Components](#dashboard-components)
- [Interactive Features](#interactive-features)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This dashboard provides comprehensive insights into medical appointment attendance patterns using over 110,000 appointment records from Brazilian public hospitals. The analysis focuses on understanding factors that influence whether patients show up for their scheduled appointments.

### Key Questions Addressed:
- What are the overall no-show vs show-up rates?
- How do age and gender affect attendance patterns?
- Which days of the week have the highest/lowest attendance?
- How does waiting time between scheduling and appointment impact attendance?
- What is the influence of medical conditions on no-show rates?
- How do SMS reminders and scholarship status affect attendance?
- Which neighborhoods have the highest no-show rates?

## 📊 Dataset Information

**Dataset Name:** Medical Appointment No Show  
**Source:** [Kaggle - Medical Appointment No Show](https://www.kaggle.com/datasets/joniarroba/noshowappointments)  
**Size:** 110,527 appointment records  
**Time Period:** April-June 2016  
**Location:** Brazil  

### Dataset Features:
- **PatientId:** Unique patient identifier
- **AppointmentID:** Unique appointment identifier
- **Gender:** Patient gender (M/F)
- **ScheduledDay:** Date when appointment was scheduled
- **AppointmentDay:** Date of the actual appointment
- **Age:** Patient age
- **Neighbourhood:** Location of the appointment
- **Scholarship:** Indicates if patient receives government financial support
- **Hipertension:** Hypertension diagnosis (0/1)
- **Diabetes:** Diabetes diagnosis (0/1)
- **Alcoholism:** Alcoholism diagnosis (0/1)
- **Handcap:** Handicap status (0-4 scale)
- **SMS_received:** Whether patient received SMS reminder (0/1)
- **No-show:** Target variable - whether patient showed up (Yes/No)

## ✨ Features

### 📈 Comprehensive Visualizations
- **Overview Pie Chart:** Overall attendance vs no-show rates
- **Age & Gender Analysis:** No-show rates by demographic groups
- **Weekly Patterns:** Appointment distribution and attendance by day of week
- **Waiting Time Analysis:** Impact of scheduling delay on attendance
- **Medical Conditions:** How chronic conditions affect attendance
- **SMS & Scholarship Impact:** Effect of reminders and financial support
- **Neighborhood Analysis:** Geographic patterns of no-show rates

### 🎛️ Interactive Controls
- **Age Group Filter:** Filter by Children, Young Adults, Middle-aged, Seniors
- **Gender Filter:** Filter by Male, Female, or All
- **Waiting Days Slider:** Adjust maximum waiting time threshold
- **Real-time Updates:** All charts update dynamically based on filters

### 📱 Responsive Design
- Bootstrap-based responsive layout
- Professional styling with custom color schemes
- Mobile-friendly interface
- Clean and intuitive user experience

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd dashboard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Dataset
Ensure `medical_appointments.csv` is in the dashboard folder. If not, download it from the Kaggle link above.

## 🖥️ Usage

### Running the Dashboard
```bash
python app.py
```

### Accessing the Dashboard
1. Open your web browser
2. Navigate to `http://localhost:8050`
3. The dashboard will load with all visualizations
4. Use the interactive filters to explore different data segments

### Stopping the Application
Press `Ctrl+C` in the terminal to stop the server.

## 📊 Dashboard Components

### 1. Key Statistics Cards
- **Total Appointments:** Overall number of appointments in dataset
- **Show-up Rate:** Percentage of patients who attended appointments
- **Average Patient Age:** Mean age of all patients
- **Average Waiting Time:** Mean days between scheduling and appointment

### 2. Interactive Filters Panel
- **Age Group Dropdown:** Filter data by age categories
- **Gender Dropdown:** Filter by patient gender
- **Waiting Days Slider:** Set maximum waiting time threshold

### 3. Main Visualizations

#### Overall Attendance Rate (Pie Chart)
- Shows proportion of show-ups vs no-shows
- Color-coded: Green for attendance, Red for no-shows

#### Age & Gender Analysis (Grouped Bar Chart)
- No-show rates by age group and gender
- Identifies demographic patterns in attendance

#### Weekly Appointment Patterns (Combined Chart)
- Bar chart: Total appointments by day of week
- Line chart: No-show rates by day of week
- Dual y-axis for clear comparison

#### Waiting Time Distribution (Histogram)
- Shows relationship between waiting time and attendance
- Separate colors for show-ups vs no-shows

#### Medical Conditions Impact (Grouped Bar Chart)
- Compares no-show rates for patients with/without conditions
- Covers Hypertension, Diabetes, Alcoholism, and Handicap

#### SMS & Scholarship Analysis (Side-by-side Bar Charts)
- Impact of SMS reminders on attendance
- Effect of scholarship status on attendance

#### Neighborhood Analysis (Horizontal Bar Chart)
- No-show rates for top 15 neighborhoods by appointment volume
- Color-coded by no-show rate intensity

## 🎛️ Interactive Features

### Dynamic Filtering
- All main charts update in real-time when filters are changed
- Filters work in combination (e.g., Female + Young Adults + Max 7 days waiting)
- Smooth transitions and responsive updates

### Hover Information
- Detailed tooltips on all chart elements
- Contextual information for better understanding

### Responsive Layout
- Adapts to different screen sizes
- Mobile-friendly design
- Optimized for both desktop and tablet viewing

## 📁 Project Structure

```
dashboard/
│
├── app.py                    # Main dashboard application
├── medical_appointments.csv  # Dataset file
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
└── (Generated when running)
    ├── __pycache__/         # Python cache files
    └── assets/              # Static assets (if any)
```

## 🔧 Technical Details

### Libraries Used
- **pandas (2.1.4):** Data manipulation and analysis
- **numpy (1.24.4):** Numerical computing
- **plotly (5.17.0):** Interactive visualizations
- **dash (2.17.1):** Web application framework
- **dash-bootstrap-components (1.5.0):** Bootstrap styling for Dash

### Data Processing Pipeline
1. **Data Loading:** CSV file loaded with pandas
2. **Data Cleaning:** Remove missing values and outliers
3. **Feature Engineering:** 
   - Calculate waiting days between scheduling and appointment
   - Extract day of week from dates
   - Create age groups for analysis
   - Convert categorical variables to binary
4. **Statistical Analysis:** Calculate summary statistics and group-wise metrics

### Visualization Architecture
- **Modular Design:** Each chart has its own function
- **Consistent Styling:** Unified color schemes and formatting
- **Performance Optimized:** Efficient data filtering and updates
- **Accessibility:** Clear labels, legends, and descriptions

### Callback System
- **Real-time Interactivity:** Dash callbacks for dynamic updates
- **Multi-output Updates:** Single callback updates multiple charts
- **Efficient Filtering:** Optimized data filtering for smooth performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Data Source:** [Kaggle - Medical Appointment No Show Dataset](https://www.kaggle.com/datasets/joniarroba/noshowappointments)
- **Visualization Libraries:** Plotly and Dash development teams
- **Inspiration:** Real-world healthcare analytics challenges

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](../../issues) section
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Built with ❤️ using Python, Dash, and Plotly**