import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Brain Stroke Detection System",
    page_icon="assets/logo_small.png",
)

_, col1, _ = st.columns([2.8, 3, 1])
with col1:
    st.image("assets/logo.png", width=200)

st.markdown(
    """
    <style>
    .app-spacing {
        margin-top: -60px;
        margin-bottom: -70px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

app_name = """
    <div class='app-spacing' style="padding:4px">
    <h1 style='text-align: center; color: #22686E; font-size: 30px;'>Brain Stroke Detection System</h1>
    </div>
"""
st.markdown(app_name, unsafe_allow_html=True)

hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

login = st.Page(page="pages/login.py", title=" ", default=True)
app = st.Page(page="pages/app.py", title=" ")

pg = st.navigation(pages=[login, app])
pg.run()
