import tkinter as tk
from tkinter import messagebox
import re  
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from tkinter import scrolledtext
from tkinter import PhotoImage
from reportlab.lib.units import inch
from reportlab.lib import colors



class MentalHealthDiagnosisApp:
    def __init__(self, master):
        self.master = master
        master.title("MHSD")
        master.geometry("11500x1500")


        # Initialize symptoms_window as None
        self.symptoms_window = None

        # Initialize variables to store user data
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

        # Load the image file

        self.bg_image = tk.PhotoImage(file="D:/mental_health.2.png")
        # Create a Label widget to display the background image
        self.background_label = tk.Label(self.master, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Set label size to fill the window

        # Header
        header_label = tk.Label(master, text="Welcome to Mental Health Self-Diagnosis ", font=("Arial", 20, "bold"))
        header_label.pack(pady=20)

        # Styling
        font_style = ("Arial", 18)

        # Left side (Form)
        left_frame = tk.Frame(master)
        left_frame.pack(side="left", padx=20, pady=20)

        tk.Label(left_frame, text="Name:", font=font_style).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(left_frame, font=font_style)
        self.name_entry.grid(row=0, column=1)

        tk.Label(left_frame, text="Age:", font=font_style).grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(left_frame, font=font_style)
        self.age_entry.grid(row=1, column=1)

        tk.Label(left_frame, text="Contact Number:", font=font_style).grid(row=2, column=0, sticky="w")
        self.contact_entry = tk.Entry(left_frame, font=font_style)
        self.contact_entry.grid(row=2, column=1)

        tk.Label(left_frame, text="Email ID:", font=font_style).grid(row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(left_frame, font=font_style)
        self.email_entry.grid(row=3, column=1)

        tk.Label(left_frame, text="Gender:", font=font_style).grid(row=4, column=0, sticky="w")
        self.gender_var = tk.StringVar(master)
        self.gender_var.set("Male")
        gender_dropdown = tk.OptionMenu(left_frame, self.gender_var, "Male", "Female", "Other")
        gender_dropdown.config(font=font_style)
        gender_dropdown.grid(row=4, column=1)

        submit_button = tk.Button(left_frame, text="Login", command=self.show_symptoms, font=font_style)
        submit_button.grid(row=5, columnspan=2, pady=10)
              # Right side (Additional Information)
        right_frame = tk.Frame(master, bg="#f5f5dc")
        right_frame.pack(side="right", padx=10, pady=10,expand=True)

        additional_info_label = tk.Label(right_frame, text="What is Mental Health..??",bg="#f5f5dc", font=("Arial", 20, "bold"))
        additional_info_label.pack()

        additional_info_text = """
        Mental health is the foundation for emotions, thinking, communication, learning, resilience, hope, and self-esteem. Mental health is also key to relationships, personal and emotional well-being, and contributing to the community or society. Mental health is a component of overall well-being. It can influence and be influenced by physical health.

        Many people who have a mental illness do not want to talk about it. But mental illness is nothing to be ashamed of! It is a medical condition, just like heart disease or diabetes. And mental health conditions are treatable. We are continually expanding our understanding of how the human brain works, and treatments are available to help people successfully manage mental health conditions.

        Mental illness does not discriminate; it can affect anyone regardless of your age, gender, geography, income, social status, race, ethnicity, religion/spirituality, sexual orientation, background, or other aspects of cultural identity. While mental illness can occur at any age, three-fourths of all mental illness begins by age 24.
    
        Mental illnesses take many forms. Some are mild and only interfere in limited ways with daily life, such as some phobias (abnormal fears). Other mental health conditions are so severe that a person may need care in a hospital. Similar to other medical illnesses, the optimal ways to provide care depend on the illness and the severity of its impact.

        """

        additional_info_para = tk.Label(right_frame, text=additional_info_text, font=font_style, bg="Light Pink", wraplength=800, justify="left")
        additional_info_para.pack(pady=10)
        
        # Initialize database connection
        self.conn = sqlite3.connect('mental_health.db')
        self.create_table_if_not_exists()

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
                            fomo_symptoms TEXT
                          )''')
        self.conn.commit()

    def show_symptoms(self):
##        # Validation for mandatory fields
##        if not self.name_entry.get() or not self.age_entry.get() or not self.contact_entry.get() or not self.email_entry.get():
##            messagebox.showerror("Error", "Please fill in all the required fields.")
##            return
##
##        # Validation for email format
##        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
##        if not re.match(email_pattern, self.email_entry.get()):
##            messagebox.showerror("Error", "Please enter a valid email address.")
##            return
##
##        # Validation for contact number format (for demonstration, assuming a 10-digit number)
##        contact_pattern = r'^\d{10}$'
##        if not re.match(contact_pattern, self.contact_entry.get()):
##            messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
##            return
##        # Validation for age
##
##        try:
##            age = int(self.age_entry.get())
##            if age < 1 or age > 150:  # Assuming a reasonable age range
##                raise ValueError
##        except ValueError:
##            messagebox.showerror("Error", "Please enter a valid age between 1 and 150.")
##            return



        # Retrieve user data from the form
        self.name = self.name_entry.get()
        self.age = self.age_entry.get()
        self.contact = self.contact_entry.get()
        self.email = self.email_entry.get()
        self.gender = self.gender_var.get()

        # Second Page - Psychiatric History
        self.open_second_window()

    def open_second_window(self):
        second_window = tk.Toplevel(self.master)
        second_window.title("Psychiatric History")

        second_window.geometry("11500x1500")

##        self.bg_image2= tk.PhotoImage(file="D:\mental_health.3.png")
##        # Create a Label widget to display the background image
##        self.second_window= tk.Label(self.second_window, image=self.bg_image2)
##        self.second_window.place(relwidth=1, relheight=1)  # Set label size to fill the window

        font_style = ("Arial", 20)

        tk.Label(second_window, text="Psychiatric History", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(second_window, text="Past Psychiatric History:", font=font_style).pack(anchor="w")
        self.history_entry = tk.Entry(second_window, font=font_style, width=30)
        self.history_entry.pack(pady=5)

        self.therapy_var = tk.IntVar()
        tk.Checkbutton(second_window, text="Have you taken therapy before?", variable=self.therapy_var, font=font_style).pack(anchor="w")

        self.biological_var = tk.IntVar()
        tk.Checkbutton(second_window, text="Have you experienced any medical factors?", variable=self.biological_var, font=font_style).pack(anchor="w")

        self.disease_var = tk.IntVar()
        tk.Checkbutton(second_window, text="Have you had any mental illiness before?", variable=self.disease_var, font=font_style).pack(anchor="w")

        self.none_var = tk.IntVar()
        def handle_none_selection():
            if self.none_var.get() == 1:
                self.therapy_var.set(0)
                self.biological_var.set(0)
                self.disease_var.set(0)# gotta make changes here

        none_checkbox = tk.Checkbutton(second_window, text="None of the above", variable=self.none_var, font=font_style, command=handle_none_selection)
        none_checkbox.pack(anchor="w")

        next_button = tk.Button(second_window, text="Next", command=self.show_diagnosis,font=font_style)
        next_button.pack(pady=10)


    def show_diagnosis(self):
##        if not self.history_entry.get() and self.therapy_var.get() == 0 and self.biological_var.get() == 0 and self.disease_var.get() == 0 and self.none_var.get() == 0:
##            messagebox.showerror("Error", "Please provide some information in the Psychiatric History section or select at least one option.")
##            return

        # Retrieve user data from the second window
        self.history = self.history_entry.get() 
        self.therapy = "Yes" if self.therapy_var.get() == 1 else "No" 
        self.biological_factors = "Yes" if self.biological_var.get() == 1 else "No"
        self.disease_history = "Yes" if self.disease_var.get() == 1 else "No"
        self.none_selected = "Yes" if self.none_var.get() == 1 else "No"

        # Third Page - Symptoms Checklist
        self.open_symptoms_window()

    def open_symptoms_window(self):
        self.symptoms_window = tk.Toplevel(self.master)
        self.symptoms_window.title("Symptoms Checklist")
        self.symptoms_window.geometry("11500x1500")

        font_style = ("Arial", 18)

        # Create a canvas
        canvas = tk.Canvas(self.symptoms_window)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self.symptoms_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the checklist
        checklist_frame = tk.Frame(canvas, bg="lightblue")
        canvas.create_window((0, 0), window=checklist_frame, anchor="nw")

        # Initialize lists to hold IntVar objects for each category of symptoms
        self.anxiety_vars = []
        self.depression_vars = []
        self.fomo_vars = []

        # Define a function to create checkbuttons with a given list of symptoms
        def create_checkbuttons(symptoms_list, column=0, vars_list=None):
            for i, symptom in enumerate(symptoms_list):
                var = tk.IntVar()
                vars_list.append(var)  # Append the IntVar to the corresponding list

                # Create a frame to hold each symptom and its scale
                symptom_frame = tk.Frame(checklist_frame, bg="lightblue")
                symptom_frame.grid(row=i, column=column, sticky="w", padx=10, pady=5)

                # Checkbutton
                check_button = tk.Checkbutton(symptom_frame, text=symptom, variable=var, bg="lightblue",font=("Arial", 18))
                check_button.pack(side="left")

                font_style = ("Arial", 18)
    
##                # Scale
##                scale = tk.Scale(symptom_frame, from_=0, to=10, orient="horizontal")
##                scale.pack(side="left")

        # Divide the symptoms into three columns
        anxiety_symptoms_list = [
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
        create_checkbuttons(anxiety_symptoms_list, column=0, vars_list=self.anxiety_vars)

        depression_symptoms_list = [
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
        create_checkbuttons(depression_symptoms_list, column=1, vars_list=self.depression_vars)

        fomo_symptoms_list = [
            "Feeling negative/excluded when missing out",
            "Low life satisfaction",
            "High social media activity",
            "Fast-paced lifestyle",
            "Concerned about other people’s opinions",
            "The urge to be surrounded by others",
            "Poor health behaviours",
            "Distracted Driving"
        ]
        create_checkbuttons(fomo_symptoms_list, column=2, vars_list=self.fomo_vars)

        # Use grid for the submit button
        submit_button = tk.Button(self.symptoms_window, text="Next", command=self.show_result, bg="blue", fg="white",font=font_style)
        submit_button.pack(pady=20)


    def show_result(self):
        # Fourth Page - Result
        result_window = tk.Toplevel(self.master)
        result_window.title("Result Page")
        result_window.geometry("11500x1500")

        tk.Label(result_window, text="Result Page", font=("Arial", 20, "bold")).pack(pady=10)

          # Create a scrolled text widget for displaying the result content
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=50, height=20)
        result_text.pack(expand=True,fill="both", padx=10, pady=10)

##        fill="both"

        # Display user data and other content in the scrolled text widget
        result_text.insert(tk.END, "Personal Information:\n")
        result_text.insert(tk.END, f"Name: {self.name}\n")
        result_text.insert(tk.END, f"Age: {self.age}\n")
        result_text.insert(tk.END, f"Contact Number: {self.contact}\n")
        result_text.insert(tk.END, f"Email ID: {self.email}\n")
        result_text.insert(tk.END, f"Gender: {self.gender}\n\n")

        result_text.insert(tk.END, "Psychiatric History:\n")
        result_text.insert(tk.END, f"Past Psychiatric History: {self.history}\n")
        result_text.insert(tk.END, f"Have taken therapy before: {self.therapy}\n")
        result_text.insert(tk.END, f"Biological Factors: {self.biological_factors}\n")
        result_text.insert(tk.END, f"Disease History: {self.disease_history}\n")
        result_text.insert(tk.END, f"None selected: {self.none_selected}\n\n")

        result_text.insert(tk.END, "Symptoms Checklist:\n")
        if self.anxiety_vars:
            selected_anxiety_symptoms = [symptom for symptom, var in zip(
                ["Churning feeling in your stomach",
                 "Feeling light-headed or dizzy",
                 "Pins and needles",
                 "Feeling restless or unable to sit still",
                 "Faster breathing",
                 "Fast, thumping, or irregular heartbeat",
                 "Sweating or hot flushes",
                 "Having panic attacks"],
                self.anxiety_vars) if var.get()]
            if selected_anxiety_symptoms:
                result_text.insert(tk.END, "\nAnxiety Symptoms:\n")
                for symptom in selected_anxiety_symptoms:
                    result_text.insert(tk.END, f"{symptom}\n")

        if self.depression_vars:
            selected_depression_symptoms = [symptom for symptom, var in zip(
                ["Clinical depression",
                 "Bipolar disorder",
                 "Feelings of helplessness and hopelessness",
                 "Loss of interest in daily activities",
                 "Appetite or weight changes",
                 "Anger or irritability",
                 "Loss of energy",
                 "Self-isolating",
                 "Self-harm",
                 "Reckless behavior"],
                self.depression_vars) if var.get()]
            if selected_depression_symptoms:
                result_text.insert(tk.END, "\nDepression Symptoms:\n")
                for symptom in selected_depression_symptoms:
                    result_text.insert(tk.END, f"{symptom}\n")

        if self.fomo_vars:
            selected_fomo_symptoms = [symptom for symptom, var in zip(
                ["Feeling negative/excluded when missing out",
                 "Low life satisfaction",
                 "High social media activity",
                 "Fast-paced lifestyle",
                 "Concerned about other people’s opinions",
                 "The urge to be surrounded by others",
                 "Poor health behaviours",
                 "Distracted Driving"],
                self.fomo_vars) if var.get()]
            if selected_fomo_symptoms:
                result_text.insert(tk.END, "\nFear of Missing Out (FOMO) Symptoms:\n")
                for symptom in selected_fomo_symptoms:
                    result_text.insert(tk.END, f"{symptom}\n")

         # Insert data into the database and pass result_window as an argument
        self.insert_into_database(result_window)

        # Feedback Button
        feedback_button = tk.Button(result_window, text="Provide Feedback", command=self.open_feedback_form, font=("Arial", 20))
        feedback_button.pack(side="bottom",pady=10)
    def open_feedback_form(self):
        feedback_window = tk.Toplevel(self.master)
        feedback_window.title("Feedback Form")

        tk.Label(feedback_window, text="Please provide your feedback, report issues, or suggest improvements:", font=("Arial", 20)).pack(pady=10)

        feedback_text = tk.Text(feedback_window, height=10, width=50)
        feedback_text.pack(pady=10)

        submit_feedback_button = tk.Button(feedback_window, text="Submit Feedback", command=lambda: self.submit_feedback(feedback_text.get("1.0", "end-1c")), font=("Arial", 12))
        submit_feedback_button.pack(pady=10)

    def submit_feedback(self, feedback):
        # gotta addd the functionality to store feedback in the database or self email
##        print("Feedback submitted:", feedback)
        tk.messagebox.showinfo("Feedback submitted", "Feedback report has been submitted successfully!")

    def insert_into_database(self, result_window):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO diagnosis_results 
                          (name, age, contact, email, gender, history, therapy, biological_factors, disease_history, none_selected,
                           anxiety_symptoms, depression_symptoms, fomo_symptoms)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (self.name, self.age, self.contact, self.email, self.gender, self.history, self.therapy,
                        self.biological_factors, self.disease_history, self.none_selected,
                        ', '.join(symptom for symptom, var in zip(
                            ["Churning feeling in your stomach",
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
                             "Having panic attacks"],
                            self.anxiety_vars) if var.get()),
                        ', '.join(symptom for symptom, var in zip(
                            ["Clinical depression",
                             "Bipolar disorder",
                             "Feelings of helplessness and hopelessness",
                             "Loss of interest in daily activities",
                             "Appetite or weight changes",
                             "Anger or irritability",
                             "Loss of energy",
                             "Self-isolating",
                             "Self-harm",
                             "Reckless behavior"],
                            self.depression_vars) if var.get()),
                        ', '.join(symptom for symptom, var in zip(
                            ["Feeling negative/excluded when missing out",
                             "Low life satisfaction",
                             "High social media activity",
                             "Fast-paced lifestyle",
                             "Concerned about other people’s opinions",
                             "The urge to be surrounded by others"
                             "Poor health behaviours",
                             "Distracted Driving"],
                            self.fomo_vars) if var.get())))
        self.conn.commit()
         #Button to download PDF report
        download_button = tk.Button(result_window, text="Download PDF Report", command=self.download_pdf_report,font=("Arial", 20))
        download_button.pack(pady=20)

    def download_pdf_report(self):
        # Generate PDF report
        self.generate_pdf_report()
        # Provide a message to the user
        tk.messagebox.showinfo("Download Complete", "PDF report has been submited successfully!")







    def generate_pdf_report(self, filename=None):

        # Determine the filename
        if filename is None:
            filename = f"{self.name}_diagnosis_report.pdf"

        # Create a PDF document
        c = canvas.Canvas(filename, pagesize=A4)
        page_width, page_height = A4
        margin = 100  # Adjust margin as needed
        max_height = page_height - margin - 50  # Leave 50 units of space at the top

        # Add background image
        c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)

        # Set up styles
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.blue)
        normal_font_size = 12
        line_spacing = 15

        # Write header
        header_text = "Diagnosis Report"
        c.setFont("Helvetica-Bold", 20)
        # Calculate the x-coordinate of the text to center it horizontally on the page
        x_coordinate = (page_width - c.stringWidth(header_text)) / 2

        # Adjust the y-coordinate to leave some space from the top margin
        y_coordinate = page_height - margin - 20  # Adjust 20 for additional space

        # Draw the text
        c.drawString(x_coordinate, y_coordinate, header_text)

        # Write user information to the PDF
        c.setFont("Helvetica", normal_font_size)
        c.setFillColor(colors.black)

        info_data = [
            (f"Name: {self.name}", -120),
            (f"Age: {self.age}", -140),
            (f"Contact Number: {self.contact}", -160),
            (f"Email ID: {self.email}", -180),
            (f"Gender: {self.gender}", -200),
        ]

        for data, y_offset in info_data:
            if page_height - margin + y_offset < margin:
                c.showPage()  # Add new page if text exceeds page height
                c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)  # Use the same background image
                c.setFont("Helvetica", normal_font_size)
            c.drawString(margin, page_height - margin + y_offset, data)

        # Write psychiatric history
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.blue)
        c.drawString(margin, page_height - 300, "Psychiatric History:")

        psychiatric_history_data = [
            (f"Past Psychiatric History: {self.history}", -320),
            (f"Have taken therapy before: {self.therapy}", -340),
            (f"Biological Factors: {self.biological_factors}", -360),
            (f"Disease History: {self.disease_history}", -380),
            (f"None selected: {self.none_selected}", -400),
        ]

        for data, y_offset in psychiatric_history_data:
            if page_height - 300 + y_offset < margin:
                c.showPage()  # Add new page if text exceeds page height
                c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)  # Use the same background image
                c.setFont("Helvetica", normal_font_size)
            c.drawString(margin, page_height - 300 + y_offset, data)

        # Write symptoms checklist
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.blue)

        # Adjust the vertical position to leave some space
        c.drawString(margin, page_height - 620, "Symptoms Checklist:")

        # Write anxiety symptoms
        if self.anxiety_vars:
            selected_anxiety_symptoms = [symptom for symptom, var in zip(
                ["Churning feeling in your stomach",
                 "Feeling light-headed or dizzy",
                 "Pins and needles",
                 "Feeling restless or unable to sit still",
                 "Faster breathing",
                 "Fast, thumping, or irregular heartbeat",
                 "Sweating or hot flushes",
                 "Having panic attacks"],
                self.anxiety_vars) if var.get()]

            for idx, symptom in enumerate(selected_anxiety_symptoms):
                if page_height - 640 - (idx + 1) * line_spacing < margin:
                    c.showPage()  # Add new page if text exceeds page height
                    c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)  # Use the same background image
                    c.setFont("Helvetica", normal_font_size)
                c.drawString(margin, page_height - 640 - (idx + 1) * line_spacing, symptom)

        # Add depression symptoms
        if self.depression_vars:
            selected_depression_symptoms = [symptom for symptom, var in zip(
                ["Clinical depression",
                 "Bipolar disorder",
                 "Feelings of helplessness and hopelessness",
                 "Loss of interest in daily activities",
                 "Appetite or weight changes",
                 "Anger or irritability",
                 "Loss of energy",
                 "Self-isolating",
                 "Self-harm",
                 "Reckless behavior"],
                self.depression_vars) if var.get()]

            for idx, symptom in enumerate(selected_depression_symptoms):
                if page_height - 640 - (len(selected_anxiety_symptoms) + idx + 2) * line_spacing < margin:
                    c.showPage()  # Add new page if text exceeds page height
                    c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)  # Use the
                            # same background image
                    c.setFont("Helvetica", normal_font_size)
                c.drawString(margin, page_height - 640 - (len(selected_anxiety_symptoms) + idx + 2) * line_spacing, symptom)

        # Add FOMO symptoms
        if self.fomo_vars:
            selected_fomo_symptoms = [symptom for symptom, var in zip(
                ["Feeling negative/excluded when missing out",
                 "Low life satisfaction",
                 "High social media activity",
                 "Fast-paced lifestyle",
                 "Concerned about other people’s opinions",
                 "The urge to be surrounded by others",
                 "Poor health behaviours",
                 "Distracted Driving"],
                self.fomo_vars) if var.get()]

            for idx, symptom in enumerate(selected_fomo_symptoms):
                if page_height - 640 - (len(selected_anxiety_symptoms) + len(selected_depression_symptoms) + idx + 3) * line_spacing < margin:
                    c.showPage()  # Add new page if text exceeds page height
                    c.drawImage("D:/pdf img 1.png", 0, 0, width=page_width, height=page_height)  # Use the same background image
                    c.setFont("Helvetica", normal_font_size)

                    c.drawString(margin, page_height - 640 - (len(selected_anxiety_symptoms) + len(selected_depression_symptoms) + idx + 3) * line_spacing, symptom)

        # Save the PDF document
        c.showPage()  # Add a final page for the letterhead
        c.drawImage("D:/Green Modern Minimalist Letterhead.png", 0, 0, width=page_width, height=page_height)

        # Save the PDF document
        c.save()

        # Get the current working directory
    current_directory = os.getcwd()

    # Print the current working directory
    print("Current Working Directory:", current_directory)

# Create the main application window
root = tk.Tk()
app = MentalHealthDiagnosisApp(root)

# Run the application
root.mainloop()

