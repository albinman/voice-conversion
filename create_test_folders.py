"""
This module generates the folders for the perceptual tests
for the subjective evaluation of the VC models
"""

import os
import re
import random

ref_parent_path = '../voice-conversion/reference_samples'
syn_parent_path = '../voice-conversion/synthesized_samples'

# the number of different test file constellations
n_test_groups = 8

def select_sample_pairs(ref_parent_path, syn_parent_path, n_test_groups):
    """
    Randomly select a synthesized sample from each model and find its
    reference sample
    :param ref_parent_path: path to folder containing all folders of
    reference samples
    :param syn_parent_path: path to folder containing all folders of
    converted samples
    :param n_test_groups: number of different constellations
    :return: list paths_of_pairs, containing n_test_groups list,
    each containing n_models (16) tuples, each containing 2 file paths for
    converted sample and reference sample
    """
    paths_of_pairs = []
    for i in range(n_test_groups):
        # create a list of file pairs for this group
        selection_per_group = []
        # go to folder with synthesized speech files
        for folder_name in os.listdir(syn_parent_path):
            if re.match('.*[A-Z]{2}$', folder_name):
                # save the folders last 4 letters. they represent the target speaker ID
                short_id = folder_name[-4:]
                # save all filenames of synthesized audio files: first element of pair
                wav_filenames_syn = []
                for filename in os.listdir(os.path.join(syn_parent_path, folder_name)):
                    if filename.endswith('.wav') and not filename.endswith('400.wav'):
                        wav_filenames_syn.append(filename)
                # randomly select a synthesized file
                syn_file = random.choice(wav_filenames_syn)
                # for each syn file, randomly select a target reference file with a different sentence ID
                wav_filenames_ref = []
                for filename in os.listdir(os.path.join(ref_parent_path, short_id)):
                    if filename.endswith('.wav') and not filename.endswith('400.wav'):
                        wav_filenames_ref.append(filename)
                ref_file = random.choice(wav_filenames_ref)
                while ref_file[-7:] == syn_file[-7:]:
                    ref_file = random.choice(wav_filenames_ref)
                # save file paths of syn file and ref file
                syn_path = os.path.join(syn_parent_path, folder_name, syn_file)
                ref_path = os.path.join(ref_parent_path, short_id, ref_file)
                selection_per_group.append((syn_path, ref_path))
        paths_of_pairs.append(selection_per_group)
        return paths_of_pairs

# paths_of_pairs is a list with 8 lists, each containing 16 tuples, each containing 2 file paths
# now, create a folder structure of this list and copy each element in the corresponding folder


