"""
Created on 2021/08/12

@author: Ronny Stricker
Example for downloading segmentation masks of GAPs 10m dataset.
"""

from gaps_dataset import gaps
import zipfile
import os

# change these parameters:
destination_directory = '/your/download/destination/directory'
login = 'yourlogin'

# download images and segmentation masks
gaps.download(login=login,
              output_dir=destination_directory,
              version='10m',
              patchsize='segmentation',
              issue='ASFaLT',
              debug_outputs=True)

# unzip images and masks
basedir = os.path.join(destination_directory, '10m', 'segmentation')

for f in ['images', 'val_p']:
    zip_filename = os.path.join(basedir, f + '.zip')
    zip_ref = zipfile.ZipFile(zip_filename, 'r')
    zip_ref.extractall(os.path.join(basedir, f))
    zip_ref.close()

# Mask images are stored as grey value images.
# Coding of the grey values:
#    0 = VOID
#    1 = Inlaid patch
#    2 = Applied patch
#    3 = Sealed crack
#    4 = Crack
#    5 = Open joint
#    6 = Pothole
#    7 = Raveling
#    8 = Scratch
#    9 = Bleeding
#   10 = Road marking
#   11 = Surface water drain
#   12 = Manhole
#   13 = Expansion Joint
#   14 = Curb
#   15 = Cobblestone
#   16 = Drill hole
#   17 = Object mobile
#   18 = Object fixed
#   19 = Joint
#   20 = Road verge
#   21 = Vegetation
#   22 = Induction loop
#   23 = Normal
