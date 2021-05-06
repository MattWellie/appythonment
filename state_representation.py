from csv import DictReader
import sys

# geometric_mean is standard library as of python 3.8
version = sys.version_info

if version.major >= 3 and version.minor >= 8:
    from statistics import geometric_mean

# otherwise use numpy equivalent
else:
    import numpy as np

    def geometric_mean(nums):
        return np.exp(np.mean(np.log(nums)))


#########
# SETUP #
#########

# establish some global variables, which can be tinkered with
max_reps = 436
use_geometric = True  # False for Arithmetic


def set_up():
    """
    Create an initial dict where we have the State name pointing to their number of reps and population
    Default representation is 1, per the algorithm
    :return:
    """
    for row in DictReader(open("state_inputs.tsv"), delimiter="\t"):
        rep_dict[row["State"]] = {"reps": 1, "pop": int(row["Population"])}


def assign_next():
    """

    :return:
    """

    highest_state = find_highest_priority()
    rep_dict[highest_state]["reps"] += 1


def find_highest_priority():
    """

    :return:
    """

    highest_priority = sorted(
        rep_dict.items(), key=lambda item: find_priority(item[1])
    )[-1]

    # return the name of the highest ranked state
    return highest_priority[0]


def find_priority(state_dict):
    """
    use the chosen mean to determine the priority value
    :return:
    """

    # find the geometric mean of the current reps + 1
    if use_geometric:
        denominator = geometric_mean([state_dict["reps"], state_dict["reps"] + 1])

    # if we're not using geometric, just add a half to the current representation?
    else:
        denominator = float(state_dict["reps"]) + 0.5
    return state_dict["pop"] / denominator


def count_current_reps():
    return sum([values["reps"] for state, values in rep_dict.items()])


# if we run naked, run this section - this sets off the rest of the script
if __name__ == "__main__":

    rep_dict = dict()

    # read the population levels from a titled TSV file of 'State' and 'Population'
    set_up()

    # count the current reps (should be 50 on setup, 1 per state)
    current_reps = count_current_reps()

    # iterate through until we hit the maximum, change max in the SETUP section to fiddle with this
    while current_reps < max_reps:
        assign_next()
        current_reps = count_current_reps()

    # fully populated
    print("State\tPopulation\tReps")
    for state in sorted(
        rep_dict.items(), key=lambda item: item[1]["reps"], reverse=True,
    ):
        print(
            "{state}\t{pop}\t{rep}".format(
                state=state[0], pop=state[1]["pop"], rep=state[1]["reps"]
            )
        )
