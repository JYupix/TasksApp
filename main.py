import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Tasks
import json
import pandas as pd

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET ONLY THE TASKS FROM DB
def get_all_tasks():
    with SessionLocal() as db:
        tasks = db.query(Tasks).all()
        return tasks

# THIS FUNCTION CONVERTS THE TASKS IN A JSON FILE
def convert_tasks_to_json(tasks):
    tasks_data = [{
        "ID": task.id,
        "Task": task.task,
        "Body": task.body,
        "State": "Completed" if task.state else "Pending"
    } for task in tasks]
    return tasks_data

# THIS FUNCTION WILL SAVE THE DATA FROM IMPORTED JSON FILE TO THE DB
def save_tasks_to_db(tasks_data):
    with SessionLocal() as db:
        for task_data in tasks_data:
            task = Tasks(
                task=task_data["Task"], 
                body=task_data["Body"], 
                state=True if task_data["State"] == "Completed" else False
            )
            db.add(task)
        db.commit()

# SIDEBAR THINGS
st.sidebar.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-lighttext.png" width="200"></div>',
    unsafe_allow_html=True
)
st.sidebar.title("My First Streamlit Task App")
st.sidebar.text("Export your tasks to a JSON file")
if st.sidebar.button("Export Tasks", icon=":material/file_export:"):
    tasks = get_all_tasks()
    if tasks:
        tasks_data = convert_tasks_to_json(tasks)
        json_data = json.dumps(tasks_data, indent=4)

        st.sidebar.download_button(
            label="Download JSON",
            data=json_data,
            file_name="tasks.json",
            mime="application/json"
        )
    else:
        st.sidebar.warning("No tasks available to export.")

uploaded_file = st.sidebar.file_uploader("Load tasks from a JSON file", type=["json"])
# THIS PROCESSES THE UPLOAD JSON FILE
if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        st.sidebar.write("File uploaded successfully.")
        if isinstance(data, list):
            save_tasks_to_db(data)
            st.success("Tasks successfully imported into the database.")
        else:
            st.error("The JSON file must contain a list of tasks.")

    except json.JSONDecodeError:
        st.sidebar.error("Error: The file is not a valid JSON.")
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")


