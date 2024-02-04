import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from PIL import Image, ImageTk
import random

class TableGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Table Pairings")

        self.label = tk.Label(self.master, text="Drag and drop a text file here")
        self.label.pack(pady=20)

        self.img_tk = None

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def create_random_pairs(self, names):
        random.shuffle(names)
        pairs = [(names[i], names[i + 1]) for i in range(0, len(names), 2)]
        return pairs

    # def create_table(self, names):
    #     pairs = self.create_random_pairs(names)
    #     table_data = {'Names': [], 'Table Number': []}

    #     for table_num, pair in enumerate(pairs, start=1):
    #         formatted_pair = ', '.join(pair)
    #         table_data['Names'].append(formatted_pair)
    #         table_data['Table Number'].append(table_num)

    #     df = pd.DataFrame(table_data)
    #     return df

    def create_table(self, names):
        pairs = self.create_random_pairs(names)
        table_data = {'Name 1': [], 'Name 2': [], 'Table Number': []}
        #print("Pairs: ",pairs)
        for table_num, pair in enumerate(pairs, start=1):
            #formatted_pair = ', '.join(pair)
            table_data['Name 1'].append(pair[0])
            table_data['Name 2'].append(pair[1])

            table_data['Table Number'].append(table_num)

            df = pd.DataFrame(table_data)
        return df

    def generate_table_image(self, file_path):

        with open(file_path, 'r') as file:
            names = [line.strip() for line in file]

        table = self.create_table(names)

        plt.axis('off')
        plt.table(cellText=table.values, colLabels=table.columns, cellLoc='center', loc='center', colColours=['#f0f0f0', '#f0f0f0', '#f0f0f0'])

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        img = Image.open(img_buffer)
        self.img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(self.master, image=self.img_tk)
        label.image = self.img_tk
        label.pack()

        # Close the matplotlib figure!!!!!
        plt.close()

    def drop(self, event):
        file_path = event.data
        self.generate_table_image(file_path)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = TableGeneratorApp(root)
    root.mainloop()
