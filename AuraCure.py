import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
try:
    nltk.download("punkt_tab", quiet=True)
except:
    pass

if "chat" not in st.session_state:
    st.session_state.chat = []

if "emotion_mode" not in st.session_state:
    st.session_state.emotion_mode = False

if "emotion_stage" not in st.session_state:
    st.session_state.emotion_stage = "start"

if "emotion_type" not in st.session_state:
    st.session_state.emotion_type = None

# IMPORTANT: this key must exist early
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# -------------------- EMOTION DETECTION --------------------
def detect_emotion(text):
    t = text.lower()
    if not t.strip():
        return "neutral"

    words = set(word_tokenize(t))

    sad_words = {"sad", "hurt", "cry", "alone", "broken", "breakup", "heartbroken", "pain"}
    anxious_words = {"stress", "worried", "anxious", "panic", "fear", "tension"}

    if words & sad_words:
        return "sad"
    if words & anxious_words:
        return "anxious"
    return "neutral"


# -------------------- EMOTIONAL ENGINE --------------------
def emotional_engine(user_msg):
    stage = st.session_state.emotion_stage
    mood = st.session_state.emotion_type

    if stage == "start":
        emotion = detect_emotion(user_msg)
        st.session_state.emotion_type = emotion
        st.session_state.emotion_stage = "listen"

        if emotion == "sad":
            return (
                "I'm really sorry you're feeling sad 💙.\n"
                "You don’t deserve to feel this way. I'm here for you.\n"
                "Do you want to tell me what happened?"
            )

        if emotion == "anxious":
            return (
                "It sounds like you're feeling anxious 😟.\n"
                "Take a deep breath… you’re safe here.\n"
                "What’s making you feel this way?"
            )

        return "I'm here to listen. Tell me what you're feeling."

    if stage == "listen":
        st.session_state.emotion_stage = "deep"

        if mood == "sad":
            return (
                "Thank you for sharing that with me 💙.\n"
                "That must have been really painful.\n"
                "What part of this hurts you the most?"
            )

        if mood == "anxious":
            return (
                "I understand why you'd feel anxious.\n"
                "Your feelings are valid.\n"
                "What worries you the most right now?"
            )

        return "I can sense this is important to you. Tell me more."

    if stage == "deep":
        return (
            "I hear you 💙.\n"
            "Your emotions make complete sense.\n"
            "You're stronger than you think.\n"
            "I'm here with you — we can talk through this."
        )


