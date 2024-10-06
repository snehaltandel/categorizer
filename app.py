import streamlit as st
import pandas as pd
from io import BytesIO

# Set the page configuration
st.set_page_config(
    page_title="Category Tagger",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title of the app
st.title("📂 File Category Tagger")

# Description
st.markdown("""
This application allows you to upload a CSV or Excel file, assign categories to each row from a predefined list, and download the updated file with the new category column.
""")

# Sidebar for category selection
st.sidebar.header("Settings")

# Predefined categories
cat_df = pd.read_excel("./data/Categories.xlsx")
PREDEFINED_CATEGORIES = cat_df["Custom Categories"].unique().tolist()
# PREDEFINED_CATEGORIES = ["Category A", "Category B", "Category C", "Category D"]

# Function to convert dataframe to bytes
def convert_df(df, file_type):
    if file_type == "CSV":
        return df.to_csv(index=False).encode('utf-8')
    else:
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        return output.getvalue()

# File uploader
uploaded_file = st.file_uploader(
    "📁 Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    # Determine file type
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.stop()

    st.success("File uploaded successfully!")

    st.markdown("### 📊 Preview of the Uploaded File:")
    
    # Display the dataframe with an editable category column
    if 'Category' not in df.columns:
        df['Category'] = None  # Initialize the Category column if it doesn't exist

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=PREDEFINED_CATEGORIES,
                help="Select a category for each row."
            )
        }
    )

    # Button to download the modified file
    st.markdown("### 📥 Download the Updated File:")
    
    # Choose file type for download
    download_file_type = st.selectbox(
        "Select the file type for download",
        ("CSV", "Excel"),
        index=0
    )
    
    # Convert the edited dataframe to bytes
    try:
        if download_file_type == "CSV":
            file_bytes = edited_df.to_csv(index=False).encode('utf-8')
            mime = 'text/csv'
            file_extension = 'csv'
        else:
            output = BytesIO()
            edited_df.to_excel(output, index=False, engine='openpyxl')
            file_bytes = output.getvalue()
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            file_extension = 'xlsx'
    except Exception as e:
        st.error(f"Error processing the file for download: {e}")
        st.stop()
    
    st.download_button(
        label="🔽 Download Updated File",
        data=file_bytes,
        file_name=f"updated_file.{file_extension}",
        mime=mime
    )

    # Optionally, display the updated dataframe
    st.markdown("### 📝 Updated Data Preview:")
    st.dataframe(edited_df)
    
else:
    st.info("Awaiting file upload. Please upload a CSV or Excel file to proceed.")

# Footer
st.markdown("""
---
Developed with ❤️ using [Streamlit](https://streamlit.io/)
""")
