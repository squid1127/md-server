/**
 * Command Palette Class
 * Provides a command palette interface with the ability to register custom commands
 */
class CommandPalette {
  constructor() {
    // DOM elements
    this.palette = document.getElementById("cmd-palette");
    this.input = document.getElementById("cmd-input");
    this.list = document.getElementById("cmd-list");

    // Command storage
    this.commands = new Map();

    // Selection state
    this.selectedIndex = 0;

    // Initialize with default commands
    this.initDefaultCommands();

    // Set up event listeners
    this.initEventListeners();

    // Handle initial hash
    this.handleInitialHash();
  }

  /**
   * Initialize default commands
   * @private
   */
  initDefaultCommands() {
    const defaultCommands = [
      {
        name: "Go to Home",
        action: () => (window.location.href = "/"),
        icon: "home",
        group: "Navigation",
      },
      {
        name: "Markdown Editor",
        action: () => (window.location.href = "/editor"),
        icon: "edit",
        group: "Navigation",
      },
      {
        name: "Dashboard",
        action: () => (window.location.href = "/dash"),
        icon: "dashboard",
        group: "Navigation",
      },
    ];

    defaultCommands.forEach((cmd) => this.registerCommand(cmd));
  }

  /**
   * Register a new command
   * @param {Object} command - Command object
   * @param {string} command.name - Display name of the command
   * @param {Function} command.action - Function to execute when command is selected
   * @param {string} [command.icon] - Material icon name (defaults to "terminal")
   * @param {string} [command.group] - Command group/category
   * @param {string} [command.id] - Unique identifier (defaults to name)
   */
  registerCommand(command) {
    if (!command.name || typeof command.action !== "function") {
      throw new Error("Command must have a name and action function");
    }

    const id = command.id || command.name;
    this.commands.set(id, {
      id,
      name: command.name,
      action: command.action,
      icon: command.icon || "terminal",
      group: command.group || null,
    });
  }

  /**
   * Register multiple commands at once
   * @param {Array} commands - Array of command objects
   */
  registerCommands(commands) {
    if (!Array.isArray(commands)) {
      throw new Error("Commands must be an array");
    }
    commands.forEach((cmd) => this.registerCommand(cmd));
  }

  /**
   * Unregister a command
   * @param {string} id - Command ID or name
   */
  unregisterCommand(id) {
    return this.commands.delete(id);
  }

  /**
   * Get all registered commands
   * @returns {Array} Array of command objects
   */
  getCommands() {
    return Array.from(this.commands.values());
  }

  /**
   * Open the command palette
   */
  open() {
    // Clear any pending close timeout
    if (this.closeTimeout) {
      clearTimeout(this.closeTimeout);
      this.closeTimeout = null;
    }
    
    // Show the element and ensure it starts hidden for transition
    this.palette.style.display = 'flex';
    
    // Force the hidden state first, then remove it to trigger transition
    this.palette.classList.add("hidden");
    
    // Use requestAnimationFrame to ensure the hidden state is applied before removing it
    requestAnimationFrame(() => {
      this.palette.classList.remove("hidden");
      this.input.focus();
      this.selectedIndex = 0;
      this.renderList(this.getCommands());
    });

    // Global state to indicate an interface is open (for the escape key behavior)
    window.interfaceOpen = true;
  }

  /**
   * Close the command palette
   */
  close() {
    this.palette.classList.add("hidden");
    this.input.value = "";
    this.selectedIndex = 0;
    
    // Don't display: none - pointer events are blocked already via CSS
    // This allows for smoother transitions when reopening
    // // Hide the element completely after the transition completes
    // this.closeTimeout = setTimeout(() => {
    //   if (this.palette.classList.contains("hidden")) {
    //     this.palette.style.display = 'none';
    //   }
    // }, 200); // Match the CSS transition duration
    // Global state to indicate no interface is open
    window.interfaceOpen = false;
  }

  /**
   * Toggle the command palette
   */
  toggle() {
    if (this.palette.classList.contains("hidden")) {
      this.open();
    } else {
      this.close();
    }
  }

  /**
   * Render the command list
   * @param {Array} items - Commands to display
   * @private
   */
  renderList(items) {
    this.list.innerHTML = "";
    this.currentItems = items; // Store current items for keyboard navigation

    if (items.length > 0) {
      // Ensure selectedIndex is within bounds
      this.selectedIndex = Math.max(
        0,
        Math.min(this.selectedIndex, items.length - 1)
      );

      items.forEach((cmd, index) => {
        const li = document.createElement("li");
        li.classList.add("cmd-item");
        if (index === this.selectedIndex) {
          li.classList.add("selected");
        }
        li.innerHTML = `<span class="material-symbols-outlined cmd-icon">${
          cmd.icon
        }</span><span class="cmd-name"><strong>${
          cmd.group ? cmd.group + " - " : ""
        }</strong>${cmd.name}</span>`;
        li.addEventListener("click", () => {
          cmd.action();
          this.close();
        });
        this.list.appendChild(li);
      });
    } else {
      const li = document.createElement("p");
      li.classList.add("cmd-no-results");
      li.textContent = "No commands found.";
      this.list.appendChild(li);
      this.selectedIndex = -1; // No items to select
    }
  }

