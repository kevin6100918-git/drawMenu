import os
from urllib.parse import quote
from github import GithubException
from github import Github
from os.path import exists


# MENU_STORE_PATH = os.getenv("MENU_STORE_PATH")

# def get_image(meal:str, menu:str) -> bytes:
#     path = os.path.join(MENU_STORE_PATH, meal, menu)
#     with open(path, "rb") as f:
#         return f.read()


# Github username
GITHUB_USER = os.getenv("GITHUB_USER")
# Github acess token
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
# pygithub object
gitHub = Github(GITHUB_ACCESS_TOKEN)
# get that user by username
gitHubUser = gitHub.get_user(GITHUB_USER)
# get repo "drawMenu"
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")
gitHubRepo = gitHubUser.get_repo(name=GITHUB_REPO_NAME)

def gen_image_url(meal: str, menu: str) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO_NAME}/main/drawMenu/menus/{meal}/{quote(menu, encoding='utf-8')}"

def get_menu_list(meal: str) -> list[tuple[str, str]]:
    try:
        menuList = gitHubRepo.get_contents(path=f"drawMenu/menus/{meal}")

    except GithubException as err:
        print(err)

    return [ (menu.name, gen_image_url(meal, menu.name)) for menu in menuList ]


def upload_menu(meal: str, menuName: str, imageData: bytes) -> int:
    try:
        gitHubRepo.create_file(path=f"drawMenu/menus/{meal}/{menuName}", message=f"upload menu {menuName}", content=imageData)
    
    except GithubException as err:
        print(err)

        return err.status
    
    return 200

def delete_menu(meal: str, menuName: str) -> None:
    try:
        menu = gitHubRepo.get_contents(path=f"drawMenu/menus/{meal}/{menuName}")
        gitHubRepo.delete_file(path=menu.path, message=f"delete menu {menuName}", sha=menu.sha)

    except GithubException as err:
        print(err)

        return err.status
    return 200

