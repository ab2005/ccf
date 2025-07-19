#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import re
import json
from pathlib import Path

class ClipboardSaver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clipboard Saver")
        self.root.geometry("500x300")
        
        # Default settings
        self.default_extension = ".html"
        self.default_path = os.path.expanduser("~/Documents")
        self.last_saved_path = self.load_last_path()
        
        self.setup_ui()
        
    def load_last_path(self):
        config_file = os.path.expanduser("~/.clipboard_saver_config.json")
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('last_path', self.default_path)
        except:
            pass
        return self.default_path
    
    def save_last_path(self, path):
        config_file = os.path.expanduser("~/.clipboard_saver_config.json")
        try:
            config = {'last_path': path}
            with open(config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def get_clipboard_content(self):
        try:
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read clipboard: {str(e)}")
            return ""
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clipboard content preview
        ttk.Label(main_frame, text="Clipboard Content Preview:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.preview_text = tk.Text(main_frame, height=8, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=scrollbar.set)
        self.preview_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        
        # File settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="File Settings", padding="5")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File path
        ttk.Label(settings_frame, text="Save to:").grid(row=0, column=0, sticky=tk.W)
        self.path_var = tk.StringVar(value=self.last_saved_path)
        self.path_entry = ttk.Entry(settings_frame, textvariable=self.path_var, width=40)
        self.path_entry.grid(row=0, column=1, padx=(5, 5), sticky=(tk.W, tk.E))
        ttk.Button(settings_frame, text="Browse", command=self.browse_path).grid(row=0, column=2)
        
        # Filename
        ttk.Label(settings_frame, text="Filename:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(settings_frame, textvariable=self.filename_var, width=40)
        self.filename_entry.grid(row=1, column=1, padx=(5, 5), pady=(5, 0), sticky=(tk.W, tk.E))
        
        # Extension
        ttk.Label(settings_frame, text="Extension:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.extension_var = tk.StringVar(value=self.default_extension)
        self.extension_entry = ttk.Entry(settings_frame, textvariable=self.extension_var, width=10)
        self.extension_entry.grid(row=2, column=1, padx=(5, 5), pady=(5, 0), sticky=tk.W)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Refresh Clipboard", command=self.refresh_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Save File", command=self.save_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Save As...", command=self.save_as).pack(side=tk.LEFT)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Load clipboard content on startup
        self.refresh_clipboard()
    
    def refresh_clipboard(self):
        clipboard_content = self.get_clipboard_content()
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, clipboard_content)
        
        # Generate filename from first line
        if clipboard_content.strip():
            first_line = clipboard_content.split('\n')[0].strip()
            # Clean filename - remove invalid characters
            filename = re.sub(r'[<>:"/\\|?*]', '', first_line)
            filename = filename[:50]  # Limit length
            if filename:
                self.filename_var.set(filename)
            else:
                self.filename_var.set("clipboard_content")
        else:
            self.filename_var.set("clipboard_content")
    
    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)
    
    def save_file(self):
        try:
            content = self.preview_text.get(1.0, tk.END).rstrip()
            if not content:
                messagebox.showwarning("Warning", "No content to save!")
                return
            
            save_path = self.path_var.get()
            filename = self.filename_var.get()
            extension = self.extension_var.get()
            
            if not extension.startswith('.'):
                extension = '.' + extension
            
            full_path = os.path.join(save_path, filename + extension)
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Save the path for future use
            self.save_last_path(save_path)
            
            messagebox.showinfo("Success", f"File saved to:\n{full_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def save_as(self):
        try:
            content = self.preview_text.get(1.0, tk.END).rstrip()
            if not content:
                messagebox.showwarning("Warning", "No content to save!")
                return
            
            filename = self.filename_var.get() + self.extension_var.get()
            file_path = filedialog.asksaveasfilename(
                initialdir=self.path_var.get(),
                initialfile=filename,
                defaultextension=self.extension_var.get(),
                filetypes=[
                    ("HTML files", "*.html"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Update path and save for future use
                save_dir = os.path.dirname(file_path)
                self.path_var.set(save_dir)
                self.save_last_path(save_dir)
                
                messagebox.showinfo("Success", f"File saved to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClipboardSaver()
    app.run()