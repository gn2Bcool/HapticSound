import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import pygame
import math

class VibrationManager:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    
    def set_vibration(self, low : float, high : float, duration : int):
        if hasattr(self.joystick, 'rumble'):
            self.joystick.rumble(low, high, duration)
    
    def remove(self):
        self.joystick.stop_rumble()
        self.joystick.quit()
        pygame.joystick.quit()


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
            #print("Swift says:", line.strip())
            if line.strip() != "🎙️ Audio capture started. Monitoring levels...":
                if not math.isinf(float(line.strip())):
                    volume = math_map(float(line.strip()), -60,0,0,1)
                else:
                    volume = 0
                low_vibration = 0.0
                high_vibration = 0.0
                if volume > 0.74:
                    low_vibration = math_map(volume, 0.74,1,0.1,1)
                if volume > 0.2:
                    high_vibration = volume
                print(low_vibration, high_vibration)
                newVibration.set_vibration(low_vibration,high_vibration,-1)
                Visualiser["value"] = volume * 100
                #print(volume)
    except Exception as e:
        print("Error:", e)
    finally:
        process.stdout.close()
        process.wait()

def on_close():
    print("Stopping vibration...")
    newVibration.remove()  # or .stop(), depending on your API
    root.destroy()

newVibration = VibrationManager() # this should be put so that it creates it when the button is first pressed

def test():
    threading.Thread(target=run_swift, daemon=True).start()

root = tk.Tk()
root.title("Haptic Sound")
root.minsize(200, 100)

tk.Label(root, text="hello!").pack()
tk.Button(root, text="test123", command=test).pack()

Visualiser = ttk.Progressbar(root, orient="horizontal",length="200",mode="determinate")
Visualiser.pack(pady=5,padx=5)



root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
