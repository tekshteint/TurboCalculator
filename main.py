import os as installer
try:
    import tkinter as tk
    from time import sleep
    import graph
except ImportError:
    installer.system("pip install tkinter --user")
    installer.system("pip install time --user")
    installer.system("pip install PIL --user")
    print("All packages successfully installed.")
    import tkinter as tk
    from time import sleep

class Calculator(tk.Tk):
    def __init__(self, pr= 0.0, units= "", airflow= 0.0, hp= 0.0, MAP = 0.0):
        """
        conversions
        trim =((inducer/exducer) ** 2) * 100
            inducer is outside of blade

        1CMS = 2120 CFM
        1CFM = 14.27 LB/Min
        1CFM = 0.34 KG/S
        ~ 1 LB/Min = 9.5HP
        
        
        lbs/min = cfm * 0.075
        lbs/min = kg/min / 0.0283168
        lbs/min = kg/sec * 60 / 0.0283168

        cfm = lbs/min / 0.075
        kg/min = lbs/min * 0.0283168
        kg/sec = lbs/min / 60 * 0.0283168

        Pressure Ratio = (ATM pressure 14.7psi + Boost pressure) / ATM 14.7

        Engine CFM:
            (Engine size * VE * max RPM * PR) / 5660
            can estimate VE as 90 normally
        """
        super().__init__()
        self.title("Turbo Calculator")
        self.minsize(400,400)
        tk.Label(self,text="A tool for helping determine proper turbo sizing",fg = "blue", font=15).grid(row = 0, column= 0, pady= 20, columnspan=4)

        tk.Button(self,text="Calculate Airflow",command= lambda:self.setAirflow()).grid(row=2,column=0)
        tk.Button(self,text="Calculate Required Manifold Pressure",command= lambda:self.setMAP()).grid(row=3,column=0)
        tk.Button(self,text="Convert Airflow Units",command= lambda:self.airflowConversion()).grid(row=4,column=0)
        tk.Button(self,text="Graph Airflow vs Targeted HP",command= lambda:self.createGraph()).grid(row=5,column=0)

        self.pr, self.units, self.airflow, self.hp, self.MAP= pr, units, airflow, hp, MAP
        self.size, self.rpm = 0.0, 0
        self.bsfc = [0.46, 0.60]
        self.afr = [11.5, 8.5]
        self.homeLabel = tk.Label(self, text=f"Pressure Ratio: {self.pr}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.MAP} psi",fg = "blue")
        self.homeLabel.grid()
        
        
    def setAirflow(self):
        self.withdraw()
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(200,300)
        self.newWindow.title("Set Airflow")
        
        tk.Label(self.newWindow,text="Input Target Crank Horsepower",fg="black",font=8).grid(row=0,column=0)
        airflow_textBox = tk.Text(self.newWindow, width= 15, height= 5)
        airflow_textBox.grid(padx= 65)
        options = ["Pump Gas","E85"]
        self.Airflow_rb_choice=tk.StringVar(self)
        
        tk.Label(self.newWindow, text= "Select Fuel Type",fg="black",font=8).grid()
        for opt in options:
            self.Airflow_rb_choice.set("Airflow")
            txt=(f"{opt}")
            radio=tk.Radiobutton(self.newWindow,text=txt,variable=self.Airflow_rb_choice,value=opt).grid()
        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmAirflow(airflow_textBox)).grid()
        
    def setMAP(self):        
        self.withdraw()
        self.newWindow = tk.Toplevel(self)
        self.newWindow.minsize(200,300)
        self.newWindow.title("Engine Parameters")
        
        tk.Label(self.newWindow,text="Engine Size in Liters)",fg="black",font=8).grid()
        size_textBox = tk.Text(self.newWindow, width= 15, height= 5)
        size_textBox.grid(padx= 65)

        tk.Label(self.newWindow,text="Peak Power RPM)",fg="black",font=8).grid()
        rpm_textBox = tk.Text(self.newWindow, width= 15, height= 5)
        rpm_textBox.grid(padx= 65)

        tk.Button(self.newWindow, text="Confirm",command=lambda : self.confirmMAP(size_textBox, rpm_textBox)).grid()
        
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
        
    def confirmAirflowConversion(self):
        units = self.unit_rb_choice.get()
        match units:
            case "CF/M":
                self.airflow = self.airflow / 0.075
                self.units = "CF/M"
            case "Kg/Min":
                self.airflow = self.airflow * 2.2046244201838
                self.units = "Kg/Min"
            case "Kg/Sec":
                self.airflow = self.airflow * 0.00755987283350059
                self.units = "Kg/Sec"

        self.newWindow.destroy()
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.MAP} psi")
        self.deiconify()
        
        
    def confirmAirflow(self, airflow_textbox):
        """Formula: Air Flow (Lbs/Min) = HP target * AFR * BSFC/60
        """
        
        self.fuelChoice = self.Airflow_rb_choice.get()
        self.targetHP = float(airflow_textbox.get("1.0", "end-1c"))
        
        
        if self.fuelChoice == "Pump Gas": 
            self.airflow = float(airflow_textbox.get("1.0", "end-1c")) * self.afr[0] * self.bsfc[0] / 60
            self.units = "Lbs/Min"
        elif self.fuelChoice == "E85":
            self.airflow = float(airflow_textbox.get("1.0", "end-1c")) * self.afr[1] * self.bsfc[1] / 60
            self.units = "Lbs/Min"
            
        self.hp = float(airflow_textbox.get("1.0", "end-1c")) * 0.88 #Assuming 12% drivetrain loss
            
        self.newWindow.destroy() 
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.MAP} psi")
        self.deiconify()
        
    def confirmMAP(self, sizeBox, rpmBox):
        """Assuming VE is 90
        Formula: MAP = (Airflow (Lbs/Min) * Gas Constant * (460 + Intake Manifold Temperature (Assume 100 deg F)))/(VE * RPM/2 * Displacement in CI)
        """
        R = 639.6
        IMT = 100
        displacementConversionFactor = 61.02
        self.size = float(sizeBox.get("1.0", "end-1c"))
        self.rpm = float(rpmBox.get("1.0", "end-1c"))
            
        if self.units != "Lbs/Min":
            match self.units:
                case "CF/M":
                    self.airflow = self.airflow / 0.075
                case "Kg/Min":
                    self.airflow = self.airflow * 0.0283168
                case "Kg/Sec":
                    self.airflow = self.airflow * 0.0283168 / 60
        #This will give us boost pressure required in PSI
        self.MAP = round((self.airflow * R * (460 + IMT)) / (0.90 * (self.rpm / 2) * (self.size * displacementConversionFactor)) - 12.7, 2)
        self.units = "Lbs/Min"            
        
        #Calculating PR
        self.pr = (self.MAP + 12.7) / 13.7
        self.newWindow.destroy() 
        self.homeLabel.configure(text=f"Pressure Ratio: {round(self.pr,2)}, Airflow: {round(self.airflow, 2)} {self.units}, Estimated Horsepower: {self.hp} @ {self.MAP} psi")
        self.deiconify()
        
    def createGraph(self):
        match self.fuelChoice:
            case "Pump Gas": 
                graph.graphing(self.targetHP, self.afr[0], self.bsfc[0])
            case "E85":
                graph.graphing(self.targetHP, self.afr[1], self.bsfc[1])
        
    def exit(self):
        raise SystemExit(0)

if __name__ == "__main__":
    main = Calculator()
    main.protocol('WM_DELETE_WINDOW',main.exit)
    
    main.mainloop()