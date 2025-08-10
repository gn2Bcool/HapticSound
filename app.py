import tkinter as tk

def test():
    print("hehe button")

root = tk.Tk()

root.title("Haptic Sound")
root.minsize(200,200)

tk.Label(root, text="hello!").pack()
tk.Button(root, text="test123", command=test).pack()


root.mainloop()