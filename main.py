import streamlit as st
import pandas as pd
from utils import perform_search, get_data_statistics

st.set_page_config(
    page_title="CSV Visualizer",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("CSV Visualizer and Analyzer 📊")
    
    # File upload section
    st.header("1. Upload your CSV file")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            # Display basic information
            st.header("2. Data Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Total rows: {len(df)}")
            with col2:
                st.write(f"Total columns: {len(df.columns)}")
            
            # Statistics section
            st.header("3. Data Statistics")
            stats = get_data_statistics(df)
            st.write(stats)
            
            # Search section
            st.header("4. Search and Filter")
            search_terms = st.text_input(
                "Enter search terms (separate multiple terms with spaces)",
                help="The search will return rows containing ALL entered terms"
            )
            
            # Column filter
            st.subheader("Column Filter")
            columns_to_display = st.multiselect(
                "Select columns to display",
                options=list(df.columns),
                default=list(df.columns)
            )
            
            # Sort options
            st.subheader("Sort Data")
            sort_column = st.selectbox("Sort by column", options=["None"] + list(df.columns))
            sort_order = st.radio("Sort order", options=["Ascending", "Descending"])
            
            # Apply filters and sorting
            filtered_df = df[columns_to_display]
            
            if sort_column != "None":
                filtered_df = filtered_df.sort_values(
                    by=sort_column,
                    ascending=(sort_order == "Ascending")
                )
            
            # Apply search if terms are provided
            if search_terms:
                filtered_df = perform_search(filtered_df, search_terms)
            
            # Display results
            st.header("5. Results")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            
            # Download filtered data
            st.download_button(
                label="Download filtered data as CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_data.csv',
                mime='text/csv'
            )
            
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
            
if __name__ == "__main__":
    main()
