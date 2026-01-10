import streamlit as st #Web app UI
import pandas as pd #For data manipulation
import matplotlib.pyplot as plt #For plotting pie chart
from utils.ai_helper import generate_itinerary #Flan-T5
from utils.pdf_helper import generate_budget_pdf #PDF generation

st.set_page_config(page_title="TripMate for Campus", layout="wide")

st.title("🎒 TripMate for Campus")
st.subheader("AI-Powered Travel Planner for College Students")

st.markdown("---")

# =========================
# Trip Input Form
# =========================
st.markdown("## 📝 Trip Details")
st.write(
    "Fill in the trip details below to generate a personalized "
    "campus travel plan."
)
with st.form("trip_form"):
    col1, col2 = st.columns(2)

    with col1:
        from_location = st.text_input("From (Starting Location)")
        to_location = st.text_input("To (Destination)")
        travel_month = st.selectbox(
            "Planned Month",
            [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
        )

    with col2:
        num_students = st.number_input(
            "Number of Students",
            min_value=1,
            max_value=500,
            value=20
        )
        num_days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=15,
            value=3
        )
        max_budget = st.number_input(
            "Maximum Budget (₹)",
            min_value=1000,
            step=1000,
            value=150000
        )

    location_types = st.multiselect(
        "Preferred Location Types",
        [
            "Nature",
            "Heritage",
            "Industry Visit",
            "Theme Park",
            "Adventure",
            "Religious"
        ]
    )

    submit = st.form_submit_button("🚀 Generate Trip Plan")

