import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import openai

st.set_page_config(
    page_title="BoloGPT",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None,
    },
)

# Set the background color and remove the footer
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
        body {
            background-color: white;
            font-family: 'Montserrat', sans-serif;
        }
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered title
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
.centered-title {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom:2px;
    color: #A3EBB1;
    font-family: 'Montserrat', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Bangla title
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
.bangla-title {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom:40px;
    color: #A3EBB1;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="centered-title">BoloGPT</div>',
            unsafe_allow_html=True)
st.markdown('<div class="bangla-title">বলোGPT</div>',
            unsafe_allow_html=True)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

        .steps-container {
            font-family: 'Montserrat', sans-serif;
        }
        .step-instructions {
            font-family: 'Montserrat', sans-serif;
        }
        .step {
            font-family: 'Montserrat', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Step-by-step guide
st.markdown("""
    <div class="steps-container" style="margin-bottom: 20px;">
        <div class="instruction" style="font-size: 1.5rem; color: #A3EBB1; margin-bottom: 10px;">Instructions</div>
        <div class="step" style="margin-bottom: 5px;font-size: 0.9rem;>
            <div class="step-instructions"style="font-size: 0.9rem;">1. To select the language for your prompt, please click the language dropdown and choose your preferred language.</div>
        </div>
        <div class="step" style="margin-bottom: 10px;font-size: 0.9rem;>
            <div class="step-instructions"style="font-size: 0.9rem;">2. Once you have selected your preferred language, click the "SPEAK" button and begin speaking into your microphone.</div>
        </div>
        <div class="step" style="margin-bottom: 10px;font-size: 0.9rem;>
            <div class="step-instructions"style="font-size: 0.9rem;">3. Please wait while BoloGPT generates your response. This process may take a moment.</div>
        </div>
        <div class="step" style="margin-bottom: 20px;font-size: 0.9rem;>
            <div class="step-instructions" style="font-size: 0.9rem;">4. Once your response is ready, an audio container will appear. Please click the play button to listen to your generated response.</div>
        </div>
        <div class="step" style="margin-bottom: 50px;font-size: 0.9rem;>
            <div class="note" style="font-size: 0.9rem;">Note:     It is recommended that you speak slowly, loudly, and clearly when providing your prompt to ensure the highest level of accuracy in the generated response.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Updated icon colors
st.markdown("""
    <style>
        .icons {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            margin-bottom:20px;
        }
        .icon {
            margin: 0 10px;
            color: #A3EBB1;
            text-decoration: none;
        }
    </style>
    """, unsafe_allow_html=True)

openai.api_key = "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"

if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [
        {"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]

# Add custom CSS to change the cursor type to pointer
st.markdown("""
    <style>
        select {
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Add the language selection dropdown
language_options = {
    "English": "en",
    "বাংলা": "bn"
}
selected_language = st.selectbox(
    "Select a language / ভাষা নির্ধারণ করুন", list(language_options.keys()))
language_code = language_options[selected_language]


def generate_response(prompt, language_code):
    translator = Translator()

    if language_code != 'en':
        translated_prompt = translator.translate(prompt, dest='en').text
    else:
        translated_prompt = prompt

    st.session_state['prompts'].append(
        {"role": "user", "content": translated_prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['prompts'],
    )

    message = completion.choices[0].message.content

    if language_code != 'en':
        translated_message = translator.translate(
            message, dest=language_code).text
    else:
        translated_message = message

    return translated_message


sound = BytesIO()

# placeholder = st.container()

stt_button = Button(label='Speak / বলুন', button_type='success', margin=(
    0, 5, 5, 0), width=433, height=40)


stt_button.js_on_event("button_click", CustomJS(code="""
    var value = "";
    var rand = 0;
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en';

    document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'start'}));
    
        recognition.onspeechstart = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'running'}));
    }
    recognition.onsoundend = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.onresult = function (e) {
        var value2 = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
                                rand = Math.random();

            } else {
                                value2 += e.results[i][0].transcript;
            }
        }
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: {t:value, s:rand}}));
        document.dispatchEvent(new CustomEvent("GET_INTRM", {detail: value2}));

    }
    recognition.onerror = function(e) {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.start();
     """))

# st.markdown("""
#     <style>
#         ...
#         .speak-button-container {
#             width: 100%;
#             margin: 0 0;
#             margin-bottom: 0px;
#         }
#         ...
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="speak-button-container">', unsafe_allow_html=True)
result = streamlit_bokeh_events(
    bokeh_plot=stt_button,
    events="GET_TEXT,GET_ONREC,GET_INTRM",
    key="listen",
    refresh_on_update=False,
    override_height=40,
    debounce_time=0)
# st.markdown('</div>', unsafe_allow_html=True)

tr = st.empty()

if 'input' not in st.session_state:
    st.session_state['input'] = {'text': '', 'session': 0}
input_text = st.session_state['input'].get('text', '')

tr.text_area("**Your input / আপনার ইনপুট**",
             value=st.session_state['input']['text'])

if result:
    if "GET_TEXT" in result:
        if result.get("GET_TEXT")["t"] != '' and result.get("GET_TEXT")["s"] != st.session_state['input']['session']:
            st.session_state['input']['text'] = result.get("GET_TEXT")["t"]
            tr.text_area("**Your input**",
                         value=st.session_state['input']['text'])
            st.session_state['input']['session'] = result.get("GET_TEXT")["s"]

    if "GET_INTRM" in result:
        if result.get("GET_INTRM") != '':
            tr.text_area(
                "**Your input**", value=st.session_state['input']['text']+' '+result.get("GET_INTRM"))

    if "GET_ONREC" in result:
        if result.get("GET_ONREC") == 'start':
            # placeholder.image("recon.gif")
            st.session_state['input']['text'] = ''
        elif result.get("GET_ONREC") == 'running':
            # placeholder.image("recon.gif")
            pass
        elif result.get("GET_ONREC") == 'stop':
            # placeholder.image("recon.jpg")
            if st.session_state['input']['text'] != '':
                input = st.session_state['input']['text']
                # Pass the language_code to generate_response
                output = generate_response(input, language_code)
                st.write("**BoloGPT:**")
                st.write(output)
                st.session_state['input']['text'] = ''

                # Set the language_code for gTTS
                tts = gTTS(output, lang=language_code, tld='com')
                tts.write_to_fp(sound)
                st.audio(sound)

                st.session_state['prompts'].append(
                    {"role": "user", "content": input})
                st.session_state['prompts'].append(
                    {"role": "assistant", "content": output})

# Add social icons and links
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">', unsafe_allow_html=True)
st.markdown("""
    <style>
        .icons {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.8rem;
            margin-bottom:20px;
        }
        .icon {
            margin: 0 10px;
            text-decoration: none;
        }
        .icon i {
            color: #A3EBB1;
        }
        .icon i:hover {
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="icons">
        <a href="https://www.linkedin.com/in/azmain-morshed/" target="_blank" class="icon"><i class="fab fa-linkedin"></i></a>
        <a href="https://www.instagram.com/azmainmd__/" target="_blank" class="icon"><i class="fab fa-instagram"></i></a>
        <a href="https://www.facebook.com/azmainm/" target="_blank" class="icon"><i class="fab fa-facebook"></i></a>
        <a href="mailto:azmainmorshed03@gmail.com" target="_blank" class="icon"><i class="fas fa-envelope"></i></a>
    </div>
    """, unsafe_allow_html=True)

# Add copyright notice
st.markdown("""
    <style>
        .copyright {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.8rem;
            color: #A3EBB1;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="copyright">&copy; Azmain Morshed 2023</div>',
            unsafe_allow_html=True)
