import matplotlib.pyplot as plt
from scipy.stats.distributions import chi2


def assignment_1(name, nfails, km, nyears):
    # 1.1
    # repair time for EHV and HV is 44 hours on average (From table 2.3)

    f = nfails / (km * nyears)  # failure rate
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

    plt.boxplot(mean)
    plt.show()


if __name__ == '__main__':
    print("Assignment 1:\n")
    mean_EHV = assignment_1('EHV', 25, 2310, 5)
    mean_HV = assignment_1('HV', 51, 3329, 5)
    if mean_EHV > mean_HV:
        print("EHV has a higher failure frequency than HV\n\n")
    else:
        print("HV has a higher failure frequency than EHV\n\n")

    print("Assignment 2:\n")
    assignment_2('EHV', 25, 2310, 5, mean_EHV)
    assignment_2('HV', 51, 3329, 5, mean_HV)
