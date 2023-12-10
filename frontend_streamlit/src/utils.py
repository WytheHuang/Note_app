from typing import Any

import requests
import config


def login(email: str, pwd: str) -> str | None:
    res = requests.post(
        f"{config.API_ROOT}/auth/obtain",
        json={
            "email": email,
            "password": pwd,
        },
    )
    if res.status_code == 200:
        return eval(res.content.decode("utf-8"))["access"]
    else:
        return None


def get_notebook_list(access_token: str) -> list[dict[str, str]]:
    res = requests.get(
        f"{config.API_ROOT}/notebooks",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return sorted(res.json(), key=lambda x: x["title"])


def _get_note_list(
    access_token=None,
    note_book_id=None,
    all: str = "true",
    is_archive: str | None = None,
    is_trash: str | None = None,
    notebook_index: int | None = None,
):
    assert access_token is not None

    query_params = {}

    if note_book_id is None:
        if is_archive is not None:
            query_params = {
                "all": "false",
                "is_archived": is_archive,
            }
        elif is_trash is not None:
            query_params = {
                "all": "false",
                "is_trash": is_trash,
            }
        else:
            query_params = {
                "all": all,
            }
    else:
        query_params = {
            "all": "false",
            "note_book_id": note_book_id,
        }

    res = requests.get(
        f"{config.API_ROOT}/notes",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        params=query_params,
    )

    return [
        {
            "index": notebook_index,
            **note,
        }
        for note in sorted(res.json(), key=lambda x: x["title"])
    ]


def get_note_options(access_token: str, notebooks: list[dict[str, str]]) -> dict[str | list[Any], list[Any]]:
    return {
        "all": _get_note_list(access_token, all="true"),
        **{
            notebook["id"]: _get_note_list(
                access_token,
                all="false",
                note_book_id=notebook["id"],
                notebook_index=i,
            )
            for i, notebook in enumerate(notebooks)
        },
        "not_in_any": _get_note_list(access_token, all="false"),
        "archive": _get_note_list(
            access_token,
            all="false",
            is_archive="true",
        ),
        "trash": _get_note_list(
            access_token,
            all="false",
            is_trash="true",
        ),
    }


def unpack_note_content(note_content: dict[str, str | bool | int]) -> tuple[str, str, str, str]:
    return note_content["id"], note_content["note_book"], note_content["title"], note_content["content"]  # type: ignore


def create_notebook(
    access_token: str,
) -> bool:
    res = requests.post(
        f"{config.API_ROOT}/notebooks",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "title": "Untitled",
        },
    )

    return res.status_code == 200


def update_notebook_title(access_token: str, notebook_id: str, new_title: str) -> bool:
    res = requests.put(
        f"{config.API_ROOT}/notebooks/{notebook_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "title": new_title,
        },
    )

    return res.status_code == 200

def delete_notebook(access_token: str, notebook_id: str) -> bool:
    res = requests.delete(
        f"{config.API_ROOT}/notebooks/{notebook_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return res.status_code == 200


def create_note(
    access_token: str,
    note_book_id: str | None = None,
) -> bool:
    if note_book_id is None:
        res = requests.post(
            f"{config.API_ROOT}/notes",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "title": "Untitle",
                "content": "content",
            },
        )
    else:
        res = requests.post(
            f"{config.API_ROOT}/notes",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "title": "Untitle",
                "content": "content",
                "note_book_id": note_book_id,
            },
        )

    return res.status_code == 200


def update_note_title(access_token: str, note_id: str, new_title: str) -> bool:
    res = requests.patch(
        f"{config.API_ROOT}/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "title": new_title,
        },
    )

    return res.status_code == 200


def update_note_content(access_token: str, note_id: str, new_content: str) -> bool:
    res = requests.patch(
        f"{config.API_ROOT}/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "content": new_content,
        },
    )

    return res.status_code == 200


def update_notebook(access_token: str, note_id: str, new_notebook_id: str | None) -> bool:
    if new_notebook_id is None:
        res = requests.patch(
            f"{config.API_ROOT}/notes/set_note_book_none/{note_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "note_book_id": new_notebook_id,
            },
        )
    else:
        res = requests.patch(
            f"{config.API_ROOT}/notes/{note_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "note_book_id": new_notebook_id,
            },
        )

    return res.status_code == 200  # type: ignore


def move_note_to_archive(access_token: str, note_id: str) -> bool:
    res = requests.patch(
        f"{config.API_ROOT}/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "is_trash": False,
            "is_archived": True,
        },
    )

    return res.status_code == 200


def move_note_to_trash(access_token: str, note_id: str) -> bool:
    res = requests.patch(
        f"{config.API_ROOT}/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "is_trash": True,
            "is_archived": False,
        },
    )

    return res.status_code == 200


def delete_note_forever(access_token: str, notebook_id: str) -> bool:
    res = requests.delete(
        f"{config.API_ROOT}/notes/{notebook_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return res.status_code == 200
