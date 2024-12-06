import streamlit as st
from ..repositories.task_comments import create_task_comment, get_task_comments, edit_task_comment, get_task_comment, delete_task_comment
from ..repositories.tasks import get_all_tasks

def show_task_comments_page():
    st.title("Task Comments")

    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please log in to view or manage comments.")
        return

    role = st.session_state["role_id"]
    user_id = st.session_state["user_id"]

    task_id = st.sidebar.selectbox("Select a Task", ["Select a task"] + [task[0] for task in get_all_tasks()])

    if task_id == "Select a task":
        return

    action = st.sidebar.radio("Choose an action", ["View Comments", "Add Comment", "Edit Comment", "Delete Comment", "Delete All Comments"])

    if action == "View Comments":
        st.subheader("Comments for Task ID: {}".format(task_id))
        comments = get_task_comments(task_id)
        if comments:
            for comment in comments:
                st.write(f"Comment ID: {comment[0]}")
                st.write(f"User ID: {comment[2]}")
                st.write(f"Comment: {comment[3]}")
                st.write("---")
        else:
            st.warning("No comments for this task.")

    elif action == "Add Comment":
        st.subheader("Add a Comment")

        comment_text = st.text_area("Your Comment")

        if st.button("Submit Comment"):
            if not comment_text:
                st.warning("Comment cannot be empty.")
            else:
                try:
                    create_task_comment(task_id, user_id, comment_text)
                    st.success("Comment added successfully.")
                except Exception as e:
                    st.error(f"Error adding comment: {str(e)}")

    elif action == "Edit Comment":
        st.subheader("Edit Your Comment")

        comments = get_task_comments(task_id)
        user_comments = [comment for comment in comments if comment[2] == user_id]

        if user_comments:
            comment_id = st.selectbox("Select a comment to edit", [comment[0] for comment in user_comments])
            comment = next(c for c in user_comments if c[0] == comment_id)
            new_comment_text = st.text_area("Edit your comment", value=comment[3])

            if st.button("Update Comment"):
                try:
                    edit_task_comment(task_id, user_id, new_comment_text)
                    st.success("Comment updated successfully.")
                except Exception as e:
                    st.error(f"Error editing comment: {str(e)}")
        else:
            st.warning("You have no comments on this task.")

    elif action == "Delete Comment":
        st.subheader("Delete Your Comment")

        comments = get_task_comments(task_id)

        # Для админа — все комментарии, для пользователя — только свои
        if role == 1:  # Роль администратора
            comment_ids = [comment[0] for comment in comments]
        else:  # Для обычного пользователя — только его комментарии
            comment_ids = [comment[0] for comment in comments if comment[2] == user_id]

        if comment_ids:
            comment_id = st.selectbox("Select a comment to delete", comment_ids)
            if st.button("Delete Comment"):
                try:
                    delete_task_comment(task_id, user_id, comment_id)
                    st.success("Comment deleted successfully.")
                except Exception as e:
                    st.error(f"Error deleting comment: {str(e)}")
        else:
            st.warning("No comments available for deletion.")

    elif action == "Delete All Comments":
        st.subheader("Delete All Comments")

        if role == 1:  # Только администратор может удалить все комментарии
            if st.button("Delete All Comments"):
                try:
                    delete_task_comment(task_id)
                    st.success("All comments deleted successfully.")
                except Exception as e:
                    st.error(f"Error deleting comments: {str(e)}")
        else:
            st.warning("You are not authorized to delete all comments.")