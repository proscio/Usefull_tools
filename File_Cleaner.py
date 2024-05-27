import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

class GUI():
    def __init__(self, main):
        self.main = main
        self.main.title("File Cleaner")
        self.main.geometry("1200x800")
        self.__file_extensions_present = []
        self.__file_extensions_to_be_removed = []        
        self.__var_dict = {}
        self.__files_to_be_removed = []
        self.__files_in_folder = []
        self.__type_search = None 

        self.__button_static_button_frame = tk.Frame(self.main)
        self.__button_static_button_frame.pack(side="bottom", pady=5)
        
        self.__quit_button = tk.Button(self.__button_static_button_frame, text="Quit", command=self.main.destroy)
        self.__quit_button.pack(side="right", padx=10)

        self.__search_directory_button = tk.Button(self.__button_static_button_frame, text="Search Directory", command=self.get_directory) 
        self.__search_directory_button.pack(side="left", padx=10)

        self.__remove_file_process_button = tk.Button(self.__button_static_button_frame, text="Remove Selected Files", command=self.remove_selected_files)
        self.__remove_file_process_button.pack(side='bottom', padx=10)

        self.__dialog_frame = tk.Frame(self.main)
        self.__dialog_frame.pack(side="bottom", padx=10, expand=True, fill="both")
        self.__dialog_window_label = tk.Label(self.__dialog_frame, text = "Dialog Window")
        self.__dialog_window_label.pack(side = "left")

        self.__dialog_window = scrolledtext.ScrolledText(self.__dialog_frame, width=100, wrap=tk.WORD, font=("Arial",8)) 
        self.__dialog_window.pack(side="left", padx=5, pady=5)

        self.__file_display_frame = tk.Frame(self.main)
        self.__file_display_frame.pack(side="top", padx=10, expand=True, fill="both")
        self.__file_display_frame.pack(side="left")
        self.__file_display_window_label = tk.Label(self.__file_display_frame, text = "Files In Folder ")
        self.__file_display_window_label.pack(side = "left")


        self.__file_display_window = scrolledtext.ScrolledText(self.__file_display_frame, width=100, wrap=tk.WORD, font=("Arial",8)) 
        self.__file_display_window.pack(side="left", padx=5, pady=5)

        self.__file_selector_window = tk.Frame(self.main)
        self.__file_selector_window.pack(side="right", padx=10)
        self.__file_selector_window.pack(side="bottom")

        self.__options_frame = tk.Frame(self.main, border=10, borderwidth=10)
        self.__options_frame.pack(side="top", padx=10)
        self.__options_frame.pack(side="right", padx=10)

        self.options()

    def get_directory(self):
        self.__file_directory = filedialog.askdirectory(title="Search Directory?", initialdir=os.getcwd())
        self.get_file_types(self.__file_directory)

    def get_file_types(self, file_directory):
        self.__file_extensions_present = set()  
        for root, dirs, files in os.walk(file_directory):
            for file in files:
                if "." in file:
                    ext = file.split(".")[-1]
                    self.__file_extensions_present.add(ext) 
        self.find_and_display_files_to_be_removed()

    def load_checkbuttons(self):
        for widget in self.__file_selector_window.winfo_children():
            widget.destroy()
        
        self.__var_dict.clear() 
        self.__file_extensions_to_be_removed = []  
        
        for ext in self.__file_extensions_present:
            var = tk.BooleanVar()
            self.__var_dict[ext] = var 
            extension_button = tk.Checkbutton(self.__file_selector_window, text=ext, variable=var,command=lambda e=ext: self.toggle_extension(e))
            extension_button.pack(side = "top")
        self.find_and_display_files_to_be_removed()

    def toggle_extension(self, ext):
        var = self.__var_dict[ext]
        if var.get():
            if ext not in self.__file_extensions_to_be_removed:
                self.__file_extensions_to_be_removed.append(ext)
        else:
            if ext in self.__file_extensions_to_be_removed:
                self.__file_extensions_to_be_removed.remove(ext)

    def update_dialog_window(self):
        extensions_str = ", ".join(self.__file_extensions_to_be_removed)
        self.__dialog_window.delete("1.0", "end")
        self.__dialog_window.insert(index="end", chars="\nFiles to be removed: " + extensions_str)

        self.__dialog_window.delete("3.0", "end")
        files_str = "\n".join(self.__files_to_be_removed)
        self.__dialog_window.insert("end", "\n\nFiles being removed:\n" + files_str)
        self.update_file_display_window()


    def find_and_display_files_to_be_removed(self):
        self.__files_to_be_removed = []
        self.__files_in_folder = []

        for root, dirs, files in os.walk(self.__file_directory):
            for file in files:
                self.__files_in_folder.append(os.path.join(root, file))
        
        files_to_check = self.__files_in_folder[:]

        if self.__type_search.get():
            temp_files_to_be_removed = []
            files_to_keep = []
            for file in files_to_check:
                matched = False
                for ext in self.__file_extensions_to_be_removed:
                    if file.endswith(ext):
                        temp_files_to_be_removed.append(file)
                        matched = True
                        break  
                if not matched:
                    files_to_keep.append(file)
            files_to_check = temp_files_to_be_removed
            self.__files_to_be_removed = temp_files_to_be_removed
        if self.__contains.get():
            temp_files_to_be_removed = []
            files_to_keep = []
            for file in files_to_check:
                if self.__contains_value.get() in file:
                    temp_files_to_be_removed.append(file)
                else:
                    files_to_keep.append(file)
            files_to_check = temp_files_to_be_removed
            self.__files_to_be_removed = temp_files_to_be_removed   

        if self.__starts_with.get():
            temp_files_to_be_removed = []
            files_to_keep = []
            for file in files_to_check:
                temp_file = file.rsplit(self.__delimeter_value.get(), 1)
                if temp_file[1].startswith(self.__starts_with_value.get()):
                    temp_files_to_be_removed.append(file)
                else:
                    files_to_keep.append(file)
            files_to_check = temp_files_to_be_removed
            self.__files_to_be_removed = temp_files_to_be_removed

        if self.__ends_with.get():
            temp_files_to_be_removed = []
            files_to_keep = []
            for file in files_to_check:
                temp_file = file.rsplit(".", 1)
                if temp_file[0].endswith(self.__ends_with_value.get()):
                    temp_files_to_be_removed.append(file)
                else:
                    files_to_keep.append(file)
            files_to_check = temp_files_to_be_removed
            self.__files_to_be_removed = temp_files_to_be_removed
            
        self.__files_to_be_removed = list(set(self.__files_to_be_removed))
        self.__files_to_be_removed.sort()

        self.update_dialog_window()

    def update_file_display_window(self):
        self.__file_display_window.delete("1.0", "end")
        file_str = "\n".join(self.__files_in_folder)
        self.__file_display_window.insert("end", file_str)


    def options(self):
        self.__starts_with = tk.BooleanVar() 
        self.__ends_with = tk.BooleanVar()
        self.__contains = tk.BooleanVar()
        self.__type_search = tk.BooleanVar()

        self.__type_search_selection = tk.Checkbutton(self.__options_frame, text="Enable Type_search", variable=self.__type_search, command=self.load_checkbuttons)
        self.__type_search_selection.pack(side="top")

        self.__starts_with_frame = tk.Frame(self.__options_frame)
        self.__starts_with_frame.pack(side="top")
        
        self.__ends_with_frame = tk.Frame(self.__options_frame)
        self.__ends_with_frame.pack(side="top")

        self.__contains_frame = tk.Frame(self.__options_frame)
        self.__contains_frame.pack(side="top")

        self.__starts_with_selection = tk.Checkbutton(self.__starts_with_frame, text="Enable Starts_with", variable=self.__starts_with, command=self.enable_starts_with)
        self.__starts_with_selection.pack(side="left")

        self.__ends_with_selection = tk.Checkbutton(self.__ends_with_frame, text="Enable Ends_with", variable=self.__ends_with, command=self.enable_ends_with)
        self.__ends_with_selection.pack(side="left")

        self.__contains_selection = tk.Checkbutton(self.__contains_frame, text="Enable Contains", variable=self.__contains, command=self.enable_contains)
        self.__contains_selection.pack(side="left")

        self.__search_buttom = tk.Button(self.__options_frame, text = "Search", command = self.find_and_display_files_to_be_removed, width = 20)
        self.__search_buttom.pack(side = "top")

    def enable_starts_with(self):
        if self.__starts_with.get():
            self.__starts_with_value = tk.Entry(self.__starts_with_frame)
            self.__starts_with_value.pack(side="left", padx=5)
            self.__starts_with_delimeter_frame = tk.Frame(self.__starts_with_frame)
            self.__starts_with_delimeter_frame.pack(side = "bottom")

            self.__delimeter_value = tk.StringVar()
            R1 = tk.Radiobutton(self.__starts_with_delimeter_frame, text = "\"\\\"", variable = self.__delimeter_value, value = "\\")
            R1.pack(side = "left")
            R2 = tk.Radiobutton(self.__starts_with_delimeter_frame, text = "\"/\"", variable = self.__delimeter_value, value = "/")
            R2.pack(side = "left")
 
        else:
            self.__starts_with_value.destroy()
            self.__starts_with_delimeter_frame.destroy()

    def enable_ends_with(self):
        if self.__ends_with.get():
            self.__ends_with_value = tk.Entry(self.__ends_with_frame)
            self.__ends_with_value.pack(side="left", padx=5)
        else:
            self.__ends_with_value.destroy()

    def enable_contains(self):
        if self.__contains.get():
            self.__contains_value = tk.Entry(self.__contains_frame)
            self.__contains_value.pack(side="left", padx=5)
        else:
            self.__contains_value.destroy()

    def remove_selected_files(self):
        messagebox_string = ""
        self.__last_chance = messagebox.askokcancel(title= "Are you sure?", message = f"Are you sure you want to permenantly delete {len(self.__files_to_be_removed)} files?")
        if self.__last_chance:
            for i in self.__files_to_be_removed:
                messagebox_string += f"\n {i}" 
            self.__review = messagebox.askokcancel(title= "Review Files: ", message=f"Files to be deleted: {messagebox_string}")
            if self.__review:
                for file in self.__files_to_be_removed:
                    os.remove(file)
                self.__files_to_be_removed = []
                self.find_and_display_files_to_be_removed()

def main():
    root = tk.Tk()
    main = GUI(root)
    root.mainloop()

main()
