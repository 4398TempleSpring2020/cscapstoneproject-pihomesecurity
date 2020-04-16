function DropDownBuilder(data) {
    console.log("Here is the data from DropDownBuilder: " + Object.values(data[0]));
    var dropdown = document.getElementById("accountIdDropDown");
    for (var i = 0; i < data.length; i++) {
        var option = document.createElement("option");
        var id = data[i].accountId;

        option.setAttribute("value", id);
        option.innerHTML = id;
        dropdown.appendChild(option);

    }

    dropdown.addEventListener("change", function () { buildTableById(data) }, false);
}