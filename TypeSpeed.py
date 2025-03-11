import customtkinter as ctk
import threading
import random
import time

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TypeSpeedApp():
    def __init__(self):
        app = ctk.CTk()
        app.title("TypeSpeed")
        app.geometry("800x570")

        header = ctk.CTkLabel(master=app, text="TypeSpeed", font=("Eras Bold ITC", 60))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(master=app, border_width=1)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Try to load sample text, or use default text if file is not found
        try:
            self.sample_text = open("SampleTextForTS.txt", "r").read().split("\n")
        except FileNotFoundError:
            self.sample_text = [
                "The quick brown fox jumps over the lazy dog.",
                "Programming is a skill best acquired by practice and example.",
                "Coding is like poetry should be short and concise.",
                "The best error message is the one that never shows up."
            ]

        frame_4_text = ctk.CTkFrame(master=main_frame, fg_color="#1F6AA5", height=30)
        frame_4_text.pack(fill="x", pady=10, padx=10)

        self.text_label = ctk.CTkLabel(master=frame_4_text, text=random.choice(self.sample_text),
                                       font=("Bahnschrift SemiBold", 20), text_color="white")
        self.text_label.pack(pady=30)

        guide_label = ctk.CTkLabel(master=main_frame, text="Type the upper text ↑").pack(pady=2)

        self.progress_bar = ctk.CTkProgressBar(master=main_frame)
        self.progress_bar.pack(pady=5, fill="x", padx=50)
        self.progress_bar.set(0)

        self.typed_text = ctk.StringVar()
        self.user_input = ctk.CTkEntry(master=main_frame, placeholder_text="Type Here..", width=700, height=40,
                                       font=("Helvetica", 20), text_color="white", textvariable=self.typed_text)
        self.user_input.pack(pady=10)
        self.user_input.bind("<KeyRelease>", self.start)
        self.user_input.focus()

        self.typed_text.trace_add("write", self.update_progress)

        self.type_stats = ctk.CTkLabel(master=main_frame,
                                       text="STATS - \nCPS    : 0.00\nCPM    : 0.00\nWPS   : 0.00\nWPM   : 0.00\nAccuracy rate  : 0.00%",
                                       font=("Helvetica", 15))
        self.type_stats.pack(pady=10)

        self.max_stats = ctk.CTkLabel(master=main_frame,
                                      text="Highest Score: CPS    : 0.00  |  CPM    : 0.00  |  WPS   : 0.00  |  WPM   : 0.00",
                                      font=("Helvetica", 15))
        self.max_stats.pack(pady=1)

        self.reset_button = ctk.CTkButton(master=main_frame, text="Reset", width=100, font=("Helvetica", 20, "bold"),
                                          command=self.reset)
        self.reset_button.pack(pady=10)

        self.high_scores = {"CPS": 0, "CPM": 0, "WPS": 0, "WPM": 0,"Accuracy rate":0}

        self.is_running = False
        self.counter = 0 
        self.correct_char = 0
        self.total_typed_char = 0

        app.mainloop()

    def high_score(self, cps, cpm, wps, wpm,accuracy_rate):
            self.high_scores["CPS"] = max(self.high_scores["CPS"], cps)
            self.high_scores["CPM"] = max(self.high_scores["CPM"], cpm)
            self.high_scores["WPS"] = max(self.high_scores["WPS"], wps)
            self.high_scores["WPM"] = max(self.high_scores["WPM"], wpm)

            # Schedule UI update on the main thread
            self.max_stats.after(0, lambda: self.max_stats.configure(
                text=f"Highest Score   : CPS    : {self.high_scores['CPS']:.2f}  |  "
                    f"CPM    : {self.high_scores['CPM']:.2f}  |  "
                    f"WPS   : {self.high_scores['WPS']:.2f}  |  "
                    f"WPM   : {self.high_scores['WPM']:.2f}  |  "
                    )
            )

    def accuracy(self):
        targeted_text = self.text_label.cget("text")
        typed_text = self.typed_text.get()

        correct_char = 0
        for i in range(len(typed_text)):
            if i < len(targeted_text) and typed_text[i] == targeted_text[i]:
                correct_char += 1

        total_typed_char = max(len(typed_text), len(targeted_text))  # Consider extra incorrect chars
        accuracy_rate = (correct_char / total_typed_char) * 100 if total_typed_char > 0 else 0

        self.correct_char = correct_char
        self.total_typed_char = total_typed_char
        self.accuracy_rate = accuracy_rate



    def time_stamp(self):
        while self.is_running:
            time.sleep(0.1)
            self.counter += 0.1

            cps = len(self.user_input.get()) / self.counter
            cpm = cps * 60

            wps = len(self.user_input.get().split(" ")) / self.counter
            wpm = wps * 60

            self.accuracy()  # Update the accuracy calculation
            accuracy_rate = self.accuracy_rate

            self.type_stats.configure(text=f"STATS - \nCPS     : {cps:.2f}\nCPM    : {cpm:.2f}\nWPS  : {wps:.2f}\nWPM  :  {wpm:.2f}\nAccuracy rate : {accuracy_rate:.2f}%")

            if self.user_input.get().strip() == self.text_label.cget("text").strip():
                self.is_running = False
                self.user_input.after(0, lambda: self.user_input.configure(text_color="lightgreen"))
                self.high_score(cps, cpm, wps, wpm, accuracy_rate)

    def start(self, event):
        if not self.is_running and event.keycode not in [8, 16, 17, 18, 32]:
            self.is_running = True
            t = threading.Thread(target=self.time_stamp)
            t.start()

        # Check typing accuracy
        targeted_text = self.text_label.cget("text")
        typed_text = self.user_input.get()
        
        if typed_text and typed_text != targeted_text[:len(typed_text)]:
            self.user_input.configure(text_color="red")
        else:
            self.user_input.configure(text_color="white")

    def reset(self):
        self.is_running = False

        self.type_stats.configure(text="STATS -\nCPS     : 0.00\nCPM    : 0.00\nWPS    : 0.00\nWPM   : 0.00\nAccuracy rate  : 0.00%")
        self.user_input.delete(0, ctk.END)
        self.user_input.configure(text_color="white")  
        self.text_label.configure(text=random.choice(self.sample_text))
        self.progress_bar.set(0)  
    
    def update_progress(self, *args):
        # Update progress bar based on correctly typed characters
        targeted_text = self.text_label.cget("text")
        typed_text = self.typed_text.get()

        correct_length = 0
        for i in range(len(typed_text)):
            if i < len(targeted_text) and typed_text[i] == targeted_text[i]:
                correct_length += 1
            else:
                break

        total_length = len(targeted_text)
        self.progress_bar.set(correct_length / total_length if total_length else 0)

if __name__ == "__main__":
    TypeSpeedApp()



#Will add these following functionalities on updates later on:
#1.Accuracy Rate
#2.If anything else feels needed