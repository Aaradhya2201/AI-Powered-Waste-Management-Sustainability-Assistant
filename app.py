import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import json
import cohere
import time
import base64

# App Config
st.set_page_config(page_title="♻️ AI Waste Assistant", page_icon="♻️", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = get_base64_of_bin_file("4vztk5m7p9651.webp")

st.markdown("""
    <h1 style='
        text-align: center;
        font-size: 3000px;
        font-weight: 2000;
        color: #E8F5E9;
        margin-top: 20px;
        line-height: 1.1;
    '>
    ♻️ AI-Powered Waste Management & Sustainability Assistant
    </h1>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Make uploader white */
    .stFileUploader {{
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 10px;
    }}
    /* Make text input white */
    .stTextInput > div > div > input {{
        background-color: #FFFFFF;
        color: #000000;
        padding: 0.75rem;
        font-size: 20px;
        border-radius: 8px;
    }}
    /* Increase font sizes */
    h1 {{
        color: #E8F5E9;
        font-size: 400px;
    }}
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
        color: #C8E6C9;
        font-size: 36px;
    }}
    .stMarkdown p, .stMarkdown li, .stMarkdown span {{
        color: #F1F8E9;
        font-size: 22px;
    }}
    .stButton>button {{
        background-color: #43A047;
        color: #FFFFFF;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-size: 22px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #2E7D32;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 22px;
        color: #E8F5E9;
        background-color: rgba(34, 139, 34, 0.7);
        padding: 10px 18px;
        border-radius: 8px;
        margin-right: 12px;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #43A047;
    }}
    .about-title {{
        color: #AED581;
        font-size: 28px;
    }}
    .team-member {{
        color: #F1F8E9;
        font-size: 18px;
    }}
    footer, .stCaption {{
        color: #C8E6C9;
        font-size: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title



st.markdown("---")

# Load model and class names
model = load_model('waste_classifier.h5')
with open('class_names.json') as f:
    class_names = json.load(f)

# Cohere API
co = cohere.Client("YOUR COHERE API KEY")  # replace your key

# Material Recommendations
recommendations = {
    "cardboard": {
        "reuse": [
            "📦 Use as protective packaging for fragile items.",
            "🗄️ Make DIY storage boxes or organizers.",
            "🌿 Use for garden mulch or compost liner."
        ],
        "recycle": [
            "♻️ Send to local recycling collection centers.",
            "🌱 Shred and mix into compost for carbon balance."
        ],
        "upcycle": [
            "🖼️ Create wall art, photo frames or eco-notebooks.",
            "🐶 Build pet houses or play structures."
        ]
    },
    "glass": {
        "reuse": [
            "🥫 Use glass jars for storage, plant vases, or candle holders.",
            "🍷 Repurpose wine bottles as lamps or decorative pieces."
        ],
        "recycle": [
            "♻️ Send to glass recycling collection points.",
            "🔥 Melt down for creating new glass products."
        ],
        "upcycle": [
            "🎨 Make mosaic art, photo frames, or garden edging.",
            "🔔 Craft wind chimes or lanterns from bottles."
        ]
    },
    "metal": {
        "reuse": [
            "🪴 Use metal cans as planters or desk organizers.",
            "🔧 Repurpose sheet metal for home repairs or DIY projects."
        ],
        "recycle": [
            "♻️ Sell to authorized scrap yards or recycling centers.",
            "🔩 Recycle aluminum, steel, and copper separately for efficiency."
        ],
        "upcycle": [
            "🎨 Create sculptures, wall art, or garden decorations.",
            "🛠️ Make functional items like hooks, handles, or tools."
        ]
    },
    "paper": {
        "reuse": [
            "📝 Use one-sided printed sheets for notes or drafts.",
            "🎁 Make eco-friendly gift wraps, origami, or paper crafts."
        ],
        "recycle": [
            "♻️ Shred and compost biodegradable paper waste.",
            "📚 Send clean paper to local paper recycling units."
        ],
        "upcycle": [
            "🎨 Create papier-mâché art, lampshades, or eco-journals.",
            "🌱 Make seed paper for plantable greeting cards or tags."
        ]
    },
    "plastic": {
        "reuse": [
            "🫙 Use containers for storage or seed starters.",
            "👜 Convert thick plastic bags into reusable totes."
        ],
        "recycle": [
            "♻️ Send clean, sorted plastics to local recycling facilities.",
            "🛒 Use drop-off bins for bottles, bags, and other specific plastics."
        ],
        "upcycle": [
            "🪴 Make hanging planters or vertical gardens from bottles.",
            "🎨 Create DIY home decor like lamp shades, wall art, or organizers."
        ]
    },
    "trash": {
        "reuse": [
            "🛠️ Salvage any reusable parts before disposal."
        ],
        "recycle": [
            "♻️ Check for recyclable components like metals or plastics."
        ],
        "upcycle": [
            "🎨 Turn non-toxic trash into creative art pieces, sculptures, or decor."
        ]
    }
}

# Chatbot Function
def ask_chatbot(prompt):
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=150
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error contacting chatbot: {str(e)}"

# Session State for Image Context
if 'last_class_label' not in st.session_state:
    st.session_state.last_class_label = None

# Tabs
tab1, tab2, tab3 = st.tabs(["📷 Waste Image Classifier", "💬 AI Chatbot", "📖 About"])

with tab1:
    st.subheader("📷 Upload and Classify Waste Image")
    uploaded_file = st.file_uploader("Upload a waste image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file).resize((224, 224))
        st.image(img, caption="Uploaded Image", use_column_width=False)

        st.markdown("---")

        if st.button("🚀 Classify & Suggest"):
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            prediction = model.predict(img_array)
            class_index = np.argmax(prediction)
            class_label = class_names[class_index]
            confidence = prediction[0][class_index]

            st.session_state.last_class_label = class_label

            st.success(f"**Prediction: {class_label.upper()} ({confidence*100:.2f}%)**")

            st.subheader("🌱 Suggestions:")
            st.write("**Reuse ideas:**")
            for idea in recommendations[class_label]['reuse']:
                st.write(f"• {idea}")

            st.write("**Recycle tips:**")
            for idea in recommendations[class_label]['recycle']:
                st.write(f"• {idea}")

            st.write("**Upcycle projects:**")
            for idea in recommendations[class_label]['upcycle']:
                st.write(f"• {idea}")


            st.markdown("""
            <div style='
                background-color: rgba(255, 255, 255, 0.12);
                padding: 20px;
                border-radius: 14px;
                margin-top: 20px;
                margin-bottom: 20px;
            '>
            <h4 style='color: #E8F5E9; font-size: 28px;'>🔍 Prediction Probabilities:</h4>
            """, unsafe_allow_html=True)
            prob_cols = st.columns(len(prediction[0]))
            for i in range(len(prediction[0])):
                prob_cols[i].markdown(f"""
        <div style='
            background-color: rgba(255, 255, 255, 0.15);
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        '>
            <div style='
                font-size: 22px;
                color: #E8F5E9;
                margin-bottom: 8px;
                font-weight: 600;
            '>{class_names[i]}</div>
            <div style='
                font-size: 26px;
                color: #FFFFFF;
                background-color: rgba(255, 255, 255, 0.2);
                padding: 8px 14px;
                border-radius: 8px;
                display: inline-block;
                font-weight: bold;
            '>{prediction[0][i]*100:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("💬 Ask the AI Sustainability Expert")
    user_question = st.text_input("Type your question here")

    if st.button("🤖 Get AI Advice"):
        if user_question.strip() != "":
            with st.spinner("Thinking..."):
                time.sleep(1)
                if st.session_state.last_class_label:
                    prompt = f"The detected waste material is {st.session_state.last_class_label}. User asks: {user_question}"
                else:
                    prompt = user_question
                answer = ask_chatbot(prompt)
            st.success("Here's what I found:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

with tab3:
    st.markdown("""
    <div style='
    background-color: rgba(129, 199, 132, 0.1);
    padding: 24px;
    border-radius: 14px;
    margin-top: 20px;
    margin-bottom: 20px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    '>

    <div style='
        font-size: 34px;
        font-weight: bold;
        color: #E8F5E9;
        margin-bottom: 18px;
        text-align: center;
    '>📖 About This Project</div>

    <p style='
        font-size: 22px;
        color: #F1F8E9;
        margin-bottom: 20px;
        text-align: justify;
    '>
        This AI-powered Waste Management and Sustainability Assistant was developed as a smart solution to classify waste images, suggest eco-friendly actions, and answer user queries on waste reuse, recycling, and upcycling.
    </p>

    <div style='
        font-size: 26px;
        font-weight: bold;
        color: #E8F5E9;
        margin-bottom: 12px;
        text-align: center;
    '>👥 Our Team:</div>

    <div style='
        font-size: 22px;
        color: #F1F8E9;
        text-align: center;
        line-height: 1.8;
    '>
        1️⃣ Aaradhya Bali<br>
        2️⃣ Gaurav Katre<br>
        3️⃣ Kaushik Tamgadge<br>
        4️⃣ Prajwal Wadichar<br>
        5️⃣ Ruchika Kale
    </div>

    </div>
    """, unsafe_allow_html=True)



st.markdown("""
    <hr style="margin-top: 50px; border: 1px solid #81C784;">
    <div style='
        text-align: center;
        padding: 12px;
        background-color: rgba(129, 199, 132, 0.1);
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    '>
        <p style='
            color: #C8E6C9;
            font-size: 17px;
            margin: 0;
        '>
            © 2025 | Designed by Students of SIT Nagpur | AI Waste Management Project ♻️
        </p>
    </div>
""", unsafe_allow_html=True)

