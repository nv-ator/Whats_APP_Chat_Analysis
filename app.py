import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Analyzer", "About"]
)

st.sidebar.divider()

# ---------- PAGE HEADER ----------
st.title("💬 WhatsApp Chat Analyzer")
st.markdown(
    "Analyze WhatsApp chats to understand timelines, activity patterns, word usage, and emojis."
)
st.divider()

# =====================================================================
# ============================= ANALYZER ===============================
# =====================================================================
if page == "Analyzer":

    st.sidebar.header("📂 Upload Chat")

    uploaded_file = st.sidebar.file_uploader(
        "Upload exported WhatsApp chat (.txt)",
        type=["txt"]
    )

    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Analysis Settings")

    if uploaded_file is None:
        st.info("👈 Upload a WhatsApp chat file from the sidebar to begin analysis.")
        st.stop()

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Select user",
        user_list
    )

    if not st.sidebar.button("🔍 Generate Analysis"):
        st.stop()

    # ---------- OVERVIEW ----------
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Messages", num_messages)
    with col2:
        st.metric("Words", words)
    with col3:
        st.metric("Media", num_media_messages)
    with col4:
        st.metric("Links", num_links)

    st.subheader("📝 Chat Summary")
    st.info(
        f"""
        • Chat duration: {df['date'].min().date()} → {df['date'].max().date()}  
        • Total participants: {df['user'].nunique()}  
        • Most active user: {df['user'].value_counts().idxmax()}
        """
    )

    st.divider()

    # ---------- TABS ----------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Timelines", "🗺️ Activity", "☁️ Content", "😀 Emojis"]
    )

    # ---------- TAB 1 : TIMELINES ----------
    with tab1:
        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.subheader("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # ---------- TAB 2 : ACTIVITY ----------
    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.subheader("Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

    # ---------- TAB 3 : CONTENT ----------
    with tab3:
        st.subheader("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        if not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(most_common_df['word'], most_common_df['count'])
            st.pyplot(fig)
        else:
            st.info("No meaningful words found.")

    # ---------- TAB 4 : EMOJIS ----------
    with tab4:
        st.subheader("Emoji Usage")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            if emoji_df.empty:
                st.info("No emojis found in this chat.")
            else:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df['count'].head(),
                    labels=emoji_df['emoji'].head(),
                    autopct="%0.2f"
                )
                st.pyplot(fig)

# =====================================================================
# =============================== ABOUT ================================
# =====================================================================
if page == "About":

    st.title("ℹ️ About This Project")

    st.markdown(
        """
        ### 💬 WhatsApp Chat Analyzer

        This web application analyzes exported WhatsApp chat files and provides insights into:

        - 📊 Message statistics  
        - 📈 Daily & monthly timelines  
        - 🗺️ User activity patterns  
        - ☁️ Word usage and word clouds  
        - 😀 Emoji analysis  

        ### 🛠️ Tech Stack
        - Python
        - Streamlit
        - Pandas
        - Matplotlib
        - Seaborn

        ### 👨‍💻 Developer
        **Ujjwal**

        - 📧 Email: thakurujjwal895@gmail.com  
        - 💬 WhatsApp: +91 9310408574  
        - 💻 GitHub: https://github.com/YOUR_GITHUB_USERNAME  
        - 🔗 LinkedIn: https://www.linkedin.com/in/YOUR_LINKEDIN_USERNAME  

        ---
        This project was built for learning, analysis, and demonstration purposes.
        """
    )

# =====================================================================
# =============================== FOOTER ===============================
# =====================================================================
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: gray;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }
    </style>

    <div class="footer">
        <strong>Developed by Ujjwal</strong> |
        📧 <a href="mailto:thakurujjwal895@gmail.com">Email</a> |
        💬 <a href="https://wa.me/919310408574" target="_blank">WhatsApp</a> |
        💻 <a href="https://https://github.com/nv-ator" target="_blank">GitHub</a> |
        🔗 <a href="https://www.linkedin.com/in/ujthakur/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)
