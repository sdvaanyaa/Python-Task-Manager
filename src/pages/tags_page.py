import streamlit as st
from ..repositories.tags import (
    create_tag,
    assign_tag_to_task,
    get_all_tags,
    get_tags_for_task,
    get_tasks_by_tag,
)
from ..repositories.tasks import get_all_tasks

# Главная функция страницы
def show_tags_page():
    st.title("Tags Management")

    # Статичное меню слева с радиокнопками
    action = st.sidebar.radio(
        "Choose Action",
        ["Create New Tag", "View Tasks by Tag", "View Tags for a Task", "Assign Tag to Task"],
    )

    # Создать новый тег
    if action == "Create New Tag":
        st.subheader("Create New Tag")
        tag_name = st.text_input("Enter tag name")
        if st.button("Create Tag"):
            if tag_name.strip():
                tag_id = create_tag(tag_name)
                st.success(f"Tag '{tag_name}' created with ID {tag_id}")
            else:
                st.error("Tag name cannot be empty")

    # Показать задачи с выбранным тегом
    elif action == "View Tasks by Tag":
        st.subheader("View Tasks by Tag")
        tags = get_all_tags()  # Функция для получения всех тегов
        tag_names = {tag["name"]: tag["id"] for tag in tags}

        selected_tag_name = st.selectbox("Select a tag", list(tag_names.keys()))
        selected_tag_id = tag_names[selected_tag_name]

        if st.button("View Tasks"):
            tasks = get_tasks_by_tag(selected_tag_id)
            if tasks:
                st.write(f"Tasks with Tag '{selected_tag_name}':")
                for task in tasks:
                    st.write(f"**ID**: {task['id']}")
                    st.write(f"**Title**: {task['title']}")
                    st.write(f"**Description**: {task['description']}")
                    st.write(f"**Status**: {task['status']}")
                    st.write(f"**Created At**: {task['created_at']}")
                    st.write("---")
            else:
                st.info(f"No tasks found for Tag '{selected_tag_name}'")

    # Показать теги у выбранной задачи
    elif action == "View Tags for a Task":
        st.subheader("View Tags for a Task")
        tasks = get_all_tasks()  # Функция для получения всех задач
        task_titles = {task[2]: task[0] for task in tasks}

        selected_task_title = st.selectbox("Select a task", list(task_titles.keys()))
        selected_task_id = task_titles[selected_task_title]

        if st.button("View Tags"):
            tags = get_tags_for_task(selected_task_id)
            if tags:
                st.write(f"Tags for Task '{selected_task_title}':")
                for tag in tags:
                    st.write(f"**ID**: {tag['id']}")
                    st.write(f"**Name**: {tag['name']}")
            else:
                st.info(f"No tags found for Task '{selected_task_title}'")

    # Связать задачу и тег
    elif action == "Assign Tag to Task":
        st.subheader("Assign Tag to Task")

        # Выбор задачи
        tasks = get_all_tasks()  # Функция для получения всех задач
        task_titles = {task[2]: task[0] for task in tasks}
        selected_task_title = st.selectbox("Select a task", list(task_titles.keys()))
        selected_task_id = task_titles[selected_task_title]

        # Выбор тега
        tags = get_all_tags()  # Функция для получения всех тегов
        tag_names = {tag["name"]: tag["id"] for tag in tags}
        selected_tag_name = st.selectbox("Select a tag", list(tag_names.keys()))
        selected_tag_id = tag_names[selected_tag_name]

        if st.button("Assign Tag"):
            assign_tag_to_task(selected_task_id, selected_tag_id)
            st.success(f"Tag '{selected_tag_name}' assigned to Task '{selected_task_title}'")