# =========================
# OUTPUT SECTION
# =========================
if submit:
    st.success("Trip plan generated successfully!")
    

    
    # =========================
    # Trip Summary
    # =========================
    st.markdown("## 🧭 TripMate for Campus – Trip Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("From", from_location)
    col2.metric("To", to_location)
    col3.metric("Travel Month", travel_month)

    col4, col5, col6 = st.columns(3)
    col4.metric("Students", num_students)
    col5.metric("Days", num_days)
    col6.metric("Max Budget", f"₹{max_budget:,}")

    st.markdown("---")
    
    # ======================================================================
    # Itinerary AI Generation using HuggingFace Inference API - Llama 3.2
    # ======================================================================
    st.markdown("## 🗓️ Day-wise Itinerary")

    prompt = f"""
    INPUT:
    From: {from_location}
    To: {to_location}
    Travel Month: {travel_month}
    Students: {num_students}
    Days: {num_days}
    Preferences: {location_types}

    TASK:
    Generate a {num_days}-day travel itinerary for college students.
    
    Rules:
    - Do NOT mention prices, costs, budget, or money
    - Focus only on travel flow, places, meals, and activities
    - Write clearly for students
    - Cover all {num_days} days

    OUTPUT FORMAT:
    Day 1:
    - Morning:
    - Afternoon:
    - Evening:

    Day 2:
    - Morning:
    - Afternoon:
    - Evening:

    (continue until Day {num_days})

    OUTPUT:
    """

    with st.spinner("🤖 Generating itinerary using AI..."):
        ai_itinerary = generate_itinerary(prompt)

    st.write(ai_itinerary)
    st.markdown("---")
        
   # =========================
    # Stay Suggestion Logic
    # =========================

    nights = max(num_days - 1, 1)

    if num_students <= 10:
        stay_type = "Homestay"
        stay_rate = 900
        stay_note = "Best for small student groups and local experience"
    elif num_students <= 40:
        stay_type = "Budget Hotel"
        stay_rate = 1200
        stay_note = "Comfortable option for medium-sized student groups"
    elif num_students <= 100:
        stay_type = "Lodge / Dormitory"
        stay_rate = 800
        stay_note = "Cost-effective option for large student groups"
    else:
        stay_type = "Hostel / Group Accommodation"
        stay_rate = 600
        stay_note = "Most economical option for very large groups"

    recommended_stay_cost = stay_rate * num_students * nights

    # =========================
    # Stay Suggestions
    # =========================
    st.markdown("## 🏨 Stay Suggestions")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Recommended Stay Type", stay_type)
        st.write(stay_note)

    with col2:
        st.metric("Cost per Student / Night", f"₹{stay_rate}")
        st.metric("Total Stay Cost", f"₹{recommended_stay_cost:,}")

    st.info(
        f"Stay cost is calculated for {num_students} students "
        f"for {nights} night(s)."
    )

    st.markdown("---")

   

    # =====================================================
    # Distance Estimation logic (Region-based)
    # =====================================================

    same_state_distance = 500
    neighbor_state_distance = 700
    far_state_distance = 2000

    kerala_cities = [
        "Kochi", "Trivandrum", "Thiruvananthapuram", "Kozhikode",
        "Kannur", "Wayanad", "Thrissur", "Alappuzha", "Kollam"
    ]

    from_in_kerala = from_location.strip().title() in kerala_cities
    to_in_kerala = to_location.strip().title() in kerala_cities

    if from_in_kerala and to_in_kerala:
        estimated_distance_km = same_state_distance
    elif from_in_kerala or to_in_kerala:
        estimated_distance_km = neighbor_state_distance
    else:
        estimated_distance_km = far_state_distance

    # =====================================================
    # Transport Cost per KM logic (Group-based)
    # =====================================================

    if num_students <= 15:
        cost_per_km = 22   # Tempo Traveller
    elif num_students <= 40:
        cost_per_km = 18   # Mini Bus
    elif num_students <= 100:
        cost_per_km = 15   # Large Bus
    else:
        cost_per_km = 14   # Multiple Buses

    # =====================================================
    # Food Cost per Student per Day logic (Budget-based)
    # =====================================================

    budget_per_student_per_day = max_budget / (num_students * num_days)

    if budget_per_student_per_day <= 500:
        food_cost_per_day = 300
        type_of_food = "Basic Meals"
    elif budget_per_student_per_day <= 800:
        food_cost_per_day = 400
        type_of_food = "Standard Meals"
    else:
        food_cost_per_day = 550
        type_of_food = "Premium Meals"

    # =====================================================
    # Misc Cost per Student logic (Based on Location Types)
    # =====================================================

    misc_cost_map = {
        "Nature": 200,
        "Heritage": 250,
        "Industry Visit": 150,
        "Theme Park": 500,
        "Adventure": 600,
        "Religious": 150
    }

    if location_types:
        misc_cost_per_student = max(
            misc_cost_map.get(loc, 200) for loc in location_types
        )
    else:
        misc_cost_per_student = 200
        
    # =========================
    # Budget calculations
    # =========================
    transport_cost = estimated_distance_km * cost_per_km
    food_cost = food_cost_per_day * num_students * num_days
    misc_cost = misc_cost_per_student * num_students

    used_budget = transport_cost + recommended_stay_cost + food_cost + misc_cost

    usage_percent = int((used_budget / max_budget) * 100) if max_budget > 0 else 0
    remaining_percent = max(0, 100 - usage_percent)
    #--------- per student calculations ---------
    transport_per_student = transport_cost / num_students
    stay_per_student = recommended_stay_cost / num_students
    food_per_student = food_cost / num_students
    misc_per_student = misc_cost / num_students
    total_per_student = used_budget / num_students
    
    
    # =========================
    # Budget Usage Visualization
    # =========================
    st.markdown("## 📊 Budget Usage")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"₹{used_budget:,}")
    if usage_percent > 100:
        col2.metric("Used %", f"{usage_percent}%")
        col2.error("⚠️ Budget Exceeded")
    else:
        col2.metric("Used %", f"{usage_percent}%")
    col3.metric("Remaining %", f"{remaining_percent}%")
    if usage_percent < 100:
        st.progress(usage_percent / 100)

    st.markdown("---")

    # =======================================
    # Budget Distribution (piechart)
    # =======================================
    
    st.markdown("## 💰 Estimated Budget Breakdown")

    col1, col2 = st.columns(2)
    with col1:
        st.write(
            f"🚍 **Transportation:** ₹{transport_cost:,}  (₹{int(transport_per_student):,} / student)"
        )

        st.write(
            f"🏨 **Stay:** ₹{recommended_stay_cost:,}  (₹{int(stay_per_student):,} / student)"
        )

        st.write(
            f"🍽️ **Food:** ₹{food_cost:,}  (₹{int(food_per_student):,} / student)"
        )

        st.write(
            f"🎟️ **Entry & Misc:** ₹{misc_cost:,}  (₹{int(misc_per_student):,} / student)"
        )
        st.write(
            f"🧑 **Total Estimated Cost/Student: ₹{int(total_per_student):,} per student**"
        )

    with col2:
        st.metric(
            "Total Estimated Cost",
            f"₹{used_budget:,}"
        )
        

        if usage_percent > 100:
            st.metric("Budget Utilization", f"{usage_percent}%")
            st.error("⚠️ Budget Exceeded")
        else:
            st.metric("Budget Utilization", f"{usage_percent}%")

    st.info(
        f"Food costs are estimated for {num_students} students across {num_days} days, "
        f"aligned with the ₹{max_budget:,} budget, resulting in a {type_of_food} meal plan."
    )

    st.markdown("---")
    # =========================================
    # Cost Breakdown & Budget Distribution
    # =========================================
    st.markdown("## 💰 Cost Breakdown & Distribution")

    cost_df = pd.DataFrame({
        "Category": ["Transportation", "Stay", "Food", "Entry & Misc"],
        "Cost": [transport_cost, recommended_stay_cost, food_cost, misc_cost]
    })

    col1, col2 = st.columns(2)

    # ----- Bar Chart -----
    with col1:
        st.markdown("### 📊 Cost Breakdown")
        st.bar_chart(cost_df.set_index("Category"))

    # ----- Pie Chart -----
    with col2:
        st.markdown("### 🥧 Budget Distribution")

        fig, ax = plt.subplots(figsize=(4, 4))
        cost_df.set_index("Category").plot.pie(
            y="Cost",
            autopct="%1.1f%%",
            legend=False,
            ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    st.markdown("---")


    # ==========================================================================
    # Alternative Budget Options (Derived from Food & Stay Logics used above)
    # ==========================================================================

    # Food tiers (already aligned with the food conditions coded above)
    food_tiers = {
        "Basic Meals": 300,
        "Standard Meals": 400,
        "Premium Meals": 550
    }
    # Stay tiers (derived from stay_type and stay_rate used above)
    budget_food_rate = food_tiers["Basic Meals"]
    mid_food_rate = food_cost_per_day
    premium_food_rate = food_tiers["Premium Meals"]
    # Stay tiers (derived from stay_rate used above)
    budget_stay_rate = max(stay_rate - 300, 600)
    mid_stay_rate = stay_rate
    premium_stay_rate = stay_rate + 800

    options = [
        {
            "Option": "Budget",
            "Stay Type": "Economy Stay",
            "Stay Rate": budget_stay_rate,
            "Food Type": "Basic Meals",
            "Food Rate": budget_food_rate
        },
        {
            "Option": "Mid-Range (Recommended)",
            "Stay Type": stay_type,
            "Stay Rate": mid_stay_rate,
            "Food Type": type_of_food,
            "Food Rate": mid_food_rate
        },
        {
            "Option": "Premium",
            "Stay Type": "Premium Hotel / Resort",
            "Stay Rate": premium_stay_rate,
            "Food Type": "Premium Meals",
            "Food Rate": premium_food_rate
        }
    ]

    option_rows = []

    for opt in options:
        total_cost = (
            transport_cost
            + (opt["Stay Rate"] * num_students * nights)
            + (opt["Food Rate"] * num_students * num_days)
            + misc_cost
        )

        option_rows.append({
            "Option": opt["Option"],
            "Accommodation": opt["Stay Type"],
            "Food": opt["Food Type"],
            "Total Cost (₹)": total_cost
        })

    options_df = pd.DataFrame(option_rows)

    # ===================================================
    # Alternative Budget Options chart and analysis
    # ===================================================
    st.markdown("## 🔁 Alternative Budget Options")
    col_chart, col_analysis = st.columns([3, 7])

    # -------- Bar Chart --------
    with col_chart:
        st.markdown("### 📊 Cost Comparison")
        st.bar_chart(options_df.set_index("Option")["Total Cost (₹)"])

    # -------- Analysis  --------
    with col_analysis:
        st.markdown("### 🧠 Option Analysis")

        subcols = st.columns(3)

        for idx, (_, row) in enumerate(options_df.iterrows()):
            with subcols[idx]:
                if "Recommended" in row["Option"]:
                    st.markdown(f"### ⭐ {row['Option']}")
                else:
                    st.markdown(f"### {row['Option']}")

                st.write(f"🏨 **Stay:** {row['Accommodation']}")
                st.write(f"🍽️ **Food:** {row['Food']}")
                st.write(f"💰 **Total:** ₹{row['Total Cost (₹)']:,}")

                if row["Total Cost (₹)"] <= max_budget:
                    st.success("✔ Within Budget")
                else:
                    st.error("✖ Exceeds Budget")

    # =========================
    # Download Section
    # =========================
    st.markdown("## 📥 Downloads")

    budget_text = f"""
    TRIPMATE FOR CAMPUS – BUDGET SUMMARY
    ==================================

    Trip Overview
    -------------
    From            : {from_location}
    To              : {to_location}
    Travel Month    : {travel_month}
    Students        : {num_students}
    Days            : {num_days}
    Preferences     : {", ".join(location_types) if location_types else "Not specified"}

    ----------------------------------
    COST BREAKDOWN (TOTAL)
    ----------------------------------
    Transportation  : Rs. {transport_cost:,}
    Stay            : Rs. {recommended_stay_cost:,}
    Food            : Rs. {food_cost:,}
    Entry & Misc    : Rs. {misc_cost:,}

    TOTAL COST      : Rs. {used_budget:,}

    ----------------------------------
    PER STUDENT COST
    ----------------------------------
    Transportation  : Rs. {int(transport_per_student):,}
    Stay            : Rs. {int(stay_per_student):,}
    Food            : Rs. {int(food_per_student):,}
    Entry & Misc    : Rs. {int(misc_per_student):,}

    TOTAL / STUDENT : Rs. {int(total_per_student):,}

    ----------------------------------
    FOOD & STAY 
    ----------------------------------
    Food Type       : {type_of_food}
    Food Cost       : Rs. {food_cost_per_day} per student per day

    Stay Type       : {stay_type}
    Stay Cost       : Rs. {stay_rate} per student per night
    Nights          : {nights}

    ----------------------------------
    ALTERNATIVE OPTIONS
    ----------------------------------
    """
    for _, row in options_df.iterrows():
        status = (
            "WITHIN BUDGET"
            if row["Total Cost (₹)"] <= max_budget
            else "EXCEEDS BUDGET"
        )

        budget_text += f"""
    {row['Option']}
    ----------------
    Accommodation   : {row['Accommodation']}
    Food             : {row['Food']}
    Total Cost       : Rs. {row['Total Cost (₹)']:,}
    Status           : {status}
    """

    #--- Itinerary section---
    itinerary_text = f"""
    TRIPMATE FOR CAMPUS – ITINERARY
    ==============================

    From         : {from_location}
    To           : {to_location}
    Travel Month : {travel_month}
    Students     : {num_students}
    Days         : {num_days}

    --------------------------------
    DAY-WISE ITINERARY
    --------------------------------

    {ai_itinerary}

    ================================
    Generated by TripMate for Campus
    """

    combined_text = itinerary_text + "\n\n" + budget_text


    for _, row in options_df.iterrows():
        budget_text += f"""
    {row['Option']}
    Stay           : {row['Accommodation']}
    Food           : {row['Food']}
    Total Cost     : Rs. {row['Total Cost (₹)']:,}
    """

    budget_text += f"""
    ----------------------------------
    BUDGET UTILIZATION
    ----------------------------------
    Maximum Budget  : Rs. {max_budget:,}
    Used Percentage : {usage_percent}%
    Status          : {"EXCEEDED" if usage_percent > 100 else "WITHIN BUDGET"}

    ==================================
    Generated by TripMate for Campus
    """
    col1, col2 = st.columns(2)

    # ---------- Itinerary button ----------
    with col1:
        itinerary_pdf = "TripMate_Itinerary.pdf"
        generate_budget_pdf(itinerary_pdf, itinerary_text)

        with open(itinerary_pdf, "rb") as f:
            st.download_button(
                label="📄 Download Itinerary (PDF) and Plan New Trip",
                data=f,
                file_name="TripMate_Itinerary.pdf",
                mime="application/pdf"
            )

    # ---------- Itinerary + Budget button ----------
    with col2:
        combined_pdf = "TripMate_Itinerary_And_Budget.pdf"
        generate_budget_pdf(combined_pdf, combined_text)

        with open(combined_pdf, "rb") as f:
            st.download_button(
                label="📄 Download Itinerary + Budget (PDF) and Plan New Trip",
                data=f,
                file_name="TripMate_Itinerary_And_Budget.pdf",
                mime="application/pdf"
            )