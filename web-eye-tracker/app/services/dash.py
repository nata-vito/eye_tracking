import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

dataset_train_path = '/home/nata-brain/Documents/tcc/web-eye-tracker/public/training/1685126241.2630084natanael/train_data.csv'
dataset_session_path = '/home/nata-brain/Documents/tcc/web-eye-tracker/public/sessions/1685126241.2630084natanael/session_data.csv'

raw_dataset = pd.read_csv(dataset_train_path)
session_dataset = pd.read_csv(dataset_session_path)

tab1, tab2 = st.tabs(["Dados Brutos", "Dados Processados"])

with tab1:
    st.title("Dados obtidos pela calibração")
    st.dataframe(raw_dataset)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Olho esquerdo")
        df = raw_dataset


        fig_left = px.scatter(
            df,
            x = "left_iris_x",
            y = "left_iris_y",
            color = "left_iris_y",
            color_continuous_scale = "reds",
        )
        
        st.plotly_chart(fig_left, theme="streamlit", use_container_width=True)

    with col2:    
        st.subheader("Olho direito")
        
        fig_right = px.scatter(
            df,
            x = "right_iris_x",
            y = "right_iris_y",
            color = "right_iris_y",
            color_continuous_scale = "reds",
        )

        st.plotly_chart(fig_right, theme="streamlit", use_container_width=True)
        
    fig3 = px.line(raw_dataset, y=["left_iris_x", "left_iris_y", "right_iris_x", "right_iris_y"], title="Left and Right Iris Position")
    st.plotly_chart(fig3,  theme="streamlit", use_container_width=True)

with tab2:
    fig_plt, ax = plt.subplots(figsize = (30, 20))

    x           = raw_dataset.left_iris_x
    y           = raw_dataset.left_iris_y
    datetime    = raw_dataset.timestamp

    ax.plot(x, y, 'r*', linestyle = '-')

    i = 0

    for xy in zip(x, y):
        i = i+1
        ax.annotate(f'{i}', xy)
    
    st.pyplot(fig_plt)
