# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

# --- Constants & Configuration ---

DATA_FILE = "cbt_diary_data.json"

COLORS = {
    "bg_app": "#f8fafc",        # slate-50
    "bg_card": "#ffffff",       # white
    "primary": "#4f46e5",       # indigo-600
    "primary_hover": "#4338ca", # indigo-700
    "primary_light": "#e0e7ff", # indigo-100
    "secondary": "#10b981",     # emerald-500
    "secondary_bg": "#ecfdf5",  # emerald-50
    "text_main": "#1e293b",     # slate-800
    "text_muted": "#64748b",    # slate-500
    "border": "#e2e8f0",        # slate-200
    "danger": "#ef4444",        # red-500
    "selected_bg": "#eef2ff",   # Very light indigo
    "selected_border": "#6366f1" # Indigo border
}

MOODS = [
    {"value": 1, "label": "Very Happy", "emoji": "😄", "color": "#dcfce7"},
    {"value": 2, "label": "Good", "emoji": "🙂", "color": "#ecfccb"},
    {"value": 3, "label": "Neutral", "emoji": "😐", "color": "#f3f4f6"},
    {"value": 4, "label": "Sad", "emoji": "🙁", "color": "#ffedd5"},
    {"value": 5, "label": "Very Sad", "emoji": "😩", "color": "#fee2e2"}
]

DISTORTIONS = [
    {"id": 1, "title": "All-or-Nothing Thinking", "desc": "Seeing things in black-and-white. 'If I fall short of perfect, I am a total failure.'"},
    {"id": 2, "title": "Overgeneralization", "desc": "Seeing a single negative event as a never-ending pattern of defeat. 'I always mess up.'"},
    {"id": 3, "title": "Mental Filter", "desc": "Picking out a single negative detail and dwelling on it exclusively, darkening your view of reality."},
    {"id": 4, "title": "Disqualifying the Positive", "desc": "Rejecting positive experiences by insisting they 'don't count' for some reason."},
    {"id": 5, "title": "Jumping to Conclusions (Mind Reading)", "desc": "Concluding someone is reacting negatively to you without checking (e.g., 'He thinks I'm stupid')."},
    {"id": 6, "title": "Jumping to Conclusions (Fortune Telling)", "desc": "Predicting things will turn out badly as if it were an established fact. 'I'm going to fail this exam.'"},
    {"id": 7, "title": "Magnification (Catastrophizing) or Minimization", "desc": "Blowing things out of proportion, or shrinking the importance of your good qualities."},
    {"id": 8, "title": "Emotional Reasoning", "desc": "Assuming your negative emotions reflect reality. 'I feel guilty, so I must have done something wrong.'"},
    {"id": 9, "title": "Should Statements", "desc": "Motivating yourself with 'shoulds' and 'musts'. 'I should have known better.' Leads to guilt."},
    {"id": 10, "title": "Labeling and Mislabeling", "desc": "Extreme overgeneralization. Instead of saying 'I made a mistake', you say 'I am a loser.'"},
    {"id": 11, "title": "Personalization", "desc": "Seeing yourself as the cause of a negative external event for which you were not primarily responsible."},
    {"id": 12, "title": "Control Fallacies", "desc": "Feeling externally controlled (helpless victim) or internally controlled (responsible for everyone's pain)."},
    {"id": 13, "title": "Fallacy of Fairness", "desc": "Resenting that life isn't 'fair' according to your personal standard of fairness."},
    {"id": 14, "title": "Fallacy of Change", "desc": "Expecting others to change to suit you if you just pressure them enough."},
    {"id": 15, "title": "Always Being Right", "desc": "Being wrong is unthinkable; you will go to any length to demonstrate your rightness."}
]

class CBTDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CBT Thought Diary")
        self.root.geometry("800x750")
        self.root.minsize(600, 500)
        self.root.configure(bg=COLORS["bg_app"])

        self.entries = self.load_data()
        self.current_entry_data = {}
        self.wizard_step = 1

        # State management for checkboxes in step 3
        self.distortion_ui_refs = {}

        self.setup_styles()
        self.create_header()

        self.content_frame = tk.Frame(self.root, bg=COLORS["bg_app"])
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.create_footer()
        self.render_home()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        base_font = ("Segoe UI", 10)
        bold_font = ("Segoe UI", 10, "bold")

        style.configure(".", background=COLORS["bg_app"], font=base_font, foreground=COLORS["text_main"])
        style.configure("TFrame", background=COLORS["bg_app"])
        style.configure("TLabel", background=COLORS["bg_app"], foreground=COLORS["text_main"])
        style.configure("TButton", borderwidth=0, padding=10, font=bold_font)

        style.configure("Primary.TButton", background=COLORS["primary"], foreground="white")
        style.map("Primary.TButton", background=[("active", COLORS["primary_hover"])])

        style.configure("Success.TButton", background=COLORS["secondary"], foreground="white")
        style.map("Success.TButton", background=[("active", "#059669")])

        style.configure("Nav.TButton", background=COLORS["bg_app"], foreground=COLORS["primary"])
        style.map("Nav.TButton", background=[("active", COLORS["primary_light"])])

        style.configure("Card.TFrame", background=COLORS["bg_card"], relief="flat")
        style.configure("Card.TLabel", background=COLORS["bg_card"])

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, indent=4, ensure_ascii=False)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- Structural Components ---

    def create_header(self):
        header = tk.Frame(self.root, bg=COLORS["primary"], height=60, padx=20)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=COLORS["primary"], cursor="hand2")
        title_frame.pack(side="left")

        def go_home(e=None): self.render_home()
        title_frame.bind("<Button-1>", go_home)

        icon_lbl = tk.Label(title_frame, text="🧠", font=("Segoe UI", 20), bg=COLORS["primary"], fg="white")
        icon_lbl.pack(side="left", padx=(0, 10))
        icon_lbl.bind("<Button-1>", go_home)

        text_lbl = tk.Label(title_frame, text="CBT Thought Diary", font=("Segoe UI", 14, "bold"), bg=COLORS["primary"], fg="white")
        text_lbl.pack(side="left")
        text_lbl.bind("<Button-1>", go_home)

        nav_frame = tk.Frame(header, bg=COLORS["primary"])
        nav_frame.pack(side="right")

        def create_nav_link(parent, text, command):
            lbl = tk.Label(parent, text=text, font=("Segoe UI", 10, "bold"),
                           bg=COLORS["primary"], fg="white",
                           padx=15, pady=8, cursor="hand2")
            lbl.pack(side="left", padx=2)

            def on_enter(e): lbl.config(bg=COLORS["primary_hover"])
            def on_leave(e): lbl.config(bg=COLORS["primary"])

            lbl.bind("<Enter>", on_enter)
            lbl.bind("<Leave>", on_leave)
            lbl.bind("<Button-1>", lambda e: command())
            return lbl

        create_nav_link(nav_frame, "Home", self.render_home)
        create_nav_link(nav_frame, "New Entry", self.init_wizard)
        create_nav_link(nav_frame, "Diary", self.render_history)

    def create_footer(self):
        footer = tk.Frame(self.root, bg=COLORS["bg_app"], pady=10)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="This tool is for educational purposes. It is not a substitute for professional therapy.",
                fg=COLORS["text_muted"], bg=COLORS["bg_app"], font=("Segoe UI", 8)).pack()

    # --- HOME VIEW ---

    def render_home(self):
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=COLORS["bg_app"])
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Welcome Back", font=("Segoe UI", 24, "bold"), bg=COLORS["bg_app"], fg=COLORS["text_main"]).pack(pady=(0, 10))
        tk.Label(container, text="Cognitive Behavioral Therapy (CBT) helps you recognize\nand change negative thought patterns.",
                justify="center", bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(pady=(0, 30))

        btn_frame = tk.Frame(container, bg=COLORS["bg_app"])
        btn_frame.pack()

        def big_button(parent, text, subtext, icon, color, cmd):
            frame = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=30, pady=30)
            frame.configure(highlightbackground=COLORS["border"], highlightthickness=1, relief="flat")
            frame.pack(side="left", padx=10)

            l1 = tk.Label(frame, text=icon, font=("Segoe UI", 32), bg="white")
            l1.pack(pady=(0, 15))
            l2 = tk.Label(frame, text=text, font=("Segoe UI", 12, "bold"), bg="white", fg=color)
            l2.pack()
            l3 = tk.Label(frame, text=subtext, font=("Segoe UI", 9), bg="white", fg=COLORS["text_muted"])
            l3.pack(pady=(5, 0))

            def click(e): cmd()
            for w in (frame, l1, l2, l3):
                w.bind("<Button-1>", click)
                w.configure(cursor="hand2")

        big_button(btn_frame, "New Entry", "Record a thought", "➕", COLORS["primary"], self.init_wizard)
        big_button(btn_frame, "Read Diary", f"{len(self.entries)} entries saved", "📖", COLORS["secondary"], self.render_history)

        info_frame = tk.Frame(container, bg=COLORS["bg_app"], bd=1, relief="solid",
                              highlightbackground=COLORS["border"], highlightthickness=1)
        info_frame.pack(fill="x", pady=40, ipadx=20, ipady=15)

        tk.Label(info_frame, text="ℹ️ How it works", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 5))
        steps = [
            "1. Identify a troubling situation.",
            "2. Catch the Automatic Negative Thought.",
            "3. Identify Cognitive Distortions.",
            "4. Challenge and Reframe."
        ]
        for step in steps:
            tk.Label(info_frame, text=step, bg=COLORS["bg_app"], fg=COLORS["text_muted"], anchor="w").pack(fill="x")

    # --- WIZARD VIEWS ---

    def init_wizard(self):
        self.wizard_step = 1
        self.current_entry_data = {
            "id": str(datetime.now().timestamp()),
            "timestamp": datetime.now().isoformat(),
            "distortions": []
        }
        self.render_wizard()

    def render_wizard(self):
        self.clear_content()

        center_frame = tk.Frame(self.content_frame, bg=COLORS["bg_app"])
        center_frame.pack(fill="both", expand=True, padx=50, pady=20)

        progress_frame = tk.Frame(center_frame, bg=COLORS["border"], height=8)
        progress_frame.pack(fill="x", pady=(0, 20))
        fill_frame = tk.Frame(progress_frame, bg=COLORS["primary"], width=1, height=8)
        fill_frame.place(relwidth=self.wizard_step/5, height=8)

        steps_lbl_frame = tk.Frame(center_frame, bg=COLORS["bg_app"])
        steps_lbl_frame.pack(fill="x", pady=(0, 20))

        self.wizard_content = tk.Frame(center_frame, bg=COLORS["bg_app"])
        self.wizard_content.pack(fill="both", expand=True)

        if self.wizard_step == 1: self.step_1_mood()
        elif self.wizard_step == 2: self.step_2_thought()
        elif self.wizard_step == 3: self.step_3_distortions()
        elif self.wizard_step == 4: self.step_4_reframe()
        elif self.wizard_step == 5: self.step_5_final()

        nav_btns = tk.Frame(center_frame, bg=COLORS["bg_app"], pady=20)
        nav_btns.pack(fill="x", side="bottom")

        if self.wizard_step == 1:
            ttk.Button(nav_btns, text="Cancel", style="Nav.TButton", command=self.render_home).pack(side="left")
        else:
            ttk.Button(nav_btns, text="< Back", style="Nav.TButton", command=self.prev_step).pack(side="left")

        if self.wizard_step < 5:
            ttk.Button(nav_btns, text="Next >", style="Primary.TButton", command=self.next_step).pack(side="right")
        else:
            ttk.Button(nav_btns, text="Save Entry 💾", style="Success.TButton", command=self.finish_entry).pack(side="right")

    def step_1_mood(self):
        tk.Label(self.wizard_content, text="STEP 1: CHECK-IN", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 10))
        tk.Label(self.wizard_content, text="How are you feeling right now?", font=("Segoe UI", 10), bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 20))

        for mood in MOODS:
            is_selected = self.current_entry_data.get('initialMood', {}).get('value') == mood['value']
            bg_color = mood['color'] if is_selected else "white"
            border_w = 2 if is_selected else 1

            btn_frame = tk.Frame(self.wizard_content, bg=bg_color, bd=border_w, relief="solid")
            btn_frame.pack(fill="x", pady=5)

            content = tk.Label(btn_frame, text=f"{mood['emoji']}   {mood['label']}",
                             bg=bg_color, fg=COLORS["text_main"],
                             font=("Segoe UI", 11), padx=20, pady=10, anchor="w")
            content.pack(fill="both")

            def select(e, m=mood): self.set_data_refresh('initialMood', m)
            btn_frame.bind("<Button-1>", select)
            content.bind("<Button-1>", select)

    def step_2_thought(self):
        tk.Label(self.wizard_content, text="STEP 2: THE SITUATION", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 10))

        # Explicit Header for the box
        tk.Label(self.wizard_content, text="NEGATIVE THOUGHT", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_app"], fg=COLORS["text_main"]).pack(anchor="w")
        tk.Label(self.wizard_content, text="Describe the situation and exactly what you are thinking.", font=("Segoe UI", 9), bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 5))

        self.txt_thought = scrolledtext.ScrolledText(self.wizard_content, height=10, font=("Segoe UI", 11), padx=10, pady=10, borderwidth=1, relief="solid")
        self.txt_thought.pack(fill="both", expand=True)
        if 'thought' in self.current_entry_data:
            self.txt_thought.insert("1.0", self.current_entry_data['thought'])

    def step_3_distortions(self):
        tk.Label(self.wizard_content, text="STEP 3: ANALYSIS", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 10))

        tk.Label(self.wizard_content, text="COGNITIVE DISTORTIONS", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_app"], fg=COLORS["text_main"]).pack(anchor="w")
        tk.Label(self.wizard_content, text="Click the box to select any thinking traps that apply.", font=("Segoe UI", 9), bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 10))

        # Responsive Scrollable Area
        canvas = tk.Canvas(self.wizard_content, bg=COLORS["bg_app"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.wizard_content, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_app"])

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(frame_window_id, width=event.width)

        scroll_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        frame_window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.distortion_ui_refs = {}
        current_list = self.current_entry_data.get('distortions', [])

        for dist in DISTORTIONS:
            is_selected = dist["title"] in current_list

            # Styles based on state
            bg_col = COLORS["selected_bg"] if is_selected else "white"
            fg_col = COLORS["primary"] if is_selected else COLORS["text_main"]
            border_col = COLORS["selected_border"] if is_selected else "#dddddd"
            border_width = 2 if is_selected else 1

            # The Card Frame (Clickable Box)
            card = tk.Frame(scroll_frame, bg=bg_col, pady=10, padx=10, bd=border_width, relief="solid")
            # For border color in standard Tkinter we use highlightbackground if typical,
            # but Frame 'relief' doesn't support custom colors well on all OS.
            # Workaround: Use a container frame for border or just accept standard relief.
            # We will use configure(highlightbackground=...) which works on Mac/Linux usually.
            card.configure(highlightbackground=border_col, highlightcolor=border_col, highlightthickness=border_width, relief="flat")
            card.pack(fill="x", pady=4, padx=2)

            # Title Row with Icon
            title_row = tk.Frame(card, bg=bg_col)
            # FIX: Changed mb=2 to pady=(0, 2)
            title_row.pack(fill="x", pady=(0, 2))

            check_char = "☑" if is_selected else "☐"

            title_lbl = tk.Label(title_row, text=f"{check_char}  {dist['title']}",
                               font=("Segoe UI", 10, "bold"), bg=bg_col, fg=fg_col, anchor="w")
            title_lbl.pack(fill="x")

            # Description
            desc_lbl = tk.Label(card, text=dist["desc"], bg=bg_col, fg=COLORS["text_muted"],
                              font=("Segoe UI", 9), justify="left", wraplength=450, anchor="w")
            desc_lbl.pack(fill="x", padx=(25, 0))

            # Store refs to update visual state later without re-render
            self.distortion_ui_refs[dist["title"]] = {
                "card": card, "title_lbl": title_lbl, "desc_lbl": desc_lbl
            }

            # Click Event Binding
            def toggle(e, d_title=dist["title"]):
                self.toggle_distortion(d_title)

            card.bind("<Button-1>", toggle)
            title_row.bind("<Button-1>", toggle)
            title_lbl.bind("<Button-1>", toggle)
            desc_lbl.bind("<Button-1>", toggle)

            card.config(cursor="hand2")
            title_lbl.config(cursor="hand2")
            desc_lbl.config(cursor="hand2")

    def toggle_distortion(self, title):
        current_list = self.current_entry_data.setdefault('distortions', [])

        if title in current_list:
            current_list.remove(title)
            is_selected = False
        else:
            current_list.append(title)
            is_selected = True

        # Update UI visually immediately
        refs = self.distortion_ui_refs.get(title)
        if refs:
            bg_col = COLORS["selected_bg"] if is_selected else "white"
            fg_col = COLORS["primary"] if is_selected else COLORS["text_main"]
            border_col = COLORS["selected_border"] if is_selected else "#dddddd"
            border_width = 2 if is_selected else 1
            check_char = "☑" if is_selected else "☐"

            refs["card"].configure(bg=bg_col, highlightbackground=border_col, highlightcolor=border_col, highlightthickness=border_width)
            refs["title_lbl"].configure(text=f"{check_char}  {title}", bg=bg_col, fg=fg_col)
            refs["desc_lbl"].configure(bg=bg_col)


    def step_4_reframe(self):
        tk.Label(self.wizard_content, text="STEP 4: REFRAME", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 10))

        # Box 1 Header
        tk.Label(self.wizard_content, text="THE CHALLENGE", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_app"], fg=COLORS["text_main"]).pack(anchor="w")
        tk.Label(self.wizard_content, text="What is the evidence against this thought? Is it 100% true?", font=("Segoe UI", 9), bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 5))

        self.txt_challenge = scrolledtext.ScrolledText(self.wizard_content, height=5, font=("Segoe UI", 10), borderwidth=1, relief="solid")
        self.txt_challenge.pack(fill="x", pady=(0, 15))
        if 'challenge' in self.current_entry_data: self.txt_challenge.insert("1.0", self.current_entry_data['challenge'])

        # Box 2 Header
        tk.Label(self.wizard_content, text="BALANCED PERSPECTIVE", font=("Segoe UI", 10, "bold"), bg=COLORS["bg_app"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 5))
        tk.Label(self.wizard_content, text="Write a more realistic thought based on the evidence.", font=("Segoe UI", 9), bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 5))

        self.txt_reframe = scrolledtext.ScrolledText(self.wizard_content, height=5, font=("Segoe UI", 10), borderwidth=1, relief="solid")
        self.txt_reframe.pack(fill="x")
        if 'reframe' in self.current_entry_data: self.txt_reframe.insert("1.0", self.current_entry_data['reframe'])

    def step_5_final(self):
        tk.Label(self.wizard_content, text="STEP 5: FINAL CHECK-IN", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_app"]).pack(anchor="w", pady=(0, 10))

        start_emoji = self.current_entry_data.get('initialMood', {}).get('emoji', '')
        tk.Label(self.wizard_content, text=f"You started with: {start_emoji}", bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 10))

        for mood in MOODS:
            is_selected = self.current_entry_data.get('finalMood', {}).get('value') == mood['value']
            bg_color = mood['color'] if is_selected else "white"
            border_w = 2 if is_selected else 1

            btn_frame = tk.Frame(self.wizard_content, bg=bg_color, bd=border_w, relief="solid")
            btn_frame.pack(fill="x", pady=5)

            content = tk.Label(btn_frame, text=f"{mood['emoji']}   {mood['label']}",
                             bg=bg_color, fg=COLORS["text_main"],
                             font=("Segoe UI", 11), padx=20, pady=10, anchor="w")
            content.pack(fill="both")

            def select(e, m=mood): self.set_data_refresh('finalMood', m)
            btn_frame.bind("<Button-1>", select)
            content.bind("<Button-1>", select)

    # --- Wizard Helpers ---

    def set_data_refresh(self, key, value):
        self.current_entry_data[key] = value
        self.render_wizard()

    def next_step(self):
        if self.wizard_step == 1:
            if 'initialMood' not in self.current_entry_data:
                messagebox.showwarning("Required", "Please select a mood.")
                return
        elif self.wizard_step == 2:
            txt = self.txt_thought.get("1.0", tk.END).strip()
            if not txt:
                messagebox.showwarning("Required", "Please describe your thought.")
                return
            self.current_entry_data['thought'] = txt
        elif self.wizard_step == 3:
            # Distortions are updated live in current_entry_data, so no extra collection step needed here
            pass
        elif self.wizard_step == 4:
            c = self.txt_challenge.get("1.0", tk.END).strip()
            r = self.txt_reframe.get("1.0", tk.END).strip()
            if not c or not r:
                messagebox.showwarning("Required", "Please complete both fields.")
                return
            self.current_entry_data['challenge'] = c
            self.current_entry_data['reframe'] = r

        self.wizard_step += 1
        self.render_wizard()

    def prev_step(self):
        self.wizard_step -= 1
        self.render_wizard()

    def finish_entry(self):
        if 'finalMood' not in self.current_entry_data:
            messagebox.showwarning("Required", "Please select your current mood.")
            return
        self.entries.insert(0, self.current_entry_data)
        self.save_data()
        messagebox.showinfo("Saved", "Entry saved successfully!")
        self.render_history()

    # --- HISTORY & DETAILS ---

    def render_history(self):
        self.clear_content()

        header = tk.Frame(self.content_frame, bg=COLORS["bg_app"])
        header.pack(fill="x", pady=(20, 10), padx=20)
        tk.Label(header, text="Your Diary", font=("Segoe UI", 16, "bold"), bg=COLORS["bg_app"]).pack(side="left")

        if not self.entries:
            tk.Label(self.content_frame, text="No entries yet.", bg=COLORS["bg_app"], fg=COLORS["text_muted"]).pack(pady=50)
            return

        outer_container = tk.Frame(self.content_frame, bg=COLORS["bg_app"])
        outer_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(outer_container, bg=COLORS["bg_app"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_app"])

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(frame_window_id, width=event.width)

        scroll_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        frame_window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for entry in self.entries:
            self.create_history_card(scroll_frame, entry)

    def create_history_card(self, parent, entry):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid")
        card.configure(highlightbackground=COLORS["border"], highlightthickness=1, relief="flat")
        card.pack(fill="x", pady=8, padx=2)

        def open_details(e): self.render_details(entry)

        header = tk.Frame(card, bg="white")
        header.pack(fill="x", padx=15, pady=(15, 5))

        date_str = datetime.fromisoformat(entry['timestamp']).strftime("%b %d, %Y • %I:%M %p")
        tk.Label(header, text="📅 " + date_str, bg="white", fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(side="left")

        arrow = tk.Label(card, text="➜", bg="white", fg=COLORS["border"], font=("Segoe UI", 14))
        arrow.place(relx=0.97, rely=0.5, anchor="e")

        moods = tk.Frame(card, bg="white")
        moods.pack(fill="x", padx=15, pady=5)

        m1 = entry.get('initialMood', {}).get('emoji', '❓')
        m2 = entry.get('finalMood', {}).get('emoji', '❓')

        tk.Label(moods, text=f"{m1}  ➜  {m2}", bg=COLORS["bg_app"], fg=COLORS["text_main"], padx=10, pady=5).pack(side="left")

        # UPDATED: Show distortion names instead of just count
        dists = entry.get('distortions', [])
        if dists:
            # Create a string like "Catastrophizing, Labeling..."
            dist_text = ", ".join(dists)
            if len(dist_text) > 40:
                dist_text = dist_text[:40] + "..."

            tk.Label(moods, text=dist_text, bg="#fef2f2", fg=COLORS["danger"], padx=10, pady=5, font=("Segoe UI", 9, "bold")).pack(side="left", padx=10)

        thought = entry.get('thought', '')
        if len(thought) > 100: thought = thought[:100] + "..."
        tk.Label(card, text=f'"{thought}"', bg="white", fg=COLORS["text_main"], font=("Segoe UI", 11, "italic"), anchor="w").pack(fill="x", padx=15, pady=(5, 15))

        for child in (card, *card.winfo_children(), *header.winfo_children(), *moods.winfo_children()):
            child.bind("<Button-1>", open_details)
            child.configure(cursor="hand2")

    def render_details(self, entry):
        self.clear_content()

        nav = tk.Frame(self.content_frame, bg=COLORS["bg_app"])
        nav.pack(fill="x", pady=(20, 10), padx=20)
        ttk.Button(nav, text="< Back", style="Nav.TButton", command=self.render_history).pack(side="left")

        del_btn = tk.Button(nav, text="🗑 Delete", bg=COLORS["bg_app"], fg=COLORS["danger"], bd=0,
                          font=("Segoe UI", 10, "bold"), command=lambda: self.delete_entry(entry))
        del_btn.pack(side="right")

        card = tk.Frame(self.content_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        meta = tk.Frame(card, bg=COLORS["bg_app"], padx=20, pady=15)
        meta.pack(fill="x")

        date_str = datetime.fromisoformat(entry['timestamp']).strftime("%A, %B %d, %Y at %I:%M %p")

        left_meta = tk.Frame(meta, bg=COLORS["bg_app"])
        left_meta.pack(side="left")
        tk.Label(left_meta, text="RECORDED ON", fg=COLORS["text_muted"], bg=COLORS["bg_app"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(left_meta, text=date_str, fg=COLORS["text_main"], bg=COLORS["bg_app"], font=("Segoe UI", 10, "bold")).pack(anchor="w")

        right_meta = tk.Frame(meta, bg="white", padx=10, pady=5, bd=1, relief="solid")
        right_meta.pack(side="right")
        m1 = entry.get('initialMood', {})
        m2 = entry.get('finalMood', {})
        tk.Label(right_meta, text=f"{m1.get('emoji')} Before  ➜  {m2.get('emoji')} After", bg="white", font=("Segoe UI", 10)).pack()

        outer_body = tk.Frame(card, bg="white")
        outer_body.pack(fill="both", expand=True)

        body_canvas = tk.Canvas(outer_body, bg="white", highlightthickness=0)
        body_scroll = ttk.Scrollbar(outer_body, orient="vertical", command=body_canvas.yview)
        body_frame = tk.Frame(body_canvas, bg="white", padx=30, pady=30)

        def on_body_frame_configure(event):
            body_canvas.configure(scrollregion=body_canvas.bbox("all"))
        def on_body_canvas_configure(event):
            body_canvas.itemconfig(body_window_id, width=event.width)

        body_frame.bind("<Configure>", on_body_frame_configure)
        body_canvas.bind("<Configure>", on_body_canvas_configure)

        body_window_id = body_canvas.create_window((0, 0), window=body_frame, anchor="nw")
        body_canvas.configure(yscrollcommand=body_scroll.set)

        body_canvas.pack(side="left", fill="both", expand=True)
        body_scroll.pack(side="right", fill="y")

        def section(title, text, icon, color_bg, color_fg):
            sec = tk.Frame(body_frame, bg="white")
            sec.pack(fill="x", pady=(0, 25))

            head = tk.Frame(sec, bg="white")
            head.pack(fill="x", pady=(0, 5))
            tk.Label(head, text=icon, font=("Segoe UI", 14), bg=color_bg, fg=color_fg, width=3).pack(side="left")
            tk.Label(head, text=title, font=("Segoe UI", 12, "bold"), bg="white", fg=COLORS["text_main"]).pack(side="left", padx=10)

            box = tk.Label(sec, text=text, bg=color_bg, fg=COLORS["text_main"], padx=15, pady=15, justify="left", wraplength=650, anchor="w")
            box.pack(fill="x")

        section("Negative Thought", entry.get('thought', ''), "☹️", "#fff1f2", COLORS["danger"])

        dists = entry.get('distortions', [])
        if dists:
            d_frame = tk.Frame(body_frame, bg="white")
            d_frame.pack(fill="x", pady=(0, 25))
            tk.Label(d_frame, text="IDENTIFIED DISTORTIONS", font=("Segoe UI", 8, "bold"), fg=COLORS["text_muted"], bg="white").pack(anchor="w", pady=(0, 5))

            for d in dists:
                lbl = tk.Label(d_frame, text=d, bg=COLORS["primary_light"], fg=COLORS["primary"], padx=10, pady=5, font=("Segoe UI", 9, "bold"))
                lbl.pack(side="left", padx=(0, 5))

        section("The Challenge", entry.get('challenge', ''), "ℹ️", "#eff6ff", COLORS["primary"])
        section("Balanced View", entry.get('reframe', ''), "🙂", "#ecfdf5", COLORS["secondary"])

    def delete_entry(self, entry):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this entry?"):
            self.entries.remove(entry)
            self.save_data()
            self.render_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = CBTDiaryApp(root)
    root.mainloop()