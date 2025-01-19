import streamlit as st
import warnings
from urllib3.exceptions import InsecureRequestWarning

def apply_sidebar_styles():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #FFDD00 !important;
        }
        [data-testid="stSidebar"] * {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_global_styles():
    st.markdown(
        """
        <style>
        /* General App Background and Text */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #000000 !important;
            color: white !important;
        }

        /* Header and Text Color */
        h1, h2, h3, h4, h5, h6, p {
            color: white !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFDD00 !important;
        }
        [data-testid="stSidebar"] * {
            color: black !important;
        }

        /* Hide the copy-to-clipboard button */
        button[title="Copy to clipboard"] {
            display: none !important;
        }

        /* Hide the </div> tag if displayed */
        code, pre {
            display: none !important;
        }

        /* Set the top horizontal bar (header) to black */
        [data-testid="stHeader"] {
            background-color: #000000 !important;  /* Black background */
            border-bottom: 2px solid #000000 !important;  /* Black border for seamless look */
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def apply_info_styles():
    st.markdown(
        """
        <style>
        /* General App Background and Text */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #000000 !important;
            color: white !important;
        }

        /* Header and Text Color */
        h1, h2, h3, h4, h5, h6, p {
            color: white !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFDD00 !important;
        }
        [data-testid="stSidebar"] * {
            color: black !important;
        }

        /* Allow proper display of code blocks */
        pre, code {
            background-color: #333333 !important;  /* Dark background */
            color: #00FF00 !important;             /* Green text */
            border-radius: 5px;
            padding: 10px;
            font-family: Consolas, monospace;
            font-size: 14px;
            overflow-x: auto;                      /* Handle long lines */
        }

        /* Ensure the clipboard copy button is visible */
        button[title="Copy to clipboard"] {
            display: inline-block !important;  /* Ensure the button is displayed */
            background-color: #FFDD00 !important;  /* Yellow background */
            border: 1px solid black !important;    /* Black border */
            color: black !important;              /* Black text */
            font-weight: bold !important;         /* Bold text */
            border-radius: 5px !important;        /* Rounded corners */
            padding: 5px 10px !important;         /* Padding */
            cursor: pointer !important;           /* Pointer cursor on hover */
        }

        /* Set the top horizontal bar (header) to black */
        [data-testid="stHeader"] {
            background-color: #000000 !important;  /* Black background */
            border-bottom: 2px solid #000000 !important;  /* Black border for seamless look */
        }

        /* Adjust the position of the clipboard button inside the code container */
        div[data-testid="stCodeBlock"] {
            position: relative;
        }

        button[title="Copy to clipboard"] {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 10;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_dropdown_styles():
    st.markdown(
        """
        <style>
        /* Dropdown main input styling */
        div[data-baseweb="select"] > div {
            background-color: #FFDD00 !important;  /* Yellow background */
            color: black !important;               /* Black text */
            font-weight: bold !important;          /* Bold text */
            border-radius: 5px !important;
            border: 1px solid black !important;
        }

        /* Dropdown options container (using ul for more reliable targeting) */
        ul[role="listbox"] {
            background-color: #FFDD00 !important;  /* Yellow dropdown background */
            color: black !important;               /* Black text */
            border-radius: 5px !important;
            border: 1px solid black !important;
        }

        /* Dropdown option items */
        li[role="option"], div[role="option"] {
            background-color: #FFDD00 !important;  /* Yellow background */
            color: black !important;               /* Black text */
            font-weight: normal !important;        /* Normal weight */
            padding: 5px 10px !important;         /* Consistent padding */
        }

        /* Hover effect for dropdown options */
        li[role="option"]:hover, div[role="option"]:hover {
            background-color: #FFC300 !important;  /* Lighter yellow on hover */
            color: black !important;
            font-weight: bold !important;
        }

        /* Selected dropdown option */
        li[role="option"][aria-selected="true"], div[aria-selected="true"] {
            background-color: #FFAA00 !important;  /* Darker yellow for selected */
            color: black !important;
            font-weight: bold !important;
        }

        /* Dropdown arrow color */
        svg[data-icon="caret-down"], svg {
            fill: black !important;  /* Black dropdown arrow */
        }

        /* Disable the blinking text cursor in dropdown input */
        input {
            caret-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_button_styles():
    st.markdown(
        """
        <style>
        /* Style for all Streamlit buttons */
        div.stButton > button:first-child {
            background-color: #FFDD00 !important; /* Yellow background */
            color: black !important;             /* Black text */
            font-weight: bold !important;        /* Bold text */
            border: 2px solid black !important;  /* Black border */
            border-radius: 5px !important;       /* Rounded corners */
            padding: 10px 20px !important;       /* Padding */
            font-size: 16px !important;         /* Optional: Adjust font size */
            text-align: center !important;      /* Center text */
            transition: background-color 0.3s ease;
        }

        /* Force button text and nested icons to be bold and black */
        div.stButton > button:first-child * {
            color: black !important;             /* Black text for all nested elements */
            font-weight: bold !important;        /* Bold text for nested elements */
        }

        /* Hover effect for the button */
        div.stButton > button:first-child:hover {
            background-color: #FFC300 !important; /* Lighter yellow */
            color: black !important;
            font-weight: bold !important;         /* Maintain bold on hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )




# Convert DataFrame to styled HTML
def apply_table_styles(df):
    styled_table = df.style.set_properties(**{
        'text-align': 'center',
        'background-color': '#FFDD00',  # Yellow background
        'color': 'black',               # Black text
        'border': '1px solid black'     # Black border for cells
    }).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), 
                                     ('background-color', '#FFAA00'),  # Darker yellow for headers
                                     ('color', 'black')]}
    ]).to_html(escape=False)  # Prevent HTML escaping

    # Correctly wrap the table for centering
    centered_table = f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        {styled_table}
    </div>"""
    
    return centered_table



def display_centered_logo(image_path, width=300):
    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider

    with col2:  # Center the image in the middle column
        st.image(image_path, width=width)




def suppress_insecure_request_warnings():
    warnings.simplefilter("ignore", InsecureRequestWarning)

# Apply custom CSS to fix the white space below the map
def apply_map_styles():
    st.markdown(
        """
        <style>
        /* Fix white space under the map */
        iframe[title="streamlit_folium.st_folium"] {
            height: 700px !important; /* Adjust height as needed */
            margin-bottom: 0px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
def hide_streamlit_spinner():
    st.markdown(
        """
        <style>
        /* Hide the spinner and its white background bar */
        div.stSpinner {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )




