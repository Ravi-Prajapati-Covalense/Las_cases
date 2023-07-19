import streamlit as st
import json

st.markdown(
    """
    <style>

    
    /* Reduce space between text areas */
    .element-container {
        margin-bottom: 0rem;
        
    }
    
    /* Reduce space between st.text_area elements */
    .stTextArea {
        margin-bottom: -2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True,
)

# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )


def load_data():
    with open(r'C:\Users\ravi.shankar p\Notebook\POC\legalDocumentsExtraction\legalDocumentsExtraction\output\document_summaries.json', 'r') as file:
        data = json.load(file)
    return data

def get_unique_sections(data):
    sections = set()
    for case_data in data:
        sections.update(case_data['sections'])
    return sorted(list(sections))

def get_case_statuses_for_sections(selected_sections, data):
    case_statuses = set()
    for case_data in data:
        if set(selected_sections).issubset(case_data['sections']):
            case_statuses.add(case_data['caseStatus'])
    return list(case_statuses)

def filter_data(selected_sections, selected_case_status, selected_court_name, data):
    filtered_data = []
    for case_data in data:
        if set(selected_sections).issubset(case_data['sections']) and selected_case_status == case_data['caseStatus'] and selected_court_name == case_data['courtName']:
            filtered_data.append(case_data)
    return filtered_data

def get_court_names_for_sections_and_status(selected_sections, selected_case_status, data):
    court_names = set()
    for case_data in data:
        if set(selected_sections).issubset(case_data['sections']) and selected_case_status == case_data['caseStatus']:
            court_names.add(case_data['courtName'])
    return list(court_names)

def main():
    data = load_data()
    sections = get_unique_sections(data)
    selected_sections = st.sidebar.multiselect('Select sections:', sections)

    if selected_sections:
        case_statuses = get_case_statuses_for_sections(selected_sections, data)
        selected_case_status = st.sidebar.selectbox('Select case status:', case_statuses)

        if selected_case_status:
            court_names = get_court_names_for_sections_and_status(selected_sections, selected_case_status, data)
            selected_court_name = st.sidebar.selectbox('Select court name:', court_names)

            if selected_court_name:
                filtered_data = filter_data(selected_sections, selected_case_status, selected_court_name, data)

                st.subheader("Similar Case Documents")

                for case_data in filtered_data:
                    case_info = (
                        f'File Name: {case_data["fileName"]}\n'
                        f'Case Status: {case_data["caseStatus"]}\n'
                        f'Court Name: {case_data["courtName"]}\n'
                        f'Introduction:\n{case_data["introduction"]}\n'
                        f'Description:\n{case_data["description"]}\n'
                    )
                    st.text_area('', case_info, height=200)

main()