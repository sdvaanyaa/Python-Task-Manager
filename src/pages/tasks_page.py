import streamlit as st
from ..repositories.tasks import create_task, get_all_tasks, get_tasks_by_uesr, delete_task
from ..repositories.users import get_username_by_id
def show_tasks_page():
    st.title("Tasks")

    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please log in to view tasks.")
        return

    role = st.session_state["role_id"]
    user_id = st.session_state["user_id"]

    action = st.sidebar.radio("Choose an action", ["View Tasks", "Create Task", "Delete Task", "Delete All My Tasks"])

    if action == "View Tasks":
        st.subheader("All Tasks")

        # Получаем все задачи или только задачи конкретного пользователя
        tasks = get_all_tasks() if role == 1 else get_tasks_by_uesr(user_id)

        # Группируем задачи по пользователям
        grouped_tasks = {}
        for task in tasks:
            task_owner_id = task[1]  # Здесь мы исправляем индекс, так как user_id в запросе - это task[1]
            if task_owner_id not in grouped_tasks:
                grouped_tasks[task_owner_id] = []
            grouped_tasks[task_owner_id].append(task)

        # Отображаем задачи по пользователям
        for owner_id, user_tasks in grouped_tasks.items():
            # Получаем имя пользователя
            user_name = get_username_by_id(owner_id)

            with st.expander(f"{user_name}'s Tasks" if user_name else f"User {owner_id}'s Tasks"):
                for task in user_tasks:
                    st.write(f"**ID**: {task[0]}")
                    st.write(f"**Title**: {task[2]}")
                    st.write(f"**Description**: {task[3]}")
                    st.write(f"**Status**: {task[4]}")
                    st.write(f"**Created At**: {task[5]}")
                    st.write("---")

    elif action == "Create Task":
        st.subheader("Create New Task")

        title = st.text_input("Title")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
        created_at = st.date_input("Created At")

        if st.button("Create Task"):
            if not title or not description:
                st.warning("Title and description are required.")
            else:
                try:
                    task_id = create_task(user_id, title, description, status, created_at)
                    st.success(f"Task created with ID: {task_id}")
                except Exception as e:
                    st.error(f"Error creating task: {str(e)}")

    elif action == "Delete Task":
        st.subheader("Delete Task")

        if role == 1:
            tasks = get_all_tasks()
        else:
            tasks = get_tasks_by_uesr(user_id)

        task_id = st.selectbox("Select a task to delete", [task[0] for task in tasks])

        if st.button("Delete Task"):
            try:
                delete_task(task_id)
                st.success("Task deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting task: {str(e)}")

    elif action == "Delete All My Tasks":
        st.subheader("Delete All My Tasks")

        if role == 1:
            tasks = get_all_tasks()
        else:
            tasks = get_tasks_by_uesr(user_id)

        if st.button("Delete All My Tasks"):
            for task in tasks:
                try:
                    delete_task(task[0])
                    st.success(f"Task with ID {task[0]} deleted successfully.")
                except Exception as e:
                    st.error(f"Error deleting task with ID {task[0]}: {str(e)}")




