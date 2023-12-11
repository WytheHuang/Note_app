import streamlit as st

from src import utils


def login_func(email: str, pwd: str) -> str | None:
    token = utils.login(email, pwd)  # type: ignore
    if token is not None:
        st.session_state["token"] = token
        st.session_state["isLogin"] = True
    else:
        st.error("Login failed, please try again.")


st.set_page_config(
    page_title="Note App",
    layout="wide",
)

st.session_state["want_register"] = False if "want_register" not in st.session_state else st.session_state["want_register"]
st.session_state["just_sign_up"] = False if "just_sign_up" not in st.session_state else st.session_state["just_sign_up"]
st.session_state["isLogin"] = False if "isLogin" not in st.session_state else st.session_state["isLogin"]
st.session_state["token"] = "" if "token" not in st.session_state else st.session_state["token"]
st.session_state["first_render_note_column"] = (
    True if "first_render_note_column" not in st.session_state else st.session_state["first_render_note_column"]
)
st.session_state["first_render_note_content_column"] = (
    True if "first_render_note_content_column" not in st.session_state else st.session_state["first_render_note_content_column"]
)

st.sidebar.markdown("# Note App")

if not st.session_state["isLogin"]:
    email_preset = None
    if not st.session_state["want_register"]:
        if st.session_state["just_sign_up"]:
            st.success("Register success, please login.")
            email_preset = st.session_state["just_sign_up"]
            st.session_state["just_sign_up"] = False

        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("email", key="user_email", value=email_preset)
        with col2:
            pwd = st.text_input(
                "Password",
                key="password",
                type="password",
                on_change=lambda: login_func(st.session_state["user_email"], st.session_state["password"]),  # type: ignore
            )

        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "Login",
                key="login",
                on_click=lambda: login_func(st.session_state["user_email"], st.session_state["password"]),  # type: ignore
            )

        with col2:
            if st.button("Register", key="register"):
                st.session_state["want_register"] = True

                st.rerun()
    else:
        with st.form(key="register_form"):
            email = st.text_input("Email", key="email")
            pwd = st.text_input("Password", key="password", type="password")
            pwd_confirm = st.text_input("Confirm Password", key="password_confirm", type="password")

            if st.form_submit_button("Register"):
                if "@" not in email:
                    st.error("Email is not valid.")
                elif pwd != pwd_confirm:
                    st.error("Password and Confirm Password are not the same.")
                else:
                    result = utils.register(email, pwd, pwd_confirm)
                    if result == "200":
                        st.session_state["want_register"] = False
                        st.session_state["just_sign_up"] = email
                        st.rerun()
                    else:
                        st.error(result["detail"])  # type: ignore

        if st.button("Already have an account? Login", key="login"):
            st.session_state["want_register"] = False

            st.rerun()
