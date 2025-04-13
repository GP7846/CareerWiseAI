
import streamlit as st
import google.generativeai as genai
import re


API_KEY = "AIzaSyCjz6s_tsalNk9GFKzY9a5mmkPSlln0eUM"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def clean_input(text):
    return re.sub(r'[^\w\s]', '', text).strip() if text else ""


def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor mentoring a B.Tech student in India. Provide highly personalized, realistic, and actionable career advice based on:
- Interests: {interests}
- Skills: {skills}
- Education: {education}
- Career Goals: {goals}

**Requirements**:
- Suggest 4 career paths relevant to the user’s profile, each including:
  1. **Job Title and Description**: Describe the role and its impact in India’s job market.
  2. **Required Skills**: List technical and soft skills, with tools or certifications.
  3. **Steps to Achieve**: Provide a 3-5 step roadmap tailored to a B.Tech student (e.g., projects, internships, courses).
  4. **Market Insights**: Include average salary (INR), demand, and remote work options.
  5. **Challenges and Solutions**: Address obstacles (e.g., competition) with practical solutions.
- Provide general advice on:
  - Building a resume (e.g., GitHub, LinkedIn).
  - Networking (e.g., meetups, online platforms).
  - Skill development (e.g., free/paid resources like Coursera, YouTube).
  - Interview tips for Indian companies.
- Use a motivational tone to inspire confidence.
- Format with clear headings (##) and bullet points for readability.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to fetch advice ({str(e)}). Check your internet or API key."


st.set_page_config(page_title="Career Guide Chatbot", page_icon="🚀", layout="centered")
st.markdown("""
    <style>
    .main {background-color: #e6f0fa; padding: 20px; border-radius: 12px;}
    .stButton>button {background-color: #0055b3; color: white; border-radius: 10px; padding: 10px; font-weight: bold;}
    .stButton>button:hover {background-color: #003d82;}
    .stTextInput>div>input {border: 2px solid #0055b3; border-radius: 10px; padding: 8px;}
    h1 {color: #001f5c; text-align: center; font-size: 36px;}
    .stSpinner {text-align: center;}
    .response-box {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Career Guide Chatbot")
st.markdown("**Your mentor for a thriving tech career!** Enter details to get personalized advice.")


with st.sidebar:
    st.header("Career Tips")
    st.markdown("""
    - **Be Specific**: Mention exact skills (e.g., Python, Java).
    - **Explore Options**: Try different interests to discover new paths.
    - **Act Fast**: Start projects or internships early in B.Tech!
    """)
    st.image("https://img.icons8.com/color/96/000000/career.png", caption="Build Your Future")


if 'history' not in st.session_state:
    st.session_state.history = []


with st.form("career_form"):
    interests = st.text_input("Interests (e.g., AI, web development)", placeholder="e.g., machine learning")
    skills = st.text_input("Skills (e.g., Python, teamwork)", placeholder="e.g., coding")
    education = st.text_input("Education (e.g., B.Tech CS)", placeholder="e.g., 2nd year B.Tech")
    goals = st.text_input("Goals (e.g., software engineer)", placeholder="e.g., work at Google")
    submit = st.form_submit_button("Get Career Advice")


if submit:
    if not all([interests, skills, education, goals]):
        st.error("Please fill all fields to continue.")
    else:
        interests = clean_input(interests)
        skills = clean_input(skills)
        education = clean_input(education)
        goals = clean_input(goals)

       
        st.subheader("Your Profile")
        st.markdown(f"- **Interests**: {interests}")
        st.markdown(f"- **Skills**: {skills}")
        st.markdown(f"- **Education**: {education}")
        st.markdown(f"- **Goals**: {goals}")

        
        with st.spinner("Crafting your career path..."):
            advice = get_career_advice(interests, skills, education, goals)
            st.markdown("<div class='response-box'>", unsafe_allow_html=True)
            st.markdown(advice, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        
        st.session_state.history.append({
            "inputs": {"interests": interests, "skills": skills, "education": education, "goals": goals},
            "advice": advice
        })


if st.session_state.history:
    st.subheader("Your Career Plans")
    for i, entry in enumerate(st.session_state.history):
        with st.expander(f"Plan {i+1}"):
            st.markdown(f"- **Interests**: {entry['inputs']['interests']}")
            st.markdown(f"- **Skills**: {entry['inputs']['skills']}")
            st.markdown(f"- **Education**: {entry['inputs']['education']}")
            st.markdown(f"- **Goals**: {entry['inputs']['goals']}")
            st.markdown(entry['advice'], unsafe_allow_html=True)