document.getElementById("button").addEventListener("click", () => {
    const main = document.getElementById("main")
    const div = document.createElement("div")
    div.setAttribute("class", "login")
    div.textContent = "from button"
    main.appendChild(div)
});
