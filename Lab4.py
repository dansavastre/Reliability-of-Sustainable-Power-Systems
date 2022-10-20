from matplotlib import pyplot as plt
import COPT4gens as gens
import COPT_function as func
import pandas as pd
import numpy as np


def question_1():
    # Question 1
    print("\nQuestion 1:\n")
    print(gens.COPT())


def question_2():
    # Question 2
    print("\nQuestion 2:\n")
    cgens = [200, 100, 200, 500, 400]
    ugens = [0.05, 0.03, 0.04, 0.06, 0.05]

    # Compute the COPT table
    copt_q2 = gens.COPT2()
    print("COPT table:\n", copt_q2)
    print("Second column of COPT: ", copt_q2[:, 1])

    # Plot the second column of the result
    fig = plt.figure(figsize=(10, 5))
    xaxis = list(copt_q2[:, 0])
    yaxis = list(copt_q2[:, 1])
    plt.bar(xaxis, yaxis, color='blue', width=100)
    plt.xlabel("Capacity Outage [MW]")
    plt.ylabel("Probability")
    plt.title("Probabilities from COPT")
    # plt.show()


def question_3():
    # Question 3
    print("\nQuestion 3:\n")
    Cgens = [200, 100, 200, 500, 400]
    Ugens = [0.05, 0.03, 0.04, 0.06, 0.05]
    copt_q3 = func.COPT_function(Cgens, Ugens, 100)
    print("COPT table:\n", copt_q3)
    print("Second column of COPT: ", copt_q3[:, 1])
    # creating the bar plot
    xaxis = list(copt_q3[:, 0])
    yaxis = list(copt_q3[:, 1])

    plt.bar(xaxis, yaxis, color='blue', width=50)
    plt.xlim(0, 5000)

    plt.xlabel("Capacity Outage [MW]")
    plt.ylabel("Probability")
    plt.title("Probabilities of COPT states")
    plt.xlim(-55, 1400)
    # plt.show()


def question_4():
    # Question 4
    print("\nQuestion 4:\n")

    # Read data from file
    df = pd.read_csv('Lab files/load_Pwind.csv')
    NLh_load = df['NLh_load'].values.tolist()
    P_off_wind1 = df['P_off_wind1'].values.tolist()
    P_off_wind2 = df['P_off_wind2'].values.tolist()
    P_off_wind3 = df['P_off_wind3'].values.tolist()
    df = pd.read_csv('Lab files/Cgens_Ugens.csv')
    cgens = df['Cgens'].values.tolist()
    ugens = df['Ugens'].values.tolist()

    gens = {}
    for key in cgens:
        for value in ugens:
            gens[key] = value
            ugens.remove(value)
            break
    # Sort the dictionary by key and print the lowest and hihest values
    gens = dict(sorted(gens.items()))
    print("Lowest capacity: ", min(gens.keys()))
    print("Highest capacity: ", max(gens.keys()))

    # Sort the dictionary by values and print the lowest and hihest values
    gens = dict(sorted(gens.items(), key=lambda item: item[1]))
    print("Lowest unavailability: ", min(gens.values()))
    print("Highest unavailability: ", max(gens.values()))

    # What is the total capacity of the system?
    print("Total capacity: ", sum(gens.keys()))

    # What is the peek load?
    print("Peek load: ", max(NLh_load))

    cgens = df['Cgens'].values.tolist()
    ugens = df['Ugens'].values.tolist()

    copt_4 = func.COPT_function(cgens, ugens, 50)
    print("COPT table:\n", copt_4)
    xaxis = list(copt_4[:, 0])
    yaxis = list(copt_4[:, 1])

    plt.bar(xaxis, yaxis, color='blue', width=50)

    plt.xlabel("Capacity Outage [MW]")
    plt.ylabel("Probability")
    plt.title("2nd Column of COPT")
    plt.show()

    # Plot the second column of the result
    # print("Second column of COPT: ", copt_4[:, 1])
    # fig = plt.figure(figsize=(10, 5))
    # plt.plot(yaxis)
    # plt.show()


