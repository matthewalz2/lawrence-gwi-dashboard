import streamlit as st
from utils.data_loader import read_csv_fallback

st.set_page_config(layout="wide")

from utils.processing import (
    edu_attainment_processing,
    edu_enrollment_processing,
    edu_tech_access_processing,
    edu_internet_processing,
    age_gender_processing,
    demo_race_processing,
    demo_hispanic_processing,
    employ_labor_processing,
    employ_commute_processing,
    employ_commute_length_processing,
    employ_gender_earnings_processing,
    employ_ed_earnings_processing,
    demo_hispanic_processing,
)

from utils.visualization import (
    plot_attainment,
    plot_enrollment,
    plot_tech_access,
    plot_internet,
    plot_age_gender,
    plot_race,
    plot_commute,
    plot_labor,
    plot_com_length,
    plot_hispanic,
)


st.title("Lawrence Community Metrics")
st.write("The data was downloded from ACS.")

try:
    edu = read_csv_fallback("data/Lawrence_Education.csv")
    demo = read_csv_fallback("data/Lawrence_Demographics.csv")
    employ = read_csv_fallback("data/Lawrence_Employment.csv")
except Exception as e:
    st.error(f"Failed to load CSV files: {e}")
    st.stop()

# save cleaned datasets as variables
# Education
cleaned_edu_attainment = edu_attainment_processing(edu)
cleaned_edu_enrollment = edu_enrollment_processing(edu)
cleaned_edu_tech_access = edu_tech_access_processing(edu)
cleaned_edu_internet = edu_internet_processing(edu)

# Demographics
cleaned_demo_age_gender = age_gender_processing(demo)
cleaned_demo_race = demo_race_processing(demo)
cleaned_demo_hispanic = demo_hispanic_processing(demo)

# Economics/Employment
cleaned_employ_labor = employ_labor_processing(employ)
cleaned_employ_commute = employ_commute_processing(employ)
cleaned_employ_com_length = employ_commute_length_processing(employ)
cleaned_employ_gender_earnings = employ_gender_earnings_processing(employ)
cleaned_employ_ed_earnings = employ_ed_earnings_processing(employ)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Demographics", "Education", "Economics", "Health", "Housing"]
)


