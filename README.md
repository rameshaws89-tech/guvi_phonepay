
# 📊 PhonePe Pulse: Data Visualization & Business Analysis

A professional **Streamlit** dashboard designed to transform raw PhonePe Pulse data into actionable business insights. This project uses a **MySQL** backend to store processed data and **Plotly** to create interactive visualizations for strategic decision-making.

## 🛠️ Technical Architecture
This application is built entirely using the Python ecosystem:
*   **Data Processing:** `Pandas` for cleaning and handling complex SQL types (Decimal to Float conversion).
*   **Database:** `MySQL` with `SQLAlchemy` for robust data storage and retrieval.
*   **Dashboard:** `Streamlit` for a high-performance, interactive user interface.
*   **Visualization:** `Plotly Express` for dynamic maps, treemaps, and bubble charts.

---

## 🚀 The 5 Business Scenarios

The dashboard is structured into five distinct analytical modules:

### 1. Transaction Value by State 🌍
*   **Objective:** Geographical analysis of transaction volume across India.
*   **Logic:** Uses a **Choropleth Map** to show the "Transaction Heat" of each state.

### 2. Device Dominance & Engagement 📱
*   **Objective:** Understand which mobile brands drive app usage.
*   **Logic:** Calculates the ratio of **App Opens** to **Registered Users**. Identifies "Underutilized Brands."

### 3. Insurance Penetration Analysis 🛡️
*   **Objective:** Prioritize regions for the new Insurance segment.
*   **Logic:** Uses a **Bubble Chart** to plot Total Users (X) vs. Penetration Rate (Y).

### 4. Market Expansion Study 📈
*   **Objective:** Identify the next high-growth region for investment.
*   **Logic:** Implements a **Treemap** where box size represents market size and color represents Average Ticket Value (ATV).

### 5. User Engagement & Growth Strategy 🎯
*   **Objective:** Improve user retention at the district level.
*   **Logic:** A ranked **Bar Chart** showing an "Engagement Score" (Opens per User) to pinpoint passive markets.

---

## 💻 Installation & Usage

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/rameshaws89-tech/guvi_phonepay.git
    ```
2.  **Install Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch the App:**
    ```bash
    streamlit run app.py
    ```



