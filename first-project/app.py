import streamlit as st
import pandas as pd
import os

from io import BytesIO

st.set_page_config(page_title="Data Sweeper" , layout="wide")
st.title("Data Sweeper")
st.write("transform your files between csv and excel file formats ")


uploaded_files = st.file_uploader("Upload your files" , type=["csv" , "xlsx"], accept_multiple_files=True)

if uploaded_files :
    for file in uploaded_files:
        file_extension  = os.path.splitext(file.name)[-1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension ==".xlsx":
            df= pd.read_excel(file)

        else:
            st.error(f"usupported file type : {file_extension}")

        st.write(f"**File name** : {file.name}")
        st.write(f"**File Size** : {file.size/1024}")

        st.write("Preview the Head of the frame")
        st.dataframe(df.head())

        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            cl1, cl2 = st.columns(2)

            with cl1:
                if st.button(f"remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed")

            with cl2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values are filled")

        st.subheader("Select columns to convert")
        columns = st.multiselect(f"Select columns to convert : {file.name} " , df.columns , default=df.columns)
        df = df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :4])


        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to :" , ["CSV" , "Excel"] , key=file.name)
        if st.button (f"{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer ,index=False)
                file.name  = file.name.replace(file_extension , ".csv")
                mime_type = "text/csv"
                
            elif conversion_type == "Excel" :
                df.to_excel(buffer ,index=False)
                file.name  = file.name.replace(file_extension , ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(label = f"Download {file.name} as {conversion_type}",
            data =buffer,
            file_name = file.name,
            mime=mime_type)

    st.success("All files processed!")
                
