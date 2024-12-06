import streamlit as st
from ..repositories.follows import create_follow, delete_follow, get_followers, get_followed
from ..repositories.users import get_all_users


def show_follows_page():
    st.title("Manage Follows")

    # Проверка авторизации
    if "user_id" not in st.session_state:
        st.warning("Please log in to manage follows.")
        return

    current_user_id = st.session_state["user_id"]

    # Боковое меню
    menu_option = st.sidebar.radio(
        "Select an action",
        ["Follow a User", "Unfollow a User", "Your Followers", "Users You Follow"]
    )

    # "Follow a User"
    if menu_option == "Follow a User":
        st.subheader("Follow a User")

        try:
            # Получаем всех пользователей, исключая текущего
            all_users = get_all_users()
            available_users = [user for user in all_users if user["id"] != current_user_id]

            if available_users:
                # Селектор для выбора пользователя
                selected_user = st.selectbox(
                    "Select a user to follow:",
                    options=available_users,
                    format_func=lambda user: f"{user['username']}"
                )
                if st.button("Follow"):
                    try:
                        create_follow(current_user_id, selected_user["id"])
                        st.success(f"You have followed {selected_user['username']}.")
                    except Exception as e:
                        st.error(f"Failed to follow user: {e}")
            else:
                st.write("No users available to follow.")
        except Exception as e:
            st.error(f"Failed to load users: {e}")

    # "Unfollow a User"
    elif menu_option == "Unfollow a User":
        st.subheader("Unfollow a User")

        try:
            # Получаем список пользователей, на которых подписан текущий пользователь
            followed_users = get_followed(current_user_id)

            if followed_users:
                # Селектор для выбора пользователя
                selected_user = st.selectbox(
                    "Select a user to unfollow:",
                    options=followed_users,
                    format_func=lambda user: f"{user['username']}"
                )
                if st.button("Unfollow"):
                    try:
                        delete_follow(current_user_id, selected_user["id"])
                        st.success(f"You have unfollowed {selected_user['username']}.")
                    except Exception as e:
                        st.error(f"Failed to unfollow user: {e}")
            else:
                st.write("You are not following any users.")
        except Exception as e:
            st.error(f"Failed to load followed users: {e}")

    # "Your Followers"
    elif menu_option == "Your Followers":
        st.subheader("Your Followers")

        try:
            followers = get_followers(current_user_id)
            if followers:
                st.write("You have the following followers:")
                for follower in followers:
                    st.write(f"User ID: {follower['id']} - {follower['username']}")
            else:
                st.write("You have no followers.")
        except Exception as e:
            st.error(f"Failed to fetch followers: {e}")

    # "Users You Follow"
    elif menu_option == "Users You Follow":
        st.subheader("Users You Follow")

        try:
            followed_users = get_followed(current_user_id)
            if followed_users:
                st.write("You are following the following users:")
                for user in followed_users:
                    st.write(f"User ID: {user['id']} - {user['username']}")
            else:
                st.write("You are not following any users.")
        except Exception as e:
            st.error(f"Failed to fetch followed users: {e}")