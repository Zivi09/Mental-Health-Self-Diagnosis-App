import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import re
import os
import threading
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set styling configurations
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Pastel Color Palette System (light_color, dark_color)
BG_COLOR = ("#FFFDE7", "#121212")           # Pale lemon yellow / Dark slate
SIDEBAR_BG = ("#B3E5FC", "#1E2B38")         # Pastel blue / Dark blue-grey
TEXT_COLOR = ("#1565C0", "#E0F7FA")         # Deep blue / Ice blue
CARD_BG = ("#FFFFFF", "#1E1E1E")            # White card / Dark grey card
BUTTON_COLOR = ("#81D4FA", "#294D5E")       # Pastel cyan / Slate blue
YELLOW_CARD = ("#FFF9C4", "#302E1B")        # Soft yellow / Deep gold-grey
LIGHT_BLUE_CARD = ("#E1F5FE", "#1B2A38")    # Soft blue card / Slate card
TEXTBOX_BG = ("#FAFAFA", "#181818")         # Warm white / Jet black

class MentalHealthDiagnosisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mental Health Self-Diagnosis Tool (MHSD)")
        self.geometry("1100x700")
        self.configure(fg_color=BG_COLOR)

        # Initialize symptoms variables
        self.name = ""
        self.age = ""
        self.contact = ""
        self.email = ""
        self.gender = ""
        self.history = ""
        self.therapy = ""
        self.biological_factors = ""
        self.disease_history = ""
        self.none_selected = ""
        self.selected_symptoms = []
        self.ai_analysis = ""

        # Initialize API Key
        self.api_key = ""
        self.load_api_key()

        # Database connection
        self.conn = sqlite3.connect('mental_health.db')
        self.create_table_if_not_exists()

        # Layout Setup
        # 1. Left Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR_BG)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Sidebar Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MHSD Tool", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 30))

        # Sidebar buttons
        self.home_btn = self.create_sidebar_btn("🏠 Home", lambda: self.show_frame("home"))
        self.diag_btn = self.create_sidebar_btn("📋 Self-Diagnosis", lambda: self.show_frame("diagnosis"))
        self.chat_btn = self.create_sidebar_btn("💬 AI Chatbot", lambda: self.show_frame("chatbot"))
        self.about_btn = self.create_sidebar_btn("ℹ️ About App", lambda: self.show_frame("about"))
        self.settings_btn = self.create_sidebar_btn("⚙️ Settings", lambda: self.show_frame("settings"))

        # Theme selector in sidebar bottom
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", font=ctk.CTkFont(size=12))
        self.theme_label.pack(side="bottom", padx=20, pady=(10, 5))
        
        self.theme_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"], 
            command=self.change_theme,
            fg_color=BUTTON_COLOR,
            button_color=BUTTON_COLOR,
            button_hover_color=("#4FC3F7", "#1D3642"),
            text_color=("#0D47A1", "#FFFFFF")
        )
        self.theme_optionmenu.pack(side="bottom", padx=20, pady=(0, 20))
        self.theme_optionmenu.set("Dark")

        # 2. Right Dynamic Container Frame
        self.container_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.container_frame.pack(side="right", fill="both", expand=True)

        # Initialize frames
        self.home_page = HomeFrame(self.container_frame, self)
        self.diagnosis_page = DiagnosisFrame(self.container_frame, self)
        self.chatbot_page = ChatbotFrame(self.container_frame, self)
        self.about_page = AboutFrame(self.container_frame, self)
        self.settings_page = SettingsFrame(self.container_frame, self)

        # Show Home page by default
        self.show_frame("home")

    def create_sidebar_btn(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            anchor="w",
            height=40,
            fg_color="transparent",
            text_color=("#0D47A1", "#E0F7FA"),
            hover_color=("#81D4FA", "#294D5E"),
            font=ctk.CTkFont(size=16, weight="bold"),
            command=command
        )
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def show_frame(self, frame_name):
        if frame_name == "diagnosis" and not self.name:
            messagebox.showwarning("Login Required", "Please complete your profile registration on the Home page first to unlock the Self-Diagnosis section.")
            return

        self.home_page.pack_forget()
        self.diagnosis_page.pack_forget()
        self.chatbot_page.pack_forget()
        self.about_page.pack_forget()
        self.settings_page.pack_forget()

        # Reset button styles
        self.home_btn.configure(fg_color="transparent")
        self.diag_btn.configure(fg_color="transparent")
        self.chat_btn.configure(fg_color="transparent")
        self.about_btn.configure(fg_color="transparent")
        self.settings_btn.configure(fg_color="transparent")

        if frame_name == "home":
            self.home_page.pack(fill="both", expand=True)
            self.home_btn.configure(fg_color=BUTTON_COLOR)
        elif frame_name == "diagnosis":
            self.diagnosis_page.pack(fill="both", expand=True)
            self.diag_btn.configure(fg_color=BUTTON_COLOR)
        elif frame_name == "chatbot":
            self.chatbot_page.pack(fill="both", expand=True)
            self.chat_btn.configure(fg_color=BUTTON_COLOR)
        elif frame_name == "about":
            self.about_page.pack(fill="both", expand=True)
            self.about_btn.configure(fg_color=BUTTON_COLOR)
        elif frame_name == "settings":
            self.settings_page.pack(fill="both", expand=True)
            self.settings_btn.configure(fg_color=BUTTON_COLOR)

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def load_api_key(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            self.api_key = api_key
            return
        if os.path.exists(".env"):
            try:
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            key = line.split("=", 1)[1].strip()
                            if key:
                                self.api_key = key
                                return
            except Exception:
                pass

    def get_gemini_client(self):
        if self.api_key:
            return genai.Client(api_key=self.api_key)
        return None

    def create_table_if_not_exists(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS diagnosis_results (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            contact TEXT,
                            email TEXT,
                            gender TEXT,
                            history TEXT,
                            therapy TEXT,
                            biological_factors TEXT,
                            disease_history TEXT,
                            none_selected TEXT,
                            anxiety_symptoms TEXT,
                            depression_symptoms TEXT,
                            fomo_symptoms TEXT,
                            ai_analysis TEXT
                          )''')
        self.conn.commit()

    def insert_into_database(self):
        cursor = self.conn.cursor()
        
        # Schema evolution check
        try:
            cursor.execute("PRAGMA table_info(diagnosis_results)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'ai_analysis' not in columns:
                cursor.execute("ALTER TABLE diagnosis_results ADD COLUMN ai_analysis TEXT")
                self.conn.commit()
        except Exception:
            pass

        # Compile symptom selections
        anxiety_str = ", ".join(self.diagnosis_page.selected_anxiety) if self.diagnosis_page.selected_anxiety else "None"
        depression_str = ", ".join(self.diagnosis_page.selected_depression) if self.diagnosis_page.selected_depression else "None"
        fomo_str = ", ".join(self.diagnosis_page.selected_fomo) if self.diagnosis_page.selected_fomo else "None"

        cursor.execute('''INSERT INTO diagnosis_results 
                          (name, age, contact, email, gender, history, therapy, biological_factors, disease_history, none_selected,
                           anxiety_symptoms, depression_symptoms, fomo_symptoms, ai_analysis)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (self.name, self.age, self.contact, self.email, self.gender, self.history, self.therapy,
                        self.biological_factors, self.disease_history, self.none_selected,
                        anxiety_str, depression_str, fomo_str, self.ai_analysis))
        self.conn.commit()

    def draw_wrapped_string(self, canvas_obj, text, x, y, max_width, height, line_height=14):
        lines = text.split("\n")
        curr_y = y
        for line in lines:
            words = line.split(" ")
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if canvas_obj.stringWidth(test_line) < max_width:
                    current_line.append(word)
                else:
                    canvas_obj.drawString(x, curr_y, ' '.join(current_line))
                    current_line = [word]
                    curr_y -= line_height
                    if curr_y < 50:
                        canvas_obj.showPage()
                        canvas_obj.setFont("Helvetica", 12)
                        curr_y = height - 50
            if current_line:
                canvas_obj.drawString(x, curr_y, ' '.join(current_line))
                curr_y -= line_height
                if curr_y < 50:
                    canvas_obj.showPage()
                    canvas_obj.setFont("Helvetica", 12)
                    curr_y = height - 50
        return curr_y

    def generate_pdf_report(self):
        c = canvas.Canvas("diagnosis_report.pdf", pagesize=letter)
        width, height = letter

        # Write user information
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, "Personal Information:")
        c.drawString(120, height - 120, f"Name: {self.name}")
        c.drawString(120, height - 140, f"Age: {self.age}")
        c.drawString(120, height - 160, f"Contact Number: {self.contact}")
        c.drawString(120, height - 180, f"Email ID: {self.email}")
        c.drawString(120, height - 200, f"Gender: {self.gender}")

        c.drawString(100, height - 240, "Psychiatric History:")
        c.drawString(120, height - 260, f"Past Psychiatric History: {self.history}")
        c.drawString(120, height - 280, f"Have taken therapy before: {self.therapy}")
        c.drawString(120, height - 300, f"Biological Factors: {self.biological_factors}")
        c.drawString(120, height - 320, f"Disease History: {self.disease_history}")
        c.drawString(120, height - 340, f"None selected: {self.none_selected}")

        c.drawString(100, height - 380, "Symptoms Checklist:")
        y_position = height - 400

        # Anxiety List
        if self.diagnosis_page.selected_anxiety:
            c.drawString(120, y_position, "Anxiety Symptoms:")
            y_position -= 20
            for symptom in self.diagnosis_page.selected_anxiety:
                c.drawString(140, y_position, symptom)
                y_position -= 20

        # Depression List
        if self.diagnosis_page.selected_depression:
            c.drawString(120, y_position, "Depression Symptoms:")
            y_position -= 20
            for symptom in self.diagnosis_page.selected_depression:
                c.drawString(140, y_position, symptom)
                y_position -= 20

        # FOMO List
        if self.diagnosis_page.selected_fomo:
            c.drawString(120, y_position, "Fear of Missing Out (FOMO) Symptoms:")
            y_position -= 20
            for symptom in self.diagnosis_page.selected_fomo:
                c.drawString(140, y_position, symptom)
                y_position -= 20

        # Draw AI Analysis section
        if self.ai_analysis:
            if y_position < 150:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50
            
            c.drawString(100, y_position - 20, "AI Diagnosis Analysis & Recommendations:")
            y_position -= 40
            y_position = self.draw_wrapped_string(c, self.ai_analysis, 120, y_position, width - 220, height)

        c.save()


