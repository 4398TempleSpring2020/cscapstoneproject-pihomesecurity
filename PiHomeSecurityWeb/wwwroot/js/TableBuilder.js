var TableBuilder = {};

TableBuilder.incidents = function (data, id) {
    var keysToShow = ["incidentId", "dateRecorded", "badIncidentFlag", "lastAccessed", "adminComments",
        "deletionBlockFlag", "microphonePath", "imagePaths", "friendlyMatchFlag", "ultrasonicPath"];

    var keysToDisplay = ["Incident Id", "Date Recorded", "Bad Incident Flag", "Last Accessed", "Admin Comments",
        "Deletion Block Flag", "Microphone Path", "Image Path", "Friendly Match Flag", "Ultrasonic Path"];

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
                    if (Object.keys(data[i])[j] == "imagePaths") {
                        var tableLink = document.createElement("img");
                        tableLink.src = TableBuilder.createImgLink(Object.values(data[i])[j]);
                        tableLink.style.width = "100px";
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

TableBuilder.useraccounts = function (data, id) {
    var keysToShow = ["userId", "username", "masterUserFlag", "dateCreated", "lastLogin"];

    var keysToDisplay = ["User Id", "Username", "Master User?", "Date Created", "Last Login"];

    console.log("Keys: " + Object.keys(data[0]));
    console.log("Values: " + Object.values(data[0]));

    console.log("1");

    var putTableHere = document.getElementById("tableHere");
    putTableHere.innerHTML = "";
    var tableEle = document.createElement("table");
    putTableHere.appendChild(tableEle);

    console.log("2");


    var tableHead = document.createElement("thead");
    tableEle.appendChild(tableHead);

    var headerRow = document.createElement("tr");
    tableHead.appendChild(headerRow);

    console.log("3");

    for (var i = 0; i < keysToShow.length; i++) {
        var headerItem = document.createElement("th");
        headerItem.innerHTML = keysToDisplay[i];
        headerRow.appendChild(headerItem);
    }

    console.log("4");

    var tableBody = document.createElement("tbody");
    tableEle.appendChild(tableBody);

    console.log("5");

    for (var i = 0; i < data.length; i++) {
        console.log("6 outter");
        console.log("data[i].accountId: " + data[i].accountId);
        console.log("id: " + id);
        if (id == data[i].accountId) {
            var tableRow = document.createElement("tr");
            tableBody.appendChild(tableRow);
            for (var j = 0; j < Object.values(data[i]).length; j++) {
                console.log("6 inner");
                if (keysToShow.includes(Object.keys(data[i])[j])) {
                    console.log("Adding data to table:");
                    console.log("Row " + i + ", Key: " + Object.keys(data[i])[j] + ": " + Object.values(data[i])[j]);
                    var tableData = document.createElement("td");
                    tableData.innerHTML = Object.values(data[i])[j];
                    tableRow.appendChild(tableData);
                }
            }
        }
    }
}

TableBuilder.createImgLink = function(urlTail){
    var urlHead = "https://whateverworks.s3.us-east-2.amazonaws.com/";
    return (urlHead + urlTail);
}