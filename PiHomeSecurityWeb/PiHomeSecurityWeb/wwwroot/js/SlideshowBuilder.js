var SlideshowBuilder = {};

SlideshowBuilder.modalBg = function () {
    var container = document.getElementById("tableHere");
    var bg = document.createElement("div");
    bg.className = "bg-modal";
    container.appendChild(bg);
}