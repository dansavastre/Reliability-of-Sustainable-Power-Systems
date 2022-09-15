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

    plt.boxplot([confidence_interval_left, mean, confidence_interval_right])
    plt.show()
    plt.close()

def assignment_4():
    print("\n\nAssignment 4:\n");
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()
    print(data)
    print("Average repair time = {}".format(sum(data) / len(data)))
    print("Minimum repair time = {}".format(min(data)))
    print("Maximum repair time = {}".format(max(data)))

def assignment_5():
    print("\n\nAssignment 5:\n");
    df = pd.read_csv("repair_times_OHL.csv")
    data = df["Repair Times"].values.tolist()
    plt.boxplot(data)
    plt.show()
    plt.close()

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
    plt.scatter(data, Ft)
    plt.plot(x_axis, exponential(x_axis, *params), '--')
    plt.show()
    print(params)

def exponential_old(t, a, b, c):
    return a * np.exp(-b * np.asarray(t)) + c

def exponential(b, t):
    return -np.exp(-b * t) + 1

if __name__ == '__main__':
    assignment_6()

# if __name__ == '__main__':
#     print("Assignment 1:\n")
#     mean_EHV = assignment_1('EHV', 25, 2310, 5)
#     mean_HV = assignment_1('HV', 51, 3329, 5)
#     if mean_EHV > mean_HV:
#         print("EHV has a higher failure frequency than HV\n\n")
#     else:
#         print("HV has a higher failure frequency than EHV\n\n")
#
#     print("Assignment 2:\n")
#     assignment_2('EHV', 25, 2310, 5, mean_EHV)
#     assignment_2('HV', 51, 3329, 5, mean_HV)
#     mean_EHV_HV = calculate_mean(25 + 51, 2310 + 3329, 5)
#     assignment_2('EHV/HV', 25 + 51, 2310 + 3329, 5, mean_EHV + mean_HV)
#
#     # 3 years later
#     # 42 EHV OHL faliures
#     # 167 HV OHL faliures
#     # 2471 km of EHV OHL
#     # 4078 km of HV OHL
#
#     # Calculate the failure frequencies of EHV, HV, and EHV/HV OHLs again, together with their
#     # 95% confidence intervals. Also plot the results as a boxplot
#     print("\n\nAssignment 3:\n")
#
#     mean_EHV_3 = assignment_1('EHV', 42, 2471, 8)
#     mean_HV_3 = assignment_1('HV', 167, 4078, 8)
#
#     assignment_2('EHV', 42, 2471, 3, mean_EHV_3)
#     assignment_2('HV', 167, 4078, 3, mean_HV_3)
#
#     assignment_4()