# Tab control for the main display
# with tab1:
#     st.header("Welcome to the Lawrence GWI Dashboard")
with tab1:
    st.header("Demographics")
    fig = plot_age_gender(cleaned_demo_age_gender)
    fig2 = plot_race(cleaned_demo_race)
    fig3 = plot_hispanic(cleaned_demo_hispanic)

    # Age Gender
    st.subheader("Gender Age Distribution")
    st.caption(
        "Lawrence has a relatively young population, with the largest age cohort being adults ages 25–34 (14,419 residents). Population counts remain high through the 35–44, 45–54, and 55–64 age groups before declining steadily among older residents. The city shows a fairly balanced gender distribution overall, though males slightly outnumber females in most groups under age 35, while females become more prevalent in older age groups. Residents ages 10–64 represent the largest share of the population, indicating a substantial working-age community. The smallest populations are found among residents ages 75–84 and 85+, reflecting the youthful demographic profile of the city"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(cleaned_demo_age_gender)

    st.divider()

    # Race
    st.subheader("Racial Distribution")
    st.caption(
        """Lawrence's population is primarily concentrated in the "Some other race alone" and "White alone" categories, with smaller Black, Asian, and Indigenous populations. The large "Some other race alone" category is likely influenced by the city's substantial Hispanic and Latino population, as many Hispanic respondents identify with an ethnicity rather than a traditional Census racial category. This highlights the importance of considering both race and ethnicity when examining Lawrence's demographic makeup."""
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.dataframe(cleaned_demo_race)

    st.divider()

    # Hispanic
    st.subheader("Hispanic Population")
    st.caption(
        """Lawrence's Hispanic population is predominantly Dominican, with 46,138 residents identifying as Dominican—nearly three times the size of the next-largest group, Puerto Ricans (15,769). Central American (5,677) and Guatemalan (3,711) populations represent smaller but notable communities, while Salvadoran, South American, and Mexican populations each account for a relatively small share of residents. Together, these figures illustrate Lawrence's strong Dominican cultural presence while highlighting the diversity of Hispanic backgrounds represented throughout the city."""
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.dataframe(cleaned_demo_hispanic)

with tab2:
    st.header("Education")

    fig = plot_attainment(cleaned_edu_attainment)
    fig2 = plot_enrollment(cleaned_edu_enrollment)
    fig3 = plot_tech_access(cleaned_edu_tech_access)
    fig4 = plot_internet(cleaned_edu_internet)

    # Education Attainment
    st.subheader("Educational Attainment")
    st.caption(
        "Most residents have either a regular high school diploma or some level of college experience, making these the most common educational outcomes in the community. A substantial number of individuals have not completed high school, while bachelor's degree holders represent a significant portion of the population. In contrast, advanced degrees such as master's, professional, and doctoral degrees are relatively rare. Overall, the population is primarily composed of individuals with high school-level education, some college education, or bachelor's degrees, with fewer residents holding graduate-level credentials."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(cleaned_edu_attainment, use_container_width=True)

    st.divider()

    # Student Enrollment
    st.subheader("Student Enrollment Distribution")
    st.caption(
        "Enrollment is concentrated in the K–12 education system, with the largest groups of students attending grades 5–8, grades 9–12, and grades 1–4. Preschool and kindergarten enrollment is noticeably smaller, reflecting the narrower age range of those programs. College and university enrollment remains substantial, indicating that many residents continue their education beyond high school, while graduate and professional school enrollment represents a much smaller portion of the student population. Overall, the data suggests a community with a strong school-age population and continued participation in higher education."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.dataframe(cleaned_edu_enrollment, use_container_width=True)

    st.divider()

    # Technology Access
    st.subheader("Household Technology Access")
    st.caption(
        "Digital device ownership is widespread within Lawrence. Most households report having a computer or smartphone, with smartphones being nearly as common as general computer access. Desktop and laptop computers remain widely used, while tablets and other portable wireless devices are somewhat less common. Only a small portion of the population reports having no computer access at all, indicating that the community is generally well connected to digital technology and communication tools."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.dataframe(cleaned_edu_tech_access, use_container_width=True)

    st.divider()

    # Internet Access
    st.subheader("Household Internet Access")
    st.caption(
        "Internet access data indicates that most households in Lawrence have access to the internet through a subscription service. Broadband connections and cellular data plans are both widely used, suggesting strong connectivity across the community. Traditional broadband services such as cable, fiber optic, or DSL remain common, while only a small number of households rely on internet access without a subscription. Although internet access is widespread, a notable portion of households still report having no internet access, highlighting a remaining digital divide within the city."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.dataframe(cleaned_edu_internet, use_container_width=True)

with tab3:
    male_workers = cleaned_employ_gender_earnings.loc[
        cleaned_employ_gender_earnings["groups"] == "Male full-time year-round workers",
        "values",
    ].iloc[0]

    male_salary = cleaned_employ_gender_earnings.loc[
        cleaned_employ_gender_earnings["groups"] == "Male: Median earnings (dollars)",
        "values",
    ].iloc[0]

    female_workers = cleaned_employ_gender_earnings.loc[
        cleaned_employ_gender_earnings["groups"]
        == "Female full-time year-round workers",
        "values",
    ].iloc[0]

    female_salary = cleaned_employ_gender_earnings.loc[
        cleaned_employ_gender_earnings["groups"] == "Female: Median earnings (dollars)",
        "values",
    ].iloc[0]

    st.subheader("Earnings by Gender")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Male Full-Time Workers", f"{male_workers:,.0f}")

    with col2:
        st.metric("Female Full-Time Workers", f"{female_workers:,.0f}")

    with col3:
        st.metric("Male Median Earnings", f"${male_salary:,.0f}")

    with col4:
        st.metric("Female Median Earnings", f"${female_salary:,.0f}")

    st.divider()

    # Education Earnings
    less_than_hs_salary = cleaned_employ_ed_earnings.loc[
        cleaned_employ_ed_earnings["groups"] == "Less than high school graduate",
        "values",
    ].iloc[0]

    hs_salary = cleaned_employ_ed_earnings.loc[
        cleaned_employ_ed_earnings["groups"]
        == "High school graduate (includes equivalency)",
        "values",
    ].iloc[0]

    some_college_salary = cleaned_employ_ed_earnings.loc[
        cleaned_employ_ed_earnings["groups"] == "Some college or associate's degree",
        "values",
    ].iloc[0]

    bachelor_salary = cleaned_employ_ed_earnings.loc[
        cleaned_employ_ed_earnings["groups"] == "Bachelor's degree", "values"
    ].iloc[0]

    grad_salary = cleaned_employ_ed_earnings.loc[
        cleaned_employ_ed_earnings["groups"] == "Graduate or professional degree",
        "values",
    ].iloc[0]

    st.subheader("Earnings by Education Level")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Less Than High School", f"${less_than_hs_salary:,.0f}")

    with col2:
        st.metric("High School Graduate", f"${hs_salary:,.0f}")

    with col3:
        st.metric("Some College", f"${some_college_salary:,.0f}")

    with col4:
        st.metric("Bachelor's Degree", f"${bachelor_salary:,.0f}")

    with col5:
        st.metric("Graduate Degree", f"${grad_salary:,.0f}")

    st.divider()
    # Labor Force
    st.subheader("Labor Force Distribution")
    st.caption(
        "Most Lawrence residents age 16 and older are employed, with 61.8% (41,147 people) working in civilian jobs. About 31.0% (20,665 people) are not in the labor force, while 7.2% (4,775 people) are unemployed and actively seeking work. Military service represents a very small share of the population. Overall, nearly 69% of residents participate in the labor force, indicating strong workforce engagement."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(plot_labor(cleaned_employ_labor), use_container_width=True)

    with col2:
        st.dataframe(cleaned_employ_labor, use_container_width=True)

    st.divider()

    # Commute
    st.subheader("Commute Patterns")
    st.caption(
        "Transportation in Lawrence is heavily dominated by personal vehicles. Most workers commute by driving alone (27,783 people), while carpooling (5,491 people) is the second most common method. Smaller numbers of residents work from home (1,747), walk (1,431), or use public transportation, such as buses and rail services. Overall, commuting by car is by far the primary mode of transportation for workers in the city."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(plot_commute(cleaned_employ_commute), use_container_width=True)

    with col2:
        st.dataframe(cleaned_employ_commute, use_container_width=True)

    st.divider()

    # Commute Length
    st.subheader("Commute Length")
    st.caption(
        "Most workers in Lawrence have relatively short commutes, with the largest groups traveling 10–14 minutes (8,144 people) and 15–19 minutes (7,050 people) to work. Commutes of 20–24 minutes (5,563 people) and 30–34 minutes (4,158 people) are also common. While some residents travel 45 minutes or more, long commutes are less frequent overall, indicating that many workers live fairly close to their workplaces."
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(
            plot_com_length(cleaned_employ_com_length), use_container_width=True
        )

    with col2:
        st.dataframe(cleaned_employ_com_length, use_container_width=True)
with tab4:
    st.header("Health")
with tab5:
    st.header("Housing")
