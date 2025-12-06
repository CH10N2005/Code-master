import tkinter as tk
from tkinter import messagebox
from quiz_game import start_quiz_game
from leaderboard import get_leaderboard_text
import pygame
from PIL import Image, ImageTk



# --- GLOBAL VARIABLES ---
root = None
canvas = None
bg_image = None
welcome_label = None
instruction_label = None
name_label = None
name_entry = None
sectionyear_label = None
sectionyear_entry = None
Start_button = None
leaderboard_button = None

def start_quiz():
    player_name = name_entry.get().strip()
    section_year = sectionyear_entry.get().strip()
    
    if not player_name and not section_year:
        messagebox.showerror("Error", "Please enter your name and your section & year!")
        return
    if not player_name:
        messagebox.showerror("Error", "Please enter your name!")
        return
    if not section_year:
        messagebox.showerror("Error", "Please enter your section & year!")
        return
    if not player_name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name should only contain letters and spaces!")
        return
    
    print(f"Player Name: {player_name}")
    print(f"Section & Year: {section_year}")
    messagebox.showinfo("Quiz Started", f"Good luck {player_name}!")

    # Clear canvas
    canvas.delete("all")
    
    player_info = f"{player_name} ({section_year})"
    
    def restart_program():
        main()
    
    start_quiz_game(root, player_info, restart_callback=restart_program)


def show_leaderboard():
    leaderboard_text = get_leaderboard_text()
    messagebox.showinfo("🏆 Leaderboard 🏆", leaderboard_text)


def main():
    global root, canvas, bg_image, welcome_label, instruction_label, name_label, name_entry, Start_button, sectionyear_label, sectionyear_entry, leaderboard_button

    # Music
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('new game/Harvestmoon.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Music error: {e}")

    root = tk.Tk()
    root.title("Code Master (Bring your syntax!)") 
    
#=========================================Center=====================================================
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 650
    window_height = 750
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    
    def lock_position(event=None):
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.bind("<Configure>", lock_position)
#===============================================================================
    
    # Create Canvas
    canvas = tk.Canvas(root, width=window_width, height=window_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Load and display background image
    try:
        bg_img = Image.open("new game/Backgroundpygame.jpg")
        bg_img = bg_img.resize((window_width, window_height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_img)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
    except Exception as e:
        print(f"Background image error: {e}")
        canvas.configure(bg="#2c3e50")
    
    # UI Elements on Canvas
    canvas.create_text(325, 80, text="🎮CODE MASTER🎮",
                      font=("Fixedsys", 30, "bold"),
                      fill="#32CD32")
    
    canvas.create_text(325, 150, text="!Answer 30 programming questions!",
                      font=("Fixedsys", 16),
                      fill="#f2f2f2")
    
    canvas.create_text(325, 230, text="Enter your name",
                      font=("Fixedsys", 16),
                      fill="white")
    
    name_entry = tk.Entry(root, font=("Arial", 14), width=25)
    canvas.create_window(325, 270, window=name_entry)
    
    canvas.create_text(325, 330, text="Enter your section & year",
                      font=("Fixedsys", 16),
                      fill="white")
    
    sectionyear_entry = tk.Entry(root, font=("Arial", 14), width=25)
    canvas.create_window(325, 370, window=sectionyear_entry)
    
    Start_button = tk.Button(root, text="START QUIZ",
                            command=start_quiz,
                            font=("Arial", 13, "bold"),
                            bg="#27ae60", fg="white", width=20)
    canvas.create_window(325, 450, window=Start_button)
    
    leaderboard_button = tk.Button(root, text="VIEW LEADERBOARD",
                                  command=show_leaderboard,
                                  font=("Arial", 10, "bold"),
                                  bg="#3498db", fg="white", width=17)
    canvas.create_window(325, 510, window=leaderboard_button)
    
    root.mainloop()


if __name__ == "__main__":
    main()