import tkinter as tk
import subprocess
import threading

def run_swift():
    process = subprocess.Popen(
        ["./audio_monitor"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            print("Swift says:", line.strip())
    except Exception as e:
        print("Error:", e)
    finally:
        process.stdout.close()
        process.wait()

def test():
    threading.Thread(target=run_swift, daemon=True).start()

root = tk.Tk()
root.title("Haptic Sound")
root.minsize(200, 200)

tk.Label(root, text="hello!").pack()
tk.Button(root, text="test123", command=test).pack()

root.mainloop()
