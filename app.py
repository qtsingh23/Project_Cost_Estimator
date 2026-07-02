import streamlit as st
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Software Project Cost Estimator", initial_sidebar_state="expanded")

# --- Custom CSS Styling --- #
st.markdown("""
<style>
    .main { background-color: #F5F7FA; color: #1E293B; }
    .stButton>button { 
        background-color: #1E3A8A; 
        color: #FFFFFF; 
        border-radius: 4px; 
        border: 1px solid #1E3A8A;
        font-weight: 600;
    }
    .stButton>button:hover { 
        background-color: #1E40AF; 
        border: 1px solid #1E40AF; 
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { 
        background-color: #FFFFFF; 
        color: #1E293B; 
        border: 1px solid #E2E8F0; 
    }
    .stSelectbox>div>div>div { 
        background-color: #FFFFFF; 
        color: #1E293B; 
        border: 1px solid #E2E8F0; 
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { 
        font-size: 1.1rem; 
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        background: #E2E8F0; 
        border-radius: 4px 4px 0 0; 
        gap: 10px; 
        padding-top: 10px; 
        padding-bottom: 10px; 
    }
    .stTabs [aria-selected="true"] { 
        background: #1E3A8A; 
        color: #FFFFFF;
        border-bottom: 3px solid #1E3A8A; 
    }
    h1, h2, h3, h4, h5, h6 { color: #1E3A8A; }
    .stMarkdown { color: #1E293B; }
    .calculation-box {
        background-color: #E0E7FF;
        border-left: 4px solid #1E3A8A;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .explanation-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 12px;
        margin: 8px 0;
        border-radius: 4px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("Automated Software Project Cost Estimation Tool")
st.markdown("*Comprehensive cost estimation using COCOMO and Function Point Analysis*")

# --- COCOMO Estimation Module --- #
def cocomo_estimation():
    st.header("COCOMO Estimation Module")
    
    st.markdown("""
    The **Constructive Cost Model (COCOMO)** is a procedural software cost estimation model that uses historical project data 
    to estimate effort, cost, and schedule. This tool supports both **Basic COCOMO** and **Intermediate COCOMO** models.
    
    **Key Formulas:**
    - **Effort (Person-Months):** `E = a * (KLOC ^ b)`
    - **Duration (Months):** `D = c * (E ^ d)`
    - **Average Staffing:** `S = E / D`
    - **Total Cost:** `Cost = Staffing * Average Salary`
    """)
    
    # Model Selection
    cocomo_model = st.radio("Select COCOMO Model:", ["Basic COCOMO", "Intermediate COCOMO"], horizontal=True)
    
    if cocomo_model == "Basic COCOMO":
        basic_cocomo()
    else:
        intermediate_cocomo()

def basic_cocomo():
    """Basic COCOMO Calculation"""
    st.subheader("Basic COCOMO Calculation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        kloc = st.number_input("Project Size (KLOC)", min_value=0.1, value=10.0, step=0.5)
    with col2:
        project_type = st.selectbox("Project Type", ["Organic", "Semi-Detached", "Embedded"])
    with col3:
        avg_salary = st.number_input("Average Salary (Annual, GBP)", min_value=10000.0, value=80000.0, step=5000.0)
    
    # Coefficient explanations
    with st.expander("View Coefficient Definitions"):
        st.markdown("""
        **COCOMO Coefficients by Project Type:**
        
        | Parameter | Organic | Semi-Detached | Embedded |
        |-----------|---------|---------------|----------|
        | **a** | 2.4 | 3.0 | 3.6 |
        | **b** | 1.05 | 1.12 | 1.20 |
        | **c** | 2.5 | 2.5 | 2.5 |
        | **d** | 0.38 | 0.35 | 0.32 |
        
        - **Organic**: Small teams, well-understood requirements, minimal constraints
        - **Semi-Detached**: Medium teams, mixed requirements clarity, moderate constraints
        - **Embedded**: Large teams, complex requirements, tight constraints
        
        - **a & b**: Scale the effort based on project size (KLOC). Higher values indicate more effort per KLOC.
        - **c & d**: Determine how duration scales with effort. Lower d values mean duration scales less steeply.
        """)
    
    if st.button("Calculate Basic COCOMO", key="basic_cocomo_btn"):
        coefficients = {
            "Organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
            "Semi-Detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
            "Embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32}
        }
        
        params = coefficients[project_type]
        effort = params["a"] * (kloc ** params["b"])
        duration = params["c"] * (effort ** params["d"])
        staffing = effort / duration
        monthly_salary = avg_salary / 12
        total_cost = effort * monthly_salary
        
        st.subheader("Basic COCOMO Results")
        
        # Display metrics in a grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Effort", f"{effort:.2f} PM", delta=None)
        with col2:
            st.metric("Duration", f"{duration:.2f} Months", delta=None)
        with col3:
            st.metric("Average Staffing", f"{math.ceil(staffing)} People", delta=None)
        with col4:
            st.metric("Total Cost", f"GBP {total_cost:,.2f}", delta=None)
        
        # Interactive Calculation Breakdown
        with st.expander("View Calculation Breakdown", expanded=True):
            st.markdown("### Step-by-Step Calculation")
            
            # Step 1: Effort Calculation
            st.markdown("**Step 1: Calculate Effort (Person-Months)**")
            st.markdown(f"""
            Formula: `E = a * (KLOC ^ b)`
            
            Where:
            - a = {params['a']} (coefficient for {project_type} projects)
            - b = {params['b']} (exponent for {project_type} projects)
            - KLOC = {kloc}
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            E = {params['a']} * ({kloc} ^ {params['b']})
            E = {params['a']} * {kloc ** params['b']:.4f}
            E = {effort:.2f} Person-Months
            ```
            """)
            
            # Step 2: Duration Calculation
            st.markdown("**Step 2: Calculate Development Duration (Months)**")
            st.markdown(f"""
            Formula: `D = c * (E ^ d)`
            
            Where:
            - c = {params['c']} (coefficient for {project_type} projects)
            - d = {params['d']} (exponent for {project_type} projects)
            - E = {effort:.2f} (effort calculated in Step 1)
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            D = {params['c']} * ({effort:.2f} ^ {params['d']})
            D = {params['c']} * {effort ** params['d']:.4f}
            D = {duration:.2f} Months
            ```
            """)
            
            # Step 3: Staffing Calculation
            st.markdown("**Step 3: Calculate Average Staffing**")
            st.markdown(f"""
            Formula: `S = E / D`
            
            Where:
            - E = {effort:.2f} Person-Months (effort from Step 1)
            - D = {duration:.2f} Months (duration from Step 2)
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            S = {effort:.2f} / {duration:.2f}
            S = {staffing:.2f} People (rounded up to {math.ceil(staffing)})
            ```
            """)
            
            # Step 4: Cost Calculation
            st.markdown("**Step 4: Calculate Total Project Cost**")
            st.markdown(f"""
            Formula: `Cost = Effort * Monthly Salary`
            
            Where:
            - Effort = {effort:.2f} Person-Months
            - Annual Salary = GBP {avg_salary:,.2f}
            - Monthly Salary = GBP {avg_salary:,.2f} / 12 = GBP {monthly_salary:,.2f}
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            Cost = {effort:.2f} * {monthly_salary:,.2f}
            Cost = GBP {total_cost:,.2f}
            ```
            """)
        
        # Visualisation
        col1, col2 = st.columns(2)
        with col1:
            # Bar chart for metrics
            data = {
                "Metric": ["Effort (PM)", "Duration (Mo)", "Staffing"],
                "Value": [effort, duration, staffing]
            }
            df = pd.DataFrame(data)
            fig = px.bar(df, x="Metric", y="Value", title="COCOMO Metrics Breakdown",
                        color_discrete_sequence=["#1E3A8A"])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost breakdown
            cost_data = {
                "Category": ["Labour Cost", "Contingency (20%)"],
                "Amount": [total_cost, total_cost * 0.2]
            }
            df_cost = pd.DataFrame(cost_data)
            fig_cost = px.pie(df_cost, values="Amount", names="Category", title="Cost Breakdown",
                             color_discrete_sequence=["#1E3A8A", "#64748B"])
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Detailed breakdown
        st.subheader("Detailed Breakdown")
        breakdown_data = {
            "Parameter": ["KLOC", "Project Type", "Effort (Person-Months)", "Duration (Months)", 
                         "Average Staffing", "Monthly Salary", "Total Labour Cost"],
            "Value": [f"{kloc}", project_type, f"{effort:.2f}", f"{duration:.2f}", 
                     f"{math.ceil(staffing)}", f"GBP {monthly_salary:,.2f}", f"GBP {total_cost:,.2f}"]
        }
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

def intermediate_cocomo():
    """Intermediate COCOMO with Cost Drivers"""
    st.subheader("Intermediate COCOMO Calculation (with Cost Drivers)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        kloc = st.number_input("Project Size (KLOC)", min_value=0.1, value=10.0, step=0.5, key="inter_kloc")
    with col2:
        project_type = st.selectbox("Project Type", ["Organic", "Semi-Detached", "Embedded"], key="inter_type")
    with col3:
        avg_salary = st.number_input("Average Salary (Annual, GBP)", min_value=10000.0, value=80000.0, step=5000.0, key="inter_salary")
    
    st.markdown("**Select Cost Driver Ratings** (1.0 = Nominal, <1.0 = Favourable, >1.0 = Unfavourable)")
    
    # Cost Drivers with explanations
    cost_drivers = {
        "RELY (Required Reliability)": [0.75, 0.88, 1.0, 1.15, 1.40],
        "DATA (Database Size)": [0.93, 1.0, 1.08, 1.16],
        "CPLX (Product Complexity)": [0.70, 0.85, 1.0, 1.15, 1.30, 1.65],
        "RUSE (Required Reusability)": [0.95, 1.0, 1.07, 1.15, 1.24],
        "DOCU (Documentation)": [0.81, 0.91, 1.0, 1.11],
        "TIME (Execution Time Constraint)": [1.0, 1.11, 1.29, 1.63],
        "STOR (Main Storage Constraint)": [1.0, 1.05, 1.17, 1.46],
        "PVOL (Platform Volatility)": [0.87, 1.0, 1.15, 1.30]
    }
    
    cost_driver_explanations = {
        "RELY (Required Reliability)": "How critical is the system? Higher values for mission-critical systems.",
        "DATA (Database Size)": "Relative database size. Larger databases increase effort.",
        "CPLX (Product Complexity)": "Overall product complexity. More complex systems require more effort.",
        "RUSE (Required Reusability)": "How much code must be reusable? Higher reusability requirements increase effort.",
        "DOCU (Documentation)": "Documentation requirements. More documentation increases effort.",
        "TIME (Execution Time Constraint)": "Real-time execution constraints. Tighter constraints increase effort.",
        "STOR (Main Storage Constraint)": "Main storage constraints. Tighter constraints increase effort.",
        "PVOL (Platform Volatility)": "Platform volatility. More volatile platforms increase effort."
    }
    
    with st.expander("View Cost Driver Explanations"):
        for driver, explanation in cost_driver_explanations.items():
            st.markdown(f"**{driver}**: {explanation}")
    
    eaf = 1.0
    driver_values = {}
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    col_idx = 0
    
    for driver_name, options in cost_drivers.items():
        with cols[col_idx % 4]:
            selected = st.selectbox(driver_name, options, index=len(options)//2, key=f"driver_{driver_name}")
            driver_values[driver_name] = selected
            eaf *= selected
        col_idx += 1
    
    if st.button("Calculate Intermediate COCOMO", key="inter_cocomo_btn"):
        coefficients = {
            "Organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
            "Semi-Detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
            "Embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32}
        }
        
        params = coefficients[project_type]
        base_effort = params["a"] * (kloc ** params["b"])
        effort = base_effort * eaf
        duration = params["c"] * (effort ** params["d"])
        staffing = effort / duration
        monthly_salary = avg_salary / 12
        total_cost = effort * monthly_salary
        
        st.subheader("Intermediate COCOMO Results")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Base Effort", f"{base_effort:.2f} PM", delta=None)
        with col2:
            st.metric("EAF", f"{eaf:.3f}", delta=None)
        with col3:
            st.metric("Adjusted Effort", f"{effort:.2f} PM", delta=None)
        with col4:
            st.metric("Duration", f"{duration:.2f} Mo", delta=None)
        with col5:
            st.metric("Total Cost", f"GBP {total_cost:,.2f}", delta=None)
        
        # Interactive Calculation Breakdown
        with st.expander("View Calculation Breakdown", expanded=True):
            st.markdown("### Step-by-Step Calculation")
            
            # Step 1: Base Effort
            st.markdown("**Step 1: Calculate Base Effort (Person-Months)**")
            st.markdown(f"""
            Formula: `E_base = a * (KLOC ^ b)`
            
            Using {project_type} coefficients:
            - a = {params['a']}
            - b = {params['b']}
            - KLOC = {kloc}
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            E_base = {params['a']} * ({kloc} ^ {params['b']})
            E_base = {base_effort:.2f} Person-Months
            ```
            """)
            
            # Step 2: EAF Calculation
            st.markdown("**Step 2: Calculate Effort Adjustment Factor (EAF)**")
            st.markdown("Formula: `EAF = Product of all cost driver multipliers`")
            
            driver_calc = " × ".join([f"{v:.2f}" for v in driver_values.values()])
            st.markdown(f"""
            Cost Driver Multipliers:
            ```
            EAF = {driver_calc}
            EAF = {eaf:.3f}
            ```
            """)
            
            # Step 3: Adjusted Effort
            st.markdown("**Step 3: Calculate Adjusted Effort**")
            st.markdown(f"""
            Formula: `E_adjusted = E_base * EAF`
            
            Calculation:
            ```
            E_adjusted = {base_effort:.2f} * {eaf:.3f}
            E_adjusted = {effort:.2f} Person-Months
            ```
            """)
            
            # Step 4: Duration
            st.markdown("**Step 4: Calculate Development Duration**")
            st.markdown(f"""
            Formula: `D = c * (E_adjusted ^ d)`
            
            Using {project_type} coefficients:
            - c = {params['c']}
            - d = {params['d']}
            - E_adjusted = {effort:.2f}
            """)
            
            st.markdown(f"""
            Calculation:
            ```
            D = {params['c']} * ({effort:.2f} ^ {params['d']})
            D = {duration:.2f} Months
            ```
            """)
            
            # Step 5: Cost
            st.markdown("**Step 5: Calculate Total Project Cost**")
            st.markdown(f"""
            Formula: `Cost = E_adjusted * Monthly Salary`
            
            Calculation:
            ```
            Monthly Salary = {avg_salary:,.2f} / 12 = {monthly_salary:,.2f}
            Cost = {effort:.2f} * {monthly_salary:,.2f}
            Cost = GBP {total_cost:,.2f}
            ```
            """)
        
        # Visualisation
        col1, col2 = st.columns(2)
        with col1:
            # Effort comparison
            effort_data = {
                "Type": ["Base Effort", "Adjusted Effort"],
                "Value": [base_effort, effort]
            }
            df_effort = pd.DataFrame(effort_data)
            fig_effort = px.bar(df_effort, x="Type", y="Value", title="Base vs. Adjusted Effort",
                               color_discrete_sequence=["#64748B", "#1E3A8A"])
            st.plotly_chart(fig_effort, use_container_width=True)
        
        with col2:
            # Cost drivers impact
            driver_names = [name.split("(")[0].strip() for name in driver_values.keys()]
            driver_vals = list(driver_values.values())
            fig_drivers = px.bar(x=driver_names, y=driver_vals, title="Cost Driver Multipliers",
                                color_discrete_sequence=["#1E3A8A"] * len(driver_names))
            fig_drivers.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_drivers, use_container_width=True)
        
        # Detailed breakdown
        st.subheader("Detailed Breakdown")
        breakdown_data = {
            "Parameter": ["KLOC", "Project Type", "Base Effort", "EAF", "Adjusted Effort (Person-Months)", 
                         "Duration (Months)", "Average Staffing", "Monthly Salary", "Total Labour Cost"],
            "Value": [f"{kloc}", project_type, f"{base_effort:.2f}", f"{eaf:.3f}", f"{effort:.2f}", 
                     f"{duration:.2f}", f"{math.ceil(staffing)}", f"GBP {monthly_salary:,.2f}", f"GBP {total_cost:,.2f}"]
        }
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

# --- Function Point Analysis Module --- #
def fpa_estimation():
    st.header("Function Point Analysis (FPA) Module")
    
    st.markdown("""
    **Function Point Analysis (FPA)** measures the functional size of an information system based on the functionality 
    provided to the user. It accounts for function complexity and system characteristics.
    
    **Key Formulas:**
    - **Unadjusted Function Points (UFP):** Sum of (count × weight) for each function type
    - **Total Degree of Influence (TDI):** Sum of ratings for 14 system characteristics
    - **Value Adjustment Factor (VAF):** `(TDI × 0.01) + 0.65`
    - **Adjusted Function Points (AFP):** `AFP = UFP × VAF`
    - **Effort (Person-Hours):** `Effort = AFP × Productivity Rate`
    - **Cost:** `Cost = Effort × Labour Cost per Hour`
    """)
    
    st.subheader("Step 1: Function Type Inputs with Complexity Levels")
    
    # Function types with complexity weights
    complexity_weights = {
        "Low": {"EI": 3, "EO": 4, "EQ": 3, "ILF": 7, "EIF": 5},
        "Average": {"EI": 4, "EO": 5, "EQ": 4, "ILF": 10, "EIF": 7},
        "High": {"EI": 6, "EO": 7, "EQ": 6, "ILF": 15, "EIF": 10}
    }
    
    function_type_explanations = {
        "EI": "External Inputs - Data or control inputs from outside the system boundary",
        "EO": "External Outputs - Data or control outputs sent outside the system boundary",
        "EQ": "External Inquiries - Interactive queries that retrieve data without updating",
        "ILF": "Internal Logical Files - User-identifiable groups of logically related data",
        "EIF": "External Interface Files - User-identifiable groups of logically related data outside the system"
    }
    
    with st.expander("View Function Type Explanations"):
        for func_type, explanation in function_type_explanations.items():
            st.markdown(f"**{func_type}**: {explanation}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    function_inputs = {}
    with col1:
        st.markdown("**External Inputs (EI)**")
        ei_count = st.number_input("EI Count", min_value=0, value=5, key="ei_count")
        ei_complexity = st.selectbox("EI Complexity", ["Low", "Average", "High"], key="ei_complex")
        function_inputs["EI"] = (ei_count, ei_complexity)
    
    with col2:
        st.markdown("**External Outputs (EO)**")
        eo_count = st.number_input("EO Count", min_value=0, value=5, key="eo_count")
        eo_complexity = st.selectbox("EO Complexity", ["Low", "Average", "High"], key="eo_complex")
        function_inputs["EO"] = (eo_count, eo_complexity)
    
    with col3:
        st.markdown("**External Inquiries (EQ)**")
        eq_count = st.number_input("EQ Count", min_value=0, value=5, key="eq_count")
        eq_complexity = st.selectbox("EQ Complexity", ["Low", "Average", "High"], key="eq_complex")
        function_inputs["EQ"] = (eq_count, eq_complexity)
    
    with col4:
        st.markdown("**Internal Logical Files (ILF)**")
        ilf_count = st.number_input("ILF Count", min_value=0, value=3, key="ilf_count")
        ilf_complexity = st.selectbox("ILF Complexity", ["Low", "Average", "High"], key="ilf_complex")
        function_inputs["ILF"] = (ilf_count, ilf_complexity)
    
    with col5:
        st.markdown("**External Interface Files (EIF)**")
        eif_count = st.number_input("EIF Count", min_value=0, value=2, key="eif_count")
        eif_complexity = st.selectbox("EIF Complexity", ["Low", "Average", "High"], key="eif_complex")
        function_inputs["EIF"] = (eif_count, eif_complexity)
    
    st.subheader("Step 2: System Characteristics (14 Factors)")
    
    characteristics = [
        "Data Communications", "Distributed Data Processing", "Performance Constraints",
        "Heavily Used Configuration", "Transaction Rate", "Online Data Entry",
        "End-User Efficiency", "Online Update", "Complex Processing",
        "Reusability", "Installation Ease", "Operational Ease",
        "Multiple Site Installation", "Facilitate Change"
    ]
    
    characteristic_explanations = {
        "Data Communications": "Degree of data communication required (0=None, 5=Extensive)",
        "Distributed Data Processing": "Degree of distributed processing (0=None, 5=Extensive)",
        "Performance Constraints": "Performance requirements (0=None, 5=Very strict)",
        "Heavily Used Configuration": "Degree of configuration for different installations (0=None, 5=Highly configurable)",
        "Transaction Rate": "Transaction rate and volume (0=Low, 5=Very high)",
        "Online Data Entry": "Percentage of transactions that are online (0=None, 5=All)",
        "End-User Efficiency": "Importance of end-user efficiency (0=Low, 5=Critical)",
        "Online Update": "Degree of online update (0=None, 5=Extensive)",
        "Complex Processing": "Complexity of internal processing (0=Low, 5=Very high)",
        "Reusability": "Design for reusability (0=None, 5=Extensive)",
        "Installation Ease": "Ease of installation (0=Difficult, 5=Very easy)",
        "Operational Ease": "Ease of operation (0=Difficult, 5=Very easy)",
        "Multiple Site Installation": "Design for multiple site installation (0=Single site, 5=Multiple sites)",
        "Facilitate Change": "Degree of design for facilitating change (0=None, 5=Extensive)"
    }
    
    with st.expander("View System Characteristic Explanations"):
        for char, explanation in characteristic_explanations.items():
            st.markdown(f"**{char}**: {explanation}")
    
    tdi = 0
    char_ratings = {}
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    for idx, char in enumerate(characteristics):
        with cols[idx % 4]:
            rating = st.slider(f"{char}", min_value=0, max_value=5, value=3, key=f"char_{idx}")
            char_ratings[char] = rating
            tdi += rating
    
    vaf = (tdi * 0.01) + 0.65
    
    st.markdown(f"**Total Degree of Influence (TDI):** {tdi} | **Value Adjustment Factor (VAF):** {vaf:.3f}")
    
    st.subheader("Step 3: Productivity and Labour Cost")
    
    col1, col2 = st.columns(2)
    with col1:
        productivity_rate = st.number_input("Productivity Rate (AFP per Person-Hour)", min_value=0.1, value=0.5, step=0.1)
    with col2:
        labour_cost_per_hour = st.number_input("Labour Cost per Hour (GBP)", min_value=1.0, value=75.0, step=5.0)
    
    if st.button("Calculate FPA", key="fpa_btn"):
        # Calculate UFP
        ufp = 0
        ufp_breakdown = {}
        for func_type, (count, complexity) in function_inputs.items():
            weight = complexity_weights[complexity][func_type]
            ufp_breakdown[func_type] = count * weight
            ufp += count * weight
        
        # Calculate AFP
        afp = ufp * vaf
        
        # Calculate Effort and Cost
        effort_hours = afp / productivity_rate
        total_cost = effort_hours * labour_cost_per_hour
        
        st.subheader("FPA Results")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("UFP", f"{ufp:.2f}", delta=None)
        with col2:
            st.metric("VAF", f"{vaf:.3f}", delta=None)
        with col3:
            st.metric("AFP", f"{afp:.2f}", delta=None)
        with col4:
            st.metric("Effort", f"{effort_hours:.2f} Hours", delta=None)
        with col5:
            st.metric("Total Cost", f"GBP {total_cost:,.2f}", delta=None)
        
        # Interactive Calculation Breakdown
        with st.expander("View Calculation Breakdown", expanded=True):
            st.markdown("### Step-by-Step Calculation")
            
            # Step 1: UFP Calculation
            st.markdown("**Step 1: Calculate Unadjusted Function Points (UFP)**")
            st.markdown("Formula: `UFP = Sum of (count × weight) for each function type`")
            
            ufp_calc_lines = []
            for func_type, (count, complexity) in function_inputs.items():
                weight = complexity_weights[complexity][func_type]
                points = ufp_breakdown[func_type]
                ufp_calc_lines.append(f"{func_type}: {count} × {weight} = {points}")
            
            st.markdown(f"""
            Calculation:
            ```
            {chr(10).join(ufp_calc_lines)}
            UFP = {ufp:.2f}
            ```
            """)
            
            # Step 2: TDI and VAF Calculation
            st.markdown("**Step 2: Calculate Total Degree of Influence (TDI) and Value Adjustment Factor (VAF)**")
            st.markdown("Formula: `VAF = (TDI × 0.01) + 0.65`")
            
            st.markdown(f"""
            System Characteristics Ratings:
            ```
            TDI = Sum of all 14 characteristic ratings
            TDI = {tdi}
            
            VAF = ({tdi} × 0.01) + 0.65
            VAF = {tdi * 0.01:.2f} + 0.65
            VAF = {vaf:.3f}
            ```
            """)
            
            # Step 3: AFP Calculation
            st.markdown("**Step 3: Calculate Adjusted Function Points (AFP)**")
            st.markdown(f"""
            Formula: `AFP = UFP × VAF`
            
            Calculation:
            ```
            AFP = {ufp:.2f} × {vaf:.3f}
            AFP = {afp:.2f}
            ```
            """)
            
            # Step 4: Effort Calculation
            st.markdown("**Step 4: Calculate Estimated Effort (Person-Hours)**")
            st.markdown(f"""
            Formula: `Effort = AFP / Productivity Rate`
            
            Calculation:
            ```
            Effort = {afp:.2f} / {productivity_rate}
            Effort = {effort_hours:.2f} Person-Hours
            ```
            """)
            
            # Step 5: Cost Calculation
            st.markdown("**Step 5: Calculate Total Project Cost**")
            st.markdown(f"""
            Formula: `Cost = Effort × Labour Cost per Hour`
            
            Calculation:
            ```
            Cost = {effort_hours:.2f} × {labour_cost_per_hour}
            Cost = GBP {total_cost:,.2f}
            ```
            """)
        
        # Visualisation
        col1, col2 = st.columns(2)
        with col1:
            # Function type breakdown
            func_breakdown = []
            for func_type, (count, complexity) in function_inputs.items():
                weight = complexity_weights[complexity][func_type]
                func_breakdown.append({"Type": func_type, "Count": count, "Weight": weight, "Points": count * weight})
            
            df_func = pd.DataFrame(func_breakdown)
            fig_func = px.bar(df_func, x="Type", y="Points", title="Function Points by Type",
                             color_discrete_sequence=["#1E3A8A"])
            st.plotly_chart(fig_func, use_container_width=True)
        
        with col2:
            # Cost breakdown
            cost_data = {
                "Category": ["Labour Cost", "Contingency (15%)"],
                "Amount": [total_cost, total_cost * 0.15]
            }
            df_cost = pd.DataFrame(cost_data)
            fig_cost = px.pie(df_cost, values="Amount", names="Category", title="Cost Breakdown",
                             color_discrete_sequence=["#1E3A8A", "#64748B"])
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Detailed breakdown
        st.subheader("Detailed Breakdown")
        breakdown_data = {
            "Parameter": ["Unadjusted Function Points (UFP)", "Total Degree of Influence (TDI)", 
                         "Value Adjustment Factor (VAF)", "Adjusted Function Points (AFP)", 
                         "Productivity Rate (AFP/Hour)", "Estimated Effort (Person-Hours)", 
                         "Labour Cost per Hour", "Total Project Cost"],
            "Value": [f"{ufp:.2f}", f"{tdi}", f"{vaf:.3f}", f"{afp:.2f}", 
                     f"{productivity_rate:.2f}", f"{effort_hours:.2f}", f"GBP {labour_cost_per_hour:.2f}", f"GBP {total_cost:,.2f}"]
        }
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

# --- Financial Tracking Module --- #
def financial_tracking():
    st.header("Financial Tracking and Labour Costs")
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    
    st.subheader("Add New Task")
    with st.form("new_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_name = st.text_input("Task Name")
        with col2:
            labour_cost_per_hour = st.number_input("Labour Cost per Hour (GBP)", min_value=0.0, value=50.0, step=5.0)
        with col3:
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, value=10.0, step=1.0)
        
        if st.form_submit_button("Add Task"):
            if not task_name:
                st.error("Task Name cannot be empty.")
            elif labour_cost_per_hour <= 0 or estimated_hours <= 0:
                st.error("Labour Cost per Hour and Estimated Hours must be positive numbers.")
            else:
                st.session_state.tasks.append({
                    "Task Name": task_name,
                    "Labour Cost/Hour": labour_cost_per_hour,
                    "Estimated Hours": estimated_hours,
                    "Total Cost": labour_cost_per_hour * estimated_hours
                })
                st.success(f"Task '{task_name}' added successfully.")
    
    st.subheader("Current Tasks and Costs")
    if st.session_state.tasks:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        st.dataframe(df_tasks, use_container_width=True, hide_index=True)
        
        total_project_cost = df_tasks["Total Cost"].sum()
        total_hours = df_tasks["Estimated Hours"].sum()
        avg_hourly_rate = total_project_cost / total_hours if total_hours > 0 else 0
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Estimated Hours", f"{total_hours:.2f}", delta=None)
        with col2:
            st.metric("Average Hourly Rate", f"GBP {avg_hourly_rate:.2f}", delta=None)
        with col3:
            st.metric("Total Project Cost", f"GBP {total_project_cost:,.2f}", delta=None)
        
        # Visualisation
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(df_tasks, values='Total Cost', names='Task Name', title='Cost Distribution by Task',
                            color_discrete_sequence=["#1E3A8A", "#64748B", "#94A3B8", "#CBD5E1"])
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(df_tasks, x='Task Name', y='Estimated Hours', title='Estimated Hours by Task',
                            color_discrete_sequence=["#1E3A8A"])
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Option to clear tasks
        if st.button("Clear All Tasks"):
            st.session_state.tasks = []
            st.rerun()
    else:
        st.info("No tasks added yet. Add a task to get started.")

# --- Main Navigation --- #
tab1, tab2, tab3 = st.tabs(["COCOMO Estimation", "Function Point Analysis", "Financial Tracking"])

with tab1
    cocomo_estimation()

with tab2:
    fpa_estimation()

with tab3:
    financial_tracking()
