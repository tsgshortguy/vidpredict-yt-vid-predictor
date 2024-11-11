import googleapiclient.discovery
import datetime
from statistics import mean
import tkinter as tk
from tkinter import ttk, messagebox
import re
import pytz
from tzlocal import get_localzone

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAQua6cjBTUqFI6B9nBdSl9tprVsJ6OjmQ"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def get_video_dates(channel_id, max_results=50):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    )
    response = request.execute()

    dates = [datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
             for item in response['items']]

    return dates

def predict_next_upload(dates):
    if len(dates) < 2:
        return "Not enough data to make a prediction."

    intervals = [(dates[i] - dates[i + 1]).days for i in range(len(dates) - 1)]
    avg_interval = mean(intervals)

    last_upload = dates[0]
    next_upload = last_upload + datetime.timedelta(days=avg_interval)

    today = datetime.datetime.now()
    while next_upload <= today:
        next_upload += datetime.timedelta(days=avg_interval)

    return next_upload

def format_time_with_timezone(dt):
    local_timezone = get_localzone()
    local_dt = dt.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_dt.strftime("%Y-%m-%d %I:%M:%S %p %Z")

def extract_channel_id(channel_url):
    if "channel/" in channel_url:
        channel_id = channel_url.split("channel/")[-1]
    elif "@" in channel_url:
        username = channel_url.split("@")[-1]
        try:
            request = youtube.search().list(
                part="snippet",
                q=f"{username}",
                type="channel",
                maxResults=1
            )
            response = request.execute()
            if response['items']:
                channel_id = response['items'][0]['snippet']['channelId']
            else:
                result_label.config(text="Invalid username or channel not found.")
                raise ValueError("Invalid username or channel not found.")
        except Exception as e:
            result_label.config(text=f"An error occurred while fetching channel ID: {e}")
            raise
    else:
        channel_id = channel_url.split("/")[-1]

    if not channel_id.startswith("UC"):
        result_label.config(text="Invalid channel ID format. Please use a valid YouTube channel URL.")
        raise ValueError("Invalid channel ID format.")

    return channel_id

def change_theme(theme):
    if theme == "Light":
        root.tk_setPalette(background="#FFFFFF", foreground="#000000")
        style.configure("TButton", background="#E0E0E0", foreground="#000000", borderwidth=1, relief="flat")
        style.configure("TLabel", background="#FFFFFF", foreground="#000000")
        style.configure("TFrame", background="#FFFFFF")
    elif theme == "Dark":
        root.tk_setPalette(background="#1E1E1E", foreground="#EDEDED")
        style.configure("TButton", background="#333333", foreground="#EDEDED", borderwidth=1, relief="flat")
        style.configure("TLabel", background="#1E1E1E", foreground="#EDEDED")
        style.configure("TFrame", background="#1E1E1E")
    elif theme == "Blue":
        root.tk_setPalette(background="#D0EFFF", foreground="#003366")
        style.configure("TButton", background="#0077B6", foreground="#FFFFFF", borderwidth=1, relief="flat")
        style.configure("TLabel", background="#D0EFFF", foreground="#003366")
        style.configure("TFrame", background="#D0EFFF")

def on_predict():
    channel_url = entry_channel.get()
    if not channel_url.startswith("https://www.youtube.com/"):
        result_label.config(text="Please enter a valid YouTube channel URL.")
        return

    try:
        channel_id = extract_channel_id(channel_url)
        dates = get_video_dates(channel_id)
        predicted_date = predict_next_upload(dates)
        
        if isinstance(predicted_date, str):
            result_label.config(text=predicted_date)
            return

        option = var_format.get()
        if option == 1:
            result = predicted_date.strftime("%Y-%m-%d")
        elif option == 2:
            result = format_time_with_timezone(predicted_date)
        else:
            result = format_time_with_timezone(predicted_date)

        result_label.config(text=f"Theoretical next upload: {result}")
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

# Main window configuration
root = tk.Tk()
root.title("VidPredict - YouTube Upload Predictor")
root.geometry("1640x856")
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 16), padding=10, relief="flat")
style.configure("TLabel", font=("Segoe UI", 18))
style.configure("TRadiobutton", font=("Segoe UI", 16))
style.configure("TEntry", font=("Segoe UI", 16))
style.configure("TFrame", font=("Segoe UI", 16))

root.configure(bg="#FFFFFF")

# Header styling
header_frame = ttk.Frame(root, padding=20)
header_frame.pack(fill="x")
label_welcome = ttk.Label(header_frame, text="Welcome to VidPredict!", font=("Segoe UI", 36, "bold"), background="#FFFFFF")
label_welcome.pack(pady=10)

# Add theme selection
frame_theme = ttk.Frame(root, padding=10)
frame_theme.pack(pady=10)
label_theme = ttk.Label(frame_theme, text="Select Theme:", font=("Segoe UI", 20, "bold"))
label_theme.pack(side=tk.LEFT, padx=10)

combo_theme = ttk.Combobox(frame_theme, values=["Light", "Dark", "Blue"], state="readonly", font=("Segoe UI", 16))
combo_theme.set("Light")
combo_theme.pack(side=tk.LEFT, padx=10)
combo_theme.bind("<<ComboboxSelected>>", lambda event: change_theme(combo_theme.get()))

# Main frame for input and options
frame_main = ttk.Frame(root, padding=30)
frame_main.pack(pady=10)

label_channel = ttk.Label(frame_main, text="Enter YouTube Channel URL:", font=("Segoe UI", 20, "bold"), background="#FFFFFF")
label_channel.grid(row=0, column=0, pady=10, sticky="w")

entry_channel = ttk.Entry(frame_main, width=50, font=("Segoe UI", 18))
entry_channel.grid(row=1, column=0, pady=10, sticky="ew")

label_format = ttk.Label(frame_main, text="Select Prediction Format:", font=("Segoe UI", 20, "bold"), background="#FFFFFF")
label_format.grid(row=2, column=0, pady=15, sticky="w")

var_format = tk.IntVar()
radio_date = ttk.Radiobutton(frame_main, text="Date Only", variable=var_format, value=1, style="TRadiobutton")
radio_time = ttk.Radiobutton(frame_main, text="Time Only", variable=var_format, value=2, style="TRadiobutton")
radio_date_time = ttk.Radiobutton(frame_main, text="Date & Time", variable=var_format, value=3, style="TRadiobutton")

radio_date.grid(row=3, column=0, sticky="w", pady=5)
radio_time.grid(row=4, column=0, sticky="w", pady=5)
radio_date_time.grid(row=5, column=0, sticky="w", pady=5)

button_predict = ttk.Button(frame_main, text="Predict Next Upload", command=on_predict, style="TButton")
button_predict.grid(row=6, column=0, pady=20)

# Result label
result_frame = ttk.Frame(root, padding=20)
result_frame.pack(pady=20)
result_label = ttk.Label(result_frame, text="", font=("Segoe UI", 20, "bold"), background="#FFFFFF", anchor="center")
result_label.pack()

root.mainloop()
