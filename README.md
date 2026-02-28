# CBT Thought Diary

A desktop application that guides users through Cognitive Behavioral Therapy (CBT) journaling using a structured 5-step wizard. Built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-GPLv3-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## About

CBT Thought Diary helps you practice identifying and challenging negative thought patterns using evidence-based CBT techniques. The app walks you through a guided process to record your mood, document triggering situations, identify cognitive distortions, and reframe your thinking.

**Note:** This is an educational tool and is not a substitute for professional therapy.

## Features

- **Guided 5-step wizard** — structured flow with progress tracking and validation
- **Mood tracking** — 5-point scale with emoji indicators; compare mood before and after
- **15 cognitive distortions** — clickable checklist with descriptions for each thinking pattern
- **Thought reframing** — space to challenge negative thoughts with evidence and develop balanced perspectives
- **Persistent diary** — entries saved locally as JSON; browse, view details, or delete past entries
- **Fully offline** — no internet connection or account required; all data stays on your machine

## Screenshots

### Home Screen
The welcome screen introduces CBT concepts and provides quick access to create a new entry or browse your diary.

### Wizard Flow
Each step guides you through the CBT process:
1. **Check-In** — record your current mood
2. **The Situation** — describe the triggering event and automatic thought
3. **Analysis** — identify which cognitive distortions are present
4. **Reframe** — challenge the thought with evidence and write a balanced perspective
5. **Final Check-In** — record your mood after working through the exercise

### Diary View
Browse all saved entries with timestamps, mood transitions, and distortion tags.

## Installation

### Requirements

- Python 3.7 or higher
- No external dependencies — uses only the Python standard library (Tkinter, json, datetime)

> **Tkinter note:** Tkinter is included with most Python installations. If it's missing on Linux, install it with your package manager (e.g. `sudo apt install python3-tk` on Debian/Ubuntu).

### Setup

```bash
# Clone the repository
git clone https://github.com/hamishdean/CBT_diary.git
cd CBT_diary

# Run the application
python cbt_diary.py
```

On first launch, the app creates a `cbt_diary_data.json` file in the project directory to store your entries.

## Usage

1. **Start a new entry** — click "New Entry" from the home screen or navigation bar
2. **Follow the wizard** — use the Back/Next buttons to move through each step
3. **Save your entry** — completing the final step saves the entry automatically
4. **Review past entries** — click "Diary" to browse your history and view full details

## Cognitive Distortions

The app includes 15 common cognitive distortions based on CBT theory:

| Distortion | Description |
|---|---|
| All-or-Nothing Thinking | Seeing things in black and white with no middle ground |
| Overgeneralization | Drawing broad conclusions from a single event |
| Mental Filter | Focusing only on the negative while ignoring the positive |
| Disqualifying the Positive | Dismissing positive experiences as not counting |
| Mind Reading | Assuming you know what others are thinking |
| Fortune Telling | Predicting things will turn out badly |
| Catastrophizing | Blowing things out of proportion |
| Emotional Reasoning | Assuming feelings reflect reality |
| Should Statements | Using "should" or "must" to set rigid expectations |
| Labeling | Attaching a fixed label to yourself or others |
| Personalization | Blaming yourself for things outside your control |
| Control Fallacies | Feeling externally controlled or overly responsible |
| Fallacy of Fairness | Expecting life to always be fair |
| Fallacy of Change | Expecting others to change to suit your needs |
| Always Being Right | Needing to prove your opinions are correct |

## Data Storage

Entries are stored locally in `cbt_diary_data.json` in the project directory. Each entry includes:

- Timestamp
- Initial and final mood (value, label, emoji, color)
- Automatic thought
- Identified cognitive distortions
- Evidence challenging the thought
- Reframed balanced perspective

No data is sent to any server. You can back up or move your data by copying the JSON file.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
