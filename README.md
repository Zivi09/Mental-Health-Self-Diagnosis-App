# 🧠 Mental Health Self-Diagnosis Tool (MHSDT)

Welcome to the **Mental Health Self-Diagnosis Tool (MHSDT)**, a dual-version Python desktop application designed to promote self-awareness, highlight mental fitness, and provide accessible coping strategies for anxiety, depression, and FOMO (Fear of Missing Out).

---

## 📖 The Story Behind the Project

### 🏆 Version 1: The Root of the Journey (2nd Place Winner!)
`Mhsd v1.py` was created when I was first learning Python. Using a classic Tkinter interface with multi-window pop-ups, it was built around a custom logic-based rule engine. By checking symptom frequencies using strings and conditional `if-else` flows, it parsed and diagnosed user inputs. 
> [!NOTE]
> This project won **2nd Place** in a Python GUI project competition! It holds a special place in my development journey as the first step towards building software that makes a difference.

### 🎨 Version 2: The Modernized SaaS Dashboard (Vibe Coded!)
`Mhsd v2.py` was created to relive the excitement of that winning moment and elevate it. The goal was to keep the core underlying spirit and string checks from V1 while bringing the user experience into the modern era. 
* **The UI was fully "vibe coded"** using **CustomTkinter** to look and feel like a modern, premium SaaS dashboard with seamless sidebar navigation.
* Integrated a real-time **Google Gemini AI Chatbot** as a wellness companion.
* Added a dynamic **Generative AI Report Analysis** that automatically writes tailored coping mechanisms into a downloadable PDF report.

---

## 📸 Screenshots & Visuals

Here is a preview of the modernized Version 2 UI:

| 🏠 Home Dashboard & Profile Setup | 📋 Interactive Symptoms Checklist |
|:---:|:---:|
| ![Home Screen](mental_health.2.png) | ![Checklist Screen](mental_health.3.png) |

| 💬 Mental Fitness AI Chatbot | ℹ️ Calming About & Disclaimer |
|:---:|:---:|
| ![Chatbot Screen](mental_health.1.png) | ![About Screen](Green%20Modern%20Minimalist%20Letterhead.png) |

---

## ⚡ Feature Comparison: V1 vs. V2

| Feature / Metric | 🏆 Version 1 (Classic) | 🚀 Version 2 (Modernized) |
| :--- | :--- | :--- |
| **UI Library** | Standard `tkinter` | Modern `customtkinter` (SaaS Dashboard) |
| **Window Layout** | Multiple popups / separate prompt boxes | Single-Window layout with sidebar navigation |
| **Visual Aesthetics** | Classic OS system gray, plain text | Calming pastel light/dark mode color palettes |
| **Theme Customization** | None | Live theme toggle (Light / Dark / System) |
| **Self-Diagnosis UI** | Multi-choice prompt boxes | 3-column scrollable checklist with database logs |
| **AI Integration** | None | Gemini 2.5 Flash chatbot + dynamic diagnosis generator |
| **PDF Reporting** | Static text summary | Empathetic AI-analyzed PDF diagnosis report |
| **Access Control** | Open access | Locked diagnostic section until profile registration |

---

## 🛠️ Technical Stack & Dependencies

The project uses the following technologies:
* **Core**: Python 3.10+
* **GUI Framework**: CustomTkinter (SaaS styling, HSL pastel styling, dynamic themes)
* **Database**: SQLite3 (`mental_health.db`)
* **AI Model**: Google Gemini 2.5 Flash (`google-genai` SDK)
* **PDF Engine**: ReportLab (structured styling and wraps long AI text blocks)

---

## ⚙️ Setup & Installation

Follow these steps to run the application locally on your PC (perfect for offline study, college lab computers, or office workstations):

### 1. Clone the Project
Open your terminal and navigate to the project directory:
```powershell
cd Mental-Health-Self-Diagnosis-Tool-in-GUI
```

### 2. Set Up a Virtual Environment (Recommended)
Create and activate a virtual environment to keep dependencies isolated:
```powershell
# Create the environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all package requirements in one go:
```powershell
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key
1. Get a free API key from Google AI Studio.
2. Launch the app, click **Settings** on the left sidebar, paste your API key, and hit **Save API Key**.
3. *Alternatively*, create a `.env` file in the root folder with:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### 5. Launch the Application
Run the modernized Version 2 dashboard app:
```powershell
python "Mhsd v2.py"
```

To run the classic, award-winning Version 1 app:
```powershell
python "Mhsd v1.py"
```

---

## ⚠️ Disclaimer

*This tool is for educational and self-awareness purposes only. The assessments and AI suggestions do not constitute medical advice or a certified psychiatric diagnosis. For professional consultation, please speak with a licensed health professional.*