def main():
    paths_of_pairs = select_sample_pairs(ref_parent_path, syn_parent_path, n_test_groups)

    if not os.path.isdir('./perception_test_folders'):
        os.system('mkdir ./perception_test_folders')

    for i, pairs in enumerate(paths_of_pairs):
        if os.path.isdir('mkdir ./perception_test_folders/test_group_{}'.format(i)):
            print("Folder test_group_{} exists. Aborting.")
            break
        else:
            os.system('mkdir ./perception_test_folders/test_group_{}'.format(i))
            os.system('touch ./perception_test_folders/test_group_{}/instructions.txt'.format(i))
            os.system('echo \"Thank you for participating in this study! \n\n'
                      'All of your answers are completely anonymous and no personal information will be used, saved or published.\n\n'
                      'You may hear recordings in English, German, and French. Before you start, please rate your \n'
                      'own language skills for these languages from 1 to 5.\n'
                      'English\t\t/5\n'
                      'German\t\t/5\n'
                      'French\t\t/5\n'
                      '5/5 means you are fluent; 1/5 means you don\'t speak the language\n\n'
                      'Instructions:\n--------------------\n\nIn this experiment, the naturalness and similarity of voices are tested.\n'
                      'In this folder, there are 16 sub folders (pair_1 - pair_16)\n'
                      'In each sub folder, there are two audio files (audio_1.wav and audio_2.wav) and a text file (score_audio_2.txt).\n'
                      'The second recording was digitally modified and therefore sounds distorted.\n'
                      'Listen to audio_1 and then to audio_2. Open the text file to rate the second audio file.\n\n'
                      'The rating consists of two aspects: naturalness and similarity.\n'
                      'Naturalness: How natural does the utterance sound? Does this sound like a real person?\n'
                      'Try to ignore the background noise.\n'
                      '4/4 = completely natural; 3/4 = rather natural;\n'
                      '2/4 = rather unnatural, 1/4 = completely unnatural\n\n'
                      'Similarity: Could they have been produced by the same person? Indicate how sure you are.\n'
                      'The sound quality should not be considered. Try to ignore the distortions and focus on the voice.\n'
                      '4/4 = same person, sure; 3/4 = same person, not sure;\n'
                      '2/4 = different person, not sure; 1/4 different person, sure\n\n'
                      'Remember to save the text file before you move on.\nWhen you are finished, please send the folders \n'
                      'back via e-mail.\n\n'
                      'If you have any questions, please contact me!'
                      'Thank you!\n\ne-mail: albin.manikkuttiyil@gmail.ch\n\n\"'
                      '>> ./perception_test_folders/test_group_{}/instructions.txt'.format(i))
            os.system('echo \"Danke für deine Teilnahme an dieser Studie!\n\n'
                      'Alle Antworten sind komplett anonym und keine persönlichen Angaben werden verwendet, gespeichert oder veröffentlicht.\n\n'
                      'Es können Aufnahmen auf Deutsch, Englisch und Französisch vorkommen. Bevor du beginnst, bitte bewerte\n'
                      'deine eigene Sprachkompetenz in diesen Sprachen von 1 bis 5.\n\n'
                      'Englisch\t\t/5\n'
                      'Deutsch\t\t\t/5\n'
                      'Französisch\t\t/5\n'
                      '5/5 = du spricht die Sprache fliessend; 1/5 = du sprichst die Sprache gar nicht.\n\n'
                      'Anleitung:\n--------------------\n\nIn diesem Experiment sollen die Natürlichkeit und Ähnlichkeit von Stimmen bewertet werden.\n'
                      'In diesem Ordner gibt es 16 Unterordner (pair_1 - pair_16)\n'
                      'In jedem dieser Unterordner gibt es zwei Sprachaufnahmen (audio_1.wav und audio_2.wav) und eine Textdatei (score_audio_2.txt).\n'
                      'Die zweite Aufnahme wurde digital bearbeitet und klingt deswegen verzerrt.\n'
                      'Hör dir zuerst audio_1 und dann audio_2 an. Öffne dann die Textdatei, um die zweite Aufnahme zu bewerten.\n\n'
                      'Die Bewertung besteht aus zwei Aspekten: Natürlichkeit und Ähnlichkeit.\n'
                      'Natürlichkeit: \n----------\nWie natürlich klingt der gesprochene Satz für dich? Klingt es wie ein echter Mensch?\n'
                      'Versuche bei deiner Bewertung, die Hintergrundgeräusche zu ignorieren.\n'
                      '4/4 = absolut natürlich; 3/4 = eher natürlich;\n'
                      '2/4 = eher unnatürlich, 1/4 = absolut unnatürlich\n\n'
                      'Ähnlichkeit: \n----------\nKönnten die Aufnahmen von derselben Person sein? Gib an, wie sicher du dir bist.\n'
                      'Die Qualität der Aufnahmen soll hier nicht berücksichtigt werden.\n'
                      'Versuche die Verzerrung zu ignorieren und konzentrier dich nur auf die Stimme.\n'
                      '4/4 = dieselbe Person, sicher; 3/4 = dieselbe Person, nicht sicher; \n'
                      '2/4 = nicht dieselbe Person, nicht sicher; 1/4 = nicht dieselbe Person, sicher\n\n'
                      'Vergiss nicht, die Textdatei zu speichern, bevor du fortfährst.\n'
                      'Wenn du fertig bist, sende den Ordner bitte per E-Mail zurück.\n\n'
                      'Solltest du irgendwelche Fragen haben oder Hilfe brauchen, kannst du mich jederzeit kontaktieren!\n'
                      'Vielen Dank!\n\n E-Mail: albin.manikkuttiyil@gmail.ch\n\n\"'
                      '>> ./perception_test_folders/test_group_{}/Anleitung.txt'.format(i))
            for j, pair in enumerate(pairs):
                os.system('mkdir ./perception_test_folders/test_group_{}/pair_{}'.format(i, j+1))
                os.system('cp {} ./perception_test_folders/test_group_{}/pair_{}/audio_1.wav'.format(pair[1], i, j+1))
                os.system('cp {} ./perception_test_folders/test_group_{}/pair_{}/audio_2.wav'.format(pair[0], i, j+1))
                os.system('echo \"Please rate the naturalness and similarity of the second audio file from 1 to 4.\n\n'
                          'Naturalness: \n----------\nHow natural does the utterance sound? Does this sound like a real person?\n'
                          '4/4 = completely natural; 3/4 = rather natural;\n'
                          '2/4 = rather unnatural, 1/4 = completely unnatural\n\n'
                          'Similarity: \n----------\nCould they be the same person? Indicate how sure you are.\n'
                          'The sound quality should not be considered. Try to ignore the distortions and focus on the voice.\n'
                          '4/4 = same person, very sure; 3/4 = same person, not sure;\n'
                          '2/4 = different person, not sure; 1/4 different person, very sure\n\n'
                          'Naturalness\t/4\nSimilarity\t/4\n\n\n\n\n[Code: {}__{} ]\" '
                          '>> ./perception_test_folders/test_group_{}/pair_{}/score_audio_2.txt'
                          .format(pair[0][-16:-4],pair[1][-16:-4], i, j+1))


if __name__ == "__main__":
    main()