def question_5():
    # Question 5
    print("\nQuestion 5:\n")

    # Read data from file
    df = pd.read_csv('Lab files/load_Pwind.csv')
    NLh_load = df['NLh_load'].values.tolist()
    P_off_wind1 = df['P_off_wind1'].values.tolist()
    P_off_wind2 = df['P_off_wind2'].values.tolist()
    P_off_wind3 = df['P_off_wind3'].values.tolist()

    # Read data from file
    df = pd.read_csv('Lab files/Cgens_Ugens.csv')
    cgens = df['Cgens'].values.tolist()
    ugens = df['Ugens'].values.tolist()
    copt = func.COPT_function(cgens, ugens, 50)

    lolps = []
    loles = []
    max_load = max(copt[:, 0])
    print("Max load: ", max_load)

    # Compute LOLP and LOLE for each load
    for load in NLh_load:
        # Calculate LOLP and LOLE using the copt table previously generated
        lolps.append(np.sum(copt[np.where(max_load - copt[:, 0] < load), 2]) / 8760)
        loles.append(np.sum(copt[np.where(max_load - copt[:, 0] < load), 2]))

    # Plot the LOLP
    fig = plt.figure(figsize=(10, 5))
    plt.plot(lolps, color='blue')
    plt.xlabel("Time [h]")
    plt.ylabel("LOLP")
    plt.title("LOLP vs Load")
    # plt.show()

    # Plot the LOLE
    fig = plt.figure(figsize=(10, 5))
    plt.plot(loles, color='blue')
    plt.xlabel("Time [h]")
    plt.ylabel("LOLE")
    plt.title("LOLE vs Load")
    # plt.show()

    # Plot the loads
    fig = plt.figure(figsize=(10, 5))
    plt.plot(NLh_load, label='Load')
    plt.xlabel("Time [h]")
    plt.ylabel("Load [MW]")
    plt.title("Load")
    plt.legend()

    # plt.show()


def question_6():
    # Question 6
    print("\nQuestion 6:\n")

    # Read data from file
    df = pd.read_csv('Lab files/load_Pwind.csv')
    NLh_load = df['NLh_load'].values.tolist()
    P_off_wind1 = df['P_off_wind1'].values.tolist()
    P_off_wind2 = df['P_off_wind2'].values.tolist()
    P_off_wind3 = df['P_off_wind3'].values.tolist()

    # Read data from file
    df = pd.read_csv('Lab files/Cgens_Ugens.csv')
    cgens = df['Cgens'].values.tolist()
    ugens = df['Ugens'].values.tolist()

    copt = func.COPT_function(cgens, ugens, 50)

    cf = np.mean(P_off_wind1) / np.max(P_off_wind1)
    print("Total installed capacity: ", np.max(P_off_wind1))
    print("Capacity factor: ", cf)

    cgens.append(np.max(P_off_wind1))
    ugens.append(1 - cf)
    print("New cgens: ", cgens)
    print("New ugens: ", ugens)

    copt = func.COPT_function(cgens, ugens, 50)
    print("COPT table:\n", copt)

    # Calculate LOLP and LOLE again
    # Compute LOLP and LOLE for each load
    lolps = []
    loles = []
    max_load = max(copt[:, 0])
    i = 0
    for load in NLh_load:
        # Calculate LOLP and LOLE using the copt table previously generated
        load = load - P_off_wind1[i]
        i = i + 1
        copt_col = copt[:, 0]
        inds = np.where(max_load - copt_col < load)
        lolps.append(copt[inds[0][0], 2] / 8760)
        loles.append(copt[inds[0][0], 2])
        # print(inds[0][0])
        # break
    print("LOLP: ", np.sum(lolps))
    print("LOLE: ", np.sum(loles))

    # Plot the LOLP
    fig = plt.figure(figsize=(10, 5))
    plt.plot(lolps, color='blue')
    plt.xlabel("Time [h]")
    plt.ylabel("LOLP")
    plt.title("LOLP vs Load")
    # plt.show()

    # Plot the LOLE
    fig = plt.figure(figsize=(10, 5))
    plt.plot(loles, color='blue')
    plt.xlabel("Time [h]")
    plt.ylabel("LOLE")
    plt.title("LOLE vs Load")
    # plt.show()

    return np.sum(lolps), np.sum(loles)


def question_7(LOLP, LOLE):
    # Read data from file
    df = pd.read_csv('Lab files/load_Pwind.csv')
    NLh_load = df['NLh_load'].values.tolist()
    P_off_wind1 = df['P_off_wind1'].values.tolist()
    P_off_wind2 = df['P_off_wind2'].values.tolist()
    P_off_wind3 = df['P_off_wind3'].values.tolist()

    # Read data from file
    df = pd.read_csv('Lab files/Cgens_Ugens.csv')
    cgens = df['Cgens'].values.tolist()
    ugens = df['Ugens'].values.tolist()

    copt = func.COPT_function(cgens, ugens, 50)

    # Calculate the Capacity Credit
    lolps = []
    loles = []
    max_load = max(copt[:, 0])
    for k in range(0, 10):
        i = 0
        lolps = []
        loles = []
        for load in NLh_load:
            # Calculate LOLP and LOLE using the copt table previously generated
            new_load = load - P_off_wind1[i] - k * 10
            i = i + 1
            copt_col = copt[:, 0]
            inds = np.where(max_load - copt_col < new_load)
            lolps.append(copt[inds[0][0], 2] / 8760)
            loles.append(copt[inds[0][0], 2])
        print("Added load ", k * 10)
        print("LOLP - lolp: ", LOLP - np.sum(lolps))
        print("LOLE - lole: ", LOLE - np.sum(loles))


if __name__ == '__main__':
    # question_1()
    # question_2()
    # question_3()
    # question_4()
    # question_5()
    LOLP, LOLE = question_6()
    question_7(LOLP, LOLE)