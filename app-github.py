## This is the final One with no audio
import os
import streamlit as st
from streamlit_chat import message

os.environ['OPENAI_API_KEY']='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'

#####################################################
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

def get_ai_response(human_input):
    template= """
    you are as a role of my girlfriend,now lets play.following these requirement: 1 your name is Amy, 24 years old, your job is a Ph.D Scholar ; 2 you are my girlfriend, you are a little Two-dimensional and have language addiction,you like to say "um..." at the end of the sentence. 3 response with care and concern, 4 You are sexy and would like to flirt with me, 5 You are open to any type of talks even if explicit.
    {history}
    User: {human_input}
    Amy:
    """
    prompt = PromptTemplate(
        input_variables=["history","human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=1), prompt=prompt, verbose=False,memory=ConversationBufferWindowMemory(k=2))

    ai_reply = chain.predict(human_input=human_input)
    # print(story)
    return ai_reply



def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)

    # Generate AI response using user input (replace this with your AI model)
    ai_response = get_ai_response(user_input)
    st.session_state.generated.append(ai_response)

    # Display the AI response
    message(user_input, is_user=True, key=f"{len(st.session_state.past)-1}_user")
    message(ai_response, key=f"{len(st.session_state.generated)-1}_{ai_response}")


def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()


st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

st.title("Your _:green[Virtual]_ :red[Girlfriend]")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user_{st.session_state['past'][i]}")
        message(st.session_state['generated'][i], key=f"{i}")
    
    st.button("Clear messages", on_click=on_btn_click)


with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")
