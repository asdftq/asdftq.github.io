(() => {
  const catalog = Array.isArray(window.INSTALL_WORTHY_CATALOG)
    ? window.INSTALL_WORTHY_CATALOG.filter((project) => project.visible !== false)
    : [];
  const installedId = new URLSearchParams(window.location.search).get("installed");
  const installedProject = catalog.find((project) => project.id === installedId);
  const projectList = document.getElementById("projectList");

  for (const project of catalog) {
    projectList.append(createProject(project, installedId));
  }

  if (installedProject) {
    document.title = `${installedProject.name} is ready — Install Worthy`;
    document.getElementById("installedTitle").textContent = `${installedProject.name} is ready.`;
    document.getElementById("installedCopy").textContent = installedProject.firstStep;
    document.getElementById("installedNote").hidden = false;
  }
})();

function createProject(project, installedId) {
  const article = document.createElement("article");
  article.className = "project";
  if (project.id === installedId) article.classList.add("is-installed");

  const icon = document.createElement("img");
  icon.className = "project-icon";
  icon.src = project.icon;
  icon.alt = "";
  icon.width = 42;
  icon.height = 42;

  const copy = document.createElement("div");
  copy.className = "project-copy";
  const title = document.createElement("h3");
  title.textContent = project.name;
  const description = document.createElement("p");
  description.textContent = project.description;
  copy.append(title, description);

  const actions = document.createElement("div");
  actions.className = "project-actions";

  for (const link of project.links) {
    if (project.id === installedId && link.platform === "Chrome") {
      const badge = document.createElement("span");
      badge.className = "installed-badge";
      badge.textContent = "Installed";
      actions.append(badge);
      continue;
    }

    const anchor = document.createElement("a");
    anchor.className = "project-link";
    anchor.href = link.url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.textContent = link.action || `Get for ${link.platform}`;
    anchor.setAttribute("aria-label", `${link.action || "Get"} ${project.name} for ${link.platform}`);
    actions.append(anchor);
  }

  article.append(icon, copy, actions);
  return article;
}
