import streamlit as st
import joblib
import pandas as pd

# 1. Load the model and feature names
model = joblib.load('performance_model.pkl')
features = joblib.load('model_features.pkl')

# Define your Mappings
edu_options = {1: 'Below College', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'}
wolbal_options = {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'}

st.set_page_config(page_title="Employee Performance Predictor", layout="wide")
st.title("Employee Performance Prediction App")

with st.form("input_form"):
    st.subheader("Employee Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hike = st.slider("Last Salary Hike (%)", 0, 50, 15)
        env_sat = st.slider("Environment Satisfaction (1-4)", 1, 4, 3)
        last_promo = st.number_input("Years Since Last Promotion", 0, 40, 1)
        hourly_rate = st.number_input("Hourly Rate", 0, 200, 65)
        mgr_years = st.number_input("Years With Current Manager", 0, 40, 2)

    with col2:
        age = st.number_input("Age", 18, 70, 30)
        role_years = st.number_input("Years In Current Role", 0, 40, 2)
        company_years = st.number_input("Total Years At Company", 0, 40, 5)
        dept_dev = st.selectbox("Department: Development?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
        total_exp = st.number_input("Total Work Experience (Years)", 0, 50, 8)

    with col3:
        distance = st.number_input("Distance From Home (km)", 0, 100, 10)
        
        # Mapping for Work Life Balance
        work_life = st.selectbox(
            "Work-Life Balance", 
            options=list(wolbal_options.keys()), 
            format_func=lambda x: wolbal_options[x]
        )
        
        num_companies = st.number_input("Number of Companies Worked", 0, 15, 1)
        
        # Mapping for Education Level
        edu_level = st.selectbox(
            "Education Level", 
            options=list(edu_options.keys()), 
            format_func=lambda x: edu_options[x]
        )
        
        training = st.number_input("Training Times Last Year", 0, 10, 2)

    submit = st.form_submit_button("Predict Performance Rating")

if submit:
    input_dict = {
        'EmpLastSalaryHikePercent': hike,
        'EmpEnvironmentSatisfaction': env_sat,
        'YearsSinceLastPromotion': last_promo,
        'EmpHourlyRate': hourly_rate,
        'YearsWithCurrManager': mgr_years,
        'Age': age,
        'ExperienceYearsInCurrentRole': role_years,
        'ExperienceYearsAtThisCompany': company_years,
        'EmpDepartment_Development': dept_dev,
        'TotalWorkExperienceInYears': total_exp,
        'DistanceFromHome': distance,
        'EmpWorkLifeBalance': work_life,
        'NumCompaniesWorked': num_companies,
        'EmpEducationLevel': edu_level,
        'TrainingTimesLastYear': training
    }
    
    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)
    
    st.divider()
    if prediction == 4:
        st.balloons()
        st.success(f"### Predicted Rating: CLASS {prediction[0]} (Outstanding)")
    elif prediction == 3:
        st.info(f"### Predicted Rating: CLASS {prediction[0]} (Good)")
    else:
        st.warning(f"### Predicted Rating: CLASS {prediction[0]} (Needs Improvement)")
