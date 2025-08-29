import face_recognition
import cv2
import os
from datetime import datetime
from pymongo import MongoClient

# MongoDB Connection Details (Replace <db_password> with your actual password)
MONGO_URI = "mongodb+srv://Gohan:39N4_zr5Crvzwir@cluster0.b0nev.mongodb.net/"
DATABASE_NAME = "attendance_db"  # You can choose your database name
COLLECTION_NAME = "attendance_records"  # You can choose your collection name

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    attendance_collection = db[COLLECTION_NAME]
    print("Connected to MongoDB Cloud Atlas successfully!")

    # Load known faces and names
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir("images"):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join("images", filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                for face_encoding in face_encodings:
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(filename.split(".")[0])
            else:
                print(f"Warning: No face found in {filename}")

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)

    # Initialize a set to keep track of who has been marked as present in the current session
    present_students = set()

    while True:
        # Read frame from video capture
        ret, frame = video_capture.read()

        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face found in the current frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face in the current frame matches any of the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the first matching known face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # If the recognized person hasn't been marked present yet in this session,
                # record their attendance in MongoDB.
                if name not in present_students and name != "Unknown":
                    now = datetime.now()
                    date_string = now.strftime("%Y-%m-%d")
                    time_string = now.strftime("%H:%M:%S")

                    attendance_data = {
                        "name": name,
                        "date": date_string,
                        "time": time_string,
                        "status": "Present"
                    }
                    try:
                        insert_result = attendance_collection.insert_one(attendance_data)
                        print(f"Attendance recorded for {name} in MongoDB at {time_string} on {date_string} (ID: {insert_result.inserted_id})")
                        present_students.add(name)
                    except Exception as e:
                        print(f"Error writing to MongoDB: {e}")

            # Draw rectangle around the face and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

except Exception as ex:
    print(f"Error during setup or main loop: {ex}")
finally:
    if 'client' in locals() and client:
        client.close()
        print("Disconnected from MongoDB.")