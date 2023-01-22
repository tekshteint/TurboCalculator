import os as installer
try:
    import tkinter as tk
    from time import sleep
    import graphing
    from PIL import ImageTk, Image
except ImportError:
    installer.system("pip install tkinter --user")
    installer.system("pip install time --user")
    installer.system("pip install PIL --user")
    print("All packages successfully installed.")
    import tkinter as tk
    from time import sleep
    import graphing
    from PIL import ImageTk, Image

class Calculator(tk.Tk):
    def __init__(self, pr= 0.0, units= "", airflow= 0.0, hp= 0.0, boost = 0.0):
        """
        conversions
        trim =((inducer/exducer) ** 2) * 100
            inducer is outside of blade

        1CMS = 2120 CFM
        1CFM = 14.27 LB/MIN
        1CFM = 0.34 KG/S
        ~ 1 LB/min = 9.5HP

        Pressure Ratio = (ATM pressure 14.7psi + Boost pressure) / ATM 14.7

        Engine CFM:
            (Engine size * VE * max RPM * PR) / 5660
            can estimate VE as 90 normally
        """
        super().__init__()
        self.title("Turbo Calculator")
        self.minsize(400,400)
        tk.Label(self,text="A tool for helping determine proper turbo sizing",fg = "blue", font=15).grid(row = 0, column= 0, pady= 20, columnspan=4)

        tk.Button(self,text="Set Airflow",command= lambda:self.setAirflow()).grid(row=2,column=0)
        tk.Button(self,text="Convert Airflow Units",command= lambda:self.airflowConversion()).grid(row=3,column=0)
        tk.Button(self,text="Set Pressure Ratio",command= lambda:self.prCalc()).grid(row=4,column=0)
        tk.Button(self,text="Engine Horsepower Calculations",command= lambda:self.engineCFM_calc()).grid(row=5,column=0)

        self.pr, self.units, self.airflow, self.hp, self.boost= pr, units, airflow, hp, boost
        self.homeLabel = tk.Label(self, text=f"Pressure Ratio: {self.pr}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.boost} psi",fg = "blue")
        self.homeLabel.grid()


    def confirmAirflowConversion(self):
        units = self.unit_rb_choice.get()
        match units:
            case "CF/M":
                self.airflow = self.airflow * 14.27
                self.units = "CF/M"
            case "Kg/Min":
                self.airflow = self.airflow / 2.205
                self.units = "Kg/Min"
            case "Kg/Sec":
                self.airflow = self.airflow / 132.3
                self.units = "Kg/Sec"

        self.newWindow.destroy()
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.boost} psi")
        self.deiconify()
        
    def confirmPR(self, textBox):
        '''Note that atmosphereic pressure is assumed to be 14.7'''
        choice = self.PR_rb_choice.get()
        userInput = float(textBox.get("1.0", "end-1c"))
        match choice:
            case "Boost":
                self.pr = (14.7 + userInput) / 14.7
                self.boost = userInput
            case "PR":
                self.boost = userInput * 14.7 - 14.7
                self.pr = userInput

        self.newWindow.destroy()
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.boost} psi")
        self.deiconify()
        
    def confirmAirflow(self, textBox):
        self.units = "Llbs/min"
        self.airflow = float(textBox.get("1.0", "end-1c")) / 9.5
        self.newWindow.destroy()
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.boost} psi")
        self.deiconify()

    def confirmHP(self, sizeBox, rpmBox):
        size = float(sizeBox.get("1.0", "end-1c"))
        rpm = float(rpmBox.get("1.0", "end-1c"))
        self.rpms = []
        curr = 0
        """while curr <= rpm:
            self.rpms.append(round((((size * 90 * curr * self.pr) / 5660) / 14.27) * 9.5, 2))
            curr += 100"""
        cfm = (size * 90 * rpm * self.pr) / 5660 #CFM = (Engine size (lt) * VE * MAX RPM * PRESSURE RATIO )/5660
        self.airflow = cfm / 14.27
        self.hp = round(self.airflow * 9.5, 2)
        self.units = "Llbs/Min"
        self.newWindow.destroy()
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.boost} psi")
        #tk.Button(self,text="Estimated Dyno Chart",command= lambda:graphing.generateGraph(self.rpms)).grid() eventually will estiamte Horsepower graph

        self.deiconify()


    def setAirflow(self):
        self.withdraw()
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(400,400)
        self.newWindow.title("Set Airflow")
        
        tk.Label(self.newWindow,text="Input Target Crank Horsepower",fg="black",font=8).grid(row=0,column=0)
        airflow_textBox = tk.Text(self.newWindow, width= 35, height= 10)
        airflow_textBox.grid(padx= 65)
        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmAirflow(airflow_textBox)).grid()

    def airflowConversion(self):
        self.withdraw()
        units = ["CF/M", "Kg/Min", "Kg/Sec"]
        self.unit_rb_choice=tk.StringVar(self)
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(400,400)
        self.newWindow.title("Airflow Unit Conversion")
        
        tk.Label(self.newWindow,text="Select Units",fg="black",font=8).grid(row=0,column=0)
        for unit in units:
            self.unit_rb_choice.set("unit")
            txt=(f"{unit}")
            radio=tk.Radiobutton(self.newWindow,text=txt,variable=self.unit_rb_choice,value=unit).grid()
        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmAirflowConversion()).grid()
        tk.Label(self.newWindow,text="Note: Convert once and if needed again go back to the set Airflow page",fg="black",font=("Arial",10)).grid()

    def prCalc(self):
        self.withdraw()
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(400,400)
        self.PR_rb_choice=tk.StringVar(self)
        self.newWindow.title("Pressure Ratio")
        options = ["Boost","Pressure Ratio"]
        for opt in options:
            self.PR_rb_choice.set("PR")
            txt=(f"{opt}")
            radio=tk.Radiobutton(self.newWindow,text=txt,variable=self.PR_rb_choice,value=opt).grid()
        tk.Label(self.newWindow, text= "Input Target Boost or Pressure Ratio",fg="black",font=8).grid()
        PR_textBox = tk.Text(self.newWindow, width= 35, height= 10)
        PR_textBox.grid(padx= 65)
        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmPR(PR_textBox)).grid()

    def engineCFM_calc(self):
        self.withdraw()
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(400,400)
        self.newWindow.title("Engine Parameters")
        
        tk.Label(self.newWindow,text="Engine Size in Liters)",fg="black",font=8).grid()
        size_textBox = tk.Text(self.newWindow, width= 15, height= 5)
        size_textBox.grid(padx= 65)

        tk.Label(self.newWindow,text="Maximum Engine RPM)",fg="black",font=8).grid()
        rpm_textBox = tk.Text(self.newWindow, width= 15, height= 5)
        rpm_textBox.grid(padx= 65)

        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmHP(size_textBox, rpm_textBox)).grid()

    def exit(self):
        raise SystemExit(0)

if __name__ == "__main__":
    main = Calculator()
    main.protocol('WM_DELETE_WINDOW',main.exit)
    
    main.mainloop()