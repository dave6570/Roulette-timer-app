import streamlit as st
import time

st.set_page_config(page_title="Roulette Predictor AI", layout="centered")

st.title("Roulette Predictor AI")
st.caption("Estimate speeds by observation, then get predictions instantly.")

st.markdown("## Step 1: Estimate Spin Speeds by Observation")

# Ball Speed Tracker
st.subheader("Ball Speed Tracker")
if 'ball_count' not in st.session_state:
    st.session_state.ball_count = 0
    st.session_state.ball_start_time = None

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Ball Timer"):
        st.session_state.ball_start_time = time.time()
        st.session_state.ball_count = 0
with col2:
    if st.button("Log Ball Rotation"):
        if st.session_state.ball_start_time is not None:
            st.session_state.ball_count += 1

if st.session_state.ball_start_time is not None and st.session_state.ball_count > 0:
    elapsed = time.time() - st.session_state.ball_start_time
    ball_rps = st.session_state.ball_count / elapsed
    st.write(f"**Ball Speed:** {ball_rps:.2f} rotations per second (RPS)")
else:
    ball_rps = None

# Wheel Speed Tracker
st.subheader("Wheel Speed Tracker")
if 'wheel_count' not in st.session_state:
    st.session_state.wheel_count = 0
    st.session_state.wheel_start_time = None

col3, col4 = st.columns(2)
with col3:
    if st.button("Start Wheel Timer"):
        st.session_state.wheel_start_time = time.time()
        st.session_state.wheel_count = 0
with col4:
    if st.button("Log Wheel Rotation"):
        if st.session_state.wheel_start_time is not None:
            st.session_state.wheel_count += 1

if st.session_state.wheel_start_time is not None and st.session_state.wheel_count > 0:
    elapsed_wheel = time.time() - st.session_state.wheel_start_time
    wheel_rps = st.session_state.wheel_count / elapsed_wheel
    st.write(f"**Wheel Speed:** {wheel_rps:.2f} rotations per second (RPS)")
else:
    wheel_rps = None

st.markdown("---")
st.markdown("## Step 2: Enter Time Until Ball Drops")
drop_time = st.slider("Time until ball drops (in seconds)", 5.0, 15.0, 9.0)

st.markdown("## Step 3: Choose Starting Number")
wheel_numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6,
    27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29,
    7, 28, 12, 35, 3, 26
]
start_number = st.selectbox("Starting number at top when ball is launched:", wheel_numbers)

st.markdown("## Step 4: Run Prediction")
if st.button("Predict Landing Zone"):
    if wheel_rps is None or ball_rps is None:
        st.warning("Please track both ball and wheel speeds first.")
    else:
        total_rotations = wheel_rps * drop_time
        offset_fraction = total_rotations % 1
        slots_forward = round(offset_fraction * len(wheel_numbers))

        start_index = wheel_numbers.index(start_number)
        landing_index = (start_index + slots_forward) % len(wheel_numbers)

        predicted_center = wheel_numbers[landing_index]
        prediction_range = []
        for i in range(-3, 4):
            idx = (landing_index + i) % len(wheel_numbers)
            prediction_range.append(wheel_numbers[idx])

        st.success(f"The ball is likely to land around **{predicted_center}**")
        st.markdown(f"### Recommended bets: {prediction_range}")
        st.caption("This tool is for fun and educational use only.")
