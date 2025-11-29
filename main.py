
"""
AI-Enabled Scientific Calculator (Tkinter)
- Basic + Scientific functions
- Memory (M+, M-, MR, MC)
- Calculation history and export to text
- Light/Dark themes
- Optional voice input/output (requires packages; will still work without them)

NOTE: Voice features require additional packages (see README).
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import math
import sys

# Try to import voice libraries optionally
VOICE_AVAILABLE = True
try:
    import speech_recognition as sr
    import pyttsx3
except Exception:
    VOICE_AVAILABLE = False

if VOICE_AVAILABLE:
    engine = pyttsx3.init()
    def speak(text):
        try:
            engine.say(str(text))
            engine.runAndWait()
        except Exception:
            pass
else:
    def speak(text):
        pass  # voice not available

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("AI Scientific Calculator")
        root.geometry("420x560")
        root.resizable(False, False)

        self.expression = ""
        self.memory_value = 0.0
        self.history = []

        self.create_widgets()
        self.light_mode()

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=("Helvetica", 20), bd=8, relief="sunken", justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=8, pady=10, ipady=8, sticky="we")

        # Basic buttons
        btn_texts = [
            ("7","8","9","/"),
            ("4","5","6","*"),
            ("1","2","3","-"),
            ("0",".","%","+"),
        ]
        for r, row in enumerate(btn_texts, start=1):
            for c, txt in enumerate(row):
                tk.Button(self.root, text=txt, width=6, height=2, font=("Helvetica",14),
                          command=lambda t=txt: self.press(t)).grid(row=r, column=c, padx=4, pady=4)

        tk.Button(self.root, text="C", width=6, height=2, font=("Helvetica",14), command=self.clear).grid(row=5, column=0, padx=4, pady=4)
        tk.Button(self.root, text="=", width=13, height=2, font=("Helvetica",14), command=self.equal).grid(row=5, column=1, columnspan=2, padx=4, pady=4)
        tk.Button(self.root, text="Ans", width=6, height=2, font=("Helvetica",14), command=self.insert_answer).grid(row=5, column=3, padx=4, pady=4)

        # Scientific buttons
        sci_row = 1
        sci_funcs = ["sin","cos","tan","log10","ln","sqrt","fact","exp"]
        for i, func in enumerate(sci_funcs):
            r = i//2 + 6
            c = i%2
            tk.Button(self.root, text=func, width=10, height=1, font=("Helvetica",12),
                      command=lambda f=func: self.apply_scientific(f)).grid(row=r, column=3+c, padx=4, pady=4, columnspan=1)

        # Memory buttons
        tk.Button(self.root, text="M+", width=6, command=lambda: self.memory_op("M+")).grid(row=8, column=0, padx=4, pady=4)
        tk.Button(self.root, text="M-", width=6, command=lambda: self.memory_op("M-")).grid(row=8, column=1, padx=4, pady=4)
        tk.Button(self.root, text="MR", width=6, command=lambda: self.memory_op("MR")).grid(row=8, column=2, padx=4, pady=4)
        tk.Button(self.root, text="MC", width=6, command=lambda: self.memory_op("MC")).grid(row=8, column=3, padx=4, pady=4)

        # Other features
        tk.Button(self.root, text="History", width=6, command=self.export_history).grid(row=9, column=0, padx=4, pady=6)
        tk.Button(self.root, text="Voice" + (" (off)" if not VOICE_AVAILABLE else ""), width=12, command=self.voice_input).grid(row=9, column=1, columnspan=2, padx=4, pady=6)
        tk.Button(self.root, text="Dark", width=6, command=self.dark_mode).grid(row=9, column=3, padx=4, pady=6)
        tk.Button(self.root, text="Light", width=6, command=self.light_mode).grid(row=9, column=4, padx=4, pady=6)

    # Input handling
    def press(self, char):
        self.expression += str(char)
        self.update_display(self.expression)

    def insert_answer(self):
        # insert last answer if available
        if self.history:
            last = self.history[-1].split(" = ")[-1]
            self.expression += str(last)
            self.update_display(self.expression)

    def update_display(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, text)

    def clear(self):
        self.expression = ""
        self.update_display("")

    def safe_eval(self, expr):
        # Limit builtins for safety
        allowed_names = {
            k: getattr(math, k) for k in dir(math) if not k.startswith("__")
        }
        # add some safe functions
        allowed_names.update({
            "sqrt": math.sqrt, "factorial": math.factorial, "pow": pow
        })
        # replace '^' with '**' if user used caret
        expr = expr.replace("^", "**")
        # allow percent operator like '50%' => 0.5
        expr = expr.replace("%", "/100")
        return eval(expr, {"__builtins__": {}}, allowed_names)

    def equal(self):
        try:
            # If expression contains functions like sin(30) we want to handle degrees: convert to radians for trig
            expr = self.expression
            # Provide shorthand: ln -> log (natural)
            expr = expr.replace("ln(", "log(")
            # Evaluate
            result = self.safe_eval(expr)
            # Format result (avoid long floats)
            if isinstance(result, float):
                result_str = ("{:.10g}".format(result))
            else:
                result_str = str(result)
            self.history.append(f"{self.expression} = {result_str}")
            self.update_display(result_str)
            self.expression = result_str
            speak(result_str)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero")
            self.expression = ""
        except Exception as e:
            messagebox.showerror("Error", "Invalid input")
            self.expression = ""

    def apply_scientific(self, func):
        try:
            # Try to use current displayed value if expression empty
            val_text = self.display.get()
            if val_text == "":
                return
            val = float(val_text)
            if func == "sin":
                res = math.sin(math.radians(val))
            elif func == "cos":
                res = math.cos(math.radians(val))
            elif func == "tan":
                res = math.tan(math.radians(val))
            elif func == "log10":
                res = math.log10(val)
            elif func == "ln":
                res = math.log(val)
            elif func == "sqrt":
                res = math.sqrt(val)
            elif func == "fact":
                res = math.factorial(int(val))
            elif func == "exp":
                res = math.exp(val)
            else:
                res = "ERR"
            res_str = ("{:.10g}".format(res)) if isinstance(res, float) else str(res)
            self.history.append(f"{func}({val}) = {res_str}")
            self.update_display(res_str)
            self.expression = res_str
            speak(res_str)
        except Exception:
            messagebox.showerror("Error", "Invalid scientific operation")
            self.expression = ""

    def memory_op(self, action):
        try:
            if action == "M+":
                self.memory_value += float(self.display.get() or 0)
            elif action == "M-":
                self.memory_value -= float(self.display.get() or 0)
            elif action == "MR":
                self.update_display(str(self.memory_value))
                self.expression = str(self.memory_value)
            elif action == "MC":
                self.memory_value = 0.0
        except Exception:
            messagebox.showerror("Error", "Memory operation failed")

    def export_history(self):
        if not self.history:
            messagebox.showinfo("History", "No history yet")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\\n".join(self.history))
                messagebox.showinfo("Saved", f"History exported to:\\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {e}")

    def voice_input(self):
        if not VOICE_AVAILABLE:
            messagebox.showinfo("Voice", "Voice packages not installed. See README to enable.")
            return
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Listening")
                audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            # Basic cleanup: replace words with operators
            text = text.replace("x", "*").replace("X", "*").replace("into", "*")
            text = text.replace("plus", "+").replace("minus", "-").replace("divide", "/")
            self.expression = text
            self.update_display(text)
        except Exception:
            messagebox.showerror("Voice", "Could not understand. Try typing instead.")

    def dark_mode(self):
        self.root.configure(bg="#222222")
        self.display.configure(bg="#000000", fg="#00ff00", insertbackground="#ffffff")

    def light_mode(self):
        self.root.configure(bg="#f0f0f0")
        self.display.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
