import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()
    bp = plt.boxplot(data)
    plt.show()

    q1 = [round(min(item.get_ydata()), 1) for item in bp['boxes']]
    q3 = [round(max(item.get_ydata()), 1) for item in bp['boxes']]
    print(f'Q1: {q1}\n'
          f'Q3: {q3}')