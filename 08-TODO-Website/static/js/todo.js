/* ========= USER-BASED TODO STORAGE ========= */

var loggedEmail = localStorage.getItem("loggedInUser");

function loadUsers() {
    try {
        return JSON.parse(localStorage.getItem("users") || "[]");
    } catch (e) {
        localStorage.setItem("users", "[]");
        return [];
    }
}

function saveUsers(users) {
    localStorage.setItem("users", JSON.stringify(users));
}

function loadTodosForCurrentUser() {
    var users = loadUsers();
    var user = null;
    for (var i = 0; i < users.length; i++) {
        if (users[i].email === loggedEmail) {
            user = users[i];
            break;
        }
    }
    if (user && user.todos) {
        return user.todos;
    }
    return [];
}

function saveTodosForCurrentUser(todos) {
    var users = loadUsers();
    var userFound = false;
    for (var i = 0; i < users.length; i++) {
        if (users[i].email === loggedEmail) {
            users[i].todos = todos;
            userFound = true;
            break;
        }
    }
    if (userFound) {
        saveUsers(users);
    }
}

/* ========= TODO LOGIC ========= */

function Todo(name, state) {
    this.name = name;
    this.state = state;
}

var todos = [];
var states = ["active", "inactive", "done"];
var tabs = ["all"].concat(states);
var currentTab = "all";

var form = null;
var input = null;

var buttons = [
    { action: "done", icon: "ok" },
    { action: "active", icon: "plus" },
    { action: "inactive", icon: "minus" },
    { action: "up", icon: "arrow-up" },
    { action: "down", icon: "arrow-down" },
    { action: "remove", icon: "trash" }
];

function initTodo() {
    // If somehow there is no logged-in user, do nothing (todo.html will redirect)
    if (!loggedEmail) {
        return;
    }

    // Load existing todos for this user
    todos = loadTodosForCurrentUser();

    form  = document.getElementById("new-todo-form");
    input = document.getElementById("new-todo-title");

    if (form) {
        form.onsubmit = function (event) {
            event.preventDefault();
            if (input && input.value && input.value.trim().length > 0) {
                todos.push(new Todo(input.value.trim(), "active"));
                input.value = "";
                saveTodosForCurrentUser(todos);
                renderTodos();
            }
        };
    }

    renderTodos();
}

function renderTodos() {
    var todoList = document.getElementById("todo-list");
    if (!todoList) return;

    todoList.innerHTML = "";

    var filtered = todos.filter(function (todo) {
        return currentTab === "all" || todo.state === currentTab;
    });

    filtered.forEach(function (todo, index) {
        var div1 = document.createElement("div");
        div1.className = "row";

        var div2 = document.createElement("div");
        div2.className = "col-xs-6 col-sm-9 col-md-10";
        div2.innerHTML = '<a class="list-group-item">' + todo.name + "</a>";

        var div3 = document.createElement("div");
        div3.className = "col-xs-6 col-sm-3 col-md-2 btn-group text-right";

        buttons.forEach(function (b) {
            var btn = document.createElement("button");
            btn.className = "btn btn-default btn-xs";
            btn.innerHTML = '<i class="glyphicon glyphicon-' + b.icon + '"></i>';
            div3.appendChild(btn);

            if (b.action === todo.state) {
                btn.disabled = true;
            }

            if (b.action === "remove") {
                btn.onclick = function () {
                    if (confirm("Delete: " + todo.name + "?")) {
                        todos.splice(todos.indexOf(todo), 1);
                        saveTodosForCurrentUser(todos);
                        renderTodos();
                    }
                };
            } else if (b.action === "up") {
                btn.onclick = function () {
                    if (index > 0) {
                        // Work on global todos, respecting current filtered order
                        var currentRealIndex = todos.indexOf(filtered[index]);
                        var prevRealIndex    = todos.indexOf(filtered[index - 1]);
                        var temp = todos[currentRealIndex];
                        todos[currentRealIndex] = todos[prevRealIndex];
                        todos[prevRealIndex] = temp;

                        saveTodosForCurrentUser(todos);
                        renderTodos();
                    }
                };
            } else if (b.action === "down") {
                btn.onclick = function () {
                    if (index < filtered.length - 1) {
                        var currentRealIndex = todos.indexOf(filtered[index]);
                        var nextRealIndex    = todos.indexOf(filtered[index + 1]);
                        var temp = todos[currentRealIndex];
                        todos[currentRealIndex] = todos[nextRealIndex];
                        todos[nextRealIndex] = temp;

                        saveTodosForCurrentUser(todos);
                        renderTodos();
                    }
                };
            } else {
                btn.onclick = function () {
                    todo.state = b.action;
                    saveTodosForCurrentUser(todos);
                    renderTodos();
                };
            }
        });

        div1.appendChild(div2);
        div1.appendChild(div3);
        todoList.appendChild(div1);
    });

    updateBadges();
}

function updateBadges() {
    var allBadge      = document.getElementById("badge-all");
    var activeBadge   = document.getElementById("badge-active");
    var inactiveBadge = document.getElementById("badge-inactive");
    var doneBadge     = document.getElementById("badge-done");

    if (!allBadge || !activeBadge || !inactiveBadge || !doneBadge) return;

    allBadge.innerText      = todos.length;
    activeBadge.innerText   = todos.filter(function (t) { return t.state === "active"; }).length;
    inactiveBadge.innerText = todos.filter(function (t) { return t.state === "inactive"; }).length;
    doneBadge.innerText     = todos.filter(function (t) { return t.state === "done"; }).length;
}

function selectTab(element) {
    currentTab = element.getAttribute("data-tab-name");

    var tabsElements = document.getElementsByClassName("todo-tab");
    for (var i = 0; i < tabsElements.length; i++) {
        tabsElements[i].classList.remove("active");
    }

    element.classList.add("active");
    renderTodos();
}
