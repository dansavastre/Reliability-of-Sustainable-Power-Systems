import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats.distributions import chi2
import numpy as np


def calculate_mean(nfails, km, nyears):
    return nfails / (km * nyears)
def assignment_1(name, nfails, km, nyears):
    # 1.1
    # repair time for EHV and HV is 44 hours on average (From table 2.3)

    f = calculate_mean(nfails, km, nyears)  # failure rate
    print("Failure frequency for {} = {}".format(name, f))

    # Mean Time To Failure (MTTF)
    mttf = (nyears * 8760) / nfails
    print("Mean Time To Failure (MTTF) for {} = {}".format(name, mttf))

    # Mean Time To Repair (MTTR)
    mttr = 44
    print("Mean Time To Repair (MTTR) for {} = {}".format(name, mttr))

    # Mean Time Between Failures (MTBF)
    mtbf = mttf + mttr
    print("Mean Time Between Failures for {} = {}\n".format(name, mtbf))
    return f


def assignment_2(name, nfails, km, nyears, mean):
    # 1.2

    # l = average failure rate [/cctkm·yr] or [/comp·yr]
    # T = total considered time length (component-years) [cctkm·yr] or [comp·yr]
    # F = statistical number of failures within T [-]
    # alpha = significance level [-]
    # χ2 = Chi-square distribution.
    # 1-α/2 or α/2 = probability
    # 2F or 2F+2 = degrees of freedom

    T = nyears * km  # years
    alpha = 0.05  # 95% confidence interval
    F = nfails  # number of failures

    confidence_interval_right = chi2.ppf(1 - alpha / 2, 2 * F) / (2 * T)
    confidence_interval_left = chi2.ppf(alpha / 2, 2 * F + 2) / (2 * T)

    print("Confidence interval for {} = [{}, {}]".format(name, confidence_interval_left, confidence_interval_right))

    # figure related code
    fig = plt.figure()
    fig.suptitle('Assignment 2', fontsize=14, fontweight='bold')
    if name.find("5") == -1:
        fig.suptitle('Assignment 3', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    ax.boxplot([confidence_interval_left, mean, confidence_interval_right])

    ax.set_title('Failure frequency for {}'.format(name))
    ax.set_xlabel('failure')
    ax.set_ylabel('frequency')

    fig.savefig('Assignment 2 - Failure frequency for {}.png'.format(name))
    plt.show()

def assignment_3():
    # 3 years later
    # 42 EHV OHL faliures
    # 167 HV OHL faliures
    # 2471 km of EHV OHL
    # 4078 km of HV OHL

    # Calculate the failure frequencies of EHV, HV, and EHV/HV OHLs again, together with their
    # 95% confidence intervals. Also plot the results as a boxplot
    print("\n\nAssignment 3:\n")

    mean_EHV_3 = assignment_1('EHV-8years', 42, 2471, 8)
    mean_HV_3 = assignment_1('HV-8years', 167, 4078, 8)

    assignment_2('EHV-8years', 42, 2471, 3, mean_EHV_3)
    assignment_2('HV-8years', 167, 4078, 3, mean_HV_3)
def assignment_4():
    print("\n\nAssignment 4:\n");
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()
    print(data)
    print("Average repair time = {}".format(sum(data) / len(data)))
    print("Minimum repair time = {}".format(min(data)))
    print("Maximum repair time = {}".format(max(data)))

def assignment_5():
    #print("\n\nAssignment 5:\n");
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()

    # figure related code
    fig = plt.figure()
    fig.suptitle('Assignment 5', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    ax.boxplot(data)

    ax.set_title('Repair times for OHL')
    ax.set_xlabel('repair')
    ax.set_ylabel('time')

    fig.savefig('Assignment 5.png')
    plt.show()

def assignment_6():
    print("\n\nAssignment 6:\n")
    # F(t) = fraction of unrepaired components (1=no repaired components, 0=all components repaired) [-]
    # t = time [h]
    # T1 (-b) = repair time (according to the exponential distribution) [h]
    # a = coefficient of the exponential term
    # c = independent term
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()
    # data.reverse()
    # sort the data
    data.sort()
    Ft = np.arange(0, 1.00001, 1/(len(data) - 1))
    Ft = np.arange(1.0/(len(data)+1), 1.00001-1.0/(len(data)+1), 1/(len(data) + 1))
    x_axis = np.arange(0, 70 + 0.00001, 0.1)
    params, covariance = curve_fit(exponential, data, Ft)

    # figure related code
    fig = plt.figure()
    fig.suptitle('Assignment 6', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    ax.scatter(data, Ft)
    ax.plot(x_axis, exponential(x_axis, *params), '--')

    ax.set_title('Fitted exponential curve')
    ax.set_xlabel('repair time')
    ax.set_ylabel('F(t)')

    fig.savefig('Assignment 6 - Fitted exponential curve.png')
    plt.show()
    print(params)

def exponential_old(t, a, b, c):
    return a * np.exp(-b * np.asarray(t)) + c

def exponential(b, t):
    return -np.exp(-b * t) + 1

if __name__ == '__main__':
    print("Assignment 1:\n")
    mean_EHV = assignment_1('EHV', 25, 2310, 5)
    mean_HV = assignment_1('HV', 51, 3329, 5)
    mean_EHV_HV = calculate_mean(25 + 51, 2310 + 3329, 5)
    if mean_EHV > mean_HV:
        print("EHV has a higher failure frequency than HV\n\n")
    else:
        print("HV has a higher failure frequency than EHV\n\n")

    print("Assignment 2:\n")
    assignment_2('EHV-5years', 25, 2310, 5, mean_EHV)
    assignment_2('HV-5years', 51, 3329, 5, mean_HV)
    assignment_2('EHV-HV-5years', 25 + 51, 2310 + 3329, 5,mean_EHV_HV)

    assignment_3()
    assignment_4()
    assignment_5()
    assignment_6()


