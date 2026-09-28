"""
this file is for Knn Handler for Face Rec Subsystem to handle
"""
import os
import pickle

import face_recognition
import math
import json
from sklearn import neighbors
from face_recognition.face_recognition_cli import image_files_in_folder
from util import const
from util import consoleLog

"""
Train method, Train dir ,
indx all the folders
TODO: Create class data structure for holdign model data
TODO: lower ram usage 
TODO: extract file io from methods 

"""

X = []
y = []


def loadTrainingData(train_dir, verbose=True):
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(
                image, model="cnn", number_of_times_to_upsample=0
            )

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print(
                        "Image {} not suitable for training: {}".format(
                            img_path,
                            "Didn't find a face"
                            if len(face_bounding_boxes) < 1
                            else "Found more than one face",
                        )
                    )
            else:
                # Add face encoding for current image to the training set
                X.append(
                    face_recognition.face_encodings(
                        image, known_face_locations=face_bounding_boxes, num_jitters=50
                    )[0]
                )
                y.append(class_dir)


# Trains Knn class model
def train(
    train_dir, model_save_path=None, n_neighbors=2, knn_algo="ball_tree", verbose=True
):

    loadTrainingData(train_dir, True)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(
        n_neighbors=n_neighbors, algorithm=knn_algo, weights="distance"
    )
    knn_clf.fit(X, y)

    saveTrainingData(model_save_path=model_save_path, knn_clf=knn_clf)


def saveTrainingData(model_save_path, knn_clf):

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, "wb") as f:
            pickle.dump(knn_clf, f)


def loadTrainedModel(knn_clf, model_path):

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, "rb") as f:
            knn_clf = pickle.load(f)
            return knn_clf

        """
        are_matches equles 
        """


# reads modle data and checks what face it is
def predict(Camera_frame, knn_clf=None, distance_threshold=0.4):

    if knn_clf is None is None:
        raise Exception(
            "Must supply knn classifier either thourgh knn_clf or model_path"
        )

    X_face_locations = face_recognition.face_locations(
        Camera_frame, model="cnn", number_of_times_to_upsample=1
    )

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(
        Camera_frame, known_face_locations=X_face_locations
    )

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)

    # checks to see if faces are maches
    are_matches = [
        closest_distances[0][i][0] <= distance_threshold
        for i in range(len(X_face_locations))
    ]

    # Predict classes and remove classifications that aren't within the threshold

    return face_predict_data(
        knn_clf,
        faces_encodings,
        X_face_locations,
        are_matches,
        closest_distances,
        distance_threshold,
    )


# Handles the data thats returned from the prediction
def face_predict_data(
    knn_clf,
    faces_encodings,
    X_face_locations,
    are_matches,
    closest_distances,
    distance_threshold,
):
    for i in range(len(X_face_locations)):
        face_distance_to_conf(closest_distances[0][i][0], distance_threshold)
    # Suppost to be like this but it wont work so reverting it back to og state
    return [
        (pred, loc) if rec else ("unknown", loc)
        for pred, loc, rec in zip(
            knn_clf.predict(faces_encodings), X_face_locations, are_matches
        )
    ]


# * allows me to display the prediction accuracy of the faces in the pipeline
def face_distance_to_conf(face_distance, face_match_threshold=0.56):
    face = face_distance

    if face > face_match_threshold:
        range = 1.0 - face_match_threshold
        linear_val = (1.0 - face) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face / (range * 2.0))

        const.facepredict = linear_val + (
            (1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2)
        )