# MAIN CONTENT
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .centered img {
        margin-right: 10px;  # Adjust this value to control spacing between image and title
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="centered">
        <img src="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-lighttext.png" width="100">
        <h1>Tasks App</h1>
    </div>
    """, unsafe_allow_html=True)

# THIS FUNCTION PROCESSES THE DATA FROM THE DB AND CONVERT THE DATA IN A TABLE
def show_tasks():
    with SessionLocal() as db:
        tasks = db.query(Tasks).all()
        if tasks:
            tasks_data = [{
                'ID': task.id,
                'Task': task.task,
                'Body': task.body,
                'State': 'Pending' if task.state == False else 'Completed'
            } for task in tasks]
        else:
            tasks_data = []

        df = pd.DataFrame(tasks_data, columns=['ID', 'Task', 'Body', 'State'])
        
        st.write("### Tasks List")
        st.dataframe(df, hide_index=True, use_container_width=True)

# THIS FUNCTION WILL ADD MY NEW TASK IN THE DB
def add_task(name, body, state):
    with SessionLocal() as db:
        new_task = Tasks(
            task=name,
            body=body,
            state=state
        )
        db.add(new_task)
        db.commit()
        st.success("Task added successfully!")

# THIS IS THE FORM TO SHOW ALL MY TASKS
def show_add_form():
    st.write("### Add Task")
    with st.form(key='my_form', clear_on_submit=True):
        task = st.text_input("Task")
        body = st.text_area("Body", height=70)
        state_boolean = st.selectbox("State", ('Pending', 'Completed'))
        state = False if state_boolean == 'Pending' else True
        
        submit_button = st.form_submit_button(label="Save")
        
    if submit_button:
        if task and body:
            add_task(task, body, state)
        else:
            st.warning("Please fill in both the Task and Body fields.")  

# FIRST I NEED THIS FUNCTION TO GET THE ID I WANT TO EDIT
def get_task_by_id(task_id):
    with SessionLocal() as db:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        return task

# THIS IS THE FUNCTION TO UPDATE THE TASK IN THE DB
def update_task(task_id, name, body, state):
    with SessionLocal() as db:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if task:
            task.task = name
            task.body = body
            task.state = state
            db.commit()

# THIS IS THE FORM TO EDIT THE TASK
def show_edit_form():
    st.write("### Edit Task")
    task_id = st.text_input("Enter Task ID to Edit")
    
    if task_id:
        task = get_task_by_id(int(task_id))

        if task:
            task_name = st.text_input("Task", value=task.task)
            task_body = st.text_area("Body", value=task.body, height=70)
            task_state = st.selectbox("State", ('Pending', 'Completed'), index=0 if task.state == False else 1)
            state = False if task_state == 'Pending' else True

            # Botón para guardar los cambios
            if st.button("Save Changes"):
                if task_name and task_body:
                    update_task(task.id, task_name, task_body, state)
                    st.success("Task updated successfully!")
                else:
                    st.warning("Please fill in both the Task and Body fields.")
        else:
            st.error("Task not found with ID: {}".format(task_id))

# THIS FUNCTION WILL PROCESSES MY QUERY AND WILL SHOW ME THE TASKS I WANT TO SEE FROM THE DB
def search_tasks(query):
    with SessionLocal() as db:
        if query.lower() == "pending":
            tasks = db.query(Tasks).filter(Tasks.state == False).all()
        elif query.lower() == "completed":
            tasks = db.query(Tasks).filter(Tasks.state == True).all()
        else:
            tasks = db.query(Tasks).filter(
                Tasks.task.ilike(f"%{query}%") | 
                Tasks.body.ilike(f"%{query}%")
            ).all()
        return tasks

# THIS IS THE FORM TO SEARCH FOR A TASK
def show_search_form():
    st.write("### Search Task")
    query = st.text_input("Search Tasks", "")
    if query:
        tasks = search_tasks(query)
        if tasks:
            tasks_data = [{
                "Task ID": task.id,
                "Task": task.task,
                "Body": task.body,
                "State": "Completed" if task.state else "Pending"
            } for task in tasks]

            df = pd.DataFrame(tasks_data)

            st.write("### Search Results")
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.warning("No tasks found matching your search.")

# THIS IS THE FUNCTION THAT PROCESSES THE ID THAT I WANT TO DELETE FROM THE DB
def delete_task(task_id):
    with SessionLocal() as db:
        task_to_delete = db.query(Tasks).filter(Tasks.id == task_id).first()
        if task_to_delete:
            db.delete(task_to_delete)
            db.commit()
            return True
        else:
            return False

# THIS IS THE FORM TO DELETE THE TASK
def show_delete_form():
    st.write("### Delete Task")
    task_id = st.text_input("Enter Task ID to Delete", "")

    if st.button("Delete"):
        if task_id:
            try:
                task_id = int(task_id)
                if delete_task(task_id):
                    st.success(f"Task with ID {task_id} has been deleted successfully.")
                else:
                    st.warning(f"No task found with ID {task_id}.")
            except ValueError:
                st.error("Please enter a valid numeric ID.")
        else:
            st.warning("Please enter a Task ID to delete.")


with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("Tasks", icon=":material/task:"):
            st.session_state.page = "tasks"

    with col2:
        if st.button("Add", icon=":material/add:"):
            st.session_state.page = "add"

    with col3:
        if st.button("Edit", icon=":material/edit:"):
            st.session_state.page = "edit"

    with col4:
        if st.button("Search", icon=":material/search:"):
            st.session_state.page = "search"

    with col5:
        if st.button("Delete", icon=":material/delete:"):
            st.session_state.page = "delete"


if "page" not in st.session_state:
    st.session_state.page = "tasks"

if st.session_state.page == "tasks":
    show_tasks()
elif st.session_state.page == "add":
    show_add_form()
elif st.session_state.page == "edit":
    show_edit_form()
elif st.session_state.page == "search":
    show_search_form()
elif st.session_state.page == "delete":
    show_delete_form()


