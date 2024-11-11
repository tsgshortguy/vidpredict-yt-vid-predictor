# VidPredict - YouTube Upload Predictor

VidPredict is a Python application that predicts the next upload date of a YouTube channel based on its previous upload history. This tool uses the YouTube Data API to fetch video data and calculates the average interval between uploads to estimate the next upload date.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Code](#code)
- [License](#license)

## Features
- **Predict Next Upload Date**: Calculates the average interval between past uploads to predict the next upload date.
- **Timezone Conversion**: Displays the predicted date and time in your local timezone.
- **Theme Selection**: Choose between Light, Dark, and Blue themes to customize the application's appearance.
- **User-Friendly Interface**: A graphical user interface (GUI) built with Tkinter for easy interaction.

## Prerequisites
Before running VidPredict, ensure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Windows

1. **Install Python 3**:
   - Download and install Python from the [official website](https://www.python.org/downloads/).
   - During installation, ensure you check the option "Add Python to PATH".

2. **Open Command Prompt**:
   - Press `Win + R`, type `cmd`, and press Enter.

3. **Install Required Packages**:
   ```cmd
   pip install google-api-python-client pytz tzlocal tkinter
   ```

### macOS

1. **Install Python 3**:
   - macOS usually comes with Python 2.x. Install Python 3 from the [official website](https://www.python.org/downloads/) or use Homebrew:
   ```bash
   brew install python3
   ```

2. **Open Terminal**.

3. **Install Required Packages**:
   ```bash
   pip3 install google-api-python-client pytz tzlocal
   ```

### Linux

1. **Install Python 3 and pip**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```
   (For other distributions, use the appropriate package manager.)

2. **Open Terminal**.

3. **Install Required Packages**:
   ```bash
   pip3 install google-api-python-client pytz tzlocal
   ```

## Setup Instructions

### Obtain a YouTube Data API Key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to `APIs & Services > Dashboard`.
4. Click **Enable APIs and Services** and enable the **YouTube Data API v3**.
5. Go to `APIs & Services > Credentials` and click **Create Credentials**.
6. Choose **API key** and copy the generated key.

### Save the Script:
1. Copy the code from the [Code](#code) section below.
2. Paste it into a file named `vidpredict.py`.

### Insert Your API Key:
1. Open `vidpredict.py` in a text editor.
2. Replace `'YOUR_API_KEY'` with the API key you obtained.

   ```python
   DEVELOPER_KEY = "YOUR_API_KEY"
   ```

## Usage

### Run the Application:
1. Open your command prompt or terminal.
2. Navigate to the directory containing `vidpredict.py`.
3. Execute the script:
   ```bash
   python vidpredict.py
   ```
   (Use `python3` instead of `python` if necessary.)

### Using VidPredict:
- **Enter YouTube Channel URL**: Input the full URL of the YouTube channel you want to analyze.
- **Select Prediction Format**: Choose how you want the predicted date displayed (Date Only, Time Only, or Date & Time).
- **Select Theme**: Choose your preferred theme from the dropdown menu.
- **Predict Next Upload**: Click the **Predict Next Upload** button to get the estimated next upload date.
- **View Results**: The predicted date will be displayed in the application window.

## Code

[Insert code here]

## License

[Chaos, Open Sourced.]
