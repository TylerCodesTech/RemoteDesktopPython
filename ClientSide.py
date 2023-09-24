import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests

# Create the main application window
root = tk.Tk()
root.title("Remote Desktop Control")

# Define the IP address of the remote computer
remote_ip = 'REMOTE_COMPUTER_IP'  # Replace with the actual IP address

# Function to send control commands to the server
def send_control_command(action, data=None):
    server_url = f"http://{remote_ip}:8080/control"
    payload = {'action': action}
    if data:
        payload.update(data)
    response = requests.post(server_url, data=payload)
    return response.text

# Function to handle button clicks
def button_click(action):
    if action == 'set_ip':
        new_ip = ip_entry.get()
        send_control_command(action, {'ip_address': new_ip})
    elif action == 'file_transfer':
        file_path = filedialog.askopenfilename()
        if file_path:
            files = {'file': open(file_path, 'rb')}
            response = requests.post(f"http://{remote_ip}:8080/upload", files=files)
            file_name = file_path.split("/")[-1]
            response_label.config(text=f"File '{file_name}' uploaded successfully")
    elif action == 'clipboard_share':
        clipboard_text = clipboard_entry.get()
        send_control_command(action, {'clipboard_text': clipboard_text})
    else:
        send_control_command(action)

# Create buttons for control actions
control_frame = ttk.LabelFrame(root, text="Control Actions")
click_button = ttk.Button(control_frame, text="Click", command=lambda: button_click('click'))
scroll_up_button = ttk.Button(control_frame, text="Scroll Up", command=lambda: button_click('scrollup'))
scroll_down_button = ttk.Button(control_frame, text="Scroll Down", command=lambda: button_click('scrolldown'))
quit_button = ttk.Button(control_frame, text="Quit", command=lambda: button_click('quit'))
set_ip_button = ttk.Button(control_frame, text="Set Remote IP", command=lambda: button_click('set_ip'))

# Create a frame for file transfer
file_frame = ttk.LabelFrame(root, text="File Transfer")
file_transfer_button = ttk.Button(file_frame, text="Send File", command=lambda: button_click('file_transfer'))
response_label = ttk.Label(file_frame, text="")

# Create a frame for clipboard sharing
clipboard_frame = ttk.LabelFrame(root, text="Clipboard Sharing")
clipboard_label = ttk.Label(clipboard_frame, text="Clipboard Text:")
clipboard_entry = ttk.Entry(clipboard_frame, width=40)
clipboard_share_button = ttk.Button(clipboard_frame, text="Share Clipboard", command=lambda: button_click('clipboard_share'))

# Create an entry field for setting the IP address
ip_label = ttk.Label(root, text="Enter Remote IP:")
ip_entry = ttk.Entry(root, width=15)

# Place the widgets in the window using the grid geometry manager
control_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
click_button.grid(row=0, column=0, padx=5, pady=5)
scroll_up_button.grid(row=0, column=1, padx=5, pady=5)
scroll_down_button.grid(row=0, column=2, padx=5, pady=5)
quit_button.grid(row=0, column=3, padx=5, pady=5)
set_ip_button.grid(row=1, column=0, padx=5, pady=5)

file_frame.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
file_transfer_button.grid(row=0, column=0, padx=5, pady=5)
response_label.grid(row=1, column=0, padx=5, pady=5)

clipboard_frame.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
clipboard_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
clipboard_entry.grid(row=0, column=1, padx=5, pady=5)
clipboard_share_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Place the IP-related widgets within the control_frame
ip_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
ip_entry.grid(row=2, column=1, padx=5, pady=5)
set_ip_button.grid(row=2, column=2, padx=5, pady=5)

# Start the Tkinter main loop
root.mainloop()