import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Flight ChatBot",
    page_icon="✈️",
    layout="centered",
)

# Load Google API Key
GOOGLE_API_KEY = os.getenv("AIzaSyDX_av4gVkS4boaEZkEET5tBfkwtoZdChE")  # Ensure API key is stored securely
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.0-flash')

# Static Airline, Seat Types, Price Estimates, and Travel Info
AIRLINE_INFO = """
Here are some airlines operating within Myanmar:

1️⃣ Myanmar Airways International (MAI) ✈️
2️⃣ Air Mandalay 🛫
3️⃣ Myanmar National Airlines (MNA) 🇲🇲✈️
4️⃣ Air KBZ 🌍🛩️
5️⃣ Air Thanlwin 🕊️✈️
6️⃣ Asian Wings Airways 🦅✈️

"""

SEAT_TYPE_INFO = """
Seat Types Available:
- **Economy Class**: Standard seating with basic amenities.
- **Business Class**: More space and premium services.
- **First Class**: Luxury seating with exclusive services.
"""

PRICE_ESTIMATES = """
Price Estimates (based on average fares):
- **Economy Class**: 200000 ks - 300,000 ks
- **Business Class**: 3500000 ks - 600,000 ks
- **First Class**: 6500000 ks - 800,000 ks
"""

BOOKING_PROCEDURE = """
How to Book a Flight:
1️⃣ Visit our SkyPalss Website.
2️⃣ Choose your flight based on destination and travel dates.
3️⃣ Select seat class (Economy, Business, First Class).
4️⃣ Enter passenger details and get e-receipt to pay in the counter.
5️⃣ Receive booking confirmation and your e-ticket.
"""

TRAVEL_RECOMMENDATIONS = """
**Travel Recommendations**:
- **Best Time to Visit**: Myanmar is great for visiting year-round, but the dry season (October - March) is ideal for sightseeing.
- **Top Destinations**: Bagan (temples), Inle Lake (nature), Yangon (city life), Ngapali Beach (relaxation).
"""

TRAVEL_ADVICE = """
**Travel Advice**:
- Always carry a photocopy of your passport and visa.
- Dress modestly when visiting religious sites.
- Ensure your travel insurance covers medical emergencies and trip cancellations.
"""

# Function to match user query to a specific prompt
def match_prompt(user_query):
    query = user_query.lower()

    if any(keyword in query for keyword in ["airlines", "airline","airlines in Myanmar"]):
        return AIRLINE_INFO
    elif any(keyword in query for keyword in ["seat", "available", "seat types"]):
        return SEAT_TYPE_INFO
    elif any(keyword in query for keyword in ["price", "cost", "fare"]):
        return PRICE_ESTIMATES
    elif any(keyword in query for keyword in ["book", "reservation", "ticket"]):
        return BOOKING_PROCEDURE
    elif any(keyword in query for keyword in ["recommendations", "top destinations"]):
        return TRAVEL_RECOMMENDATIONS
    elif any(keyword in query for keyword in ["advice", "travel tips", "travel advice"]):
        return TRAVEL_ADVICE
    else:
        return "Sorry, I can help with information on airlines, seat types, pricing, booking procedures, and travel tips."

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("✈️ Pyan Tan Lyk - ပျံသန်းလိုက် Chatbot")

# Show previous conversation
if st.session_state.chat_session.history:
    last_response = st.session_state.chat_session.history[-1]
    with st.chat_message("assistant"):
        st.markdown(last_response.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask me about airlines, seat types, pricing, booking, or travel tips...")

if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)

    # Match user query to the appropriate response
    full_prompt = f"{match_prompt(user_prompt)}\nUser's Question: {user_prompt}"

    # Send the prompt to Gemini AI
    gemini_response = st.session_state.chat_session.send_message(full_prompt)

    # Display chatbot's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
