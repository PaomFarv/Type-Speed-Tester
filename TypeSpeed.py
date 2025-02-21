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
        app.geometry("800x500")

        header = ctk.CTkLabel(master=app,text="TypeSpeed",font=("Eras Bold ITC",60))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(master=app,border_width=1)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.sample_text = open("SampleTextForTS.txt","r").read().split("\n")

        frame_4_text = ctk.CTkFrame(master=main_frame,fg_color="#1F6AA5",height=30)
        frame_4_text.pack(fill="x",pady=10,padx=10)

        self.text_label = ctk.CTkLabel(master=frame_4_text,text=random.choice(self.sample_text),font=("Bahnschrift SemiBold",20),text_color="white")
        self.text_label.pack(pady=30)

        guide_label = ctk.CTkLabel(master=main_frame,text="Type the upper text ↑").pack(pady=2)

        self.user_input = ctk.CTkEntry(master=main_frame,placeholder_text="Type Here..",width=700,height=40,font=("Helvetica",20),text_color="white")
        self.user_input.pack(pady=10)
        self.user_input.bind("<KeyRelease>",self.start)

        self.type_stats = ctk.CTkLabel(master=main_frame,text="CPS    : 0.00\nCPM    : 0.00\nWPS   : 0.00\nWPM   : 0.00",font=("Helvetica",15))
        self.type_stats.pack(pady=10)

        self.reset_button = ctk.CTkButton(master=main_frame,text="Reset",width=100,font=("Helvetica",20,"bold"),command=self.reset)
        self.reset_button.pack(pady=20)

        self.is_running = False
        self.counter = 0

        app.mainloop()

    def time_stamp(self):
        while self.is_running:
            time.sleep(0.1)
            self.counter += 0.1

            cps = len(self.user_input.get()) / self.counter
            cpm = cps * 60

            wps = len(self.user_input.get().split(" ")) / self.counter
            wpm = wps * 60

            self.type_stats.configure(text=f"Speed -\nCPS     : {cps:.2f}\nCPM    : {cpm:.2f}\nWPS  : {wps:.2f}\nWPM  :  {wpm:.2f}")

    def start(self,event):
        if not self.is_running and not event.keycode in [8,16,17,18,32]:
                self.is_running = True
                t = threading.Thread(target=self.time_stamp)
                t.start()

        targeted_text = self.text_label.cget("text")

        if self.user_input.get() and not self.user_input.get() == targeted_text[:len(self.user_input.get())]:
            self.user_input.configure(text_color="red")
        
        else:
            self.user_input.configure(text_color="white")

        if self.user_input.get() == targeted_text.strip():
            self.user_input.configure(text_color="green")
            self.is_running = False

    def reset(self):
        self.is_running = False
        self.type_stats.configure(text="CPS     : 0.00\nCPM    : 0.00\nWPS    : 0.00\nWPM   : 0.00")
        self.text_label.configure(text=random.choice(self.sample_text))
        self.user_input.delete(0,ctk.END)

if __name__ == "__main__":
    TypeSpeedApp()