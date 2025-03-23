import streamlit as st
import numpy as np
import joblib

# Load model and scaler
model = joblib.load('calorie_model.pkl')
scaler = joblib.load('scaler.pkl')

# Set page configuration to use full screen width
st.set_page_config(
    page_title="Personal Fitness Tracker",
    page_icon="🔥",
    layout="wide",  # Use wide layout for full screen
    initial_sidebar_state="collapsed"
)

# Modern and visually appealing CSS with darker theme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Dark teal background for the entire app */
        .stApp {
            background: #1A2E35 !important;  /* Dark teal */
            padding: 2rem !important;
        }

        /* Full-width container */
        .main-container {
            max-width: 100% !important;
            margin: 0 auto !important;
            padding: 0 !important;
        }

        /* Darker card-like styling for inputs and results */
        .stSlider, .stRadio, .stNumberInput, .stMetric {
            background: rgba(0, 0, 0, 0.2) !important;  /* Dark semi-transparent */
            border-radius: 20px !important;
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
        }

        /* Ensure metric values are white */
        .stMetric > div > div > div {
            color: #ffffff !important;
        }

        /* Custom button styling */
        .custom-button {
            background: #40E0D0 !important;  /* Turquoise accent */
            color: #1A2E35 !important;
            border: none !important;
            padding: 20px 50px !important;  /* Larger padding for bigger button */
            border-radius: 30px !important;
            font-size: 1.5rem !important;  /* Larger font size */
            transition: all 0.3s ease !important;
            width: 100% !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            text-align: center !important;
            display: block !important;
            margin: 2rem auto !important;
        }

        .custom-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
            background: #30C0B0 !important;  /* Slightly darker turquoise */
        }

        /* Darker sliders */
        .stSlider > div > div > div > div {
            background: #40E0D0 !important;  /* Turquoise accent */
        }

        /* Darker result card */
        .result-card {
            background: #40E0D0 !important;  /* Turquoise accent */
            color: #1A2E35 !important;
            padding: 3rem !important;
            border-radius: 20px !important;
            text-align: center !important;
            margin: 2rem 0 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            animation: fadeIn 0.5s ease-in !important;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Darker metric cards */
        .stMetric {
            background: rgba(0, 0, 0, 0.2) !important;  /* Dark semi-transparent */
            border-radius: 20px !important;
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
        }

        /* Larger headers and text */
        h1 {
            font-size: 3rem !important;
            margin-bottom: 1rem !important;
            color: #ffffff !important;
        }

        h2 {
            font-size: 2rem !important;
            margin-bottom: 1rem !important;
            color: #ffffff !important;
        }

        h3 {
            font-size: 1.5rem !important;
            margin-bottom: 1rem !important;
            color: #ffffff !important;
        }

        p, label, .stMarkdown {
            font-size: 1.1rem !important;
            color: #ffffff !important;
        }

        /* Center align headers */
        h1, h2, h3 {
            text-align: center !important;
        }

        /* Darker footer */
        .footer {
            color: #ffffff !important;  /* White text */
            text-align: center !important;
            margin-top: 2rem !important;
            padding: 2rem !important;
            background: rgba(0, 0, 0, 0.2) !important;  /* Dark semi-transparent */
            border-radius: 20px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            font-size: 1.1rem !important;
        }

        /* Full-width columns */
        .stColumn {
            padding: 0 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1>🔥 Personal Fitness Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Smart Calorie Expenditure Analyzer</h3>", unsafe_allow_html=True)

    # Input columns
    col1, col2 = st.columns(2)

    with col1:
        gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
        age = st.slider("Age", 10, 100, 25)
        height = st.slider("Height (cm)", 100, 250, 170)

    with col2:
        weight = st.slider("Weight (kg)", 30, 150, 70)
        duration = st.slider("Duration (mins)", 1, 120, 30)
        heart_rate = st.slider("Heart Rate", 60, 200, 90)

    # Body temp input
    body_temp = st.slider("Body Temperature (°C)", 35.0, 42.0, 37.0)

    # Convert inputs
    gender_num = 0 if gender == "Female" else 1
    input_data = np.array([[gender_num, age, height, weight, duration, heart_rate, body_temp]])

    # Prediction logic
    if st.markdown("""
        <div class='custom-button' onclick='this.parentElement.querySelector("button").click()'>
            Calculate Calorie Burn
        </div>
    """, unsafe_allow_html=True):
        try:
            scaled_input = scaler.transform(input_data)
            predicted_calories = model.predict(scaled_input)
            st.markdown(f"""
                <div class='result-card'>
                    <h2 style='margin: 0; font-size: 2.5rem;'>🔥 {predicted_calories[0]:.2f} kcal</h2>
                    <p style='margin: 0; opacity: 0.9;'>Estimated Calories Burned</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

    # Features section
    st.markdown("## 📊 Activity Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Avg Heart Rate", value=f"{heart_rate} BPM")

    with col2:
        st.metric(label="Exercise Duration", value=f"{duration} mins")

    with col3:
        st.metric(label="Body Temp", value=f"{body_temp}°C")

    # Expanded "How It Works" section
    st.markdown("""
        <div style='margin-top: 2rem; text-align: center;'>
            <h3 style='font-size: 2rem; color: #40E0D0; margin-bottom: 1.5rem;'>💡 How It Works</h3>
            <p style='font-size: 1.1rem; color: #ffffff; margin-bottom: 2rem;'>
                Personal Fitness Tracker uses advanced machine learning algorithms to estimate your calorie burn based on your biometric data and workout stats. Here's how it works:
            </p>
            <div style='display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1.5rem;'>
                <div style='background: rgba(0, 0, 0, 0.2); border-radius: 20px; padding: 1.5rem; width: 22%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.1);'>
                    <h4 style='font-size: 1.5rem; color: #40E0D0; margin-bottom: 1rem;'>📥 Input Data</h4>
                    <p style='font-size: 1rem; color: #ffffff;'>
                        Provide your age, gender, height, weight, workout duration, heart rate, and body temperature.
                    </p>
                </div>
                <div style='background: rgba(0, 0, 0, 0.2); border-radius: 20px; padding: 1.5rem; width: 22%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.1);'>
                    <h4 style='font-size: 1.5rem; color: #40E0D0; margin-bottom: 1rem;'>⚙️ Data Processing</h4>
                    <p style='font-size: 1rem; color: #ffffff;'>
                        Your inputs are normalized using a scaler to ensure accurate predictions.
                    </p>
                </div>
                <div style='background: rgba(0, 0, 0, 0.2); border-radius: 20px; padding: 1.5rem; width: 22%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.1);'>
                    <h4 style='font-size: 1.5rem; color: #40E0D0; margin-bottom: 1rem;'>🤖 Machine Learning</h4>
                    <p style='font-size: 1rem; color: #ffffff;'>
                        A pre-trained model analyzes the data to estimate your calorie expenditure.
                    </p>
                </div>
                <div style='background: rgba(0, 0, 0, 0.2); border-radius: 20px; padding: 1.5rem; width: 22%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.1);'>
                    <h4 style='font-size: 1.5rem; color: #40E0D0; margin-bottom: 1rem;'>📊 Results</h4>
                    <p style='font-size: 1rem; color: #ffffff;'>
                        The calculated calories burned are displayed in an easy-to-read format.
                    </p>
                </div>
            </div>
            <p style='font-size: 1.1rem; color: #ffffff; margin-top: 2rem;'>
                Personal Fitness Tracker is trained on thousands of workout sessions, ensuring precise and reliable results for your fitness journey.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Close main container

# Footer
st.markdown("""
    <div class='footer'>
        <p>Developed with ❤️ by Shreya Ravi K</p>
    </div>
""", unsafe_allow_html=True)