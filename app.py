import streamlit as st

st.set_page_config(page_title="MyApp", layout="wide")

st.title("🏠 หน้าหลัก ")
st.write("### Boot Camp: Data Science and Machine Learning")
st.info("7 Day Intensive Hands-on Workshop")
st.markdown("':rainbow[ANUSORN]'")

if st.button("💰 ระบบคำนวณส่วนลดตามยอดซื้อ"):
    st.switch_page("pages/app1_discount_calc.py")
elif st.button("💰 การทำความสะอาดข้อมูล"):
    st.switch_page("pages/clean_app.py")
elif st.button("💰 การทำความสะอาดข้อมูลของเก่ง"):
    st.switch_page("pages/clean_customers.py")
elif st.button("💰 การแปลงข้อมูล"):
    st.switch_page("pages/transform_app.py")
elif st.button("💰 การวิเคราะห์ข้อมูลเชิงสำรวจ"):
    st.switch_page("pages/EDA_app.py")
elif st.button("💰 การพยากรณ์ยอดขายแบบง่าย"):
    st.switch_page("pages/sale_predict.py")
elif st.button("💰 การพยากรณ์ระยะเวลาการให้บริการขนส่ง"):
    st.switch_page("pages/truck_predict.py")
elif st.button("💰 การจำแนกประเภทข้อมูลยอดขาย"):
    st.switch_page("pages/classify_redbull_sale.py")    
