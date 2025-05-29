import os
import requests

USERNAME = "ukihunter"
TOKEN = os.environ["GITHUB_TOKEN"]

def get_repos(url):
    repos = []
    page = 1
    while True:
        r = requests.get(f"{url}&page={page}", headers={"Authorization": f"token {TOKEN}"})
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def format_table(repos):
    lines = ["| Project Name | Description | Stars | Link |",
             "|-------------|-------------|-------|------|"]
    for repo in repos:
        name = repo["name"]
        desc = repo["description"] or ""
        stars = repo["stargazers_count"]
        url = repo["html_url"]
        lines.append(f"| {name} | {desc} | {stars} | [Repo]({url}) |")
    return "\n".join(lines)

def main():
    own_repos = get_repos(f"https://api.github.com/users/{USERNAME}/repos?type=owner&per_page=100")
    collab_repos = get_repos(f"https://api.github.com/users/{USERNAME}/repos?type=member&per_page=100")

    with open("README.md", "r") as f:
        readme = f.read()

    own_table = format_table(own_repos)
    collab_table = format_table(collab_repos)

    # Replace markers in README.md
    new_readme = readme
    new_readme = new_readme.split("<!-- MY_PROJECTS_START -->")[0] + \
        "<!-- MY_PROJECTS_START -->\n" + own_table + "\n<!-- MY_PROJECTS_END -->" + \
        new_readme.split("<!-- MY_PROJECTS_END -->")[1]

    new_readme = new_readme.split("<!-- COLLAB_PROJECTS_START -->")[0] + \
        "<!-- COLLAB_PROJECTS_START -->\n" + collab_table + "\n<!-- COLLAB_PROJECTS_END -->" + \
        new_readme.split("<!-- COLLAB_PROJECTS_END -->")[1]

    with open("README.md", "w") as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()
