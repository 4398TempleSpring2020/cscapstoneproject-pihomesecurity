var TableBuilder = {};

var keysToShow = ["incidentId", "dateRecorded", "badIncidentFlag", "lastAccessed", "adminComments",
    "deletionBlockFlag", "imagePath", "friendlyMatchFlag"];

var keysToDisplay = ["Incident Id", "Date Recorded", "Bad Incident Flag", "Last Accessed", "Admin Comments",
    "Deletion Block Flag", "Image Path", "Friendly Match Flag"];

TableBuilder.user = function(data, id) {
    console.log("Keys: " + Object.keys(data[0]));
    console.log("Values: " + Object.values(data[0]));

    var putTableHere = document.getElementById("tableHere");
    putTableHere.innerHTML = "";
    var tableEle = document.createElement("table");
    putTableHere.appendChild(tableEle);


    var tableHead = document.createElement("thead");
    tableEle.appendChild(tableHead);

    var headerRow = document.createElement("tr");
    tableHead.appendChild(headerRow);

    for (var i = 0; i < keysToShow.length; i++) {
        var headerItem = document.createElement("th");
        headerItem.innerHTML = keysToDisplay[i];
        headerRow.appendChild(headerItem);
    }

    var tableBody = document.createElement("tbody");
    tableEle.appendChild(tableBody);

    for (var i = 0; i < data.length; i++) {
        if (id == data[i].accountId) {
            var tableRow = document.createElement("tr");
            tableBody.appendChild(tableRow);
            for (var j = 0; j < Object.values(data[i]).length; j++) {
                if (keysToShow.includes(Object.keys(data[i])[j])) {
                    console.log("Adding data to table:");
                    console.log("Row " + i + ", Key: " + Object.keys(data[i])[j] + ": " + Object.values(data[i])[j]);
                    var tableData = document.createElement("td");
                    if (Object.keys(data[i])[j] == "imagePath") {
                        var tableLink = document.createElement("img");
                        tableLink.src = Object.values(data[i])[j];
                        tableData.appendChild(tableLink);
                    }
                    else {
                        tableData.innerHTML = Object.values(data[i])[j];
                    }
                    tableRow.appendChild(tableData);
                }
            }
        }
    }
}

TableBuilder.employee = function (data) {
    var id = document.getElementById("accountIdDropDown").value;
    console.log(data);

    var putTableHere = document.getElementById("tableHere");
    putTableHere.innerHTML = "";
    var tableEle = document.createElement("table");
    putTableHere.appendChild(tableEle);


    var tableHead = document.createElement("thead");
    tableEle.appendChild(tableHead);

    var headerRow = document.createElement("tr");
    tableHead.appendChild(headerRow);

    for (var i = 0; i < keysToShow.length; i++) {
        var headerItem = document.createElement("th");
        headerItem.innerHTML = keysToDisplay[i];
        headerRow.appendChild(headerItem);
    }

    var tableBody = document.createElement("tbody");
    tableEle.appendChild(tableBody);

    for (var i = 0; i < data.length; i++) {
        if (id == data[i].accountId) {
            var tableRow = document.createElement("tr");
            tableBody.appendChild(tableRow);
            for (var j = 0; j < Object.values(data[i]).length; j++) {
                if (keysToShow.includes(Object.keys(data[i])[j])) {
                    console.log("Adding data to table:");
                    console.log("Row " + i + ", Key: " + Object.keys(data[i])[j] + ": " + Object.values(data[i])[j]);
                    var tableData = document.createElement("td");
                    if (Object.keys(data[i])[j] == "imagePath") {
                        var tableLink = document.createElement("a");
                        tableLink.innerHTML = Object.values(data[i])[j];
                        tableLink.href = Object.values(data[i])[j];
                        tableData.appendChild(tableLink);
                    }
                    else {
                        tableData.innerHTML = Object.values(data[i])[j];
                    }
                    tableRow.appendChild(tableData);
                }
            }
        }
    }
}