from flask import Flask, request
import os
import dlib
import csv
import numpy as np
import logging
import cv2

app = Flask(__name__)

#  Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

#  Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

#  Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

#  Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

#  Return 128D features for single image
def return_128d_features(img_rd):
    faces = detector(img_rd, 1)

    logging.info("%-40s %-20s", " Image with faces detected:", "Received Image")

    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor

# Save image and extract features
@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files["image"]
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Save the image
    filename = file.filename
    save_path = os.path.join(path_images_from_camera, filename)
    cv2.imwrite(save_path, img)
    
    # Extract features from the image
    features_128d = return_128d_features(img)
    
    # Save features to CSV
    with open("data/features_all.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([filename.split(".jpg")[0]] + list(features_128d))
    
    response = [filename.split(".jpg")[0]] + list(features_128d)
    
    print(f'###################{response}')
    print(f'###################{[filename.split(".jpg")[0]]}')
    
    return str(response)
    # return 
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run()