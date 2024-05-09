import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

st.set_page_config(page_title="INPR", page_icon="🤖")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after{content : "Vinit, Nikunj, Parag, Murtaza";
                         display : block;
                         position: relative;
                         color: #fff4e9;
                         font: san serif;
                         padding: 10px;
                         top:3px;
                         visibility: visible;}
            header {visibility: hidden;}
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Intelligent Number Plate Recognition System")

# Function to capture video from webcam
def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            yield frame
        else:
            break

# Function to process image and perform OCR
def process_image(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detection
    lplate_data = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    found = lplate_data.detectMultiScale(image_gray)

    if len(found) != 0:
        w1 = 0
        h1 = 0
        for (x, y, w, h) in found:
            if w > w1 and h > h1:
                w1 = w
                x1 = x
                y1 = y
                h1 = h
            else:
                break
        cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
        cv2.rectangle(image, (x1, y1-40), (x1+w1, y1+h1-50), (0, 0, 0), -1)

        plate_image = image_gray[y1:(y1+h1), x1-10:(x1+w1)+10]

        # Extract text from plate image using EasyOCR
        result = reader.readtext(plate_image)
        text = ' '.join([box[1] for box in result])

        if len(found) != 0:
            w1 = 0
            h1 = 0
            for (x, y, w, h) in found:
                if w > w1 and h > h1:
                    w1 = w
                    x1 = x
                    y1 = y
                    h1 = h
                else:
                    break
            cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return image

# Sidebar options
option = st.sidebar.selectbox("Choose Option", ["Webcam", "Upload Photo", "Upload Video"])
if option == "Webcam":
    if st.sidebar.button("Enable Webcam"):
        for frame in capture_video():
            processed_frame = process_image(frame)
            st.image(processed_frame, channels="BGR", use_column_width=True)
elif option == "Upload Photo":
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        processed_image = process_image(image)
        st.image(processed_image, channels="BGR", use_column_width=True)
elif option == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Upload Video", type=['mp4', 'avi', 'mov'])
    if uploaded_file is not None:
        video_bytes = uploaded_file.read()
        st.video(video_bytes)