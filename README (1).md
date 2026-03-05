# CBT Thought Diary 🧠

A lightweight, modern desktop application built with Python and Tkinter to help users recognize and reframe negative thought patterns using Cognitive Behavioral Therapy (CBT) techniques. 

## 📖 Overview

The CBT Thought Diary guides users through a structured 5-step process to analyze troubling situations, identify automatic negative thoughts, recognize cognitive distortions, and establish a more balanced perspective. All data is stored locally, ensuring complete privacy.

## ✨ Features

* **Guided Entry Wizard:** A step-by-step interface for logging thoughts:
  1. **Check-in:** Record initial mood using a 5-point emoji scale.
  2. **The Situation:** Document the negative thought and surrounding circumstances.
  3. **Analysis:** Select from 15 common cognitive distortions (e.g., All-or-Nothing Thinking, Catastrophizing).
  4. **Reframe:** Challenge the thought with evidence and write a balanced perspective.
  5. **Final Check-in:** Record mood after the reframing exercise.
* **Diary History:** A scrollable dashboard to review past entries, sortable by timestamp.
* **Detailed View:** Deep dive into individual entries to review the specific distortions identified and the reframing logic applied.
* **Local Storage:** Entries are securely saved to a local `cbt_diary_data.json` file.
* **Modern UI:** Custom Tkinter styling with a clean, responsive, and accessible color palette.

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Library)
* **Data Storage:** JSON

## 🚀 Getting Started

### Prerequisites

This application uses only Python's standard libraries. You do not need to install any external dependencies via `pip`. Ensure you have **Python 3.6 or higher** installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://gitlab.com/yourusername/cbt-diary.git](https://gitlab.com/yourusername/cbt-diary.git)
   cd cbt-diary

```

2. Run the application:
```bash
python cbt_diary.py

```


*(Note: Depending on your OS, you may need to use `python3` instead of `python`)*

## 📂 Project Structure

```text
├── cbt_diary.py           # Main application script containing the GUI and logic
├── cbt_diary_data.json    # Local database (generated automatically on first save)
└── README.md              # Project documentation

```

## ⚠️ Disclaimer

**This tool is for educational and self-help purposes only.** It is not a substitute for professional medical advice, diagnosis, or therapy. If you are experiencing a mental health crisis, please reach out to a qualified healthcare provider or emergency services in your area.

## 📄 License

[GNU General Public License v3 (GPLv3)]

```

Would you like me to write up a short project description that you can use on your portfolio website to accompany this repository?

```