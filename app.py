import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import math

def math_map(x, input_min, input_max, output_min, output_max):
    y = output_min + ((x - input_min) / (input_max - input_min)) * (output_max - output_min)
    return y

def run_swift(): #this runs the swift binary
    process = subprocess.Popen(
        ["./audio_monitor"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            print("Swift says:", line.strip())
            if line.strip() != "🎙️ Audio capture started. Monitoring levels...":
                Visualiser["value"] = math_map(float(line.strip()), -50,0,0,100)
    except Exception as e:
        print("Error:", e)
    finally:
        process.stdout.close()
        process.wait()

def test():
    threading.Thread(target=run_swift, daemon=True).start()

root = tk.Tk()
root.title("Haptic Sound")
root.minsize(200, 100)

tk.Label(root, text="hello!").pack()
tk.Button(root, text="test123", command=test).pack()

Visualiser = ttk.Progressbar(root, orient="horizontal",length="200",mode="determinate")
Visualiser.pack(pady=5,padx=5)



root.mainloop()
