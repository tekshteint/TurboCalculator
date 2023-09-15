import matplotlib.pyplot as plt
import numpy as np

def graphing(HP, afr, bsfc):
    # Create an array of airflow values based on horsepower
    # You can adjust the range of horsepower as needed
    horsepower_values = np.linspace(0, HP, 100)

    # Calculate airflow for each horsepower value using the formula
    airflow = (horsepower_values * afr * bsfc / 60)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(airflow, horsepower_values, label=f'Horsepower vs. Airflow\nNote this assumes Pressure Ratio remains constant', color='blue')
    plt.xlabel('Airflow')
    plt.ylabel('Horsepower')
    plt.title('Airflow vs. Horsepower')
    plt.grid(True)
    plt.legend()
    plt.show()
