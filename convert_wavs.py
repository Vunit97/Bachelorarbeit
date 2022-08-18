
import os
import glob

# Getting all wav files and convert them with ffmpeg
for file in glob.glob("data/Actor_*/*.wav"):

    output = os.path.basename(file)
    output = output[:-4]

    new_output = output + "-converted"
    print(new_output)

