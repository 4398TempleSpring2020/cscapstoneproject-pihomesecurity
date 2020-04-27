var TableBuilder = {};

TableBuilder.incidents = function (data, id, isEmployee) {
    var jsonKeys = ["incidentId", "dateRecorded", "badIncidentFlag", "lastAccessed", "adminComments",
        /*"deletionBlockFlag",*/ "microphonePath", "imagePaths", "friendlyMatchFlag", "ultrasonicPath"];

    var keysToDisplay = ["Incident Id", "Date/Time (UTC)", "Bad Incident Flag", "Last Accessed (UTC)", "Admin Comments",
        /*"Deletion Block Flag",*/ "Microphone File", "Images", "Friendly Match Flag", "Ultrasonic Data"];

    if (isEmployee) {
        keysToDisplay.push("Delete");
    }

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
                            if (isEmployee) {
                                var text = document.createElement("a");
                                text.className = "adminCommentText";
                                text.innerHTML = Object.values(data[i])[j] + '<span class="adminCommentTip">Click to edit</span>';
                                text.href = "EditComment?id=" + incidentId;
                                tableData.appendChild(text);
                            }
                            else {
                                tableData.innerHTML = Object.values(data[i])[j];
                            }
                            break;

                        case "microphonePath":
                            var tableLink = document.createElement("a");
                            tableLink.href = TableBuilder.createLink(Object.values(data[i])[j]);
                            tableLink.innerHTML = "Download";
                            tableData.appendChild(tableLink);
                            break;

                        case "imagePaths":
                            var imgArray = this.createImgArray(Object.values(data[i])[j]);
                            console.log("IMG ARRAY LENGTH: " + imgArray.length);

                            tableData.innerHTML = `
                                <a href=`+ imgArray[0] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[0] + ` style="width:100px;"></a>
                                <div style="display:none;">
                                    <a href=`+ imgArray[1] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[1] + ` style="width:100px;"></a>
                                    <a href=`+ imgArray[2] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[2] + ` style="width:100px;"></a>
                                    <a href=`+ imgArray[3] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[3] + ` style="width:100px;"></a>
                                    <a href=`+ imgArray[4] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[4] + ` style="width:100px;"></a>
                                </div>
                            `;

                            /*var HTMLcontent = ``;
                            HTMLcontent.concat(`<a href=` + imgArray[0] + ` data-lightbox="mygallery` + i.toString() + `"><img src=` + imgArray[0] + ` style="width:100px;"></a>\n`);
                            HTMLcontent.concat(`<div style="display:none;">\n`);
                            for (var i = 1; i < imgArray.length; i++) {
                                HTMLcontent.concat(`<a href=` + imgArray[i] + ` data - lightbox="mygallery` + i.toString() + `" > <img src=` + imgArray[i] + ` style = "width:100px;" ></a>\n`);
                            }
                            HTMLcontent.concat(`</div>`);

                            tableData.innerHTML = HTMLcontent;*/
                            break;

                        case "ultrasonicPath":
                            var tableLink = document.createElement("a");
                            tableLink.href = TableBuilder.createLink(Object.values(data[i])[j]);
                            tableLink.innerHTML = "Download";
                            tableData.appendChild(tableLink);
                            break;

                        default:
                            tableData.innerHTML = Object.values(data[i])[j];
                    }

                    tableRow.appendChild(tableData);
                }
            }

            if (isEmployee) {
                var deleteTableData = document.createElement("td");
                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.onclick = function () {
                    var row = this.parentNode.parentNode;
                    var id = row.cells[0].innerHTML;
                    if (confirm("Would you like to delete incident: " + id)) {
                        console.log("Running delete api");
                        $.ajax({
                            url: '/api/incidentdatas/' + id,
                            method: 'DELETE'
                        }).done(function () {
                            row.parentNode.removeChild(row);
                        });
                    }
                }
                deleteTableData.appendChild(deleteButton);

                tableRow.appendChild(deleteTableData);
            }

        }
    }
}

TableBuilder.useraccounts = function (data, id) {
    var keysToShow = ["userId", "username", "masterUserFlag", "dateCreated", "lastLogin"];

    var keysToDisplay = ["User Id", "Username", "Master User?", "Date Created (UTC)", "Last Login"];

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
    var returnArray = [];
    var splitString = imgString.split(",");
    for (i = 0; i < splitString.length; i++) {
        returnArray[i] = this.createLink(splitString[i]);
    }
    return returnArray;
}

TableBuilder.buildLightBox = function (imgArray) {
    var HTMLcontent = '';
    if (arraySize === 0) {
        return HTMLcontent;
    }
    else if (arraySize === 1) {
        HTMLcontent += ' < a href = ' + imgArray[i] + ' data - lightbox="mygallery' + i.toString() + '" > <img src=' + imgArray[i] + ' style = "width:100px;" ></a >';
    }
    else {
        HTMLcontent += ' < a href = ' + imgArray[0] + ' data - lightbox="mygallery' + i.toString() + '" > <img src=' + imgArray[0] + ' style = "width:100px;" ></a >';
        HTMLcontent += '<div style="display:none;">';
        for (i = 1; i < imgArray.length; i++) {
            HTMLcontent += ' < a href = ' + imgArray[i] + ' data - lightbox="mygallery' + i.toString() + '" > <img src=' + imgArray[i] + ' style = "width:100px;" ></a >';
        }
        HTMLcontent += '</div>';

    }
    

}