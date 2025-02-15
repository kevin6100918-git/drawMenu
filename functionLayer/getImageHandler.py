import os
from github import GithubException
from github import Github


MENU_STORE_PATH = os.getenv("MENU_STORE_PATH")

def get_image(meal:str, menu:str) -> bytes:
    path = os.path.join(MENU_STORE_PATH, meal, menu)
    with open(path, "rb") as f:
        return f.read()


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

def get_menu_list(meal: str) -> list:
    try:
        menuList = gitHubRepo.get_contents(path=f"drawMenu/menus/{meal}")

    except GithubException as err:
        print(err)

    return [ (menu.name, fr"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO_NAME}/main/{menu.path}") for menu in menuList ]