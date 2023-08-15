import os
import openai
from langchain.document_loaders import PyPDFLoader

import streamlit as st

# streamlit run app.py

from dotenv import load_dotenv
load_dotenv()

api_base = os.getenv("AZURE_OPENAI_BASE")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = "2023-03-15-preview"

openai.api_type = 'azure'
openai.api_key = api_key
openai.api_version = api_version
openai.api_base = api_base

def get_response(messages):
    return openai.ChatCompletion.create(
        engine="Gpt35Turbo16k",
        messages = messages,
        temperature=0,
        max_tokens=4000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        request_timeout=3600,
        timeout=3600
    )

def load_file(file_name):
    loader = PyPDFLoader(file_name)
    pages = loader.load()
    allpages = ""
    for page in pages:
        allpages += page.page_content
    return allpages


def read_receipt(file_name):
    actor = "I want you to act as my personal assistant and organize expenses."

    prompt = """
            The following is a receipt between '''
            Give me the following information from the receipt:
            1. Seller
            2. Date
            3. Category
            4. Tax rates
            5. Tax amounts
            6. Total amount with tax

            '''{context}'''
            """

    # prompt = """
    #         The following is a receipt between '''
    #         Extract all relevant key information and give it to me in a JSON object.

    #         '''{context}'''
    #         """

    pages = load_file(file_name)

    # st.write(pages)

    messages = [
        {"role":"system","content":actor},
        {"role":"user","content":prompt.format(context=pages)}
    ]

    st.subheader(file_name)
    response = get_response(messages)
    st.markdown(response.choices[0].message.content)

    # with st.expander('Document Response'):
    #     st.write(response)

    st.divider()

def read_invoice(file_name):
    actor = "I want you to act as my personal assistant and organize invoices."

    prompt = """
            The following is an invoice between '''
            Give me the following information from the invoice:
            1. Seller information
            2. Invoice date, Due date
            3. Shipping information
            4. Invoice number
            5. Order number
            6. Payment information
            7. Payment terms
            8. Items
            9. Sub total
            10. Tax rate
            11. Tax amount
            12. Total

            '''{context}'''
            """

    # prompt = """
    #         The following is an invoice between '''
    #         Extract all relevant key information and give it to me in a JSON object.

    #         '''{context}'''
    #         """


    pages = load_file(file_name)
        
    #st.write(pages)

    messages = [
        {"role":"system","content":actor},
        {"role":"user","content":prompt.format(context=pages)}
    ]

    st.subheader(file_name)
    response = get_response(messages)
    st.markdown(response.choices[0].message.content.replace('$', '\$').replace('\n', '  \n'))

    # with st.expander('Document Response'):
    #     st.write(response)

    st.divider()

st.title('Personal accountant')

# read_receipt("receipt1.pdf")
# read_receipt("receipt2.pdf")

# read_invoice("invoice1.pdf")
# read_invoice("invoice2.pdf")
read_invoice("invoice3.pdf")
