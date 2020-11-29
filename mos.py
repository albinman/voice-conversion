"""
This module reads the subjective evaluations and saves the results as csv file
"""

import os
import re
import csv

# opinion scores are saved in dictionaries
# key = model name; value = {score: counter} -> score from 1 to 4
mos_sim = {}
mos_nat = {}


def update_dicts(code, nat_score, sim_score):
    """
    Update a MOS dictionary with new scores
    :param code: name for VC model used as key in MOS dictionary
    :param nat_score: perceived naturalness score from 1 to 4
    :param sim_score: perceived similarity score from 1 to 4
    :return: None
    """
    # import the global MOS dictionaries
    global mos_nat
    global mos_sim
    # if MOS dictionary for naturalness does not have an entry for
    # model=code, create entry with current score
    if code not in mos_nat:
        mos_nat[code] = {nat_score: 1}
    else:
        # update existing MOS dictionary entry
        # if current nat_score is first for this model, create entry
        if nat_score not in mos_nat[code]:
            mos_nat[code].update({nat_score: 1})
        else:
            # increment counter for current nat_score for current model
            mos_nat[code][nat_score] += 1
    # same procedure for similarity MOS dictionary
    if code not in mos_sim:
        mos_sim[code] = {sim_score: 1}
    else:  
        if sim_score not in mos_sim[code]:
            mos_sim[code].update({sim_score: 1})
        else:
            mos_sim[code][sim_score] += 1


def text_only(feedback_folder_path):
    """
    Iterate a folder consisting only of audio score text files,
    where test subject copied score text files and deleted rest,
    and update MOS dictionaries
    :param feedback_folder_path: path to folder provided by test subject
    :return: None
    """
    elems = os.listdir(feedback_folder_path)
    global mos_sim
    global mos_nat
    # ignore instruction text files
    for junk in ["Anleitung.txt", "instructions.txt"]:
        if junk in elems: elems.remove(junk)
    # iterate score text files and update MOS dictionaries
    for file in elems:
        filepath = os.path.join(feedback_folder_path, file)
        code, nat_score, sim_score = score_filepath_to_scores(filepath)
        update_dicts(code, nat_score, sim_score)


def normal_structure(feedback_folder_path):
    """
    Iterate a folder structure equivalent to example_folder_for_test_subjects,
    where test subject only entered scores in the text files,
    and update MOS dictionaries
    :param feedback_folder_path: path to folder provided by test subject
    :return: None
    """
    elems = os.listdir(feedback_folder_path)
    global mos_sim
    global mos_nat
    # ignore instruction text files
    for junk in ["Anleitung.txt", "instructions.txt", ".DS_Store"]:
        if junk in elems: elems.remove(junk)
    # iterate score text files and update MOS dictionaries
    for elem in elems:
        for file in os.listdir(os.path.join(feedback_folder_path, elem)):
            if file.endswith('.txt'):
                filepath = os.path.join(feedback_folder_path, elem, file)
                code, nat_score, sim_score = score_filepath_to_scores(filepath)
                update_dicts(code, nat_score, sim_score)


def score_filepath_to_scores(score_filepath):
    """
    Extract the opinion scores for naturalness and similarity
    from the score text file
    :param score_filepath: path to score text file
    :return: code=model name, nat_score from 1 to 4, sim_score from 1 to 4
    """
    with open(score_filepath, 'r') as os_file:
        for line in os_file.readlines():
            if line.startswith("Naturalness\t"):
                nat_score = re.findall('\d\/\d', line)[0]
                nat_score = re.sub('/4','',nat_score)
                if len(nat_score) < 1:
                    print(score_filepath)
                    raise ValueError
                nat_score = int(nat_score)
            if line.startswith("Similarity\t"):
                sim_score = re.findall('\d\/\d', line)[0]
                sim_score = re.sub('/4','',sim_score)
                if len(sim_score) < 1:
                    print(score_filepath)
                    raise ValueError
                sim_score = int(sim_score)
            if line.startswith("[Code"):
                code = line
                code = re.sub('\[Code: ', '', code)
                code = re.sub(']', '', code)
                code = re.sub('/', '', code)
                code = code.split('_')
                code = '_'.join([code[0],code[2],code[5],code[7]])
    return code, nat_score, sim_score


def write_scores(mos, outfile):
    """
    Write a MOS dictionary to a CSV file
    :param mos: MOS dictionary, either mos_nat or mos_sim
    :param outfile: filepath and filename for CSV file
    :return: None
    """
    with open(outfile, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in mos:
            csv_writer.writerow([key, mos[key]])


def main():
    path = '../opinion_scores/'
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        print(folder_path)
        try:
            normal_structure(folder_path)
        except NotADirectoryError:
            text_only(folder_path)

    write_scores(mos_nat, outfile='../voice-conversion/nat_scores_test.csv')
    write_scores(mos_sim, outfile='../voice-conversion/sim_scores_test.csv')


if __name__ == '__main__':
    main()
