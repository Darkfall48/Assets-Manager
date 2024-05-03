import os
import tkinter as tk
from PIL import Image, ImageTk

class GameAssetsManager:
    def __init__(self, assets_directory):
        self.assets_directory = assets_directory
        self.assets = self.load_assets()
        self.root = tk.Tk()
        self.create_widgets()

    def load_assets(self):
        assets = {}
        for root, dirs, files in os.walk(self.assets_directory):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp3', '.wav', '.txt', '.pdf')):
                    file_path = os.path.join(root, file)
                    assets[file] = file_path
        return assets

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        for asset in self.assets.keys():
            self.listbox.insert(tk.END, asset)

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def on_select(self, event):
        index = self.listbox.curselection()[0]
        asset_name = self.listbox.get(index)
        image_path = self.assets[asset_name]

        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image = Image.open(image_path)
            image = image.resize((500, 500), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo

    def run(self):
        self.root.mainloop()

# Usage
manager = GameAssetsManager('./Assets')
manager.run()
