"""
This module converts all test samples files using pre-trained VC models
trained by CycleGAN
https://github.com/leimao/Voice_Converter_CycleGAN
"""

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def convert(model_name, source, target, direction):
    os.system('python3 ./Voice_Converter_CycleGAN/convert.py '
              '--model_dir ./Voice_Converter_CycleGAN/model/{} '
              '--model_name {}.ckpt '
              '--data_dir ./Voice_Converter_CycleGAN/siwis_speech_data/{}/test '
              '--conversion_direction {} '
              '--output_dir ./Voice_Converter_CycleGAN/synthesized_samples/{}_{}'
              .format(model_name, model_name, source, direction, source, target))


def main():
    models = os.listdir('voice-conversion/VC_models')
    for model_name in models:
        A, B = model_name.split('_')
        print(A, B)
        convert(model_name=model_name, source=A, target=B, direction="A2B")
        convert(model_name=model_name, source=B, target=A, direction="B2A")


if __name__ == "__main__":
    main()