# ---------------------- HOME FRAME ----------------------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Column - Form Card
        self.form_card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.form_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.form_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.form_card, 
            text="Profile Registration", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=(30, 20))

        # Inputs
        self.name_entry = self.create_input("Name")
        self.age_entry = self.create_input("Age")
        self.contact_entry = self.create_input("Contact Number")
        self.email_entry = self.create_input("Email ID")

        # Gender Dropdown
        self.gender_label = ctk.CTkLabel(self.form_card, text="Gender:", anchor="w")
        self.gender_label.pack(fill="x", padx=40, pady=(10, 2))

        self.gender_menu = ctk.CTkOptionMenu(
            self.form_card, 
            values=["Male", "Female", "Other"],
            fg_color=BUTTON_COLOR,
            button_color=BUTTON_COLOR,
            button_hover_color=("#4FC3F7", "#1D3642"),
            text_color=("#0D47A1", "#FFFFFF")
        )
        self.gender_menu.pack(fill="x", padx=40, pady=(0, 20))

        # Button
        self.submit_btn = ctk.CTkButton(
            self.form_card, 
            text="Login & Start Diagnosis", 
            height=45,
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.submit_login
        )
        self.submit_btn.pack(fill="x", padx=40, pady=20)

        # Right Column - Info Card
        self.info_card = ctk.CTkFrame(self, fg_color=YELLOW_CARD, corner_radius=15)
        self.info_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            self.info_card, 
            text="What is Mental Health?", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("#5D4037", "#FFE082")
        ).pack(pady=(30, 10))

        info_text = (
            "Mental health includes our emotional, psychological, and social well-being. "
            "It affects how we think, feel, and act. It also helps determine how we handle stress, "
            "relate to others, and make healthy choices.\n\n"
            "Many people face mental health conditions, and it is nothing to be ashamed of. "
            "They are medical conditions, just like diabetes, and are highly treatable.\n\n"
            "Take a step toward understanding your wellness today using our self-assessment."
        )
        
        self.info_label = ctk.CTkLabel(
            self.info_card, 
            text=info_text, 
            wraplength=350, 
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color=("#5D4037", "#FFE082")
        )
        self.info_label.pack(padx=20, pady=10)

        # Add visual image if exists
        if os.path.exists("mental_health.2.png"):
            try:
                img = Image.open("mental_health.2.png")
                self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(320, 200))
                self.img_label = ctk.CTkLabel(self.info_card, text="", image=self.ctk_img)
                self.img_label.pack(pady=(15, 0))
            except Exception:
                pass

    def create_input(self, placeholder):
        entry = ctk.CTkEntry(
            self.form_card, 
            placeholder_text=placeholder,
            height=40,
            border_color=BUTTON_COLOR
        )
        entry.pack(fill="x", padx=40, pady=10)
        return entry

    def submit_login(self):
        # Retrieve form data
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        gender = self.gender_menu.get()

        # Validation
        if not name or not age_str or not contact or not email:
            messagebox.showerror("Validation Error", "Please fill in all the required fields.")
            return

        # Email check
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return

        # Contact check
        contact_pattern = r'^\d{10}$'
        if not re.match(contact_pattern, contact):
            messagebox.showerror("Validation Error", "Please enter a 10-digit contact number.")
            return

        # Age check
        try:
            age = int(age_str)
            if age < 1 or age > 150:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter an age between 1 and 150.")
            return

        # Save to app variables
        self.app.name = name
        self.app.age = age
        self.app.contact = contact
        self.app.email = email
        self.app.gender = gender

        # Move to Self-Diagnosis screen
        self.app.show_frame("diagnosis")


