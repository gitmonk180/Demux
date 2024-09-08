import streamlit as st
import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Configure the API with the key from .env file
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to extract CSV data
def extract_csv(pathname: str) -> str:
    parts = ["start of csv data"]
    with open(pathname, "r", newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            parts.append(' '.join(row))
    return '\n'.join(parts)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

# Extract CSV data
csv_data = extract_csv(r"C:\Users\jaisaikrishna\Desktop\crop_compress.csv")

# Start chat with CSV data as initial history
chat = model.start_chat(history=[{
    "role": "user",
    "parts": csv_data
}])

# Streamlit UI
st.header("FarmAssist")

# Function to get response from Gemini API
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

lang=st.text_input("Language: ", key="input1")
lang=GoogleTranslator(source='auto', target='en').translate(lang)
lang_dict={"telugu":'te',"english":'en',"hindi":'hi'}


# Input box for user query
input_query = st.text_input("Input: ", key="input2")
submit = st.button("Ask")

# Process the response when the "Ask" button is clicked
if submit:
    if input_query:
        # Get the response from the Gemini model
        translated_text= GoogleTranslator(source='auto', target='en').translate(input_query)
        response = get_gemini_response(input_query)
        
        bot_response = ""
        for chunk in response:
            bot_response += chunk.text
    
        if "cannot" or "does not" in bot_response:
            response=model.generate_content(input_query)
            response_tr=GoogleTranslator(source='auto', target=lang_dict[lang]).translate(response.text)
            st.write(response_tr)  
        else:
            # Display the original bot response
            response_tr=GoogleTranslator(source='auto', target=lang_dict[lang]).translate(bot_response)
            st.write(response_tr)
        end_line="If there is anything else you would like to know, feel free to ask"
        st.write(GoogleTranslator(source='auto', target=lang_dict[lang]).translate(end_line))
    
    else:
        end_line="Please ask your queries"
        st.write(GoogleTranslator(source='auto', target=lang_dict[lang]).translate(end_line))
