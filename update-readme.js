const fs = require("fs");
// Remove: const fetch = require("node-fetch");

const username = "Ukihunter";

async function getRepos() {
  const res = await fetch(
    `https://api.github.com/users/${username}/repos?sort=updated`
  );
  return res.json();
}

function generateTable(repos) {
  let table =
    "| Project Name | Description | Link |\n| ------------ | ----------- | ---- |\n";
  repos.forEach((repo) => {
    table += `| ${repo.name} | ${repo.description || ""} | [${repo.html_url}](${
      repo.html_url
    }) |\n`;
  });
  return table;
}

(async () => {
  const repos = await getRepos();
  const table = generateTable(repos.slice(0, 5)); // Top 5 projects
  let readme = fs.readFileSync("README.md", "utf8");
  readme = readme.replace(
    /## My Projects[\s\S]*?## Collaborative Projects/,
    `## My Projects\n\n${table}\n## Collaborative Projects`
  );
  fs.writeFileSync("README.md", readme);
})();
