import os

# Install Streamlit and pyngrok
!pip install streamlit -q
!pip install pyngrok -q

# Authenticate ngrok if you have an authtoken (optional but recommended for longer sessions)
# from pyngrok import ngrok
# print("Enter your ngrok authtoken. Get it from https://dashboard.ngrok.com/auth/your-authtoken")
# ngrok_auth_token = input()
# !ngrok authtoken {ngrok_auth_token}

# Run the Streamlit app in the background
!nohup streamlit run clean_app.py &>/dev/null & 

# Get the public URL for the Streamlit app
from pyngrok import ngrok

# Terminate any previous ngrok tunnels to avoid issues
ngrok.kill()

# Set up a new ngrok tunnel
public_url = ngrok.connect(8501)
print(f"Your Streamlit app is live at: {public_url}")
