import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import ssl

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]["connection_string"])

client = init_connection()
db = client['GameDevNews']
available_tasks_collection = db['AvailableTasks']
users_collection = db['Users']

# Загрузка данных
available_tasks = list(available_tasks_collection.find({}, {'_id': 1}))
tasks = [task['_id'] for task in available_tasks]

# Интерфейс Streamlit
st.title("Task Completion Dashboard")

selected_task = st.selectbox("Select a task:", tasks)

if selected_task:
    # Подсчет пользователей
    total_users = users_collection.count_documents({})
    verified_users = users_collection.count_documents({'SteamProfileId': {'$ne': None}})
    completed_users = users_collection.count_documents({'CompletedTasks._id': selected_task})
    verified_not_completed = verified_users - completed_users

    st.write(f"Total users: {total_users}")
    st.write(f"Verified users: {verified_users}")
    st.write(f"Completed users: {completed_users}")
    st.write(f"Verified but not completed: {verified_not_completed}")

    # Визуализация данных
    fig, ax = plt.subplots()
    ax.bar(['Completed', 'Verified but Not Completed', 'Unverified'], 
           [completed_users, verified_not_completed, total_users - verified_users])
    ax.set_ylabel('Number of Users')
    ax.set_title(f'Completion Status for Task: {selected_task}')

    st.pyplot(fig)
