import Tkinter as tk
import tkFileDialog
import tkMessageBox
from collections import defaultdict

import subprocess
import csv
import re

class Tablets(tk.Frame):
    
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=4)
        self.controlCanvas = tk.Canvas(root,borderwidth = 0)
        self.frame = tk.Frame(self.canvas, width = 400, height = 100)
        self.controlFrame = tk.Frame(self.canvas, padx = 10, pady = 10)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.prevSel = "Bad"
        
        self.blenderLocation = tk.StringVar(root)
        self.blenderLocation.set("C://Program Files/Blender Foundation/Blender/blender.exe")
    
        self.qualVariable = tk.StringVar(root)
        self.qualVariable.set("Good")

        self.entry = tk.Entry(self.controlFrame)
        self.entry.insert(0,"errorLog.txt")
        
        #browse button        
        self.button = tk.Button(self.controlFrame, text="Browse", command=self.fileLocation, width=10)
        self.button.pack(side = "top", anchor = "sw")
        
        #instructions label
        tk.Label(self.controlFrame, text="Select alternate Blender location if necessary", borderwidth="1", 
                relief="solid").pack(side = "top", anchor = "nw")
        
        #file location output label
        tk.Label(self.controlFrame, textvariable = self.blenderLocation,borderwidth="1", relief="solid").pack(side = "top", anchor = "nw")

        #options dropdown menu
        self.options = tk.OptionMenu(self.controlFrame, self.qualVariable, "Good", "Bad", "Evaluate", "Unlabeled","Manual","All",command = self.highlight)
        self.options.pack(side = "top", anchor = "w", pady = (18,0))
        
        #instructions label
        tk.Label(self.controlFrame, text="Select which quality to output\n(click ID numbers for manual)", borderwidth="1", 
                relief="solid").pack(side = "top", anchor = "nw")

        #entry for error file output
        self.entry.pack(side = "top", anchor = "w", pady = (18,0))
        
        #instructions label
        tk.Label(self.controlFrame, text="Change error output file if necessary", borderwidth="1", 
                relief="solid").pack(side = "top", anchor = "nw")

        #export button
        self.exportButton = tk.Button(self.controlFrame, text = "Export", command = self.export)
        self.exportButton.pack(side = "top", anchor = "nw", pady = (10,0))
        
        self.vsb.pack(side = "left", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((10,10), window=self.frame, anchor="ne", 
                                  tags="self.frame")
        self.canvas.create_window((4,4), window = self.controlFrame,anchor = "nw", tags = "self.frame")
        
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        
        
        with open('O:\data\databases\excel\pylos_scan_combined_final.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            i=1
            for row in reader:
                tableInfo[i] = row
                #print(tableInfo[i]["Geras ID"])
                i+=1
        self.populate()
        self.highlight("Good")
            
    def populate(self):
        
        for row in range(len(tableInfo)):
            numberID =tableInfo[row+1]["Geras ID"]

            label = tk.Label(self.frame, text = numberID, width=6, borderwidth="1", 
                     relief="solid", bg = "gray")
            label.bind("<Button-1>",self.manualSelect)
            qualText=tableInfo[row+1]["Final Qual"]
            
            background = "gray"
            if(qualText.upper() == "GOOD"):
                background = "green"
                fileQuality["Good"].append(label)
            elif (qualText.upper() == "BAD" or qualText.upper() == "DO NOT USE"):
                background = "red"
                fileQuality["Bad"].append(label)
            elif (qualText.upper() == "EVALUATE"):
                background = "yellow"
                fileQuality["Evaluate"].append(label)
            else:
                fileQuality["Unlabeled"].append(label)
    
            tk.Label(self.frame, text=qualText, bg = background).grid(row=row, column=1)
            tk.Label(self.frame, text=tableInfo[row+1]["Notes"]).grid(row=row, column=2, sticky = "w")
            label.grid(row=row, column=0)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.frame.bbox("all"))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fileLocation(self):
        if(tkFileDialog.askopenfilename() != ""):
            self.blenderLocation.set(tkFileDialog.askopenfilename())
        
    def highlight(self,event):
        if(event == "All" and self.prevSel != "All"):
            for entry in fileQuality:
                for i in range(len(fileQuality[entry])):
                    fileQuality[entry][i].configure(bg = "green")
        elif(event != "All" and self.prevSel == "All"):
            for entry in fileQuality:
                if(entry != event):
                    for i in range(len(fileQuality[entry])):
                        fileQuality[entry][i].configure(bg = "gray")
        else:
            if(self.prevSel != event):
                for entry in range(len(fileQuality[self.prevSel])):
                    fileQuality[self.prevSel][entry].configure(bg = "gray")
                if(self.qualVariable.get() != "Manual"):
                    for entry in range(len(fileQuality[event])):
                        fileQuality[event][entry].configure(bg = "green")
        self.prevSel = event
                
        
    def manualSelect(self, event):
        self.prevSel = "Manual"
        if(self.qualVariable.get() != "Manual"):
            None
        elif(not event.widget in fileQuality["Manual"]):
            event.widget.configure(bg = "green")
            fileQuality["Manual"].append(event.widget)
        else:
            fileQuality["Manual"].remove(event.widget)
            event.widget.configure(bg = "gray")

    def export(self):
        ifExport = tkMessageBox.askquestion("Export","Are you sure you want to export [{0}]?".format(self.prevSel))
        if(ifExport == "yes"):
            #os.system('chdir {0}'.format(self.blenderLocation))
            subprocess.call(['chdir',self.blenderLocation], shell = True)
            subprocess.call('blender', shell = True)


if __name__ == "__main__":
    tableInfo = {}
    fileQuality = defaultdict(list)
    
    root=tk.Tk()
    root.title("Blender OBJ/JSON converter")
    root.resizable(width = False, height=True)
    root.geometry('830x600')
    Tablets(root).pack(side="top", fill="both", expand=False)
    root.mainloop()
