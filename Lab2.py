import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Assignment 1:
    ff_ohl = 0.0022 * 10
    u_ohl = 0.0022 * 8 * 10 / 8760
    print("Assignment 1:")
    print("For a 10km circuit of EHV with a failure frequency of 0.0022 per cctkm year:"
          "\n - the failure frequency is: ", ff_ohl, " per year",
          "\n - the unavailability is: ", u_ohl)

    p0 = u_ohl ** 2
    p1 = 2 * u_ohl * (1 - u_ohl)
    p2 = (1 - u_ohl) ** 2
    print("For a double circuit the probability of:",
          "\n- 0 circuits available is: ", p0, " which is {} hours/year".format(p0 * 8760),
          "\n- 1 circuit available is: ", p1, " which is {} hours/year".format(p1 * 8760),
          "\n- 2 circuits available is: ", p2, " which is {} hours/year".format(p2 * 8760))

    # Assignment 2:
    print("\nAssignment 2:")
    # Cable part length is 800m
    # In 10km we have 13 cable parts
    # 10km of double circuit UGC Randstad380 (Double circuit = 2 cables)
    # cable failure frequency: 0.0012/cctkmy
    # joint failure frequency: 0.00035/cctkmy
    # termination failure frequency: 0.00168/cctkmy
    # What are the failure frequency and unavailability of the circuit?
    # Repair time: 730h

    ff_oneCable = 0.0012 * 10 + 0.00035 * 12 + 0.00168 * 2
    u_oneCable = ff_oneCable * 730 / 8760
    ff_circuit = 2 * ff_oneCable * u_oneCable
    u_circuit = u_oneCable ** 2
    print("Failure frequency of one cable: ", ff_oneCable, " per year",
          "\nUnavailability of one cable: ", u_oneCable,
          "\nFailure frequency of the circuit: ", ff_circuit, " per year",
          "\nUnavailability of the circuit: ", u_circuit)

    # What are then the probabilities of having 0, 1 or 2 circuit(s) available?
    p0 = u_circuit ** 2
    p1 = 2 * u_circuit * (1 - u_circuit)
    p2 = (1 - u_circuit) ** 2
    print("For a double circuit the probability of:",
          "\n- 0 circuits available is: ", p0, " which is {} hours/year".format(p0 * 8760),
          "\n- 1 circuit available is: ", p1, " which is {} hours/year".format(p1 * 8760),
          "\n- 2 circuits available is: ", p2, " which is {} hours/year".format(p2 * 8760))

    # Assignment 3:
    c = 0.1
    print("\nAssignment 3:")
    u_ugc_2dep = c * u_circuit
    ff_ugc_2dep = c * ff_circuit
    print("For UGCs:")
    print("For a 2 dependent circuits the failure frequency is: ", ff_ugc_2dep, " per year",
          "\nFor a 2 dependent circuits the unavailability is: ", u_ugc_2dep)

    print("\nFor OHLs:")
    u_ohl_2dep = c * u_ohl
    ff_ohl_2dep = c * ff_ohl
    print("For a 2 dependent circuits the failure frequency is: ", ff_ohl_2dep, " per year",
          "\nFor a 2 dependent circuits the unavailability is: ", u_ohl_2dep)

    # Assignment 4:
    print("\nAssignment 4:")
    c_values = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
    for c in c_values:
        u_ugc_2dep = c * u_circuit
        ff_ugc_2dep = c * ff_circuit
        print("\nFor a 2 dependent circuits with c = {} the failure frequency is: {} per year".format(c, ff_ugc_2dep),
              "\nFor a 2 dependent circuits with c = {} the unavailability is: {}".format(c, u_ugc_2dep))