# -------------------- HEALTH ENGINE --------------------
def health_engine(user_msg):
    text = user_msg.lower()

    # FEVER
    if "fever" in text or "temperature" in text or "bukhar" in text:
        return (
            "🌡 **Fever Care Tips:**\n"
            "- Drink warm water\n"
            "- Take rest\n"
            "- Avoid cold drinks\n"
            "- Paracetamol only if prescribed\n"
            "- If fever continues 2+ days → doctor"
        )

    # COLD/COUGH
    if any(w in text for w in ["cold", "cough", "sore throat", "khansi"]):
        return (
            "🤧 **Cold & Cough Relief:**\n"
            "- Steam inhalation\n"
            "- Ginger + honey mix\n"
            "- Warm water\n"
            "- Avoid cold items\n"
            "- Long-lasting → see doctor"
        )

    # HEADACHE
    if "headache" in text or "sir dard" in text:
        return (
            "🤕 **Headache Tips:**\n"
            "- Drink water\n"
            "- Reduce screen exposure\n"
            "- Sit in dark quiet room\n"
            "- Relax neck muscles"
        )

    # STOMACH PAIN
    if "stomach" in text or "pet dard" in text or "tummy ache" in text:
        return (
            "😣 **Stomach Pain Relief:**\n"
            "- Warm water\n"
            "- Avoid oily food\n"
            "- Eat light meals like khichdi\n"
            "- Rest properly"
        )

    # BODY PAIN
    if any(w in text for w in ["body pain", "whole body", "sharir dard", "body ache"]):
        return (
            "🧍 **Body Pain Care:**\n"
            "- Warm bath\n"
            "- Light stretching\n"
            "- Heat compress\n"
            "- Hydrate well"
        )

    # MUSCLE FATIGUE
    if "muscle" in text or "fatigue" in text or "thakaan" in text:
        return (
            "💪 **Muscle Fatigue Relief:**\n"
            "- Rest muscles\n"
            "- Light stretching\n"
            "- Warm compress\n"
            "- ORS or coconut water"
        )

    # SPRAIN / MOCH
    if "sprain" in text or "moch" in text or "ankle" in text or "joint" in text:
        return (
            "🦵 **Sprain (Moch) Care — RICE Method:**\n"
            "R - Rest\n"
            "I - Ice for 15 mins\n"
            "C - Compression bandage\n"
            "E - Elevation\n"
            "- Avoid massage for 48 hours"
        )

    # FRACTURE
    if "fracture" in text or "bone" in text:
        return (
            "🦴 **Fracture First Aid:**\n"
            "- Do NOT move injured area\n"
            "- Support using cloth/sling\n"
            "- Apply ice (wrapped)\n"
            "- Go to hospital immediately"
        )

    # NECK NERVE PAIN
    if "neck" in text or "nass" in text:
        return (
            "🧠 **Neck Nerve Pain Relief:**\n"
            "- Warm compress\n"
            "- Slow neck stretches\n"
            "- Avoid sudden movements\n"
            "- Use soft pillow"
        )

    # PERIOD CRAMPS
    if "period" in text or "cramp" in text or "mens" in text:
        return (
            "🩸 **Period Cramp Relief:**\n"
            "- Heating pad\n"
            "- Warm water / tea\n"
            "- Light walking\n"
            "- Avoid caffeine"
        )

    # MIGRAINE
    if "migraine" in text or "light sensitivity" in text:
        return (
            "⚡ **Migraine Relief:**\n"
            "- Sit in dark quiet room\n"
            "- Drink water\n"
            "- Cold compress"
        )

    # ACIDITY
    if "acidity" in text or "gas" in text or "indigestion" in text:
        return (
            "🔥 **Acidity Relief:**\n"
            "- Cold milk\n"
            "- Avoid spicy food\n"
            "- Small meals\n"
            "- Don't lie down immediately after eating"
        )

    # DIARRHEA
    if "diarrhea" in text or "loose motion" in text:
        return (
            "🚰 **Diarrhea Care:**\n"
            "- ORS frequently\n"
            "- Hydrate well\n"
            "- Eat bananas, curd\n"
            "- Avoid outside food"
        )

    # CONSTIPATION
    if "constipation" in text:
        return (
            "🌿 **Constipation Relief:**\n"
            "- Warm water every morning\n"
            "- High-fiber foods\n"
            "- Light exercise"
        )

    # SKIN RASH
    if "rash" in text or "itching" in text or "allergy" in text:
        return (
            "🌸 **Rash / Allergy Relief:**\n"
            "- Cold compress\n"
            "- Avoid scratching\n"
            "- Use mild soap"
        )

    # FOOD POISONING
    if "food poisoning" in text or "vomit" in text:
        return (
            "🤢 **Food Poisoning Care:**\n"
            "- ORS\n"
            "- Avoid solid food initially\n"
            "- Rest properly"
        )

    # BACK PAIN
    if "back pain" in text or "lower back" in text:
        return (
            "🔙 **Back Pain Tips:**\n"
            "- Warm compress\n"
            "- Gentle stretching\n"
            "- Maintain posture"
        )

    # SINUS
    if "sinus" in text or "blocked nose" in text:
        return (
            "🌬 **Sinus Relief:**\n"
            "- Steam inhalation\n"
            "- Warm liquids"
        )

    # EYE IRRITATION
    if "eye pain" in text or "itchy eye" in text:
        return (
            "👁 **Eye Irritation Care:**\n"
            "- Wash eyes\n"
            "- Cold compress\n"
            "- Reduce screen time"
        )

    # DEHYDRATION
    if "dehydration" in text or "dry mouth" in text or "pyaas" in text:
        return (
            "💧 **Dehydration Relief:**\n"
            "- ORS / electrolyte drink\n"
            "- Coconut water"
        )

    return None


# -------------------- FINAL RESPONSE HANDLER --------------------
def generate_response(user_msg):
    emotion = detect_emotion(user_msg)

    if emotion in ["sad", "anxious"] or st.session_state.emotion_mode:
        st.session_state.emotion_mode = True
        return emotional_engine(user_msg)

    remedy = health_engine(user_msg)
    if remedy:
        return remedy

    return (
        "I understand. Tell me a little more so I can help you better 😊.\n"
        "If it's emotional, I'm here for you. If it's health-related, I'll guide you safely."
    )


# -------------------- STREAMLIT UI --------------------
st.title("AuraCure — Emotional & Healthcare Support Chatbot")

# Show previous chat
for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AuraCure:** {msg}")

# Input field
st.text_input("Type your message here…", key="user_input")

# SEND BUTTON
if st.button("Send"):
    msg = st.session_state.get("user_input", "").strip()

    if msg:
        # Add user message
        st.session_state.chat.append(("user", msg))

        # Generate reply
        reply = generate_response(msg)
        st.session_state.chat.append(("bot", reply))

        # SAFE CLEAR input field
        st.session_state.pop("user_input", None)

        st.experimental_rerun()

# CLEAR BUTTON
if st.button("Clear Chat"):
    st.session_state.chat = []
    st.session_state.emotion_mode = False
    st.session_state.emotion_stage = "start"
    st.session_state.emotion_type = None
    st.session_state.pop("user_input", None)
    st.experimental_rerun()
