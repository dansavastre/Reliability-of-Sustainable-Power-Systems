# state_enumeration_MVL - Bart Tuinema
# Performs deterministic (n-1) contingency analysis
# using and generation/load data for a complete year (2020)
# MVL region only (MVL region load flow)
import numpy as np
from get_B_matrix import get_B_matrix_NL_func2020_MVL_without_SMH
from get_P_lines import get_P_lines_MVL_func
import matplotlib.pyplot as plt
import pandas as pd


extra_offshore_wind = 2 ##offshore wind to be added (in GW)

## Circuit unavailabilities
# 1-2   = 2.46e-3
# 3-4   = 2.01e-5
# 5-6   = 6.18e-3
# 7-8   = 3.58e-5
# 9-10  = 1.33e-4
# 11-12 = 2.93e-5
unavailability = [2.46e-3, 2.46e-3, 2.01e-5, 2.01e-5, 6.18e-3, 6.18e-3,
                  3.58e-5, 3.58e-5, 1.33e-4, 1.33e-4, 2.93e-5, 2.93e-5]

## Line capacities

C_lines = [2650, 2650, 2632.7, 2632.7, 2909.9, 2909.9,
           2632.7, 2632.7, 2909.9, 2909.9, 2632.7, 2632.7]


## state enumeration: initial values

P_lines_normal = np.zeros([12,8736])     # circuit loadings in normal operation (for one year)
P_lines_max_cont = np.zeros([12,1])      # maximum circuit loadings in deterministic n-1 contingency analysis


## contingency analysis: bus loads (substation loads)
df = pd.read_csv('../Practicum Material/scenario2020_MVL.csv') # these are the generation and load (in MW) per substation
MVL380_load = np.matrix(df['MVL380_load'].values.tolist())
SMH380_load = np.matrix(df['SMH380_load'].values.tolist())
WL380W_load = np.matrix(df['WL380W_load'].values.tolist())
WL380Z_load = np.matrix(df['WL380Z_load'].values.tolist())
WTR380_load = np.matrix(df['WTR380_load'].values.tolist())
BWK380_load = np.matrix(df['BWK380_load'].values.tolist())
CST380_load = np.matrix(df['CST380_load'].values.tolist())
KIJ380_load = np.matrix(df['KIJ380_load'].values.tolist())
MVL380_gen = np.matrix(df['MVL380_gen'].values.tolist())
SMH380_gen = np.matrix(df['SMH380_gen'].values.tolist())
MVL380_exp = np.matrix(df['MVL380_exp'].values.tolist())
MVL380_wind = np.matrix(df['MVL380_wind'].values.tolist())
print(MVL380_wind)

df = pd.read_csv('../Practicum Material/scenario2020_line_flows_MVL.csv') # these are the line flows (in MW) to the rest of the 380kV network
VHZ380_BWK380a = np.matrix(df['VHZ380_BWK380a'].values.tolist())
VHZ380_BWK380b = np.matrix(df['VHZ380_BWK380b'].values.tolist())
BKL380_KIJ380 = np.matrix(df['BKL380_KIJ380'].values.tolist())
KIJ380_GT380a = np.matrix(df['KIJ380_GT380a'].values.tolist())
KIJ380_GT380b = np.matrix(df['KIJ380_GT380b'].values.tolist())
KIJ380_OZN380 = np.matrix(df['KIJ380_OZN380'].values.tolist())

