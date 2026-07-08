# 📊 Pro Data Cleaning & Visualization Studio

A modern desktop application built using **Python** and **CustomTkinter** for performing data cleaning, filtering, searching, and visualization on CSV and Excel datasets.

This application provides an easy-to-use graphical interface for data preprocessing and exploratory data analysis (EDA) without writing code.

---

## ✨ Features

### 📂 Data Import
- Load CSV files
- Load Excel (.xlsx/.xls) files

### 📋 Dataset Overview
- Number of rows
- Number of columns
- Missing values count
- Duplicate rows count
- Dataset preview
- Column information
  - Data Type
  - Missing Values
  - Unique Values

### 🧹 Data Cleaning
- Remove duplicate rows
- Drop rows containing missing values
- Fill missing values with:
  - Zero
  - Mean
  - Median
  - Mode
- Convert column datatype
  - Integer
  - Float
  - String

### 🔍 Filtering & Search
- Filter using operators:
  - ==
  - !=
  - >
  - <
  - >=
  - <=
  - Contains
- Global search across all columns
- Reset filters

### 📈 Visualization

Supports multiple chart types:

- Bar Chart
- Line Chart
- Scatter Plot
- Pie Chart
- Histogram
- Box Plot
- Correlation Heatmap
- Multi-Series Comparison

### 💾 Export

Export:
- Cleaned CSV
- Cleaned Excel
- Filtered CSV
- Filtered Excel
- Chart as PNG

### 🎨 UI Features

- Modern GUI
- Dark Theme
- Light Theme
- Responsive Layout
- Scrollable Tables

---

# 🛠 Technologies Used

- Python
- CustomTkinter
- Pandas
- NumPy
- Matplotlib
- Tkinter

---

# 📂 Project Structure

```
ProDataDashboard/
│
├── DataDeshboard2.py
├── README.md
├── requirements.txt
├── LICENSE
└── screenshots/
      home.png
      cleaning.png
      visualization.png
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ProDataDashboard.git
```

Go into the project directory

```bash
cd ProDataDashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python DataDeshboard2.py
```

---

# 📦 Requirements

- Python 3.10+
- Pandas
- NumPy
- Matplotlib
- CustomTkinter
- OpenPyXL

---

# 📸 Screenshots

Add screenshots here after uploading them.

Example:

```
screenshots/home.png
screenshots/cleaning.png
screenshots/charts.png
```

---

# Future Improvements

- Machine Learning Integration
- Automatic Data Cleaning Suggestions
- PDF Report Generation
- SQL Database Support
- Data Profiling
- Dashboard Templates
- Advanced Statistical Analysis

---

# Author

**Vatsalya Sahu**

B.Tech CSE (Data Science)

---

# License

This project is licensed under the MIT License.
