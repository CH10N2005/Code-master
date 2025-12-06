import tkinter as tk
from tkinter import messagebox
from questions import questions_database
from leaderboard import save_score, get_leaderboard_text
import random
import winsound
import pygame
from PIL import Image, ImageTk

# Sound initialization
pygame.mixer.init()
pygame.mixer.music.load('new game/Harvestmoon.mp3')
pygame.mixer.music.set_volume(0.3)

try:
    Victory_sound = pygame.mixer.Sound('new game/Victorysound.mp3')
    Gameover_sound = pygame.mixer.Sound('new game/GameOver.mp3')
except Exception as e:
    print(f"Sound loading error: {e}")
    Victory_sound = None
    Gameover_sound = None

# Global variables
current_score = 0
total_questions = 30
current_answer = None
player_name = ""
fill_blank_score = 0
true_false_score = 0
lives = 5
restart_to_main_callback = None
current_root = None
canvas = None
bg_image = None

score_label = None
lives_label = None
question_text = None
current_question = None
answer_entry = None
all_fill_blank = []
all_true_false = []
white_frame = None
question_queue = []
answered_count = 0

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def load_background(parent, width, height):
    """Load background image on canvas"""
    global canvas, bg_image
    
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    try:
        bg_img = Image.open("new game/Backgroundpygame.jpg")
        bg_img = bg_img.resize((width, height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_img)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        # Store reference in canvas to prevent garbage collection
        canvas.bg_image = bg_image
    except Exception as e:
        print(f"Background error: {e}")
        canvas.configure(bg="#2c3e50")
    
    return canvas

def start_quiz_game(root_window, name, restart_callback=None):
    global player_name, all_fill_blank, all_true_false, current_question_type, current_score, current_question_num, fill_blank_score, true_false_score, skipped_questions, question_queue, answered_count, lives, restart_to_main_callback, current_root, canvas, bg_image
    
    # Reset all variables including canvas
    canvas = None
    bg_image = None
    current_score = 0
    current_question_num = 0
    fill_blank_score = 0
    true_false_score = 0
    skipped_questions = []
    answered_count = 0
    lives = 5
    restart_to_main_callback = restart_callback
    current_root = root_window
    
    player_name = name
    
    all_fill_blank = questions_database["fill_in_blank"].copy()
    all_true_false = questions_database["true_false"].copy()
    random.shuffle(all_fill_blank)
    random.shuffle(all_true_false)
    
    question_queue = []
    
    selected_fill_blank = random.sample(all_fill_blank, 15)
    for i, q in enumerate(selected_fill_blank):
        question_queue.append({"question": q, "type": "fill_blank", "original_num": i + 1})
    
    selected_true_false = random.sample(all_true_false, 15)
    for i, q in enumerate(selected_true_false):
        question_queue.append({"question": q, "type": "true_false", "original_num": i + 16})

    current_question_type = "fill_in_blank"
    
    pygame.mixer.music.play(-1)
   
    show_quiz_screen(root_window)

def exit_to_main():
    global current_root
    print("EXIT button clicked!")
    
    pygame.mixer.music.stop()
    
    if restart_to_main_callback:
        if current_root:
            current_root.destroy()
        restart_to_main_callback()
    else:
        if current_root:
            current_root.quit()

def show_quiz_screen(root):
    global score_label, lives_label, question_text, current_question, answer_entry, current_question_type, white_frame, current_answer, canvas, bg_image
    
    if not question_queue:
        show_final_score()
        return
    
    if lives <= 0:
        show_game_over()
        return
    
    # Don't destroy widgets if canvas already exists - just clear it
    if canvas is None:
        for widget in root.winfo_children():
            widget.destroy()
        center_window(root, 650, 750)
        canvas = load_background(root, 650, 750)
    else:
        # Just clear the canvas instead of destroying everything
        canvas.delete("all")
        # Reload background using stored bg_image
        if bg_image:
            canvas.create_image(0, 0, image=bg_image, anchor="nw")
        else:
            # If bg_image is None, try to load it
            try:
                bg_img = Image.open("new game/Backgroundp.jpg")
                bg_img = bg_img.resize((650, 750), Image.Resampling.LANCZOS)
                bg_image = ImageTk.PhotoImage(bg_img)
                canvas.bg_image = bg_image  # Keep reference
                canvas.create_image(0, 0, image=bg_image, anchor="nw")
            except Exception as e:
                print(f"Background error: {e}")
                canvas.configure(bg="#2c3e50")
    
    # Title
    canvas.create_text(325, 60, text="🎯 QUIZ TIME 🎯",
                      font=("Fixedsys", 27, "bold"),
                      fill="#32CD32")
    
    # Lives
    canvas.create_text(325, 110, text=f"Lives: {lives}",
                      font=("Fixedsys", 17, "bold"),
                      fill="#e74c3c")
    
    # Score
    canvas.create_text(325, 145, text=f"Score: {current_score}/{total_questions}",
                      font=("Arial", 17, "bold"),
                      fill="#f39c12")
    
    # Questions remaining
    remaining = len(question_queue)
    canvas.create_text(325, 180, text=f"Questions remaining: {remaining}",
                      font=("Fixedsys", 13, "bold"),
                      fill="white")
    
    current_q = question_queue[0]
    question_data = current_q["question"]
    current_answer = question_data["answer"]
    question_text_display = question_data["question"]
    
    # White frame for question
    white_frame = tk.Frame(root, bg="white", relief="solid", bd=2, padx=35, pady=25)
    canvas.create_window(325, 280, window=white_frame)
    
    current_question = tk.Label(white_frame, text=question_text_display,
                               font=("Arial", 15),
                               bg="white", fg="#2c3e50",
                               wraplength=450,
                               justify="center")
    current_question.pack()
    
    if current_q["type"] == "fill_blank":
        show_fill_blank_input(root, canvas)
    else:
        show_true_false_buttons(root, canvas)

def show_fill_blank_input(root, canvas):
    global answer_entry
    
    canvas.create_text(325, 380, text="Your answer",
                      font=("Arial", 12, "bold"), 
                      fill="white")
    
    answer_entry = tk.Entry(root, font=("Arial", 14), width=30)
    canvas.create_window(325, 415, window=answer_entry)
    
    submit_btn = tk.Button(root, text="SUBMIT ANSWER",
                          command=check_answer,
                          font=("Arial", 12, "bold"),
                          bg="#27ae60", fg="white", width=15, height=1)
    canvas.create_window(255, 470, window=submit_btn)
    
    skip_btn = tk.Button(root, text="SKIP",
                        command=skip_question,
                        font=("Arial", 12, "bold"),
                        bg="#42A5F5", fg="white", width=10, height=1)
    canvas.create_window(395, 470, window=skip_btn)

def show_true_false_buttons(root, canvas):
    true_btn = tk.Button(root, text="TRUE ✓",
                        command=lambda: check_tf_answer(True),
                        font=("Arial", 12, "bold"),
                        bg="#27ae60", fg="white", 
                        width=12, height=1)
    canvas.create_window(245, 400, window=true_btn)
    
    false_btn = tk.Button(root, text="FALSE ✗",
                         command=lambda: check_tf_answer(False),
                         font=("Arial", 12, "bold"),
                         bg="#e74c3c", fg="white",
                         width=12, height=1)
    canvas.create_window(405, 400, window=false_btn)
    
    skip_btn = tk.Button(root, text="SKIP",
                        command=skip_question,
                        font=("Arial", 12, "bold"),
                        bg="#42A5F5", fg="white", width=15, height=1)
    canvas.create_window(325, 460, window=skip_btn)

def skip_question():
    global question_queue
    
    if question_queue:
        skipped = question_queue.pop(0)
        question_queue.append(skipped)
        print(f"Skipped question, moved to end of queue")
    
    # Update screen without destroying canvas
    root = current_root
    show_quiz_screen(root)

def play_correct_sound():
    winsound.Beep(1000, 300)

def play_wrong_sound():
    winsound.Beep(300, 300)

def flash_background(is_correct):
    global white_frame
    if white_frame:
        original_color = "white"
        flash_color = "#27ae60" if is_correct else "#e74c3c"
        
        white_frame.config(bg=flash_color)
        current_question.config(bg=flash_color)
        
        white_frame.after(1000, lambda: [
            white_frame.config(bg=original_color),
            current_question.config(bg=original_color)
        ])

def check_answer():
    global current_score, fill_blank_score, question_queue, answered_count, lives
    
    user_answer = answer_entry.get().strip()
    if user_answer == "":
        messagebox.showerror("Error", "Please enter your answer!")
        return
    
    correct_answer_str = str(current_answer)
    
    if user_answer.lower() == correct_answer_str.lower():
        current_score += 1
        fill_blank_score += 1
        flash_background(True)
        play_correct_sound()
        print("User got it right!")
    else:
        lives -= 1
        flash_background(False)
        play_wrong_sound()
        print("User got it wrong! Lives remaining:", lives)
    
    if question_queue:
        question_queue.pop(0)
        answered_count += 1
    
    if lives <= 0:
        current_root.after(1000, show_game_over)
        return
    
    if answered_count == 15 and question_queue:
        current_root.after(1000, lambda: switch_to_true_false())
    else:
        current_root.after(1000, lambda: show_quiz_screen(current_root))

def check_tf_answer(user_answer):
    global current_score, true_false_score, question_queue, answered_count, lives
    
    correct_answer = current_answer
    
    if user_answer == correct_answer:
        current_score += 1
        true_false_score += 1
        flash_background(True)
        play_correct_sound()
        print("User got it right!")
    else:
        lives -= 1
        flash_background(False)
        play_wrong_sound()
        print("User got it wrong! Lives remaining:", lives)
    
    if question_queue:
        question_queue.pop(0)
        answered_count += 1
    
    if lives <= 0:
        current_root.after(1000, show_game_over)
        return
    
    current_root.after(1000, lambda: show_quiz_screen(current_root))

def switch_to_true_false():
    messagebox.showinfo("Section Complete!", "Great job! Now let's do True/False questions!")
    show_quiz_screen(current_root)

def show_game_over():
    global current_score, player_name, fill_blank_score, true_false_score, canvas
    
    pygame.mixer.music.stop()

    if Gameover_sound:
        Gameover_sound.play()
    
    for widget in current_root.winfo_children():
        widget.destroy()
    
    center_window(current_root, 750, 850)
    
    canvas = load_background(current_root, 750, 850)
    
    canvas.create_text(330, 80, text="💀GAME OVER💀",
                      font=("Fixedsys", 29, "bold"),
                      fill="#e74c3c")
    
    # Create white frame centered
    white_frame = tk.Frame(current_root, bg="white", relief="solid", bd=3, padx=25, pady=20)
    # Move more to the left - try 330
    canvas.create_window(325, 400, window=white_frame, anchor="center")
    
    game_over_msg = tk.Label(white_frame, text="You ran out of lives!",
                            font=("Arial", 16, "bold"),
                            bg="white", fg="#e74c3c")
    game_over_msg.pack(pady=10)
    
    player_label = tk.Label(white_frame, text=f"Player: {player_name}",
                           font=("Arial", 12),
                           bg="white", fg="#2c3e50")
    player_label.pack(pady=6)
    
    separator1 = tk.Label(white_frame, text="─" * 35,
                         font=("Arial", 10),
                         bg="white", fg="#95a5a6")
    separator1.pack(pady=6)
    
    total_label = tk.Label(white_frame, text="Final Score:",
                          font=("Arial", 13, "bold"),
                          bg="white", fg="#2c3e50")
    total_label.pack(pady=(10,2))
    
    total_score_label = tk.Label(white_frame, text=f"{current_score}/30",
                                 font=("Arial", 26, "bold"),
                                 bg="white", fg="#2c3e50")
    total_score_label.pack(pady=2)
    
    answered_label = tk.Label(white_frame, text=f"Questions Answered: {answered_count}/30",
                             font=("Arial", 12),
                             bg="white", fg="#2c3e50")
    answered_label.pack(pady=10)
    
    save_score(player_name, current_score, total_questions)
    
    button_frame = tk.Frame(white_frame, bg="white")
    button_frame.pack(pady=10)
    
    retry_btn = tk.Button(button_frame, text="RETRY",
                          command=lambda: restart_quiz(current_root),
                          font=("Arial", 10, "bold"),
                          bg="#27ae60", fg="white", 
                          relief="raised", bd=2,
                          width=12, height=2)
    retry_btn.pack(side="left", padx=8)
    
    exit_btn = tk.Button(button_frame, text="EXIT",
                         command=exit_to_main,
                         font=("Arial", 10, "bold"),
                         bg="#e74c3c", fg="white",
                         relief="raised", bd=2,
                         width=12, height=2)
    exit_btn.pack(side="left", padx=8)
    
    print(f"Game Over! Final score: {current_score}/{total_questions}")

def show_final_score():
    global current_score, player_name, fill_blank_score, true_false_score, canvas
    
    pygame.mixer.music.stop()
    
    if Victory_sound:
        Victory_sound.play()

    for widget in current_root.winfo_children():
        widget.destroy()
    
    center_window(current_root, 750, 850)
    
    canvas = load_background(current_root, 750, 850)
    
    canvas.create_text(330, 30, text="🎓 Quiz Complete 🎓",
                      font=("Arial", 28, "bold"),
                      fill="#32CD32")
    
    white_frame = tk.Frame(current_root, bg="white", relief="solid", bd=3, padx=30, pady=30)
    canvas.create_window(325, 400, window=white_frame, anchor="center")
    
    player_label = tk.Label(white_frame, text=f"Player: {player_name}",
                           font=("Arial", 12),
                           bg="white", fg="#2c3e50")
    player_label.pack(pady=6)
    
    separator1 = tk.Label(white_frame, text="─" * 35,
                         font=("Arial", 10),
                         bg="white", fg="#95a5a6")
    separator1.pack(pady=6)
    
    fill_status = "✓ Passed" if fill_blank_score >= 9 else "✗ Failed"
    fill_color = "#27ae60" if fill_blank_score >= 9 else "#e74c3c"
    
    fill_label = tk.Label(white_frame, text="Fill-in-the-Blank Score:",
                         font=("Arial", 11, "bold"),
                         bg="white", fg="#2c3e50")
    fill_label.pack(pady=(10,2))
    
    fill_score_label = tk.Label(white_frame, text=f"{fill_blank_score}/15",
                                font=("Arial", 18, "bold"),
                                bg="white", fg="#2c3e50")
    fill_score_label.pack(pady=2)
    
    fill_status_label = tk.Label(white_frame, text=fill_status,
                                 font=("Arial", 11, "bold"),
                                 bg="white", fg=fill_color)
    fill_status_label.pack(pady=2)
    
    separator2 = tk.Label(white_frame, text="─" * 35,
                         font=("Arial", 10),
                         bg="white", fg="#95a5a6")
    separator2.pack(pady=6)
    
    tf_status = "✓ Passed" if true_false_score >= 9 else "✗ Failed"
    tf_color = "#27ae60" if true_false_score >= 9 else "#e74c3c"
    
    tf_label = tk.Label(white_frame, text="True/False Score:",
                       font=("Arial", 11, "bold"),
                       bg="white", fg="#2c3e50")
    tf_label.pack(pady=(10,2))
    
    tf_score_label = tk.Label(white_frame, text=f"{true_false_score}/15",
                             font=("Arial", 18, "bold"),
                             bg="white", fg="#2c3e50")
    tf_score_label.pack(pady=2)
    
    tf_status_label = tk.Label(white_frame, text=tf_status,
                               font=("Arial", 11, "bold"),
                               bg="white", fg=tf_color)
    tf_status_label.pack(pady=2)
    
    separator3 = tk.Label(white_frame, text="─" * 35,
                         font=("Arial", 10),
                         bg="white", fg="#95a5a6")
    separator3.pack(pady=6)
    
    overall_status = "✓ Passed" if current_score >= 18 else "✗ Failed"
    overall_color = "#27ae60" if current_score >= 18 else "#e74c3c"
    
    total_label = tk.Label(white_frame, text="Total Score:",
                          font=("Arial", 13, "bold"),
                          bg="white", fg="#2c3e50")
    total_label.pack(pady=(10,2))
    
    total_score_label = tk.Label(white_frame, text=f"{current_score}/30",
                                 font=("Arial", 26, "bold"),
                                 bg="white", fg="#2c3e50")
    total_score_label.pack(pady=2)
    
    overall_status_label = tk.Label(white_frame, text=overall_status,
                                    font=("Arial", 13, "bold"),
                                    bg="white", fg=overall_color)
    overall_status_label.pack(pady=6)
    
    lives_remaining_label = tk.Label(white_frame, text=f"Lives Remaining: {lives}",
                                    font=("Arial", 12, "bold"),
                                    bg="white", fg="#27ae60")
    lives_remaining_label.pack(pady=10)
    
    save_score(player_name, current_score, total_questions)
    
    button_frame = tk.Frame(white_frame, bg="white")
    button_frame.pack(pady=18)
    
    retry_btn = tk.Button(button_frame, text="RETRY",
                          command=lambda: restart_quiz(current_root),
                          font=("Arial", 10, "bold"),
                          bg="#27ae60", fg="white", 
                          relief="raised", bd=2,
                          width=12, height=2)
    retry_btn.pack(side="left", padx=8)
    
    exit_btn = tk.Button(button_frame, text="EXIT",
                         command=exit_to_main,
                         font=("Arial", 10, "bold"),
                         bg="#e74c3c", fg="white",
                         relief="raised", bd=2,
                         width=12, height=2)
    exit_btn.pack(side="left", padx=8)
    
    print(f"Final score: {current_score}/{total_questions}")

def show_leaderboard():
    leaderboard_text = get_leaderboard_text()
    messagebox.showinfo("Leaderboard", leaderboard_text)

def restart_quiz(root):
    global current_score, current_question_num, fill_blank_score, true_false_score, all_fill_blank, all_true_false, player_name, question_queue, answered_count, lives, canvas, bg_image
    
    # Reset canvas and all variables
    canvas = None
    bg_image = None
    
    for widget in root.winfo_children():
        widget.destroy()
    
    current_score = 0
    current_question_num = 0
    fill_blank_score = 0
    true_false_score = 0
    question_queue = []
    answered_count = 0
    lives = 5
    
    center_window(root, 650, 750)
    
    all_fill_blank = questions_database["fill_in_blank"].copy()
    all_true_false = questions_database["true_false"].copy()
    random.shuffle(all_fill_blank)
    random.shuffle(all_true_false)
    
    start_quiz_game(root, player_name, restart_to_main_callback)