import streamlit as st

# Set page configuration
st.set_page_config(page_title="Welcome", layout="centered")

# Welcome message
st.title("👋 Welcome to My Streamlit App")
st.subheader("This is a simple welcome page.")
st.write("Use this app as a starting point for your Streamlit projects!")

# Optional image or logo
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

# Footer note
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
