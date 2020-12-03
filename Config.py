import argparse
import logging
import cv2
import random as rnd


##
## Basic defines
##

# Extract resultions
EXT_RES_150x300             = 1
EXT_RES_75x150              = 2

# TAG enumeration
TAG_VARROA                  = 300
TAG_POLLEN                  = 400
TAG_COOLING                 = 500
TAG_WESPE                   = 600


##
## Image processing
##

# Step though frames by keypress
# - True next frame processed on keypress
# - False process all frames consecutively
FRAME_AUTO_PROCESS                      = True

# Limit FPS to the given number:
LIMIT_FPS_TO                            = 20

# Length of buffered images for video file inputs
FRAME_SET_BUFFER_LENGTH_VIDEO           = 20

# Length of buffered images for camera inputs
FRAME_SET_BUFFER_LENGTH_CAMERA          = 3

# The input resolution of the camera to use
# must be larger or equal to the 'frame_config' below
# Set to (None, None, None) to use default
# Use 'v4l2-ctl --list-formats-ext' to list formats
CAMERA_INPUT_RESOLUTION                 = (1920, 1080, "MJPG")

# Wait the given time, if the buffer is full
FRAME_SET_FULL_PAUSE_TIME               = 0.1

# Save preview as video file
SAVE_AS_VIDEO                           = False

# The name of the video to store
SAVE_AS_VIDEO_PATH                      = "output.avi"

# Amount of different track colors to use
TRACK_COLOR_COUNT                       = 100

# Marks the detected bees in the preview
DRAW_DETECTED_ELLIPSES                  = True

# Marks the detected group of bees in the preview
DRAW_DETECTED_GROUPS                    = False

# Whether to draw any tracking related results
DRAW_TRACKING_RESULTS                   = True

# Draw rectangle over a bee in the preview when the bee is inside of a group
DRAW_GROUP_MARKER                       = False

# Mark last detected position with a small rectangle
DRAW_RECTANGLE_OVER_LAST_POSTION        = False

# Draw the bees movement trace
DRAW_TRACK_TRACE                        = True

# Draw the predicted position as circle
DRAW_TRACK_PREDICTION                   = False

# Draw estimated acceleration of the bee (Kalman)
DRAW_ACCELERATION                       = False

# Draw estimated velocity of the bee (Kalman)
DRAW_VELOCITY                           = False

# Draw the tracks id and name
DRAW_TRACK_ID                           = True

# Draw statistics of bees entering and leaving the hive
DRAW_IN_OUT_STATS                       = True


##
## Bee Tracking
##

# Whether to enable Bee tracking
ENABLE_TRACKING                         = True

# Whether to enable counting of bees entering and leaving the hive
ENABLE_COUNTING                         = True

# Number of waypoints to store for each track
MAX_BEE_TRACE_LENGTH                    = 10000


##
## Bee Detection
##

# During the bee detection cv2.conturs/fitEllipse will be used to find
# ellipses that could be bees. Below you find find some configuration
# values which are used to decide whether a bee or or a group of bees
# was detected.
# Before contours of bees can be extracted. The image is converted to gray
# -scale and then a binary threshold is applied, to separate the bees from
# their background.

# Binary threshold value used to separate bees from their background
BINARY_THRESHOLD_VALUE          = 150

# Binary threshold max-value used to separate bees from their background
BINARY_THRESHOLD_MAX            = 255

# A single bee has at least an ellipse area size of:
DETECT_ELLIPSE_AREA_MIN_SIZE    = 100

# A single bee has at maximum an ellipse area size of:
DETECT_ELLIPSE_AREA_MAX_SIZE    = 2500

# Multiple bees have at least an ellipse area size of:
DETECT_GROUP_AREA_MIN_SIZE      = 3000

# Multiple bees have at maximum an ellipse area size of:
DETECT_GROUP_AREA_MAX_SIZE      = 12500


##
## Neural Network
##