bus_loads = np.zeros([8736,6])
bus_loads[:,0] = MVL380_load + SMH380_load   # the loads are added to the buses (i.e. substations)
bus_loads[:,1] = WL380W_load + WL380Z_load
bus_loads[:,2] = WTR380_load
bus_loads[:,3] = BWK380_load
bus_loads[:,4] = CST380_load
bus_loads[:,5] = KIJ380_load
bus_loads[:,0] = bus_loads[:,0] + MVL380_gen + SMH380_gen   # the generation of MVL and SMH are added to bus 1 (MVL)
bus_loads[:,0] = bus_loads[:,0] + MVL380_exp   # the export to the UK is added to MVL
bus_loads[:,3] = bus_loads[:,3] - VHZ380_BWK380a - VHZ380_BWK380b   # at bus 4 (BWK), the line loadings to the rest of the 380kV network (VHZ) are added
bus_loads[:,5] = bus_loads[:,5] - BKL380_KIJ380 + KIJ380_GT380a + KIJ380_GT380b +KIJ380_OZN380   # at bus 6 (KIJ), the line loadings to the rest of the 380kV network (BKL/GT/OZN) are added
bus_loads[:,0] = bus_loads[:,0] + (1+extra_offshore_wind) * MVL380_wind   # 1x 1GW offshore wind is added to MVL
bus_loads[:,5] = bus_loads[:,5] - extra_offshore_wind * MVL380_wind   # If extra wind generation is added to bus 1(MVL), it can be absorbed here at bus 6 (KIJ)
slackbus = np.zeros(8736)
for i in range(8736):
    slackbus[i] = sum(bus_loads[i,:])  # these are the slackbus values based on the bus_loads/bus_generation (should be almost 0), so before the DC load flow calculation

## Contingency analysis: normal operation

print('normal operation')
lines = np.ones(12)    # these are the statuses of the lines (1=working)
B_matrix, Y_lines = get_B_matrix_NL_func2020_MVL_without_SMH(lines)    # get B_matrix etc for DC load flow
# print('B_matrix', B_matrix)
# print('Y_lines', Y_lines)
if np.linalg.cond(B_matrix) < 1e-15:   # bus in island check (if a bus is islanded, the load flow cannot be performed)
    print('RIP: bus in island / split system in normal case')   # an error message in given
else:
    for i in range(8736):    # for each hour in the year (8736 hours = 52 weeks)
        if abs(slackbus[i])>100:   # check whether the slackbus value is small (otherwise there is a mismatch between load/generation)
            print('slackbus>100, hour: ', i, slackbus[i])
        else:
            #Y_bus[0,0] = np.sum([Y_lines[0], Y_lines[1], Y_lines[8], Y_lines[9])
            P_lines = get_P_lines_MVL_func(B_matrix, Y_lines, C_lines, bus_loads[i,:])   # result from the DC load flow (=line flows in MW)
            P_lines_normal[:,i] = P_lines   # circuit loadings during normal operation
            if any(abs(P_lines)>100):   # if there is an overloaded circuit
                print('RIP: line overloaded in normal case')   # an error message in given


## Contingency analysis: 1st-order contingencies

print('1st-order contingencies')
p_island = 0   # this is the probability that a bus is islanded (i.e. a line is out of service)
p_overload = 0   # this is the probability that a line is overloaded (i.e. a line is out of service)
state_failure_probability = np.zeros(1000)   # these are the failure probabilities of the lines
s = 0
for j in range(12):    # for each of the 12 lines in the network
    print("Failure of ", j, " as State ", s)         # display line number
    # failure probability of line j
    probability = 1
    for k in range(12):
        if k != j:
            probability = probability * (1 - unavailability[k])
        else:
            probability = probability * unavailability[k]
    state_failure_probability[s] = probability   # the failure probability of the line
    print("State Failure probability: ", state_failure_probability[s])   # display state failure probability

    lines = np.ones(12)    # these are the statuses of the lines (1=working)
    lines[j] = 0     # line #j is out
    B_matrix, Y_lines = get_B_matrix_NL_func2020_MVL_without_SMH(lines)   # get B-matrix and Y-lines for this network configuration
    if np.linalg.cond(B_matrix) < 1e-15:   # bus in island check
        print('Oof: bus in island / split system: ', str(j))
        p_island = p_island + state_failure_probability[s]   # if a bus is islanded, the probability that a bus is islanded is increased

    else:
        for i in range(8736):   # for each hour of the year
            if abs(slackbus[i])<=100:         # check whether there is a mismatch between generation and load
                P_lines = get_P_lines_MVL_func(B_matrix, Y_lines, C_lines, bus_loads[i,:])
                if any(abs(P_lines)>100):      # if a line is overloaded, give an error message
                    p_overload = p_overload + state_failure_probability[s]   # if a line is overloaded, the probability that a line is overloaded is increased
                    print('Oof: line overloaded under 1st-order contingency, hour: ', i, ', contingency: ', j)
                for k in range(12):    # for each of the 12 lines, find and save the maximum loading
                    P_lines_max_cont[k] = max(P_lines_max_cont[k],P_lines[k])

    s = s + 1
