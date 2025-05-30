import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk
import json
import os

# Define color palette
BG_COLOR = "#F4F6F8"  # Light Greyish Blue
FRAME_COLOR = "#EAECEE"  # Lighter Grey
BUTTON_COLOR = "#A9CCE3"  # Soft Blue
BUTTON_ACTIVE_COLOR = "#85C1E9"  # Brighter Blue
LISTBOX_BG = "#FFFFFF"  # White
LISTBOX_FG = "#2C3E50"  # Dark Slate Blue
COMPLETED_FG = "#95A5A6"  # Greyish Silver (for completed tasks)
INPUT_BG = "#FFFFFF"
INPUT_FG = "#1C2833"  # Very Dark Blue
ACCENT_COLOR = "#3498DB"  # Bright Blue (for titles, selection)
PRIORITY_HIGH_COLOR = "#E74C3C"  # Red
PRIORITY_MEDIUM_COLOR = "#F39C12"  # Orange
PRIORITY_LOW_COLOR = "#2ECC71"  # Green

# Define font styles
DEFAULT_FONT_FAMILY = "Segoe UI"  # A more modern font, falls back to Arial
DEFAULT_FONT_SIZE = 11
LISTBOX_FONT_SIZE = 12
TITLE_FONT_SIZE = 16

# Data file
DATA_FILE = "todo_tasks.json"