else:
    with st.sidebar:
        st.markdown("## Note Book")

        notebooks = utils.get_notebook_list(st.session_state["token"])
        note_options = utils.get_note_options(st.session_state["token"], notebooks)

        st.radio(
            "Notebooks",
            [
                {
                    "title": "All Notes",
                    "note_book_id": None,
                    "options_id": "all",
                },
                *[
                    {
                        "title": notebook["title"],
                        "note_book_id": notebook["id"],
                        "options_id": notebook["id"],
                    }
                    for notebook in sorted(notebooks, key=lambda x: x["title"])
                ],
                {
                    "title": "Not in any notebook",
                    "note_book_id": None,
                    "options_id": "not_in_any",
                },
                {
                    "title": "Archive",
                    "note_book_id": None,
                    "options_id": "archive",
                },
                {
                    "title": "Trash",
                    "note_book_id": None,
                    "options_id": "trash",
                },
            ],
            key="notebooks",
            format_func=lambda x: x["title"],
            index=0,
            label_visibility="hidden",
        )

        create_notebook = st.button(
            "Create Note Book",
            key="create_notebook",
            on_click=lambda: utils.create_notebook(st.session_state["token"]),  # type: ignore
        )

        if st.button("Logout", key="logout"):
            st.session_state["isLogin"] = False
            st.session_state["token"] = ""
            st.session_state["notebook"] = None
            st.session_state["notes"] = None
            st.session_state["note_note_book"] = None
            st.session_state["note_title"] = ""
            st.session_state["note_content"] = ""

            st.rerun()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("## Note Book info")

        st.text_input(
            "NoteBook Title",
            value=st.session_state["notebooks"]["title"],  # type: ignore
            disabled=True if st.session_state["notebooks"]["options_id"] in ("all", "trash", "archive", "not_in_any") else False,
            key="notebook_title",
            on_change=lambda: utils.update_notebook_title(
                st.session_state["token"],
                st.session_state["notebooks"]["note_book_id"],
                st.session_state["notebook_title"],
            ),  # type: ignore
        )

        st.button(
            "Delete NoteBook",
            disabled=True if st.session_state["notebooks"]["options_id"] in ("all", "trash", "archive", "not_in_any") else False,
            key="delete_notebook",
            on_click=lambda: utils.delete_notebook(st.session_state["token"], st.session_state["notebooks"]["note_book_id"]),  # type: ignore
        )

        st.markdown("## Notes")
        # st.write(st.session_state["notebooks"])

        st.radio(
            "Notes",
            options=note_options[st.session_state["notebooks"]["options_id"]],  # type: ignore
            key="notes",
            format_func=lambda x: x["title"],
            index=0,
            label_visibility="hidden",
        )

        st.button(
            "Create Note",
            key="create_note",
            disabled=True if st.session_state["notebooks"]["options_id"] in ("trash", "archive") else False,  # type: ignore
            on_click=lambda: utils.create_note(  # type: ignore
                st.session_state["token"],
                st.session_state["notebooks"]["note_book_id"],  # type: ignore
            ),
        )

    with col2:
        st.markdown("## Note Content")
        # st.write(st.session_state["notes"])

        if st.session_state["notes"] is not None:
            id, in_notebook, note_title, note_content = utils.unpack_note_content(st.session_state["notes"])
            st.text_input(
                "Note Title",
                value=note_title,
                key="note_title",
                on_change=lambda: utils.update_note_title(st.session_state["token"], id, st.session_state["note_title"]),  # type: ignore
            )
            st.text_area(
                "Content",
                value=note_content,
                key="note_content",
                # height=500,
                on_change=lambda: utils.update_note_content(st.session_state["token"], id, st.session_state["note_content"]),  # type: ignore
            )

            st.selectbox(
                "Note Book",
                options=notebooks
                + [
                    {
                        "id": None,
                        "title": "Not in any notebook",
                    }
                ],
                key="note_note_book",
                format_func=lambda x: x["title"],
                index=st.session_state["notes"]["index"],  # type: ignore
                on_change=lambda: utils.update_notebook(st.session_state["token"], id, st.session_state["note_note_book"]["id"]),  # type: ignore
            )

            # st.write(st.session_state["note_note_book"])

            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                st.button(
                    "Archive",
                    key="move_archive",
                    disabled=True if st.session_state["notes"]["is_archived"] else False,  # type: ignore
                    on_click=lambda: utils.move_note_to_archive(st.session_state["token"], id),  # type: ignore
                )
            with sub_col2:
                st.button(
                    "Move to Trash",
                    key="move_trash",
                    disabled=True if st.session_state["notes"]["is_archive"] == "trash" else False,
                    on_click=lambda: utils.move_note_to_trash(st.session_state["token"], id),  # type: ignore
                )  # type: ignore
            with sub_col3:
                st.button(
                    "Delete Forever",
                    key="delete_forever",
                    on_click=lambda: utils.delete_note_forever(st.session_state["token"], id),  # type: ignore
                )