# Second order contingencies
print('2nd-order contingencies')
for i in range(11):
    for j in range(i + 1, 12):    # for each of the 12 lines in the network
        s = s + 1
        print("Failure of ", i, " and ", j, " as State ", s)         # display line number

        # failure probability of lines i and j
        probability = 1
        for k in range(12):
            if k != i and k != j:
                probability = probability * (1 - unavailability[k])
            else:
                probability = probability * unavailability[k]
        state_failure_probability[s] = probability   # the failure probability of the line
        print("State Failure probability: ", state_failure_probability[s])   # display state failure probability

        lines = np.ones(12)    # these are the statuses of the lines (1=working)
        lines[i] = 0  # line #i is out
        lines[j] = 0     # line #j is out
        B_matrix, Y_lines = get_B_matrix_NL_func2020_MVL_without_SMH(lines)   # get B-matrix and Y-lines for this network configuration
        if np.linalg.cond(B_matrix) < 1e-15:   # bus in island check
            print('Oof: bus in island / split system: ', str(i), ", ", str(j))   # an error message in given
            p_island = p_island + state_failure_probability[s]   # if a bus is islanded, the probability that a bus is islanded is increased

        else:
            for k in range(8736):   # for each hour of the year
                if abs(slackbus[k])<=100:         # check whether there is a mismatch between generation and load
                    P_lines = get_P_lines_MVL_func(B_matrix, Y_lines, C_lines, bus_loads[k,:])
                    if any(abs(P_lines)>100):      # if a line is overloaded, give an error message
                        p_overload = p_overload + state_failure_probability[s]   # if a line is overloaded, the probability that a line is overloaded is increased
                        print('Oof: line overloaded under 1st-order contingency, hour: ', k, ', contingency: ', i, " and ", j)
                    for l in range(12):    # for each of the 12 lines, find and save the maximum loading
                        P_lines_max_cont[l] = max(P_lines_max_cont[l],P_lines[l])
p_available = 1
for i in range(12):
    p_available = p_available * (1 - unavailability[i])
p_total = p_available + np.sum(state_failure_probability)   # this is the total probability of all considered states
print("Max Loading:\n", P_lines_max_cont)  # display the maximum loading for all contingencies
print("Probability of bus in island: ", p_island)  # display the probability that a bus is islanded
print("Probability of line overloaded: ", p_overload / 8736)   # display the probability that a line is overloaded
print("Total probability of all considered states: ", p_total)   # display the total probability of all considered states
print("Probability of not considered states: ", 1 - p_total)   # display the probability of all the not considered states

## Figures
for i in range(12):
    plt.bar(i, P_lines_max_cont[i])

# plt.show()

plt.boxplot([P_lines_normal[0], P_lines_normal[1], P_lines_normal[2], P_lines_normal[3], P_lines_normal[4], P_lines_normal[5], P_lines_normal[6], P_lines_normal[7], P_lines_normal[8], P_lines_normal[9], P_lines_normal[10], P_lines_normal[11]])

plt.xticks(range(0, 12))
plt.title('Deterministic contingency analysis 2020 MVL-region')

plt.ylabel("Relative Line Loading")
# plt.show()

print(max(P_lines_normal[0]), max(P_lines_normal[1]), max(P_lines_normal[2]), max(P_lines_normal[3]), max(P_lines_normal[4]), max(P_lines_normal[5]), max(P_lines_normal[6]), max(P_lines_normal[7]), max(P_lines_normal[8]), max(P_lines_normal[9]), max(P_lines_normal[10]), max(P_lines_normal[11]))