# ---------------------- DIAGNOSIS WIZARD FRAME ----------------------
class DiagnosisFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Symptom selections storage lists
        self.selected_anxiety = []
        self.selected_depression = []
        self.selected_fomo = []

        # Current step tracker (1: history, 2: symptoms checklist, 3: result page)
        self.step = 1

        # Setup step containers
        self.step1_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.step2_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.step3_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)

        self.setup_step1()
        self.setup_step2()
        self.setup_step3()

        self.show_step(1)

    def show_step(self, step_num):
        self.step1_frame.pack_forget()
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()

        self.step = step_num
        if step_num == 1:
            self.step1_frame.pack(fill="both", expand=True, padx=20, pady=20)
        elif step_num == 2:
            self.step2_frame.pack(fill="both", expand=True, padx=20, pady=20)
        elif step_num == 3:
            self.step3_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.generate_ai_analysis()

    # STEP 1: Psychiatric History UI
    def setup_step1(self):
        ctk.CTkLabel(
            self.step1_frame, 
            text="Step 1: Psychiatric History", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=20)

        # Past Psychiatric History input
        self.history_label = ctk.CTkLabel(self.step1_frame, text="Past Psychiatric History Details:", anchor="w")
        self.history_label.pack(fill="x", padx=60, pady=(15, 2))

        self.history_entry = ctk.CTkEntry(
            self.step1_frame, 
            placeholder_text="Describe any past psychiatric history or details here...",
            height=40,
            border_color=BUTTON_COLOR
        )
        self.history_entry.pack(fill="x", padx=60, pady=(0, 20))

        # Checkboxes
        self.therapy_var = tk.IntVar()
        self.therapy_cb = ctk.CTkCheckBox(
            self.step1_frame, 
            text="Have you taken therapy before?", 
            variable=self.therapy_var
        )
        self.therapy_cb.pack(anchor="w", padx=60, pady=10)

        self.biological_var = tk.IntVar()
        self.biological_cb = ctk.CTkCheckBox(
            self.step1_frame, 
            text="Have you experienced any medical/biological factors?", 
            variable=self.biological_var
        )
        self.biological_cb.pack(anchor="w", padx=60, pady=10)

        self.disease_var = tk.IntVar()
        self.disease_cb = ctk.CTkCheckBox(
            self.step1_frame, 
            text="Have you had any mental illness before?", 
            variable=self.disease_var
        )
        self.disease_cb.pack(anchor="w", padx=60, pady=10)

        # None of the above logic
        self.none_var = tk.IntVar()
        def clear_other_options():
            if self.none_var.get() == 1:
                self.therapy_var.set(0)
                self.biological_var.set(0)
                self.disease_var.set(0)

        self.none_cb = ctk.CTkCheckBox(
            self.step1_frame, 
            text="None of the above options apply", 
            variable=self.none_var,
            command=clear_other_options
        )
        self.none_cb.pack(anchor="w", padx=60, pady=10)

        # Navigation Button
        self.to_step2_btn = ctk.CTkButton(
            self.step1_frame, 
            text="Next: Symptoms Checklist", 
            height=45,
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.submit_step1
        )
        self.to_step2_btn.pack(fill="x", padx=60, pady=30)

    def submit_step1(self):
        # Validate selection
        if not self.history_entry.get().strip() and self.therapy_var.get() == 0 and self.biological_var.get() == 0 and self.disease_var.get() == 0 and self.none_var.get() == 0:
            messagebox.showerror("Validation Error", "Please provide some information in the text field or select at least one checkbox.")
            return

        # Save variables to app state
        self.app.history = self.history_entry.get().strip()
        self.app.therapy = "Yes" if self.therapy_var.get() == 1 else "No"
        self.app.biological_factors = "Yes" if self.biological_var.get() == 1 else "No"
        self.app.disease_history = "Yes" if self.disease_var.get() == 1 else "No"
        self.app.none_selected = "Yes" if self.none_var.get() == 1 else "No"

        # Show next step
        self.show_step(2)

    # STEP 2: Scrollable Checklist UI
    def setup_step2(self):
        ctk.CTkLabel(
            self.step2_frame, 
            text="Step 2: Symptoms Checklist", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=10)

        # Scrollable Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self.step2_frame, label_text="Check all the symptoms that apply to you:")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Column containers inside scrollable area
        self.scroll_frame.columnconfigure(0, weight=1)
        self.scroll_frame.columnconfigure(1, weight=1)
        self.scroll_frame.columnconfigure(2, weight=1)

        # Anxiety column
        anxiety_label = ctk.CTkLabel(self.scroll_frame, text="Anxiety Symptoms", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#0D47A1", "#4FC3F7"))
        anxiety_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.anxiety_symptoms = [
            "Churning feeling in your stomach",
            "Feeling light-headed or dizzy",
            "Pins and needles",
            "Feeling restless or unable to sit still",
            "Headaches, backache, or other aches and pains",
            "Faster breathing",
            "Fast, thumping, or irregular heartbeat",
            "Sweating or hot flushes",
            "Sleep problems",
            "Grinding your teeth, especially at night",
            "Nausea (feeling sick)",
            "Needing the toilet more or less often",
            "Changes in your sex drive",
            "Having panic attacks"
        ]
        self.anxiety_checkbox_vars = []
        for index, item in enumerate(self.anxiety_symptoms):
            var = tk.IntVar()
            self.anxiety_checkbox_vars.append(var)
            cb = ctk.CTkCheckBox(self.scroll_frame, text=item, variable=var)
            cb.grid(row=index+1, column=0, padx=10, pady=5, sticky="w")

        # Depression column
        dep_label = ctk.CTkLabel(self.scroll_frame, text="Depression Symptoms", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#0D47A1", "#4FC3F7"))
        dep_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.dep_symptoms = [
            "Clinical depression",
            "Bipolar disorder",
            "Feelings of helplessness and hopelessness",
            "Loss of interest in daily activities",
            "Appetite or weight changes",
            "Anger or irritability",
            "Loss of energy",
            "Self-isolating",
            "Self-harm",
            "Reckless behavior"
        ]
        self.dep_checkbox_vars = []
        for index, item in enumerate(self.dep_symptoms):
            var = tk.IntVar()
            self.dep_checkbox_vars.append(var)
            cb = ctk.CTkCheckBox(self.scroll_frame, text=item, variable=var)
            cb.grid(row=index+1, column=1, padx=10, pady=5, sticky="w")

        # FOMO column
        fomo_label = ctk.CTkLabel(self.scroll_frame, text="FOMO Symptoms", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#0D47A1", "#4FC3F7"))
        fomo_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.fomo_symptoms = [
            "Feeling negative/excluded when missing out",
            "Low life satisfaction",
            "High social media activity",
            "Fast-paced lifestyle",
            "Concerned about other people’s opinions",
            "The urge to be surrounded by others",
            "Poor health behaviours",
            "Distracted Driving"
        ]
        self.fomo_checkbox_vars = []
        for index, item in enumerate(self.fomo_symptoms):
            var = tk.IntVar()
            self.fomo_checkbox_vars.append(var)
            cb = ctk.CTkCheckBox(self.scroll_frame, text=item, variable=var)
            cb.grid(row=index+1, column=2, padx=10, pady=5, sticky="w")

        # Navigation Bottom Buttons
        self.step2_nav_frame = ctk.CTkFrame(self.step2_frame, fg_color="transparent")
        self.step2_nav_frame.pack(fill="x", padx=20, pady=15)

        self.back_to_step1 = ctk.CTkButton(
            self.step2_nav_frame, 
            text="Back", 
            width=100,
            fg_color="transparent",
            border_width=2,
            border_color=BUTTON_COLOR,
            text_color=TEXT_COLOR,
            hover_color=("#E1F5FE", "#1E2B38"),
            command=lambda: self.show_step(1)
        )
        self.back_to_step1.pack(side="left")

        self.submit_checklist_btn = ctk.CTkButton(
            self.step2_nav_frame, 
            text="Submit Checklist & Get AI Recommendations", 
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.submit_step2
        )
        self.submit_checklist_btn.pack(side="right")

    def submit_step2(self):
        # Extract selected checklists
        self.selected_anxiety = [symptom for symptom, var in zip(self.anxiety_symptoms, self.anxiety_checkbox_vars) if var.get()]
        self.selected_depression = [symptom for symptom, var in zip(self.dep_symptoms, self.dep_checkbox_vars) if var.get()]
        self.selected_fomo = [symptom for symptom, var in zip(self.fomo_symptoms, self.fomo_checkbox_vars) if var.get()]

        self.show_step(3)

    # STEP 3: AI Recommendations and PDF Export UI
    def setup_step3(self):
        ctk.CTkLabel(
            self.step3_frame, 
            text="Step 3: Self-Diagnosis Results", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=10)

        # Scrolled Text panel styled cleanly
        self.results_textbox = ctk.CTkTextbox(
            self.step3_frame, 
            wrap="word", 
            font=ctk.CTkFont(size=15),
            fg_color=TEXTBOX_BG,
            border_color=BUTTON_COLOR,
            border_width=1
        )
        self.results_textbox.pack(fill="both", expand=True, padx=20, pady=10)

        # Navigation row
        self.step3_nav_frame = ctk.CTkFrame(self.step3_frame, fg_color="transparent")
        self.step3_nav_frame.pack(fill="x", padx=20, pady=15)

        self.back_to_step2 = ctk.CTkButton(
            self.step3_nav_frame, 
            text="Retake assessment", 
            fg_color="transparent",
            border_width=2,
            border_color=BUTTON_COLOR,
            text_color=TEXT_COLOR,
            hover_color=("#E1F5FE", "#1E2B38"),
            command=lambda: self.show_step(2)
        )
        self.back_to_step2.pack(side="left")

        # Action Buttons will pack dynamically when AI analysis finishes
        self.download_btn = ctk.CTkButton(
            self.step3_nav_frame, 
            text="Download PDF Report", 
            fg_color=LIGHT_BLUE_CARD,
            text_color=("#0D47A1", "#E0F7FA"),
            hover_color=("#B3E5FC", "#23394D"),
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.download_pdf
        )
        
        self.feedback_btn = ctk.CTkButton(
            self.step3_nav_frame, 
            text="Provide Feedback", 
            fg_color=YELLOW_CARD,
            text_color=("#5D4037", "#FFE082"),
            hover_color=("#FFF59D", "#3B3821"),
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.open_feedback_modal
        )

    def generate_ai_analysis(self):
        # Reset button visibility
        self.download_btn.pack_forget()
        self.feedback_btn.pack_forget()

        # Build initial display details
        self.results_textbox.configure(state='normal')
        self.results_textbox.delete("1.0", tk.END)

        profile_details = (
            f"Personal Profile Information:\n"
            f"- Name: {self.app.name}\n"
            f"- Age: {self.app.age}\n"
            f"- Gender: {self.app.gender}\n"
            f"- Email ID: {self.app.email}\n"
            f"- Contact Number: {self.app.contact}\n\n"
            f"Psychiatric History:\n"
            f"- Past Psychiatric History: {self.app.history}\n"
            f"- Taken therapy before: {self.app.therapy}\n"
            f"- Experienced biological factors: {self.app.biological_factors}\n"
            f"- Had mental illness before: {self.app.disease_history}\n\n"
            f"Symptom Checklist Results:\n"
            f"- Anxiety symptoms checked: {', '.join(self.selected_anxiety) if self.selected_anxiety else 'None'}\n"
            f"- Depression symptoms checked: {', '.join(self.selected_depression) if self.selected_depression else 'None'}\n"
            f"- FOMO symptoms checked: {', '.join(self.selected_fomo) if self.selected_fomo else 'None'}\n\n"
        )
        self.results_textbox.insert(tk.END, profile_details)

        # Check API key configuration
        client = self.app.get_gemini_client()
        if not client:
            self.app.ai_analysis = "Gemini API Key is not set. Go to Settings on the left sidebar to generate AI recommendations."
            self.results_textbox.insert(tk.END, f"AI recommendations:\n{self.app.ai_analysis}\n")
            self.results_textbox.configure(state='disabled')
            
            # Show buttons immediately since no AI loading is needed
            self.app.insert_into_database()
            self.download_btn.pack(side="right", padx=10)
            self.feedback_btn.pack(side="right", padx=10)
            return

        self.results_textbox.insert(tk.END, "AI diagnosis analysis & recommendations:\n[Generating dynamic AI report... please wait.]\n")
        self.results_textbox.configure(state='disabled')

        def fetch_analysis_thread():
            anxiety_str = ", ".join(self.selected_anxiety) if self.selected_anxiety else "None"
            depression_str = ", ".join(self.selected_depression) if self.selected_depression else "None"
            fomo_str = ", ".join(self.selected_fomo) if self.selected_fomo else "None"

            prompt = (
                f"You are a supportive mental wellness assistant.\n"
                f"Analyze the following user profile and selected symptoms:\n\n"
                f"User: {self.app.name}, Age: {self.app.age}, Gender: {self.app.gender}\n"
                f"Psychiatric History: {self.app.history} (Therapy before: {self.app.therapy}, Bio-factors: {self.app.biological_factors}, Prev Illness: {self.app.disease_history})\n"
                f"Selected Symptoms:\n"
                f"- Anxiety: {anxiety_str}\n"
                f"- Depression: {depression_str}\n"
                f"- FOMO: {fomo_str}\n\n"
                f"Please generate a short, simple, and easy-to-understand summary of results. "
                f"Do not use complicated medical jargon. Use bullet points and simple language.\n"
                f"Structure your response exactly as follows in under 200 words:\n"
                f"1. **Summary of Concerns**: Briefly state what the checked symptoms suggest in friendly, simple terms (no clinical diagnosis).\n"
                f"2. **Simple Action Steps**: 2-3 very easy wellness tips they can do today.\n"
                f"3. **Next Steps**: A simple, encouraging reminder to speak with a professional if they need further support."
            )
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config={
                        "temperature": 0.2,
                        "top_p": 0.9,
                        "max_output_tokens": 400
                    }
                )
                self.app.ai_analysis = response.text

                def update_textbox():
                    self.results_textbox.configure(state='normal')
                    # Remove placeholder
                    content = self.results_textbox.get("1.0", tk.END)
                    placeholder = "[Generating dynamic AI report... please wait.]"
                    p_idx = content.find(placeholder)
                    if p_idx != -1:
                        lines_before = content[:p_idx].count('\n') + 1
                        self.results_textbox.delete(f"{lines_before}.0", tk.END)
                        self.results_textbox.insert(tk.END, "\n")
                    
                    self.results_textbox.insert(tk.END, self.app.ai_analysis)
                    self.results_textbox.configure(state='disabled')

                    # Write to database and show actions
                    self.app.insert_into_database()
                    self.download_btn.pack(side="right", padx=10)
                    self.feedback_btn.pack(side="right", padx=10)

                self.after(0, update_textbox)
            except Exception as e:
                self.app.ai_analysis = f"Failed to generate analysis: {e}"
                def show_error():
                    self.results_textbox.configure(state='normal')
                    self.results_textbox.insert(tk.END, f"\nError: {self.app.ai_analysis}\n")
                    self.results_textbox.configure(state='disabled')
                    self.app.insert_into_database()
                    self.download_btn.pack(side="right", padx=10)
                    self.feedback_btn.pack(side="right", padx=10)
                self.after(0, show_error)

        threading.Thread(target=fetch_analysis_thread, daemon=True).start()

    def download_pdf(self):
        self.app.generate_pdf_report()
        messagebox.showinfo("Export Successful", "Dynamic PDF Report saved as 'diagnosis_report.pdf' inside the project folder.")

    def open_feedback_modal(self):
        feedback_window = ctk.CTktoplevel(self)
        feedback_window.title("Provide Feedback")
        feedback_window.geometry("500x380")
        feedback_window.lift()
        feedback_window.focus_force()

        ctk.CTkLabel(
            feedback_window, 
            text="User Feedback & Suggestions", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=15)

        ctk.CTkLabel(
            feedback_window, 
            text="Help us improve. Share your feedback or report problems:",
            wraplength=420
        ).pack(pady=5)

        text_input = ctk.CTkTextbox(feedback_window, height=150, border_color=BUTTON_COLOR, border_width=1)
        text_input.pack(fill="both", expand=True, padx=20, pady=10)

        def send_feedback():
            feedback_msg = text_input.get("1.0", "end-1c").strip()
            if not feedback_msg:
                return
            messagebox.showinfo("Feedback Received", "Thank you! Your feedback report has been saved successfully.")
            feedback_window.destroy()

        btn = ctk.CTkButton(
            feedback_window, 
            text="Submit Feedback",
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            command=send_feedback
        )
        btn.pack(pady=15)


# ---------------------- CHATBOT FRAME ----------------------
class ChatbotFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Card
        self.header_card = ctk.CTkFrame(self, height=60, fg_color=LIGHT_BLUE_CARD, corner_radius=10)
        self.header_card.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="nsew")
        
        self.chat_title = ctk.CTkLabel(
            self.header_card, 
            text="Mental Fitness AI Companion", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.chat_title.pack(pady=15)

        # Chat history console
        self.chat_history = ctk.CTkTextbox(
            self, 
            wrap="word", 
            state="disabled", 
            font=ctk.CTkFont(size=15),
            fg_color=TEXTBOX_BG,
            border_color=BUTTON_COLOR,
            border_width=1
        )
        self.chat_history.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        # Bottom Input area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Message your mental wellness coach...", 
            height=40,
            border_color=BUTTON_COLOR
        )
        self.message_entry.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="Send", 
            width=90, 
            height=40,
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, sticky="nsew")

        # Add generic prompt greeting
        self.print_chat("AI", "Hello! I am your AI mental fitness companion. How can I help you support your wellness today?")

    def print_chat(self, sender, message):
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.yview(tk.END)

    def send_message(self):
        user_msg = self.message_entry.get().strip()
        if not user_msg:
            return

        self.print_chat("You", user_msg)
        self.message_entry.delete(0, tk.END)

        client = self.app.get_gemini_client()
        if not client:
            self.print_chat("AI", "Gemini API Key is not set. Go to Settings on the left sidebar to configure it.")
            return

        # Set loading status
        self.send_btn.configure(state="disabled")
        self.message_entry.configure(state="disabled")
        self.print_chat("AI", "Thinking...")

        def fetch_response_thread():
            try:
                # Initialize Chat Session if not present
                if not hasattr(self, 'chat_session'):
                    system_instruction = (
                        "You are an empathetic, supportive, and friendly mental fitness and wellness companion.\n"
                        "Follow these strict rules:\n"
                        "1. Role: Act as a supportive coach for stress management, sleep hygiene, and emotional well-being.\n"
                        "2. Safety: If the user indicates self-harm, suicidal thoughts, or a severe crisis, immediately provide helpline info (e.g., 988 Suicide & Crisis Lifeline) and advise seeking professional help.\n"
                        "3. Scope: Do NOT provide clinical diagnoses or prescribe treatments. Emphasize you are a helper, not a doctor.\n"
                        "4. Style: Keep responses warm, encouraging, conversational, and concise (under 150 words). Use bullet points for readability."
                    )
                    try:
                        self.chat_session = client.chats.create(
                            model='gemini-2.5-flash',
                            config={
                                "system_instruction": system_instruction,
                                "temperature": 0.7,
                                "top_p": 0.9,
                                "max_output_tokens": 600
                            }
                        )
                    except Exception:
                        self.chat_session = client.chats.create(
                            model='gemini-2.5-flash',
                            config={
                                "temperature": 0.7,
                                "top_p": 0.9,
                                "max_output_tokens": 600
                            }
                        )

                response = self.chat_session.send_message(user_msg)
                ai_reply = response.text

                def update_ui():
                    self.chat_history.configure(state="normal")
                    content = self.chat_history.get("1.0", tk.END)
                    placeholder = "AI: Thinking...\n\n"
                    idx = content.rfind(placeholder)
                    if idx != -1:
                        lines_before = content[:idx].count('\n') + 1
                        self.chat_history.delete(f"{lines_before}.0", tk.END)
                        self.chat_history.insert(tk.END, "\n")
                    self.chat_history.configure(state="disabled")

                    self.print_chat("AI", ai_reply)
                    self.send_btn.configure(state="normal")
                    self.message_entry.configure(state="normal")
                    self.message_entry.focus()

                self.after(0, update_ui)
            except Exception as e:
                error_msg = str(e)
                def show_error():
                    self.chat_history.configure(state="normal")
                    content = self.chat_history.get("1.0", tk.END)
                    placeholder = "AI: Thinking...\n\n"
                    idx = content.rfind(placeholder)
                    if idx != -1:
                        lines_before = content[:idx].count('\n') + 1
                        self.chat_history.delete(f"{lines_before}.0", tk.END)
                        self.chat_history.insert(tk.END, "\n")
                    self.chat_history.configure(state="disabled")

                    self.print_chat("AI", f"Error generating reply: {error_msg}")
                    self.send_btn.configure(state="normal")
                    self.message_entry.configure(state="normal")
                    self.message_entry.focus()
                self.after(0, show_error)

        threading.Thread(target=fetch_response_thread, daemon=True).start()


