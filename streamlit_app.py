import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("education_income.csv")
st.subheader("Average Income by Education Level and Country")
pivot_df = df.pivot(index ="Country", columns ="Education Level", values="Average Income")
st.dataframe(pivot_df)

#Plot using matplotlib for grouped bars

fig, ax = plt.subplots()
pivot_df.plot(kind="bar", ax=ax)
plt.ylabel("Income in Euro")
plt.title("Income by Education Level and Country")
st.pyplot(fig)

# Dropdown-Auswahl mit allen Ländern erstellen

country_options = df["Country"].unique()
selected_country = st.selectbox("Select a country", country_options)

filtered_df = df[df["Country"] == selected_country]
grouped_filtered = filtered_df.groupby("Education Level")["Average Income"].mean()

st.subheader(f"Average Income in {selected_country}")

# Balkendiagramm für das gewählte Land anzeigen
st.bar_chart(grouped_filtered)

df_display =df.copy()

df_display["Average Income"] = df_display["Average Income"].apply(lambda x:f"Euro{x:,.0f}")

st.dataframe(df_display)

# Download-Button anbieten, um den Original-Datensatz als CSV herunterzuladen
st.download_button(
    "Download Dataset as CSV",
    data=df.to_csv(index=False),
    file_name="education_income.csv",
    mime="text/csv"
)
