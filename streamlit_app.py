import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Employee Salary Analysis",
    page_icon="💼",
    layout="wide"
)

# ---------- SAMPLE DATA ----------
sample_data = pd.DataFrame({
    "Employee ID": ["E001","E002","E003","E004","E005","E006","E007","E008"],
    "Name": ["Arun","Priya","Rahul","Sneha","Kiran","Divya","Ravi","Anjali"],
    "Age": [25,28,30,26,32,29,35,27],
    "Gender": ["Male","Female","Male","Female","Male","Female","Male","Female"],
    "Department": ["IT","HR","Finance","IT","Sales","HR","Finance","Sales"],
    "Salary": [45000,38000,55000,48000,42000,40000,65000,36000],
    "Experience": [2,4,6,3,5,3,8,2]
})

# ---------- SESSION DATA ----------
if "employee_data" not in st.session_state:
    st.session_state.employee_data = sample_data.copy()

df = st.session_state.employee_data

# ---------- SIDEBAR ----------
st.sidebar.title("💼 Employee Analytics")
st.sidebar.caption("Salary Analysis System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Employee Records",
        "Data Analysis",
        "Questions",
        "Upload Dataset"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Employee Salary Analysis")

# ---------- DASHBOARD ----------
if page == "Dashboard":

    st.title("Employee Salary Analysis Dashboard")
    st.caption("Summary of employee and salary data analysis")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", len(df))
    col2.metric("Average Salary", f"₹{df['Salary'].mean():,.0f}")
    col3.metric("Highest Salary", f"₹{df['Salary'].max():,.0f}")
    col4.metric("Lowest Salary", f"₹{df['Salary'].min():,.0f}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.subheader("Employees by Department")

        dept_count = df["Department"].value_counts().reset_index()
        dept_count.columns = ["Department", "Employees"]

        fig1 = px.bar(
            dept_count,
            x="Department",
            y="Employees",
            title="Department-wise Employees"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with right:

        st.subheader("Salary Distribution")

        salary_data = df.groupby("Department")["Salary"].sum().reset_index()

        fig2 = px.pie(
            salary_data,
            names="Department",
            values="Salary",
            title="Salary Distribution by Department"
        )

        st.plotly_chart(fig2, use_container_width=True)


# ---------- EMPLOYEE RECORDS ----------
elif page == "Employee Records":

    st.title("Employee Records")
    st.caption("View employee information")

    st.dataframe(
        df,
        use_container_width=True
    )


# ---------- DATA ANALYSIS ----------
elif page == "Data Analysis":

    st.title("Salary Data Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Average Salary by Department")

        avg_salary = (
            df.groupby("Department")["Salary"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            avg_salary,
            x="Department",
            y="Salary",
            title="Average Salary"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Experience vs Salary")

        fig = px.scatter(
            df,
            x="Experience",
            y="Salary",
            color="Department",
            hover_name="Name",
            title="Experience vs Salary"
        )

        st.plotly_chart(fig, use_container_width=True)


# ---------- QUESTIONS ----------
elif page == "Questions":

    st.title("Employee Salary Analysis - Questions")

    st.caption(
        "Select a question to get insights from the employee data"
    )

    st.markdown("---")

    question = st.selectbox(
        "Select a Question",
        [
            "What is the average salary of employees?",
            "Which employee has the highest salary?",
            "Which employee has the lowest salary?",
            "Which department has the highest average salary?",
            "Which department has the most employees?",
            "What is the average experience of employees?",
            "Who has the highest experience?",
            "What is the total salary of all employees?"
        ]
    )

    st.markdown("---")

    # Question 1
    if question == "What is the average salary of employees?":

        average_salary = df["Salary"].mean()

        st.subheader("Answer")
        st.success(
            f"The average salary of employees is ₹{average_salary:,.0f}"
        )


    # Question 2
    elif question == "Which employee has the highest salary?":

        employee = df.loc[df["Salary"].idxmax()]

        st.subheader("Answer")

        st.success(
            f"{employee['Name']} has the highest salary "
            f"of ₹{employee['Salary']:,.0f}"
        )


    # Question 3
    elif question == "Which employee has the lowest salary?":

        employee = df.loc[df["Salary"].idxmin()]

        st.subheader("Answer")

        st.success(
            f"{employee['Name']} has the lowest salary "
            f"of ₹{employee['Salary']:,.0f}"
        )


    # Question 4
    elif question == "Which department has the highest average salary?":

        avg_department_salary = (
            df.groupby("Department")["Salary"]
            .mean()
        )

        department = avg_department_salary.idxmax()
        salary = avg_department_salary.max()

        st.subheader("Answer")

        st.success(
            f"{department} department has the highest average salary "
            f"of ₹{salary:,.0f}"
        )


    # Question 5
    elif question == "Which department has the most employees?":

        department_count = df["Department"].value_counts()

        department = department_count.idxmax()
        count = department_count.max()

        st.subheader("Answer")

        st.success(
            f"{department} department has the most employees: {count}"
        )


    # Question 6
    elif question == "What is the average experience of employees?":

        average_experience = df["Experience"].mean()

        st.subheader("Answer")

        st.success(
            f"The average experience of employees is "
            f"{average_experience:.1f} years"
        )


    # Question 7
    elif question == "Who has the highest experience?":

        employee = df.loc[df["Experience"].idxmax()]

        st.subheader("Answer")

        st.success(
            f"{employee['Name']} has the highest experience "
            f"of {employee['Experience']} years"
        )


    # Question 8
    elif question == "What is the total salary of all employees?":

        total_salary = df["Salary"].sum()

        st.subheader("Answer")

        st.success(
            f"The total salary of all employees is "
            f"₹{total_salary:,.0f}"
        )


# ---------- UPLOAD DATASET ----------
elif page == "Upload Dataset":

    st.title("Upload Employee Dataset")
    st.caption("Upload your employee CSV file for analysis")

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Upload CSV File")

        uploaded_file = st.file_uploader(
            "Drop your CSV file here or choose a file",
            type=["csv"]
        )

        if uploaded_file is not None:

            new_df = pd.read_csv(uploaded_file)

            required_columns = [
                "Employee ID",
                "Name",
                "Age",
                "Gender",
                "Department",
                "Salary",
                "Experience"
            ]

            missing = [
                col
                for col in required_columns
                if col not in new_df.columns
            ]

            if missing:

                st.error(
                    "Missing columns: " + ", ".join(missing)
                )

            else:

                st.session_state.employee_data = new_df

                st.success(
                    "Employee dataset uploaded successfully!"
                )

                st.dataframe(
                    new_df.head(),
                    use_container_width=True
                )

    with right:

        st.subheader("Required CSV Columns")

        for column in [
            "Employee ID",
            "Name",
            "Age",
            "Gender",
            "Department",
            "Salary",
            "Experience"
        ]:

            st.write("✓", column)

        st.info(
            "Upload a CSV file containing the required columns."
        )


# ---------- FOOTER ----------
st.markdown("---")

st.caption(
    "Employee Salary Analysis | Data Analytics Project"
)