# Set to to True to enable the neural network
NN_ENABLE                   = True

# Neural Network model path
NN_MODEL_FOLDER             = "SavedModel"

## Image Extraction

# Enable image extraction of bee images from the video to perform neural network detections
ENABLE_IMAGE_EXTRACTION     = True

# Skip every N steps to avoid similar images beeing passed to the classification network
EXTRACT_FAME_STEP           = 10

# Only pass images to that have at least a sharpness value as given below.
# Higher values corresond to a higher image sharpness
EXTRACT_MIN_SHARPNESS       = 120

# Save the extracted image to evaluate the extraction process or to generate image to
# train the neural network?
SAVE_EXTRACTED_IMAGES       = True

# The folder to store the extracted images to
SAVE_EXTRACTED_IMAGES_PATH  = "ext4"

# Save images that passed the classification with positiv results?
SAVE_DETECTION_IMAGES       = True
SAVE_DETECTION_PATH         = "Detections"
SAVE_DETECTION_TYPES        = [TAG_VARROA]

# Resolution of the images passed to the classification network
# Can be either EXT_RES_75x150 or EXT_RES_150x300
NN_EXTRACT_RESOLUTION       = EXT_RES_75x150

# Classification result thresholds
CLASSIFICATION_THRESHOLDS = {
        'pollen':   (0.90, TAG_POLLEN),
        'varroa':   (0.95, TAG_VARROA),
        'wespe':    (0.80, TAG_WESPE),
        'cooling':  (0.90, TAG_COOLING)
    }


##
## LORAWAN
##

# The USB port where the RN2483A is connected to
RN2483A_USB_PORT                        = "/dev/ttyUSB0"

# Disable duty cycle tests. This can help during development
LORAWAN_DISABLE_DUTY_CYCLE_CHECKS       = False

# Device address as given in the things network (ABP)
LORAWAN_DEVADDR                         = "260135C6"

# Network session key as given in the things network (ABP)
LORAWAN_NET_SESSION_KEY                 = "BDBB97C4CC0A6DB3C27F78C45B028D8F"

# Application session key as given in the things network (ABP)
LORAWAN_APP_SESSION_KEY                 = "1E682B441E3F1FFCFCF1AF07DC8EB88E"

# LoRaWAN channel configuration
# (Channel ID, Frequency, Data-rate min, Data-rate max)
LORAWAN_CHANNEL_CONFIG                  = [
                         (0, 868100000, 0, 5),
                         (1, 868300000, 0, 5),
                         (2, 868500000, 0, 5),
                         (3, 867100000, 0, 5),
                         (4, 867300000, 0, 5),
                         (5, 867500000, 0, 5),
                         (6, 867700000, 0, 5),
                         (7, 867900000, 0, 5),
                     ]


##
## Internal
##

# Create random track colors
track_colors = []
for i in range(TRACK_COLOR_COUNT):
    track_colors.append((rnd.randint(100,255), rnd.randint(100,255), rnd.randint(100,255)))


frame_config = None
if NN_EXTRACT_RESOLUTION == EXT_RES_75x150:
    frame_config = (
                    (540, 960, cv2.IMREAD_UNCHANGED),
                    (180, 320,  cv2.IMREAD_UNCHANGED)
                )
elif NN_EXTRACT_RESOLUTION == EXT_RES_150x300:
    frame_config = (
                    (1080, 1920, cv2.IMREAD_UNCHANGED),
                    (540, 960, cv2.IMREAD_UNCHANGED),
                    (180, 320,  cv2.IMREAD_UNCHANGED)
                )
else:
    raise BaseException("Wrong image extraction setting")

#TODO: Does not belong to config
parser = argparse.ArgumentParser()
parser.add_argument("--noPreview", help="Run without producing any visual output", action="store_true")
parser.add_argument("--video", help="Do not run on camera, use provided video file instead")
args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - \t%(message)s')

