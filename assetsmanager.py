import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame.mixer  # for audio preview
from pyglet import font  # for font preview

class AssetManager:
    def __init__(self, root):
        self.root = root
        self.root.title('Game Asset Manager')
        self.root.geometry('800x600')

        # Create a search bar
        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.root, textvariable=self.search_var)
        self.search_bar.pack()

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Define asset categories
        self.asset_categories = {
            '2D Assets': ['.png', '.jpg', '.jpeg', '.gif'],
            'Audio': ['.wav', '.mp3', '.ogg'],
            'Fonts': ['.ttf', '.otf'],
            # Add more categories as needed...
        }

        # Create tabs
        self.preview_label = {}
        for category in self.asset_categories:
            self.create_tab(category)

        # Bind the search bar to the search function
        self.search_var.trace('w', lambda name, index, mode: self.search_files())

    def create_tab(self, name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)

        # Create a Treeview in the tab for displaying files
        treeview = ttk.Treeview(frame)
        treeview.pack(fill='both', expand=1)

        # Add columns to the Treeview
        treeview['columns'] = ('Name', 'Tags')
        treeview.column('#0', width=0, stretch='no')
        treeview.column('Name', anchor='w', width=120)
        treeview.column('Tags', anchor='w', width=120)

        # Add headings to the Treeview
        treeview.heading('#0', text='', anchor='w')
        treeview.heading('Name', text='Name', anchor='w')
        treeview.heading('Tags', text='Tags', anchor='w')

        # Bind the selection event to update the preview pane
        treeview.bind('<<TreeviewSelect>>', lambda event: self.update_preview(treeview, name))

        # Create a label to serve as the preview pane
        self.preview_label[name] = tk.Label(frame, text='Preview Pane', bg='white')
        self.preview_label[name].pack(side='bottom', fill='both', expand=True)

        # Populate the Treeview with files
        self.populate_treeview(treeview, name)

    def populate_treeview(self, treeview, category):
        # Get the directory for the assets
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Assets')

        # Check if the directory exists
        if not os.path.exists(directory):
            print(f'The directory {directory} does not exist.')
            return

        # List all files in the directory and its subdirectories
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))

        # Sort the files
        sorted_files = sorted(all_files, key=lambda x: x.lower())

        for filepath in sorted_files:
            filename = os.path.basename(filepath)
            # Check if the file belongs to the current category
            if any(filename.endswith(ext) for ext in self.asset_categories[category]):
                # Add the file to the Treeview with only the file name
                treeview.insert('', 'end', text='', values=(filename, ''), tags=(filepath,))

    def update_preview(self, treeview, name):
        # Get the selected item
        selected_item = treeview.selection()[0]
        if selected_item:  # Check if an item is actually selected
            file_path = treeview.item(selected_item, 'tags')[0]  # Get the full file path from the tags
            
            # Determine the file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Clear the current preview
            for widget in self.preview_label[name].winfo_children():
                widget.destroy()
            
            # Display the appropriate preview based on the file type
            if file_ext in ['.png', '.jpg', '.jpeg', '.gif']:
                try:
                    # Open the image and resize it to the size of the preview pane while maintaining aspect ratio
                    image = Image.open(file_path)
                    width, height = image.size
                    aspect_ratio = width / height
                    new_width = self.preview_label[name].winfo_width()
                    new_height = int(new_width / aspect_ratio)
                    if new_height > self.preview_label[name].winfo_height():
                        new_height = self.preview_label[name].winfo_height()
                        new_width = int(new_height * aspect_ratio)
                    image = image.resize((new_width, new_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Create a label to display the image
                    image_label = tk.Label(self.preview_label[name], image=photo)
                    image_label.image = photo  # Keep a reference to avoid garbage collection
                    image_label.pack()
                except Exception as e:
                    print(f"Unable to open image: {e}")
            elif file_ext in ['.wav', '.mp3', '.ogg']:
                # Implement audio preview logic here
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                # Create a frame for the audio controls
                control_frame = tk.Frame(self.preview_label[name])
                control_frame.pack(side='bottom', fill='x')
                
                # Create the play button
                play_button = tk.Button(control_frame, text='Play', command=pygame.mixer.music.play)
                play_button.pack(side='left')
                
                # Create the pause button
                pause_button = tk.Button(control_frame, text='Pause', command=pygame.mixer.music.pause)
                pause_button.pack(side='left')
            elif file_ext in ['.ttf', '.otf']:
                # Implement font preview logic here
                font.add_file(file_path)
                sample_text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n1234567890\n!@#$%^&*()'
                label = tk.Label(self.preview_label[name], text=sample_text, font=(os.path.splitext(os.path.basename(file_path))[0], 16))
                label.pack()
            # Add more conditions for other file types as needed

    def search_files(self):
        # Get the search query
        query = self.search_var.get().lower()

        # Search for the file in all tabs
        for tab_id in self.notebook.tabs():
            tab = self.root.nametowidget(tab_id)
            treeview = tab.winfo_children()[0]
            for item in treeview.get_children():
                filename = treeview.item(item, 'values')[0]
                if query in filename.lower():
                    # Select the file and open it in the preview pane
                    treeview.selection_set(item)
                    self.update_preview(treeview, self.notebook.tab(tab_id, 'text'))
                    # Switch to the tab where the file is found
                    self.notebook.select(tab_id)
                    return

if __name__ == '__main__':
    root = tk.Tk()
    app = AssetManager(root)
    root.mainloop()