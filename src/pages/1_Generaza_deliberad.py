import streamlit as st
from openai import OpenAI
# Imports for summarization

# map reduce with custom prompt method
def summarize_text(text_all):
    client = OpenAI()
    output = ''
 

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
            "role": "system",
            "content": "Ești un grefier de ședință virtual. Textul este o pagină din cererea unei părți depusă la instanță și trebuie transpusă într-o proiect de hotărâre judecătorească. Parafrazează cererea în aproximativ 3000 de cuvinte. Păstrează obiectul acțiunii exact cum este menționat. Păstrează datele, numere documentelor și argumentele. Omite prudențialele precum numerele de telefon, adresele poștale si de email. \nTextul rezultat să aibă 3 părți: situația de fapt prezentată de parte; temeiurile de drept invocate; probele care solicită a fi administrate. \nRezultatul să fie în felul următorul: \"A solicitat [...] \"sau \"A susținut că [...]\"; În drept au fost invocate [...]; În probațiune a fost solicitată încuviințarea următoarelor probe [...]. Fără concluzii."
            },
            {
            "role": "user",
            "content": f'{text_all}'
            }
        ],
        stream=True,
        temperature=1,
        max_tokens=8363,
        top_p=0.4,
        frequency_penalty=0,
        presence_penalty=0
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            output = output + chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    # Remove double new lines
    formatted_output = output.replace('\n\n', '\n')

    return formatted_output


# Initialize Streamlit app
st.title("Generează partea de la deliberând")

# Create global variable to be used in all the methods
# Save the variable in the session state, the browser memory
if 'text_all' not in st.session_state:
    st.session_state.text_all = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""

st.session_state.text_all = st.text_area("Conținutul ce trebuie sumarizat", height=300, max_chars=21000)

# "Summarize" button appears after "Convert PDF to Text" has been used
if st.session_state.text_all and st.button("Crează deliberând"):
    with st.spinner("Se crează partea de deliberând"):
        st.session_state.summary = summarize_text(st.session_state.text_all)
            
if st.session_state.summary:
        st.text_area("Partea de la deliberând:", st.session_state.summary, height=300)


