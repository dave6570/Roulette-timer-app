
import streamlit as st
import time

st.set_page_config(page_title="Roulette Predictor AI", layout="centered")

st.title("Roulette Predictor AI")
st.caption("Track ball and wheel speed in real-time and get smart predictions.")

# Initialize session state
for key in [
    "ball_count", "ball_start_time", "ball_timer_running", "ball_drop_time",
    "wheel_count", "wheel_start_time", "wheel_timer_running"
]:
    if key not in st.session_state:
        st.session_state[key] = None if "time" in key else 0

# Start both timers
if st.button("🎯 Start Round (Both Timers)"):
    now = time.time()
    st.session_state.ball_start_time = now
    st.session_state.wheel_start_time = now
    st.session_state.ball_count = 0
    st.session_state.wheel_count = 0
    st.session_state.ball_timer_running = True
    st.session_state.wheel_timer_running = True
    st.session_state.ball_drop_time = None

st.markdown("### Live Timers (from round start)")
cols = st.columns(2)

if st.session_state.ball_start_time:
    elapsed_ball = time.time() - st.session_state.ball_start_time
    cols[0].metric("Ball Timer", f"{elapsed_ball:.2f} sec")
else:
    cols[0].metric("Ball Timer", "---")

if st.session_state.wheel_start_time:
    elapsed_wheel = time.time() - st.session_state.wheel_start_time
    cols[1].metric("Wheel Timer", f"{elapsed_wheel:.2f} sec")
else:
    cols[1].metric("Wheel Timer", "---")

# Ball Rotation Button
if st.session_state.ball_timer_running:
    if st.button("➕ Ball Rotation"):
        st.session_state.ball_count += 1

# Wheel Rotation Button
if st.session_state.wheel_timer_running:
    if st.button("➕ Wheel Rotation"):
        st.session_state.wheel_count += 1

# Stop Ball Timer (marks drop)
if st.session_state.ball_timer_running:
    if st.button("🛑 Ball Dropped"):
        st.session_state.ball_timer_running = False
        st.session_state.ball_drop_time = time.time() - st.session_state.ball_start_time
        st.success(f"Ball Drop Time Recorded: {st.session_state.ball_drop_time:.2f} sec")

# Calculate RPS values
ball_rps = None
wheel_rps = None

if st.session_state.ball_start_time and st.session_state.ball_count > 0:
    elapsed = time.time() - st.session_state.ball_start_time
    if not st.session_state.ball_timer_running:
        elapsed = st.session_state.ball_drop_time
    ball_rps = st.session_state.ball_count / elapsed
    st.markdown(f"**Ball Speed:** {ball_rps:.2f} RPS")

if st.session_state.wheel_start_time and st.session_state.wheel_count > 0:
    elapsed = time.time() - st.session_state.wheel_start_time
    wheel_rps = st.session_state.wheel_count / elapsed
    st.markdown(f"**Wheel Speed:** {wheel_rps:.2f} RPS")

st.markdown("---")
st.markdown("### Choose Starting Number")

wheel_numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6,
    27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29,
    7, 28, 12, 35, 3, 26
]
start_number = st.selectbox("Starting number at top when ball is launched:", wheel_numbers)

st.markdown("### Predict Landing Zone")

if st.button("🔮 Predict"):
    if ball_rps is None or wheel_rps is None or st.session_state.ball_drop_time is None:
        st.warning("Please make sure you've started a round, tracked spins, and logged the ball drop.")
    else:
        total_rotations = wheel_rps * st.session_state.ball_drop_time
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
        st.markdown(f"### 💡 Recommended bets: {prediction_range}")
        st.caption("This tool is for fun and educational use only.")
