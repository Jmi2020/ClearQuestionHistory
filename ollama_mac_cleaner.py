import os
import json
import shutil
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

class OllamaMacHistoryCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama History Cleaner for macOS")
        self.root.geometry("500x400")
        self.root.minsize(400, 300)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger("OllamaMacHistoryCleaner")
        
        # Define the macOS specific path
        self.history_path = os.path.join(os.path.expanduser('~'), '.ollama')
        self.history_file = os.path.join(self.history_path, 'history')
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        # Create style
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
        
        # Configure button styles
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and description
        title_label = ttk.Label(
            main_frame, 
            text="Ollama History Cleaner for macOS", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        description = ttk.Label(
            main_frame,
            text="This tool clears Ollama history on macOS.",
            wraplength=400
        )
        description.pack(pady=(0, 20))
        
        # Paths info
        paths_frame = ttk.LabelFrame(main_frame, text="Ollama History Location")
        paths_frame.pack(fill=tk.X, pady=10)
        
        path_label = ttk.Label(
            paths_frame,
            text=f"History file: {self.history_file}",
            wraplength=400
        )
        path_label.pack(padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Backup option
        self.backup_var = tk.BooleanVar(value=True)
        backup_check = ttk.Checkbutton(
            options_frame, 
            text="Create Backup Before Cleaning", 
            variable=self.backup_var
        )
        backup_check.pack(anchor=tk.W, padx=5, pady=2)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 10))
        
        check_button = ttk.Button(
            buttons_frame, 
            text="Check History File", 
            command=self.check_history_file,
            width=15
        )
        check_button.pack(side=tk.LEFT, padx=5)
        
        self.clean_button = ttk.Button(
            buttons_frame, 
            text="Clear History", 
            command=self.clean_history,
            style="Accent.TButton",
            width=15
        )
        self.clean_button.pack(side=tk.RIGHT, padx=5)
        
        exit_button = ttk.Button(
            buttons_frame, 
            text="Exit", 
            command=self.root.destroy,
            width=10
        )
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = tk.Text(results_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.results_text, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
    
    def update_status(self, message, is_error=False):
        """Update status message"""
        self.status_var.set(message)
        self.results_text.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if is_error:
            self.results_text.insert(tk.END, f"[{timestamp}] ERROR: {message}\n")
            self.logger.error(message)
        else:
            self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.logger.info(message)
            
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.NORMAL)
    
    def check_history_file(self):
        """Check if history file exists and display info about it"""
        self.progress.start()
        self.update_status("Checking Ollama history file...")
        
        # Start check in a separate thread
        Thread(target=self._check_thread).start()
    
    def _check_thread(self):
        """Background thread for checking history file"""
        try:
            if os.path.exists(self.history_file):
                try:
                    # Check file size first
                    file_size = os.path.getsize(self.history_file)
                    if file_size == 0:
                        self.root.after(0, lambda: self.update_status(
                            "History file exists but is empty."
                        ))
                        self.root.after(0, lambda: self.progress.stop())
                        return
                    
                    with open(self.history_file, 'r') as f:
                        file_content = f.read().strip()
                        
                        # Handle empty or nearly empty file
                        if not file_content:
                            self.root.after(0, lambda: self.update_status(
                                "History file exists but is empty."
                            ))
                            return
                        
                        try:
                            data = json.loads(file_content)
                            
                            # Count items in history
                            history_count = 0
                            if isinstance(data, dict):
                                for key in data:
                                    if isinstance(data[key], list):
                                        history_count += len(data[key])
                            elif isinstance(data, list):
                                history_count = len(data)
                            
                            self.root.after(0, lambda: self.update_status(
                                f"History file found with {history_count} entries."
                            ))
                        except json.JSONDecodeError:
                            # Try line-by-line parsing (for JSON Lines format)
                            try:
                                lines = file_content.split('\n')
                                history_count = 0
                                
                                for line in lines:
                                    if line.strip():
                                        json.loads(line.strip())
                                        history_count += 1
                                
                                self.root.after(0, lambda: self.update_status(
                                    f"History file found with {history_count} entries (JSONL format)."
                                ))
                            except json.JSONDecodeError:
                                # Not JSON or JSONL
                                self.root.after(0, lambda: self.update_status(
                                    "History file exists but is not in a recognized JSON format. Will be treated as text."
                                ))
                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"Error reading history file: {str(e)}", is_error=True
                    ))
            else:
                self.root.after(0, lambda: self.update_status(
                    "History file not found at expected location."
                ))
        except Exception as e:
            self.root.after(0, lambda: self.update_status(
                f"Unexpected error: {str(e)}", is_error=True
            ))
        
        self.root.after(0, lambda: self.progress.stop())
    
    def clean_history(self):
        """Clean the Ollama history file"""
        if not messagebox.askyesno(
            "Confirm Cleanup", 
            "Are you sure you want to clear the Ollama history?\n\n"
            "This will remove all command history data."
        ):
            return
        
        self.progress.start()
        self.update_status("Cleaning Ollama history...")
        
        # Start cleanup in a separate thread
        Thread(target=self._clean_thread).start()
    
    def _clean_thread(self):
        """Background thread for cleaning history"""
        try:
            if not os.path.exists(self.history_file):
                self.root.after(0, lambda: self.update_status(
                    "History file not found, nothing to clean."
                ))
                self.root.after(0, lambda: self.progress.stop())
                return
            
            # Backup if enabled
            if self.backup_var.get():
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = f"{self.history_file}_backup_{timestamp}"
                    shutil.copy2(self.history_file, backup_file)
                    self.root.after(0, lambda: self.update_status(
                        f"Created backup: {backup_file}"
                    ))
                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"Failed to create backup: {str(e)}", is_error=True
                    ))
            
            try:
                # Read the file to preserve structure
                with open(self.history_file, 'r') as f:
                    file_content = f.read().strip()
                    
                    # Handle empty file
                    if not file_content:
                        self.root.after(0, lambda: self.update_status(
                            "History file is already empty."
                        ))
                        self.root.after(0, lambda: self.progress.stop())
                        return
                    
                    try:
                        # Try standard JSON format
                        data = json.loads(file_content)
                        
                        # Clear history but keep structure
                        if isinstance(data, dict):
                            for key in data:
                                if isinstance(data[key], list):
                                    data[key] = []
                        elif isinstance(data, list):
                            data = []
                        
                        # Write back the empty structure
                        with open(self.history_file, 'w') as f_out:
                            json.dump(data, f_out)
                        
                        self.root.after(0, lambda: self.update_status(
                            "Successfully cleared Ollama history."
                        ))
                    except json.JSONDecodeError:
                        # Try line-by-line parsing (JSONL format)
                        try:
                            lines = file_content.split('\n')
                            valid_jsonl = False
                            
                            for line in lines:
                                if line.strip():
                                    json.loads(line.strip())
                                    valid_jsonl = True
                                    break
                            
                            if valid_jsonl:
                                # It's JSONL format, empty the file but keep a placeholder
                                with open(self.history_file, 'w') as f_out:
                                    f_out.write("")
                                
                                self.root.after(0, lambda: self.update_status(
                                    "Successfully cleared Ollama history (JSONL format)."
                                ))
                            else:
                                # Not JSON or JSONL, just empty the file
                                open(self.history_file, 'w').close()
                                self.root.after(0, lambda: self.update_status(
                                    "File format not recognized. File has been emptied."
                                ))
                        except:
                            # Just empty the file as a fallback
                            open(self.history_file, 'w').close()
                            self.root.after(0, lambda: self.update_status(
                                "File format not recognized. File has been emptied."
                            ))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"Error cleaning history: {str(e)}", is_error=True
                ))
        except Exception as e:
            self.root.after(0, lambda: self.update_status(
                f"Unexpected error during cleanup: {str(e)}", is_error=True
            ))
        
        self.root.after(0, lambda: self.progress.stop())
        
        self.root.after(0, lambda: messagebox.showinfo(
            "Cleanup Complete", 
            "Ollama history has been cleared successfully."
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaMacHistoryCleaner(root)
    root.mainloop()
