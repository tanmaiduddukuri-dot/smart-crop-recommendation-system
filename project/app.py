

import random
import time

import pandas as pd
import streamlit as st

st.set_page_config(page_title="CropWise — Smart Crop Recommendation", page_icon="🌱", layout="wide")

# ==============================================================================
# 1. PALETTE — same earthy green + brown palette as the website version
# ==============================================================================
PALETTE = {
    "forest": "#0F3D2E",
    "forest_light": "#1F6B45",
    "navy": "#2A1E13",   # deep soil brown-black, used for dark cards
    "sage": "#6FA287",
    "canvas": "#F5F7F3",
    "white": "#FFFFFF",
    "gold": "#C9922E",
    "clay": "#A9713F",
    "bark": "#4A3423",
    "sand": "#EEE3D0",
    "ink": "#14231C",
    "muted": "#5B6B63",
    "line": "#E1E8E1",
}

# ==============================================================================
# 2. FIELD RULES & REFERENCE DATA
# ==============================================================================
FIELD_LABELS = {
    "nitrogen": "Nitrogen", "phosphorus": "Phosphorus", "potassium": "Potassium",
    "temperature": "Temperature", "humidity": "Humidity", "ph": "Soil pH", "rainfall": "Rainfall",
}

CROP_INFO = {
    "rice": {"emoji": "🌾", "name": "Rice"},
    "maize": {"emoji": "🌽", "name": "Maize"},
    "chickpea": {"emoji": "🫘", "name": "Chickpea"},
    "cotton": {"emoji": "🌱", "name": "Cotton"},
    "coffee": {"emoji": "☕", "name": "Coffee"},
    "banana": {"emoji": "🍌", "name": "Banana"},
    "mango": {"emoji": "🥭", "name": "Mango"},
    "watermelon": {"emoji": "🍉", "name": "Watermelon"},
    "lentil": {"emoji": "🌿", "name": "Lentil"},
    "jute": {"emoji": "🧵", "name": "Jute"},
}

# Left as None until a trained model is connected — see render_performance().
DEMO_METRICS = {"accuracy": 95, "precision": 94, "recall": 93, "f1": 93}


# ==============================================================================
# 3. PREDICTION — mock now, structured to be swapped for a real model later
# ==============================================================================
def mock_prediction(data: dict) -> dict:
    """
    Lightweight, rule-of-thumb heuristic used ONLY to make the demo feel
    responsive to the inputs. This is NOT the real model — the actual
    Multinomial Logistic Regression prediction should come from a trained
    model once one is ready (see get_prediction below).
    """
    n, temp, hum, ph, rain = data["nitrogen"], data["temperature"], data["humidity"], data["ph"], data["rainfall"]

    if rain > 180 and hum > 70 and temp > 20:
        candidates = ["rice", "jute", "coffee"]
    elif n > 80 and 18 <= temp <= 30:
        candidates = ["maize", "cotton", "banana"]
    elif ph < 6 and rain < 120:
        candidates = ["chickpea", "lentil", "watermelon"]
    elif temp > 28 and hum < 60:
        candidates = ["cotton", "mango", "watermelon"]
    else:
        candidates = ["maize", "rice", "lentil"]

    top_crop = candidates[0]
    others = [c for c in CROP_INFO if c != top_crop]
    random.shuffle(others)

    top_confidence = random.randint(62, 84)
    remaining = 100 - top_confidence

    probabilities = {top_crop: top_confidence}
    support = others[:3]
    for i, crop in enumerate(support):
        is_last = i == len(support) - 1
        share = remaining if is_last else round(remaining * (0.5 - i * 0.15))
        probabilities[crop] = max(1, share)
        remaining -= probabilities[crop]
    if remaining > 0:
        probabilities["others"] = remaining

    return {"crop": top_crop, "confidence": top_confidence, "probabilities": probabilities}


def get_prediction(form_data: dict) -> dict:
    """
    Returns a prediction for the given form data.

    TEMPORARY DEMO — calls mock_prediction() below. Once a trained model
    exists, replace the body with something like:

        model = joblib.load("model/crop_model.pkl")
        scaler = joblib.load("model/scaler.pkl")
        X = scaler.transform([[form_data[k] for k in FIELD_LABELS]])
        pred = model.predict(X)[0]
        proba = dict(zip(model.classes_, (model.predict_proba(X)[0] * 100).round(1)))
        return {"crop": pred, "confidence": round(max(proba.values())), "probabilities": proba}

    Keep the same return shape — {"crop": ..., "confidence": ..., "probabilities": {...}} —
    and every render function below keeps working unchanged.
    """
    time.sleep(1.1)  # stands in for real inference latency, drives the spinner below
    return mock_prediction(form_data)


