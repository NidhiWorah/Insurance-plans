
POC - Insurance Plans - v3 phone-camera-photos-added
==============================

This dataset was exported via roboflow.com on July 9, 2024 at 10:51 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 428 images.
Term-d8bv-term-tBOs-lVgW are annotated in YOLO v5 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 416x416 (Stretch)
* Auto-contrast via contrast stretching

The following augmentation was applied to create 5 versions of each source image:
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise, upside-down
* Random rotation of between -4 and +4 degrees
* Random shear of between -5° to +5° horizontally and -5° to +5° vertically
* Random brigthness adjustment of between -18 and +18 percent
* Random exposure adjustment of between -4 and +4 percent
* Salt and pepper noise was applied to 0.5 percent of pixels


