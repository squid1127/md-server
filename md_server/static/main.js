/*
Main JavaScript for MD Server (for base.html)
Handles:
- Main Width Button
- Header Scroll Effect
- Command Palette Integration
*/

// Width Params
const NO_OPTIONS_ICON = null; // Icon when no width options available
const WIDTH_CLASSES = [
  // Width Classes and their Icons
  { name: "normal", width: 800, icon: "fullscreen_exit", minWidth: 0 },
  { name: "wide", width: 1200, icon: "arrow_range", minWidth: 800 },
  { name: "full", width: null, icon: "fullscreen", minWidth: 1200 },
];

function determineWidthList() {
  const widthList = [];
  const screenWidth = window.innerWidth;
  for (const cls of WIDTH_CLASSES) {
    if (!cls.minWidth || screenWidth >= cls.minWidth) {
      widthList.push(cls);
    }
  }
  return widthList;
}
function applyNextIcon() {
  const mainWidthBtn = document.getElementById("main-width");
  const currentClasses = determineWidthList();
  if (currentClasses.length <= 1) {
    if (NO_OPTIONS_ICON) {
      mainWidthBtn.innerHTML = `<span class="material-symbols-outlined">${NO_OPTIONS_ICON}</span>`;
      mainWidthBtn.style.display = "";
    } else {
      mainWidthBtn.style.display = "none";
    }
    return;
  }
  let i = 0;
  for (; i < currentClasses.length; i++) {
    if (document.body.classList.contains(currentClasses[i].name)) {
      break;
    }
  }
  mainWidthBtn.innerHTML = `<span class="material-symbols-outlined">${
    currentClasses[(i + 1) % currentClasses.length].icon
  }</span>`;
  mainWidthBtn.style.display = "";
}
function applyWidthClass(index) {
  // Remove all width classes
  for (const cls of WIDTH_CLASSES) {
    document.body.classList.remove(cls.name);
  }
  // Add the specified class if not "normal"
  if (index > 0 && index < WIDTH_CLASSES.length) {
    document.body.classList.add(WIDTH_CLASSES[index].name);
  }

  // Show next available option on button
  applyNextIcon();
}

// Change Main Width
const mainWidthBtn = document.getElementById("main-width");
mainWidthBtn.addEventListener("click", () => {
  let currentClasses = determineWidthList();
  if (currentClasses.length <= 1) {
    mainWidthBtn.innerHTML = `<span class="material-symbols-outlined">${NO_OPTIONS_ICON}</span>`;
    return;
  }
  let i = 0;
  for (; i < currentClasses.length; i++) {
    if (document.body.classList.contains(currentClasses[i].name)) {
      break;
    }
  }

  applyWidthClass((i + 1) % currentClasses.length);
});

// Show/Hide Main Width Button based on screen size
function updateMainWidthButton() {
  applyNextIcon();
}

// Set initial width class
applyWidthClass(parseInt("{{ initial_width_index | default(0) }}"));

// Initial check
updateMainWidthButton();

// Update button on resize
window.addEventListener("resize", updateMainWidthButton);

// Command Palette - Add width controls
document.addEventListener("DOMContentLoaded", () => {
  if (window.cmdPalette) {
    window.cmdPalette.registerCommands([
      {
        name: "Set Width: Normal",
        action: () => applyWidthClass(0),
        icon: "fullscreen_exit",
        group: "View",
      },
      {
        name: "Set Width: Wide",
        action: () => applyWidthClass(1),
        icon: "arrow_range",
        group: "View",
      },
      {
        name: "Set Width: Full",
        action: () => applyWidthClass(2),
        icon: "fullscreen",
        group: "View",
      },
    ]);
  } else {
    console.warn("Command Palette not loaded");
  }
});

// Header scroll effect
window.addEventListener("scroll", () => {
  const header = document.querySelector(".header");
  if (window.scrollY < 16) {
    header.classList.remove("scrolled");
  } else {
    header.classList.add("scrolled");
  }
});