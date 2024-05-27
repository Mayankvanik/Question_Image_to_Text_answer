import speech_recognition as sr
import openpyxl

# Create a new Excel file
wb = openpyxl.Workbook()
sheet = wb.active

# Set up the speech recognition engine
r = sr.Recognizer()

while True:
    # Get the user's input
    with sr.Microphone() as source:
        print("Speak a digit:")
        audio = r.listen(source)

    try:
        # Recognize the spoken digit
        digit = r.recognize_google(audio, language="en-US")
        print(f"You said: {digit}")

        # Add the digit to the notebook
        sheet.append([digit])
        wb.save("digits.xlsx")

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Try again!")