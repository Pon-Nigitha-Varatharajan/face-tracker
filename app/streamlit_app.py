import streamlit as st
import tempfile
import pandas as pd
import sqlite3
import os

from main import run

st.set_page_config(page_title="AI Face Tracking System", layout="wide")

st.title("🎯 Intelligent Face Tracking System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Input Source")

option = st.sidebar.selectbox(
    "Choose Input Type",
    ["Upload Video", "RTSP Stream"]
)

video_path = None

if option == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "avi"])
    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        video_path = tfile.name

elif option == "RTSP Stream":
    rtsp_url = st.sidebar.text_input("Enter RTSP URL")
    if rtsp_url:
        video_path = rtsp_url

start = st.sidebar.button("Start Processing")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["🎥 Live", "📁 History"])

# =========================
# 🎥 LIVE TAB
# =========================
with tab1:

    col1, col2 = st.columns([3, 1])

    with col1:
        frame_placeholder = st.empty()

    with col2:
        st.subheader("📊 Metrics")
        entries_metric = st.empty()
        exits_metric = st.empty()
        unique_metric = st.empty()

        st.subheader("📜 Logs")
        log_box = st.empty()

        st.subheader("🖼️ Recent Detections")
        image_box = st.empty()

    # ---------------- FETCH LOGS + IMAGES ----------------
    def get_recent_events(video_id):
        conn = sqlite3.connect("logs/data.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT event, face_id, image_path
            FROM events
            WHERE video_id = ?
            ORDER BY id DESC
            LIMIT 6
        """, (video_id,))

        rows = cursor.fetchall()
        conn.close()
        return rows

    # ---------------- CALLBACK ----------------
    def streamlit_callback(frame, video_id, entry, exit, unique_persons):

        frame_placeholder.image(frame, channels="BGR")

        # Metrics
        entries_metric.metric("Entries", entry)
        exits_metric.metric("Exits", exit)
        unique_metric.metric("Unique Visitors", len(unique_persons))

        # Logs + Images
        events = get_recent_events(video_id)

        logs = []
        cols = image_box.columns(2)

        for i, (event, face_id, img_path) in enumerate(events):

            logs.append(f"{event} - {face_id}")

            if img_path and os.path.exists(img_path):
                with cols[i % 2]:
                    st.image(
                        img_path,
                        caption=f"{event} - {face_id}",
                        use_container_width=True
                    )

        log_box.text("\n".join(logs))

    # ---------------- RUN ----------------
    if start:
        if not video_path:
            st.warning("Please provide a video or RTSP URL")
        else:
            st.info("Processing started...")

            run(
                video_path,
                streamlit_callback=streamlit_callback
            )

            st.success("Processing completed!")

# =========================
# 📁 HISTORY TAB
# =========================
with tab2:

    st.subheader("📁 Processing History")

    try:
        conn = sqlite3.connect("logs/data.db")

        videos = pd.read_sql_query(
            "SELECT * FROM videos ORDER BY video_id DESC",
            conn
        )

        if videos.empty:
            st.info("No history available")
        else:
            for _, row in videos.iterrows():

                with st.expander(f"🎬 {row['video_name']}"):

                    st.write(f"📅 Timestamp: {row['timestamp']}")
                    st.write(f"👥 Entries: {row['total_entries']}")
                    st.write(f"🚪 Exits: {row['total_exits']}")
                    st.write(f"🧠 Unique Visitors: {row['unique_people']}")

                    events = pd.read_sql_query(
                        f"SELECT * FROM events WHERE video_id={row['video_id']}",
                        conn
                    )

                    st.dataframe(events)

                    st.markdown("### 🖼️ Event Images")

                    # Filter
                    event_filter = st.selectbox(
                        f"Filter Events (Video {row['video_id']})",
                        ["All", "ENTRY", "EXIT"],
                        key=f"filter_{row['video_id']}"
                    )

                    cols = st.columns(3)

                    for i, ev in events.iterrows():

                        img_path = ev["image_path"]
                        face_id = ev["face_id"]
                        event_type = ev["event"]

                        if event_filter != "All" and event_type != event_filter:
                            continue

                        if img_path and os.path.exists(img_path):
                            with cols[i % 3]:
                                st.image(
                                    img_path,
                                    caption=f"{event_type} - {face_id}",
                                    use_container_width=True
                                )

    except Exception as e:
        st.error(e)