# ==============================================================================
# 4. NAVIGATION
# ==============================================================================
PAGES = ["Home", "Recommend", "How It Works", "Performance", "About"]
ICONS = {"Home": "🏠", "Recommend": "🌾", "How It Works": "🔬", "Performance": "📊", "About": "ℹ️"}

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "result" not in st.session_state:
    st.session_state.result = None
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None


def go_to(page: str):
    st.session_state.page = page


def render_navbar():
    st.markdown(
        f'<div style="font-family:serif;font-weight:700;font-size:1.3rem;color:{PALETTE["forest"]};margin-bottom:10px;">'
        f"🌱 CropWise</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(PAGES))
    for col, page in zip(cols, PAGES):
        with col:
            if st.button(f"{ICONS[page]}  {page}", key=f"nav_{page}", use_container_width=True,
                         type="primary" if st.session_state.page == page else "secondary"):
                go_to(page)
                st.rerun()


# ==============================================================================
# 5. PAGE: HOME
# ==============================================================================
def render_home():
    st.markdown(f"""
    <div style="background:linear-gradient(160deg, {PALETTE['forest']} 0%, {PALETTE['navy']} 100%);
                border-radius:24px; padding:44px 40px; color:white; margin-bottom:26px;">
      <p style="color:{PALETTE['sage']}; font-weight:600; font-size:0.82rem; letter-spacing:0.02em; margin-bottom:12px;">
        MULTINOMIAL LOGISTIC REGRESSION
      </p>
      <div style="font-family:serif; font-size:2.3rem; font-weight:700; line-height:1.2; margin-bottom:14px;">
        Smart Crop Recommendation<br>Powered by Data
      </div>
      <p style="max-width:48ch; color:rgba(255,255,255,0.82); font-size:1.05rem;">
        Make smarter agricultural decisions using soil and environmental conditions.
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌱 Get Recommendation", use_container_width=True, type="primary"):
            go_to("Recommend")
            st.rerun()
    with c2:
        if st.button("Explore How It Works", use_container_width=True):
            go_to("How It Works")
            st.rerun()

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Input Features", "7")
    m2.metric("Classification", "Multi-Class")
    m3.metric("Recommendation", "ML Powered")
    m4.metric("Decisions", "Data-Driven")


# ==============================================================================
# 6. PAGE: RECOMMEND
# ==============================================================================
def render_result(result: dict, inputs: dict):
    crop = result["crop"]
    info = CROP_INFO.get(crop, {"emoji": "🌱", "name": crop.title()})
    confidence = result["confidence"]
    probabilities = result["probabilities"]

    st.write("")
    col_result, col_side = st.columns([1, 1.3])

    with col_result:
        st.markdown(f"""
        <div style="background:linear-gradient(160deg, {PALETTE['forest']} 0%, {PALETTE['navy']} 100%);
                    border-radius:20px; padding:30px; text-align:center; color:white;">
          <p style="color:rgba(255,255,255,0.65); font-size:0.78rem; font-weight:700; letter-spacing:0.02em; margin-bottom:14px;">
            YOUR RECOMMENDATION
          </p>
          <div style="font-size:2.4rem;">{info['emoji']}</div>
          <div style="font-family:serif; font-size:1.5rem; font-weight:700;">{info['name'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Confidence", f"{confidence}%")
        st.caption(f"Based on the conditions you provided, {info['name']} has the highest predicted probability.")
        if st.button("↺ Try Another", use_container_width=True):
            st.session_state.result = None
            st.rerun()

    with col_side:
        st.markdown("**Prediction Probabilities**")
        for crop_key, pct in sorted(probabilities.items(), key=lambda kv: -kv[1]):
            label = "Others" if crop_key == "others" else CROP_INFO.get(crop_key, {}).get("name", crop_key.title())
            bar_color = PALETTE["gold"] if crop_key == crop else PALETTE["sage"]
            st.markdown(f"""
            <div style="margin-bottom:10px;">
              <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                <span style="font-weight:600;">{label}</span><span>{pct}%</span>
              </div>
              <div style="background:{PALETTE['line']}; border-radius:999px; height:8px;">
                <div style="width:{pct}%; background:{bar_color}; height:100%; border-radius:999px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Your Conditions**")
        summary = pd.DataFrame({
            "Parameter": ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "Soil pH", "Rainfall"],
            "Value": [
                f"{inputs['nitrogen']} kg/ha", f"{inputs['phosphorus']} kg/ha", f"{inputs['potassium']} kg/ha",
                f"{inputs['temperature']} °C", f"{inputs['humidity']} %", f"{inputs['ph']}", f"{inputs['rainfall']} mm",
            ],
        }).set_index("Parameter")
        st.table(summary)


def render_recommend():
    st.subheader("Find the Right Crop for Your Conditions")
    st.caption("Enter your soil and environmental conditions to get a data-driven crop recommendation.")

    with st.container(border=True):
        with st.form("crop_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Soil Nutrients**")
                nitrogen = st.number_input("Nitrogen (N) · kg/ha", min_value=0, max_value=150, value=90,
                                            help="Nutrient availability in soil. Supports leaf and stem growth.")
                phosphorus = st.number_input("Phosphorus (P) · kg/ha", min_value=0, max_value=150, value=42,
                                              help="Supports root and flower development.")
                potassium = st.number_input("Potassium (K) · kg/ha", min_value=0, max_value=210, value=43,
                                             help="Improves plant resilience and helps regulate water uptake.")
            with c2:
                st.markdown("**Climate**")
                temperature = st.number_input("Temperature · °C", min_value=-5.0, max_value=55.0, value=25.0, step=0.5,
                                               help="Average environmental temperature for the growing period.")
                humidity = st.number_input("Humidity · %", min_value=0.0, max_value=100.0, value=80.0, step=1.0,
                                            help="Relative atmospheric moisture level.")
            with c3:
                st.markdown("**Water & Soil**")
                ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1,
                                      help="Acidity or alkalinity of the soil, on a 0–14 scale.")
                rainfall = st.number_input("Rainfall · mm", min_value=0.0, max_value=500.0, value=200.0, step=5.0,
                                            help="Total precipitation available during the growing period.")

            submitted = st.form_submit_button("🌱 Recommend Crop", use_container_width=True, type="primary")

    if submitted:
        form_data = {
            "nitrogen": nitrogen, "phosphorus": phosphorus, "potassium": potassium,
            "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rainfall,
        }
        with st.spinner("Analyzing soil and environmental conditions…"):
            st.session_state.result = get_prediction(form_data)
            st.session_state.last_inputs = form_data

    if st.session_state.result:
        render_result(st.session_state.result, st.session_state.last_inputs)


# ==============================================================================
# 7. PAGE: HOW IT WORKS
# ==============================================================================
def render_how_it_works():
    st.subheader("How CropWise Works")
    st.caption("From raw field readings to a single recommended crop, in five steps.")

    steps = [
        ("01", "Enter Conditions", "User provides soil and environmental data."),
        ("02", "Process Features", "The values are prepared for the machine-learning model."),
        ("03", "Analyze with ML", "Multinomial Logistic Regression calculates probabilities for different crops."),
        ("04", "Compare Probabilities", "The system identifies the crop with the highest probability."),
        ("05", "Get Recommendation", "The highest-probability crop is displayed."),
    ]
    cols = st.columns(5)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div>
              <div style="width:30px;height:30px;border-radius:50%;background:{PALETTE['forest']};color:white;
                          display:flex;align-items:center;justify-content:center;font-weight:700;
                          font-size:0.8rem;margin-bottom:10px;">{num}</div>
              <div style="font-weight:700;margin-bottom:4px;">{title}</div>
              <div style="font-size:0.85rem;color:{PALETTE['muted']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown("#### Behind the Prediction")
        st.write("For each crop _k_, the model calculates a score from the input features:")
        st.latex(r"Z_k = b_k + \sum_i w_{ik}\, x_i")
        st.write("The scores are converted into probabilities with the Softmax function:")
        st.latex(r"P(y=k \mid X) = \frac{e^{Z_k}}{\sum_j e^{Z_j}}")
        st.write("The crop with the highest probability is returned:")
        st.latex(r"\hat{y} = \arg\max_k P(y=k \mid X)")
        st.caption("The model learns the weights from agricultural training data and recommends the crop "
                   "with the highest predicted probability.")

    st.write("")
    st.markdown("#### What Does the Model Analyze?")
    features = [
        ("N", "Nitrogen", "Nutrient availability in soil."),
        ("P", "Phosphorus", "Supports root and plant development."),
        ("K", "Potassium", "Important for plant growth and resilience."),
        ("°C", "Temperature", "Environmental temperature conditions."),
        ("%", "Humidity", "Atmospheric moisture level."),
        ("pH", "Soil pH", "Soil acidity/alkalinity."),
        ("mm", "Rainfall", "Available precipitation."),
    ]
    cols = st.columns(4)
    for i, (icon, name, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:{PALETTE['canvas']};border:1px solid {PALETTE['line']};border-radius:14px;
                        padding:16px;margin-bottom:14px;">
              <div style="display:inline-flex;align-items:center;justify-content:center;min-width:32px;height:32px;
                          padding:0 8px;border-radius:8px;background:rgba(15,61,46,0.1);color:{PALETTE['forest']};
                          font-weight:700;font-size:0.82rem;margin-bottom:10px;">{icon}</div>
              <div style="font-weight:700;margin-bottom:4px;">{name}</div>
              <div style="font-size:0.83rem;color:{PALETTE['muted']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### How Each Feature Influences Crop Growth")
    st.caption("What each measurement actually does inside a growing plant, beyond just being a model input.")
    influence = [
        ("Nitrogen", "High", "Fuels leafy, vegetative growth by supporting chlorophyll production. Too little "
                              "stunts growth; too much can delay flowering and fruiting."),
        ("Phosphorus", "High", "Establishes strong root systems and supports flowering and seed formation, "
                                "especially early in a crop's life cycle."),
        ("Potassium", "Medium", "Helps regulate water movement within the plant, strengthens stems, and "
                                 "improves resistance to disease and drought."),
        ("Temperature", "High", "Sets the pace for germination, photosynthesis, and enzyme activity. Each crop "
                                 "has an optimal range outside of which growth slows."),
        ("Humidity", "Medium", "Influences transpiration and water loss. High humidity can raise fungal disease "
                                "risk; low humidity increases water stress."),
        ("Soil pH", "Medium", "Determines how easily roots can access nutrients already in the soil. Most "
                               "nutrients are most available in a near-neutral range."),
        ("Rainfall", "High", "Supplies the water needed to transport nutrients and support cell growth. Too "
                              "little causes drought stress; too much can cause waterlogging."),
    ]
    level_fill = {"High": 1.0, "Medium": 0.66}
    cols = st.columns(2)
    for i, (name, level, desc) in enumerate(influence):
        accent = PALETTE["sage"] if i % 2 == 0 else PALETTE["clay"]
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:white;border:1px solid {PALETTE['line']};border-left:3px solid {accent};
                        border-radius:14px;padding:18px;margin-bottom:14px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <strong>{name}</strong>
                <span style="font-size:0.7rem;font-weight:700;background:rgba(169,113,63,0.14);color:{PALETTE['bark']};
                             padding:2px 9px;border-radius:999px;white-space:nowrap;">{level} influence</span>
              </div>
              <div style="font-size:0.85rem;color:{PALETTE['muted']};margin-bottom:10px;">{desc}</div>
              <div style="background:{PALETTE['line']};border-radius:999px;height:6px;">
                <div style="width:{level_fill[level]*100:.0f}%;background:linear-gradient(90deg,{PALETTE['sage']},{PALETTE['forest']});
                            height:100%;border-radius:999px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    st.caption("These reflect general agronomic patterns, not this specific model's learned weights — a "
               "trained classifier may end up relying on some of these features more than others, depending "
               "on the dataset.")

    st.write("")
    st.markdown("#### ML Concepts & Course Outcomes")
    st.caption("How this project's design connects back to the course's learning outcomes.")
    concepts = [
        ("CO1 · Analyze", "End-to-End ML Lifecycle",
         "CropWise mirrors the full pipeline traced by this outcome: raw soil and weather readings become "
         "model-ready features, pass through a trained classifier, and return as a prediction back to this app."),
        ("CO2 · Apply", "Multinomial Logistic Regression",
         "The recommendation engine is built specifically around multinomial logistic regression — extending "
         "logistic regression's linear scoring so the model can choose among many possible crops at once, not "
         "just two."),
        ("CO5 · Analyze", "Evaluation Metrics",
         "The Model Performance page reports accuracy, precision, recall, and F1 score — the same "
         "classification metrics this outcome covers for judging how well a trained model separates one crop "
         "from another."),
        ("CO6 · Apply", "Serving Predictions",
         "The get_prediction() function is deliberately isolated from its mock logic so it can later call a "
         "packaged model — the same separation of a trained model from the interface that serves it."),
    ]
    cols = st.columns(2)
    for i, (tag, title, desc) in enumerate(concepts):
        bg = PALETTE["sand"] if i % 2 == 0 else "rgba(15,61,46,0.06)"
        tag_bg = PALETTE["bark"] if i % 2 == 0 else PALETTE["forest"]
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{bg};border-radius:14px;padding:18px;margin-bottom:14px;">
              <span style="display:inline-block;font-size:0.7rem;font-weight:700;color:white;background:{tag_bg};
                           padding:3px 10px;border-radius:999px;margin-bottom:10px;">{tag}</span>
              <div style="font-weight:700;margin-bottom:6px;">{title}</div>
              <div style="font-size:0.85rem;color:{PALETTE['muted']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.caption("CO3 (tree-based models) and CO4 (unsupervised learning) are part of the broader course but sit "
               "outside the multinomial logistic regression classifier this project is built around.")


# ==============================================================================
# 8. PAGE: PERFORMANCE
# ==============================================================================
def render_performance():
    st.subheader("Model Performance")
    st.caption("These figures populate automatically once the trained model is connected.")

    labels_keys = [("Accuracy", "accuracy"), ("Precision", "precision"), ("Recall", "recall"), ("F1 Score", "f1")]
    cols = st.columns(4)
    for col, (label, key) in zip(cols, labels_keys):
        value = DEMO_METRICS.get(key)
        with col:
            if value is None:
                st.metric(label, "—")
                st.caption("Awaiting trained model")
            else:
                st.metric(label, f"{value}%")
                st.caption("Demo value")

    st.write("")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        with st.container(border=True):
            st.markdown("**Confusion Matrix**")
            st.info("Awaiting trained model")
            st.caption("The confusion matrix shows how accurately the model distinguishes between different crops.")
    with c2:
        with st.container(border=True):
            st.markdown("**Dataset Overview**")
            dataset = pd.DataFrame({
                "Field": ["Input Features", "Target", "Problem Type", "Algorithm"],
                "Value": ["7", "Crop", "Multi-Class Classification", "Multinomial Logistic Regression"],
            }).set_index("Field")
            st.table(dataset)

    st.write("")
    with st.container(border=True):
        st.markdown("**Future Enhancements**")
        st.markdown(
            "**AQI Integration** — Air Quality Index can potentially be added as an additional environmental "
            "feature if historical AQI data is available for the training samples. AQI is not currently part "
            "of the seven-feature model unless the dataset contains it."
        )
        extras = ["Weather API", "Fertilizer Recommendations", "IoT Soil Sensors",
                  "Real-Time Monitoring", "Location-Based Recommendations", "Weather Forecasting"]
        cols = st.columns(3)
        for i, item in enumerate(extras):
            cols[i % 3].markdown(f"- {item}")


# ==============================================================================
# 9. PAGE: ABOUT
# ==============================================================================
def render_about():
    st.subheader("About the Project")
    st.write(
        "CropWise is a machine-learning-based crop recommendation interface designed to demonstrate how soil "
        "and environmental data can be used to support agricultural decision-making."
    )
    tech = ["Python", "Pandas", "NumPy", "Scikit-learn", "Streamlit", "Multinomial Logistic Regression"]
    chip_html = "".join(
        f'<span style="display:inline-block;background:{PALETTE["canvas"]};border:1px solid {PALETTE["line"]};'
        f'border-radius:999px;padding:6px 14px;margin:4px 6px 0 0;font-size:0.85rem;font-weight:600;'
        f'color:{PALETTE["forest"]};">{t}</span>'
        for t in tech
    )
    st.markdown(chip_html, unsafe_allow_html=True)


# ==============================================================================
# 10. FOOTER
# ==============================================================================
def render_footer():
    st.write("")
    st.markdown("---")
    st.caption("🌱 **CropWise** — Smart decisions. Better farming. · Crop Recommendation Using Multinomial "
                "Logistic Regression · © 2026 CropWise")


# ==============================================================================
# MAIN
# ==============================================================================
render_navbar()
st.write("")

_page = st.session_state.page
if _page == "Home":
    render_home()
elif _page == "Recommend":
    render_recommend()
elif _page == "How It Works":
    render_how_it_works()
elif _page == "Performance":
    render_performance()
elif _page == "About":
    render_about()

render_footer()
