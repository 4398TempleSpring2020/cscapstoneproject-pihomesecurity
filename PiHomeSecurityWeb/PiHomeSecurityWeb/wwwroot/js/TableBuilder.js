var TableBuilder = {};

TableBuilder.incidents = function (data, id) {
    var jsonKeys = ["incidentId", "dateRecorded", "badIncidentFlag", "lastAccessed", "adminComments",
        "deletionBlockFlag", "microphonePath", "imagePaths", "friendlyMatchFlag", "ultrasonicPath"];

    var keysToDisplay = ["Incident Id", "Date Recorded", "Bad Incident Flag", "Last Accessed", "Admin Comments",
        "Deletion Block Flag", "Microphone Path", "Image Path", "Friendly Match Flag", "Ultrasonic Path", "Delete"];

    SlideshowBuilder.modalBg();

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

    for (var i = 0; i < keysToDisplay.length; i++) {
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
                if (jsonKeys.includes(Object.keys(data[i])[j])) {
                    console.log("Adding data to table:");
                    console.log("Row " + i + ", Key: " + Object.keys(data[i])[j] + ": " + Object.values(data[i])[j]);
                    var tableData = document.createElement("td");

                    switch (Object.keys(data[i])[j]) {
                        case "incidentId":
                            tableData.innerHTML = Object.values(data[i])[j];
                            var incidentId = Object.values(data[i])[j];
                            break;

                        case "adminComments":
                            var text = document.createElement("a");
                            text.className = "adminCommentText";
                            text.innerHTML = Object.values(data[i])[j] + '<span class="adminCommentTip">Click to edit</span>';
                            text.href = "EditComment?id=" + incidentId;
                            tableData.appendChild(text);
                            break;

                        case "microphonePath":
                            var tableLink = document.createElement("a");
                            tableLink.href = TableBuilder.createLink(Object.values(data[i])[j]);
                            tableLink.innerHTML = "Click Here";
                            tableData.appendChild(tableLink);
                            break;

                        case "imagePaths":
                            var tableLink = document.createElement("img");
                            var imgArray = TableBuilder.createImgArray(Object.values(data[i])[j]);
                            tableLink.src = TableBuilder.createLink(imgArray[0]);
                            tableLink.style.width = "100px";
                            tableData.appendChild(tableLink);
                            break;

                        case "ultrasonicPath":
                            var tableLink = document.createElement("a");
                            tableLink.href = TableBuilder.createLink(Object.values(data[i])[j]);
                            tableLink.innerHTML = "Click Here";
                            tableData.appendChild(tableLink);
                            break;

                        default:
                            tableData.innerHTML = Object.values(data[i])[j];
                    }

                    tableRow.appendChild(tableData);
                }
            }

            var deleteTableData = document.createElement("td");
            var deleteLink = document.createElement("a");
            deleteLink.innerHTML = "Delete";
            deleteLink.href = 'DeleteIncident?id=' + incidentId; 
            deleteTableData.appendChild(deleteLink);

            tableRow.appendChild(deleteTableData);

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

TableBuilder.createLink = function(urlTail){
    var urlHead = "https://d1uydrbc3kb9ug.cloudfront.net/";
    return (urlHead + urlTail);
}

TableBuilder.createImgArray = function (imgString) {
    console.log("FROM IMAGE ARRAY: " + imgString.split(",")[0]);
    return imgString.split(","); 
}