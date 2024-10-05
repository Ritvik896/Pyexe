import tkinter as tk
from tkinter import filedialog, ttk

def browse_files():
    # Determine file types based on user selection
    file_types = file_type_var.get()
    
    if file_types == "All Files":
        file_types = [("All Files", "*.*")]
    elif file_types == "PDF Files":
        file_types = [("PDF Files", "*.pdf")]
    elif file_types == "Word Files":
        file_types = [("Word Files", "*.docx")]
    elif file_types == "Excel Files":
        file_types = [("Excel Files", "*.xlsx")]
    elif file_types == "Executable Files":
        file_types = [("Executable Files", "*.exe")]
    elif file_types == "JSON Files":
        file_types = [("JSON Files", "*.json")]
    elif file_types == "Rego Files":
        file_types = [("Rego Files", "*.rego")]
    else:
        file_types = [("All Files", "*.*")]

    # Open the file dialog to browse for files of the selected type
    filename = filedialog.askopenfilename(title="Select a File", filetypes=file_types)
    
    # Display the selected file in the label
    if filename:
        file_label.config(text=f"Selected: {filename}", fg="black")
    else:
        file_label.config(text="No file selected", fg="red")

def open_application():
    # Create the main window
    root = tk.Tk()
    root.title("OPA Application")

    # Set the window size
    root.geometry("400x300")

    # Welcome message
    welcome_label = tk.Label(root, text="Welcome to OPA Application", font=("Arial", 14))
    welcome_label.pack(pady=10)

    # Dropdown menu to select file type
    global file_type_var
    file_type_var = tk.StringVar(value="All Files")
    file_types = ["All Files", "PDF Files", "Word Files", "Excel Files", "Executable Files", "JSON Files", "Rego Files"]
    file_type_label = tk.Label(root, text="Select file type to view:", font=("Arial", 10))
    file_type_label.pack(pady=5)
    file_type_dropdown = ttk.Combobox(root, textvariable=file_type_var, values=file_types, state="readonly")
    file_type_dropdown.pack(pady=5)

    # Browse button styled as a standard button
    browse_button = tk.Button(root, text="Browse", command=browse_files, font=("Arial", 10), relief="raised", bd=2)
    browse_button.pack(pady=5)

    # Label to display the selected file
    global file_label
    file_label = tk.Label(root, text="No file selected", font=("Arial", 10))
    file_label.pack(pady=10)

    # Submit button styled as a standard button
    submit_button = tk.Button(root, text="Submit", font=("Arial", 10), relief="raised", bd=2)
    submit_button.pack(pady=20)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    open_application()