# ---------------------- ABOUT FRAME ----------------------
class AboutFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Scrollable about window
        self.scroll_about = ctk.CTkScrollableFrame(self, label_text="About the MHSDT Application")
        self.scroll_about.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            self.scroll_about, 
            text="Know About MHSDT", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=15)

        about_text = (
            "The Mental Health Self-Diagnosis Tool (MHSDT) is an innovative digital platform "
            "designed to raise awareness and promote proactive mental health management.\n\n"
            "By guiding users through dynamic questions, psychiatric history logs, and symptom checklists, "
            "the app compiles detailed profiles and feeds them to Gemini AI to generate personalized "
            "analyses, lifestyle coping suggestions, and custom wellness recommendations.\n\n"
            "Features include a real-time AI Chatbot for emotional de-escalation, immediate PDF diagnostic report downloads, "
            "and theme customization setups.\n\n"
            "Designed to prioritize absolute user privacy, this tool is ideal for local study, college computer labs, "
            "or work desktop sessions."
        )

        self.about_lbl = ctk.CTkLabel(
            self.scroll_about, 
            text=about_text,
            wraplength=600,
            justify="center",
            font=ctk.CTkFont(size=15)
        )
        self.about_lbl.pack(padx=20, pady=10)

        # Image if exists
        if os.path.exists("mental_health.1.png"):
            try:
                img = Image.open("mental_health.1.png")
                self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 250))
                self.img_lbl = ctk.CTkLabel(self.scroll_about, text="", image=self.ctk_img)
                self.img_lbl.pack(pady=20)
            except Exception:
                pass

        # Disclaimer
        disclaimer_card = ctk.CTkFrame(self.scroll_about, fg_color=YELLOW_CARD, corner_radius=10)
        disclaimer_card.pack(fill="x", padx=40, pady=20)

        disclaimer_text = (
            "⚠️ Disclaimer: The outcomes and AI suggestions generated by this tool are for educational and "
            "self-awareness purposes only. They DO NOT constitute professional medical advice or a certified psychiatric diagnosis. "
            "Please consult a certified mental health professional for medical consultations."
        )
        
        self.disclaimer_lbl = ctk.CTkLabel(
            disclaimer_card, 
            text=disclaimer_text,
            wraplength=500,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#5D4037", "#FFE082"),
            pady=10
        )
        self.disclaimer_lbl.pack(padx=15, pady=5)