# Unicode characters for checkboxes and icons
CHECK_UNCHECKED = "[ ]"
CHECK_CHECKED = "[✓]"
ICON_ADD = "➕"
ICON_EDIT = "✎"
ICON_REMOVE = "🗑️"
ICON_PRIORITY = "⭐"  # Alternative: 🚩
ICON_CLEAR_COMPLETED = "🧹"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To - Do List")
        self.root.geometry("650x750")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(550, 600)

        # --- Custom Fonts ---
        try:
            self.default_font = font.Font(family=DEFAULT_FONT_FAMILY, size=DEFAULT_FONT_SIZE)
            self.listbox_font = font.Font(family=DEFAULT_FONT_FAMILY, size=LISTBOX_FONT_SIZE)
            self.completed_font = font.Font(family=DEFAULT_FONT_FAMILY, size=LISTBOX_FONT_SIZE, overstrike=True)
            self.title_font = font.Font(family=DEFAULT_FONT_FAMILY, size=TITLE_FONT_SIZE, weight="bold")
        except tk.TclError:  # Fallback if Segoe UI is not available
            self.default_font = font.Font(family="Arial", size=DEFAULT_FONT_SIZE)
            self.listbox_font = font.Font(family="Arial", size=LISTBOX_FONT_SIZE)
            self.completed_font = font.Font(family="Arial", size=LISTBOX_FONT_SIZE, overstrike=True)
            self.title_font = font.Font(family="Arial", size=TITLE_FONT_SIZE, weight="bold")

        self.tasks = []  # List of dicts: {"text": str, "completed": bool, "priority": str}

        self.setup_ui()
        self.load_tasks()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_priority_display(self, priority_level):
        """Returns a display string and color for priority."""
        if priority_level == "High":
            return "(H)", PRIORITY_HIGH_COLOR
        elif priority_level == "Medium":
            return "(M)", PRIORITY_MEDIUM_COLOR
        elif priority_level == "Low":
            return "(L)", PRIORITY_LOW_COLOR
        return "", LISTBOX_FG  # Default

    def setup_ui(self):
        # --- Title ---
        title_label = tk.Label(
            self.root,
            text="To - Do List",
            font=self.title_font,
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            pady=20
        )
        title_label.pack(fill=tk.X)

        # --- Input Frame ---
        input_frame = tk.Frame(self.root, bg=BG_COLOR, pady=10)
        input_frame.pack(fill=tk.X, padx=25)

        self.task_entry = tk.Entry(
            input_frame,
            font=self.default_font,
            bd=2,
            relief=tk.FLAT,
            bg=INPUT_BG,
            fg=INPUT_FG,
            insertbackground=INPUT_FG
        )
        self.task_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        add_button = tk.Button(
            input_frame,
            text=f"{ICON_ADD} Add",
            command=self.add_task,
            font=self.default_font,
            bg=BUTTON_COLOR,
            fg=INPUT_FG,
            activebackground=BUTTON_ACTIVE_COLOR,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6
        )
        add_button.pack(side=tk.RIGHT)

        # --- Listbox Frame ---
        listbox_outer_frame = tk.Frame(
            self.root,
            bg=ACCENT_COLOR,
            bd=1,
            relief=tk.SOLID,
            padx=1,
            pady=1
        )
        listbox_outer_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=(5, 10))

        listbox_frame = tk.Frame(listbox_outer_frame, bg=BG_COLOR)
        listbox_frame.pack(expand=True, fill=tk.BOTH)

        self.task_listbox = tk.Listbox(
            listbox_frame,
            font=self.listbox_font,
            selectbackground=ACCENT_COLOR,
            selectforeground=LISTBOX_BG,
            bg=LISTBOX_BG,
            fg=LISTBOX_FG,
            bd=0,
            highlightthickness=0,
            activestyle="none",
            height=15
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.task_listbox.bind("<ButtonRelease-1>", self.toggle_task_complete_click)

        scrollbar = ttk.Scrollbar(
            listbox_frame,
            orient=tk.VERTICAL,
            command=self.task_listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0, 5))
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # --- Button Frame ---
        controls_frame = tk.Frame(self.root, bg=BG_COLOR, pady=15)
        controls_frame.pack(fill=tk.X, padx=25)

        button_style = {
            "font": self.default_font,
            "bg": BUTTON_COLOR,
            "fg": INPUT_FG,
            "activebackground": BUTTON_ACTIVE_COLOR,
            "relief": tk.FLAT,
            "bd": 0,
            "padx": 10,
            "pady": 7
        }

        edit_task_button = tk.Button(
            controls_frame, text=f"{ICON_EDIT} Edit", command=self.edit_task, **button_style
        )
        edit_task_button.pack(side=tk.LEFT, expand=True, padx=(0, 5))

        set_priority_button = tk.Button(
            controls_frame, text=f"{ICON_PRIORITY} Priority", command=self.set_task_priority, **button_style
        )
        set_priority_button.pack(side=tk.LEFT, expand=True, padx=5)

        remove_task_button = tk.Button(
            controls_frame, text=f"{ICON_REMOVE} Remove", command=self.remove_task, **button_style
        )
        remove_task_button.pack(side=tk.LEFT, expand=True, padx=5)

        remove_completed_button = tk.Button(
            controls_frame,
            text=f"{ICON_CLEAR_COMPLETED} Clear Done",
            command=self.remove_completed_tasks,
            **button_style
        )
        remove_completed_button.pack(side=tk.LEFT, expand=True, padx=(5, 0))

        # --- Status Bar ---
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.FLAT,
            anchor=tk.W,
            bg=FRAME_COLOR,
            fg=INPUT_FG,
            font=font.Font(family=DEFAULT_FONT_FAMILY, size=DEFAULT_FONT_SIZE - 1)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, ipady=3)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task_item in enumerate(self.tasks):
            checkbox = CHECK_CHECKED if task_item["completed"] else CHECK_UNCHECKED
            priority_display, _ = self.get_priority_display(task_item.get("priority", "Medium"))
            display_text = f"{checkbox} {priority_display} {task_item['text']}"
            self.task_listbox.insert(tk.END, display_text)

            # Only change the text color
            current_fg = COMPLETED_FG if task_item["completed"] else LISTBOX_FG
            self.task_listbox.itemconfig(i, foreground=current_fg)

        self.update_status_bar()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False, "priority": "Medium"})
            self.refresh_task_list()
            self.task_entry.delete(0, tk.END)
            self.status_bar.config(text=f"Task '{task_text[:30]}...' added.")
        else:
            messagebox.showwarning("Empty Task", "Task description cannot be empty.", parent=self.root)
            self.status_bar.config(text="Failed to add: Task empty.")

    def toggle_task_complete_click(self, event):
        try:
            selected_index = self.task_listbox.nearest(event.y)
            if selected_index < 0 or selected_index >= len(self.tasks):
                return
            self.task_listbox.selection_clear(0, tk.END)
            self.task_listbox.selection_set(selected_index)
            self.task_listbox.activate(selected_index)

            task_item = self.tasks[selected_index]
            task_item["completed"] = not task_item["completed"]
            self.refresh_task_list()
            status = "completed" if task_item["completed"] else "pending"
            self.status_bar.config(text=f"Task '{task_item['text'][:20]}...' marked {status}.")
        except Exception:
            self.status_bar.config(text="Could not toggle task.")

    def edit_task(self):
        try:
            idx = self.task_listbox.curselection()[0]
            task_item = self.tasks[idx]
            new_text = simpledialog.askstring(
                "Edit Task", "Enter new task description:",
                initialvalue=task_item["text"], parent=self.root
            )
            if new_text is not None:
                new_text = new_text.strip()
                if new_text:
                    task_item["text"] = new_text
                    self.refresh_task_list()
                    self.status_bar.config(text=f"Task edited to '{new_text[:30]}...'.")
                else:
                    messagebox.showwarning("Empty Task", "Description cannot be empty.", parent=self.root)
                    self.status_bar.config(text="Edit failed: Empty description.")
            else:
                self.status_bar.config(text="Edit cancelled.")
        except IndexError:
            messagebox.showwarning("No Task Selected", "Select a task to edit.", parent=self.root)
            self.status_bar.config(text="Edit failed: No selection.")

    def set_task_priority(self):
        try:
            idx = self.task_listbox.curselection()[0]
            task_item = self.tasks[idx]
            priorities = ["High", "Medium", "Low"]
            current_priority = task_item.get("priority", "Medium")

            dlg = tk.Toplevel(self.root)
            dlg.title("Set Priority")
            dlg.geometry("250x150")
            dlg.resizable(False, False)
            dlg.configure(bg=BG_COLOR)
            dlg.transient(self.root)
            dlg.grab_set()

            tk.Label(
                dlg,
                text=f"Set priority for:\n'{task_item['text'][:30]}...'",
                bg=BG_COLOR,
                fg=INPUT_FG,
                font=self.default_font
            ).pack(pady=10)

            var = tk.StringVar(value=current_priority)
            combo = ttk.Combobox(dlg, textvariable=var, values=priorities, state="readonly", font=self.default_font)
            combo.pack(pady=5)

            def on_ok():
                task_item["priority"] = var.get()
                self.refresh_task_list()
                self.status_bar.config(
                    text=f"Priority for '{task_item['text'][:20]}...' set to {var.get()}."
                )
                dlg.destroy()

            tk.Button(
                dlg, text="OK", command=on_ok,
                font=self.default_font, bg=BUTTON_COLOR, fg=INPUT_FG,
                relief=tk.FLAT, padx=10
            ).pack(pady=10)

            dlg.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dlg.winfo_width() // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dlg.winfo_height() // 2)
            dlg.geometry(f"+{x}+{y}")
        except IndexError:
            messagebox.showwarning("No Task Selected", "Select a task to change priority.", parent=self.root)
            self.status_bar.config(text="Priority change failed: No selection.")

    def remove_task(self):
        try:
            idx = self.task_listbox.curselection()[0]
            text = self.tasks[idx]["text"]
            if messagebox.askyesno("Confirm Delete", f"Remove task '{text}'?", parent=self.root):
                del self.tasks[idx]
                self.refresh_task_list()
                self.status_bar.config(text=f"Task '{text[:30]}...' removed.")
        except IndexError:
            messagebox.showwarning("No Task Selected", "Select a task to remove.", parent=self.root)
            self.status_bar.config(text="Remove failed: No selection.")

    def remove_completed_tasks(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t["completed"]]
        removed = before - len(self.tasks)
        if removed:
            self.refresh_task_list()
            messagebox.showinfo("Tasks Cleared", f"{removed} completed task(s) removed.", parent=self.root)
            self.status_bar.config(text=f"{removed} completed removed.")
        else:
            messagebox.showinfo("No Completed Tasks", "Nothing to remove.", parent=self.root)
            self.status_bar.config(text="No completed tasks to remove.")

    def update_status_bar(self):
        total = len(self.tasks)
        done = sum(t["completed"] for t in self.tasks)
        self.status_bar.config(text=f"Total: {total} | Completed: {done} | Pending: {total - done}")

    def save_tasks(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save tasks: {e}", parent=self.root)
            self.status_bar.config(text="Error saving tasks.")

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
                for t in self.tasks:
                    if "priority" not in t:
                        t["priority"] = "Medium"
                self.refresh_task_list()
                self.status_bar.config(text="Tasks loaded successfully.")
            except (IOError, json.JSONDecodeError) as e:
                messagebox.showerror("Load Error", f"Could not load tasks: {e}\nStarting fresh.", parent=self.root)
                self.tasks = []
                self.status_bar.config(text="Error loading tasks.")
        else:
            self.status_bar.config(text="Welcome! Add your first task.")

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        if os.name == "nt":
            style.theme_use("vista")
        else:
            style.theme_use("clam")
    except tk.TclError:
        pass

    app = TodoApp(root)
    root.mainloop()