  /**
   * Filter commands based on query
   * @param {string} query - Search query
   * @returns {Array} Filtered commands
   * @private
   */
  filterCommands(query) {
    const lowerQuery = query.toLowerCase();
    return this.getCommands().filter(
      (cmd) =>
        cmd.name.toLowerCase().includes(lowerQuery) ||
        (cmd.group && cmd.group.toLowerCase().includes(lowerQuery))
    );
  }

  /**
   * Move selection up
   * @private
   */
  moveSelectionUp() {
    if (!this.currentItems || this.currentItems.length === 0) return;

    this.selectedIndex =
      this.selectedIndex > 0
        ? this.selectedIndex - 1
        : this.currentItems.length - 1;
    this.updateSelection();
  }

  /**
   * Move selection down
   * @private
   */
  moveSelectionDown() {
    if (!this.currentItems || this.currentItems.length === 0) return;

    this.selectedIndex =
      this.selectedIndex < this.currentItems.length - 1
        ? this.selectedIndex + 1
        : 0;
    this.updateSelection();
  }

  /**
   * Update visual selection in the list
   * @private
   */
  updateSelection() {
    const items = this.list.querySelectorAll(".cmd-item");
    items.forEach((item, index) => {
      if (index === this.selectedIndex) {
        item.classList.add("selected");
      } else {
        item.classList.remove("selected");
      }
    });
  }

  /**
   * Execute the currently selected command
   * @private
   */
  executeSelected() {
    if (
      !this.currentItems ||
      this.selectedIndex < 0 ||
      this.selectedIndex >= this.currentItems.length
    ) {
      return;
    }

    const selectedCommand = this.currentItems[this.selectedIndex];
    selectedCommand.action();
    this.close();
  }

  /**
   * Initialize event listeners
   * @private
   */
  initEventListeners() {
    // Filter commands on input
    this.input.addEventListener("input", (e) => {
      const query = e.target.value;
      this.selectedIndex = 0; // Reset selection when filtering
      this.renderList(this.filterCommands(query));
    });

    // Keyboard handling
    document.addEventListener("keydown", (e) => {
      // Only handle keyboard navigation when palette is open and input is focused
      const paletteOpen = !this.palette.classList.contains("hidden");
      const inputFocused = document.activeElement === this.input;

      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "p") {
        e.preventDefault();
        this.toggle();
        return;
      }

      if (e.key === "Escape") {
        if (paletteOpen) {
          e.preventDefault();
          this.close();
        }
        if (!window.interfaceOpen && !paletteOpen) {
          // If no other interface is open, open the palette
          e.preventDefault();
          this.open();
        }
        return;
      }

      // Handle keyboard navigation only when palette is open and input is focused
      if (paletteOpen && inputFocused) {
        switch (e.key) {
          case "ArrowUp":
            e.preventDefault();
            this.moveSelectionUp();
            break;
          case "ArrowDown":
            e.preventDefault();
            this.moveSelectionDown();
            break;
          case "Enter":
            e.preventDefault();
            this.executeSelected();
            break;
        }
      }
    });

    // Handle hash changes
    window.addEventListener("hashchange", () => {
      if (window.location.hash === "#cmd") {
        console.log("Opening Command Palette from URL hash (hashchange)");
        this.open();
        // Remove hash from URL
        history.replaceState("", document.title, window.location.pathname);
      }
    });

    // Click outside to close
    this.palette.addEventListener("click", (e) => {
      // Only close if clicking on the backdrop (not the container)
      if (e.target === this.palette) {
        this.close();
      }
    });
  }

  /**
   * Handle initial hash on page load
   * @private
   */
  handleInitialHash() {
    if (window.location.hash === "#cmd") {
      console.log("Opening Command Palette from URL hash (on load)");
      this.open();
      // Remove hash from URL
      history.replaceState("", document.title, window.location.pathname);
    }
  }
}

// Initialize the command palette only once
if (!window.cmdPalette) {
  console.log("Initializing Command Palette");
  window.cmdPalette = new CommandPalette();
}

// Expose the instance globally for other scripts to use
window.CommandPalette = CommandPalette;
