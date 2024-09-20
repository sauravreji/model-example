import streamlit as st
import pandas as pd
import plotly.express as px
from huggingface_hub import InferenceClient

client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token="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",
)

def get_chat_response(prompt, max_tokens=50):
    messages = [{"role": "user", "content": prompt}]
    response = ""
    for message in client.chat_completion(messages=messages, max_tokens=max_tokens, stream=True):
        response += message.choices[0].delta.content
    return response.strip()

def plot_graph(data, x, y, graph_type):
    if graph_type == 'line':
        fig = px.line(data, x=x, y=y)
    elif graph_type == 'Bar':
        fig = px.bar(data, x=x, y=y, orientation='v')  
    elif graph_type == 'scatter':
        fig = px.scatter(data, x=x, y=y)
    elif graph_type == 'Histogram':
        fig = px.histogram(data, x=x, y=y)
    elif graph_type == 'Pie Chart':
        fig = px.pie(data, names=x, values=y, title=f'{graph_type.capitalize()} Plot')
    else:
        fig = px.line(data, x=x, y=y , orientation='v')
    fig.update_layout(width=900, height=600)

    return fig

def compute_statistics(data, x, y):
    total_count = len(data)
    average = data[y].mean()
    highest = data[y].max()
    lowest = data[y].min()
    return total_count, average, highest, lowest

def save_query_to_file(query, filename="llm_query.txt"):
    with open(filename, "w") as file:
        file.write(query)

st.markdown(
    """
    <style>
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        max-width: 70%;
        word-wrap: break-word.
    }
    .user-message {
        background-color: #DCF8C6.
        align-self: flex-end.
    }
    .bot-message {
        background-color: #EDEDED.
        align-self: flex-start.
    }
    .message-container {
        display: flex.
        flex-direction: column.
    }
    .chat-history {
        display: flex.
        flex-direction: column.
        max-height: 400px.
        overflow-y: auto.
        margin-bottom: 20px.
    }
    .stats-container {
        padding: 10px.
        border-radius: 10px.
        background-color: #F0F0F0.
        margin-top: 20px.
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Intelligent Data Visualization Tool")
st.write("Upload a CSV file and enter your description to get visualizations and reports.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    st.session_state.file_uploaded = True
    st.session_state.data = pd.read_csv(uploaded_file)
    st.session_state.columns = st.session_state.data.columns.tolist() 
    st.write("CSV file uploaded successfully! You can now enter your description.")

if 'file_uploaded' in st.session_state and st.session_state.file_uploaded:
    user_input = st.text_input("Enter your description: ", "")
    save_query_to_file(user_input)

    
    if user_input:
        with open("gpt.py") as z:
            exec(z.read())  
        prompt = f"Based on the following data, determine the most appropriate x-axis, y-axis for visualization based on the user's description:\n\n"
        prompt += f"Dataset Information:\n"
        prompt += f"- Number of rows: {len(st.session_state.data)}\n"
        prompt += f"- Number of columns: {len(st.session_state.data.columns)}\n"
        prompt += f"- Columns: {', '.join(st.session_state.data.columns)}\n\n"

        prompt += f"Sample Data:\n"
        prompt += f"{st.session_state.data.head().to_string(index=False)}\n\n"
        
        prompt += f"User Description:\n"
        prompt += f"{user_input}\n\n"
        
        prompt += f"Please provide the x-axis, y-axis,  in the format [x-axis, y-axis] based on the above details. Provide answer only in three words." 

        if st.button("Generate Graph"):
            # Save the query to a file
           

            with st.spinner('Bot is analyzing data...'):
                response = get_chat_response(prompt)
            
            st.write(f"**Model's Response**:\n{response}")

            
            with open('output.txt', "r") as file:
                second_input = file.readline()

            prompt2 = (
            f"find the graph mentioned:\n"
            f"{second_input}\n\n"
            f"Tell me which is the first graph mentioned after correction. If it's a bar chart, respond with 'Bar'; if it's a line chart, respond with 'line'; if it's a scatter plot, respond with 'scatter'; if it's a histogram, respond with 'Histogram'; if it's a pie chart, respond with 'Pie Chart'.\n"
            f"Only provide the type of the first graph in one word."
            f"for example: line"
            f"no need for any other information"
            )
            response2 = get_chat_response(prompt2)
            st.write(f"Graph type:\n{response2}")
            
            
            response = response + "," + response2
            

            st.write(f"response is: {response}")
            response_parts = response.strip().strip('[]').split(',')
            if len(response_parts) == 3:
                x_axis, y_axis, graph_type = [part.strip() for part in response_parts]
                
                if x_axis in st.session_state.columns and y_axis in st.session_state.columns:
                    try:
                        fig = plot_graph(st.session_state.data, x_axis, y_axis, graph_type)
                        st.plotly_chart(fig)
                    except Exception as e:
                        st.write(f"Error plotting graph: {e}")
                else:
                    st.write("The suggested x-axis and/or y-axis do not match the available columns. Please provide more information.")



