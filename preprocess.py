"""
This module converts speech recordings into mel-cepstral feature vectors
and saves them as numpy arrays to compute mel-cepstral distortion
"""

import os
import librosa
import pyworld
import pysptk
import numpy as np

alpha=0.65
fft_size=512
mcep_size=34
SAMPLING_RATE = 22050
FRAME_PERIOD = 5.0

# save root folder to save time and space writing directories
root = './voice-conversion/'


def save_mcg_np(path):
    # Check if recording ID list (and thereby numpy representations)
    # have already been created
    if os.path.isfile(os.path.join(path, 'rec_ids.txt')):
        print('Recording ID list already exists. Assuming numpy arrays'
              ' exist as well. Skipping this folder.')
        return
    files = os.listdir(path)
    # Create a list of file endings to save as text file for later use
    rec_id_list = []
    # Iterate through all .wav files and save as mcep feature arrays
    for filename in files:
        if filename.endswith('.wav'):
            rec_id_list.append(filename.rstrip('.wav')[-3:])
            wav_path = os.path.join(path,filename)
            loaded_wav, _ = librosa.load(wav_path, sr=SAMPLING_RATE)
            # Use WORLD vocoder for spectral envelope
            _, sp, _ = pyworld.wav2world(loaded_wav.astype(np.double),
                                         fs=SAMPLING_RATE,
                                         frame_period=FRAME_PERIOD,
                                         fft_size=fft_size)
            # Extract MCEP features
            mgc = pysptk.sptk.mcep(sp, order=mcep_size, alpha=alpha,
                                   maxiter=0, etype=1, eps=1.0E-8,
                                   min_det=0.0, itype=3)
            # Save as numpy
            np.save(os.path.join(path, filename.rstrip('.wav') + '.npy'),
                    mgc, allow_pickle=False)
    # Save list of file endings
    rec_id_file = open(os.path.join(path, 'rec_ids.txt'), 'w')
    for rec_id in sorted(rec_id_list):
        rec_id_file.write(rec_id+'\n')


def preprocess_wavs(directory):
    for folder in os.listdir(directory):
        try:
            print('Preprocessing: '+folder)
            save_mcg_np(os.path.join(directory, folder))
        except Exception as e:
            print(e)


def main():
    reference_audios = os.path.join(root, 'reference_samples')
    preprocess_wavs(reference_audios)
    synthesized_audios = os.path.join(root, 'synthesized_samples')
    preprocess_wavs(synthesized_audios)


if __name__ == '__main__':
    main()
