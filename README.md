# Automated Software Project Cost Estimation Tool

This application is a comprehensive tool designed to assist project managers and software developers in estimating project costs, effort, and duration using industry-standard models. Built with Streamlit, it provides an interactive and user-friendly interface for cost estimation and financial tracking.

## Features

### 1. COCOMO Estimation Module
The Constructive Cost Model (COCOMO) is used to estimate the effort, duration, and staffing required for a software project based on its size (in KLOC - Thousands of Lines of Code) and type (Organic, Semi-Detached, or Embedded).
- **Effort Calculation**: Predicts person-months based on project complexity.
- **Duration Prediction**: Estimates the total months required for project completion.
- **Staffing Estimation**: Calculates the average number of staff members needed.
- **Visual Breakdown**: Provides a bar chart visualization of the estimation metrics.

### 2. Function Point Analysis (FPA) Module
FPA measures the functional size of an information system based on the functionality provided to the user.
- **Functional Inputs**: Allows input for External Inputs (EI), External Outputs (EO), External Inquiries (EQ), Internal Logical Files (ILF), and External Interface Files (EIF).
- **Adjustment Factors**: Includes a Value Adjustment Factor (VAF) and productivity rate for more accurate estimations.
- **Calculated Metrics**: Outputs Unadjusted Function Points (UFP), Adjusted Function Points (AFP), and Estimated Effort.
- **Visual Analysis**: Displays a bar chart for functional point breakdown.

### 3. Financial Tracking and Labor Costs
A dedicated module for tracking specific tasks and their associated costs.
- **Task Management**: Add tasks with their name, labor cost per hour, and estimated hours.
- **Real-time Cost Calculation**: Automatically calculates the total cost per task and for the entire project.
- **Cost Distribution**: Features a pie chart showing the distribution of costs across different tasks.

## Installation and Setup

To run this application locally, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Install Dependencies**:
    Ensure you have Python installed, then install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Technologies Used

- **Streamlit**: For the interactive web interface.
- **Pandas**: For data manipulation and organization.
- **Plotly Express**: For generating dynamic and interactive charts.
- **Python**: The core programming language.

## Customization

The application features a custom "RGB and Black" theme with specialized CSS to enhance the user experience, including:
- High-contrast color schemes for better readability.
- Custom styled buttons, input fields, and navigation tabs.