# ---------------------- SETTINGS FRAME ----------------------
class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Card container
        self.card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.card, 
            text="Settings Configuration", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(pady=25)

        # Gemini API settings
        ctk.CTkLabel(
            self.card, 
            text="Google Gemini API Key:", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=60, pady=(10, 2))

        self.key_entry = ctk.CTkEntry(
            self.card, 
            placeholder_text="Enter API Key (e.g. AIzaSy...)", 
            show="*", 
            height=40,
            border_color=BUTTON_COLOR
        )
        self.key_entry.pack(fill="x", padx=60, pady=5)
        if self.app.api_key:
            self.key_entry.insert(0, self.app.api_key)

        # Save Button
        self.save_btn = ctk.CTkButton(
            self.card, 
            text="Save API Key", 
            height=40,
            fg_color=BUTTON_COLOR,
            text_color=("#0D47A1", "#FFFFFF"),
            hover_color=("#4FC3F7", "#1D3642"),
            command=self.save_key
        )
        self.save_btn.pack(anchor="w", padx=60, pady=15)

        # Theme color guide representation
        theme_guide_frame = ctk.CTkFrame(self.card, fg_color=LIGHT_BLUE_CARD, corner_radius=10)
        theme_guide_frame.pack(fill="x", padx=60, pady=30)

        theme_guide_text = (
            "🎨 Pastel Theme Palette Activated!\n"
            "This modern interface uses a custom light/dark design theme incorporating soft light blues, "
            "lemon yellows, and warm card layers. Toggle 'Appearance Mode' in the bottom-left corner to "
            "switch between Light and Dark styles instantly."
        )

        ctk.CTkLabel(
            theme_guide_frame, 
            text=theme_guide_text,
            wraplength=480,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color=("#0D47A1", "#E0F7FA"),
            pady=15
        ).pack(padx=20)

    def save_key(self):
        new_key = self.key_entry.get().strip()
        self.app.api_key = new_key
        if hasattr(self.app.chatbot_page, 'chat_session'):
            delattr(self.app.chatbot_page, 'chat_session')
        try:
            with open(".env", "w") as f:
                f.write(f"GEMINI_API_KEY={new_key}\n")
            messagebox.showinfo("Saved", "Gemini API Key saved and loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API Key locally: {e}")


# ---------------------- APP INITIALIZATION ----------------------
if __name__ == "__main__":
    app = MentalHealthDiagnosisApp()
    app.mainloop()
