import tkinter as tk
from tkinter import filedialog as fd, scrolledtext, INSERT, YES, BOTH
from App.Summarize import Semantic_Extractor
from App.parse_pdf import Doc


def main():
    def read_pdf():
        filename = fd.askopenfilename()
        doc = Doc(filename)
        doc.parse_nodes()
        entry.delete(1.0, tk.END)
        entry.insert(1.0, open(doc.output).read())

    def summarize_text():
        txt.delete(1.0, tk.END)
        sample = entry.get(1.0, tk.END)
        if sample.strip():
            doc = Semantic_Extractor(sample)
            doc.layer_two()
            for sent in doc.summary():
                txt.insert(INSERT, sent)

    window = tk.Tk()
    window.title('Text Summarization ;) ')
    window.geometry('1210x720')

    input_frame = tk.Frame(window)
    input_frame.pack(expand=YES, fill=BOTH, side=tk.LEFT, padx=5, pady=4)

    buttons = tk.Frame(input_frame)
    buttons.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=4)

    output_frame = tk.Frame(window)
    output_frame.pack(expand=YES, fill=BOTH, side=tk.RIGHT, padx=5, pady=4)

    stats = tk.Frame(output_frame)
    stats.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=4)

    Scrollbar = tk.Scrollbar(input_frame)
    entry = tk.Text(input_frame)
    Scrollbar.config(command=entry.yview())
    entry.config(yscrollcommand=Scrollbar.set)
    Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entry.pack(expand=YES, fill=tk.BOTH)

    txt = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
    txt.pack(expand=YES, fill=tk.BOTH, side=tk.TOP, padx=5, pady=4)

    button1 = tk.Button(buttons, text='Read Pdf', height=2, command=read_pdf)
    button1.pack(expand=YES, fill=tk.X, side=tk.LEFT, padx=3)
    button2 = tk.Button(buttons, text='Summarize', height=2, command=summarize_text)
    button2.pack(expand=YES, fill=tk.X, side=tk.RIGHT, padx=3)

    tk.mainloop()
