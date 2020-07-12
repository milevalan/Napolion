import tkinter as tk
from tkinter import filedialog as fd, scrolledtext, INSERT, YES, BOTH


# def summarize_file():
#     name = fd.askopenfilename()
#     filename = name.split('/')[-1].split('.')[-2]
#     print('Path : {path} \nFilename : {file}'.format(path=name, file=filename))
#
from App.Summarize import Semantic_Extractor


def main():
    def summarize_text():
        txt.delete(1.0, tk.END)
        sample = entry.get(1.0, tk.END)
        doc = Semantic_Extractor(sample)
        doc.layer_two()
        for sent in doc.summary():
            txt.insert(INSERT, sent)

    window = tk.Tk()
    window.title('Text Summarization ;) ')
    window.geometry('1210x720')

    frame = tk.Frame(window)
    frame.pack(expand=YES, fill=BOTH, side=tk.LEFT, padx=5, pady=4)

    Scrollbar = tk.Scrollbar(frame)
    entry = tk.Text(frame)
    Scrollbar.config(command=entry.yview())
    entry.config(yscrollcommand=Scrollbar.set)
    Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entry.pack(expand=YES, fill=tk.BOTH)

    txt = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    txt.pack(expand=YES, fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=4)

    button = tk.Button(frame, text='Click to Summarize', height=2, command=summarize_text)
    button.pack(side=tk.BOTTOM, fill=tk.X, pady=3)

    tk.mainloop()


main()
