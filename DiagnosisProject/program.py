import os
from GenerationRelatedStuff import generate_hash , generate_diagnosis, write_diagnosis_to_result, update_normal_obs, parse_file_to_list_of_lines
from Diagnoser import Diagnoser
"""
    This file run the algorithms for each problem file in the given directory.
"""
DIRECTORY_PATH = 'C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\ProblemDataset\\'


def run_experiments():
    for filename in os.listdir(DIRECTORY_PATH):
        if filename.endswith(".txt"):
            path = DIRECTORY_PATH+filename
            lines = parse_file_to_list_of_lines(path)
            generate_hash(lines)
            indexes_of_subsystems = update_normal_obs(lines)
            diagnosis, hits = generate_diagnosis(lines, indexes_of_subsystems)
            write_diagnosis_to_result(lines, diagnosis, hits)
            continue
        else:
            continue


#run_experiments()

def run_regression_expirment():

    for filename in os.listdir(DIRECTORY_PATH):
        if filename.endswith(".txt"):
            path = DIRECTORY_PATH+filename
            lines = parse_file_to_list_of_lines(path)
            observations = lines[lines.index('NormalObservations:'): lines.index('TotalBuggyObservations:')][1: -1]
            bug_obs = lines[lines.index('BuggyObservations:'): lines.index('BuggyIds')][1: -1]
            observations = [eval(obs) for obs in observations]
            bug_obs = [eval(obs) for obs in bug_obs]
            diagnoser = Diagnoser(observations)
            diagnosis = diagnoser.full_diagnosis(bug_obs)
            number_of_subsystems = len(lines[lines.index('Subsystems:'): lines.index('')][1:])
            buggy_ids = [i for i in lines[lines.index('BuggyIds'):lines.index('MinRange:')][1: -1]][0].split(', ')
            hits, extra_comps = diagnoser.get_hits(buggy_ids, bug_obs, number_of_subsystems)
            write_diagnosis_to_result(lines, diagnosis, hits)
            continue
        else:
            continue


run_regression_expirment()