function routeFw(parameters) {

    var fw = {}; 

    var startingPath = parameters.startingPath || '/landing';
    var contentId = parameters.contentId || "view";

    if (!parameters.routeArray || parameters.routeArray[0]) 
    {
        alert("parameter object must specify array 'routeArray' with at least one element");
        return;
    }

    var routes = parameters.routeArray;

    function router() 
    {

        console.log("location.hash (the link that was clicked) is " + location.hash);
        

        // remove leading # from string that holds the clicked link
        var path = location.hash.slice(1) || '/';
        console.log('path (with no #) is ' + path);

        if (!routes[path]) 
        {
            document.getElementById(contentId).innerHTML = "Error: link '" + path +
                    "' was never added to the routing.";
        } 
        else 
        {
            // invoke the function that's specified by the ajaxFillId(routes[url], "view");
            // pass the correct route object to that function (either staticContent or jsonContent)
            routes[path](contentId); // invoke function routes[path], a JS funtion/component
        }
    }

    fw.printRoutes = function () 
    {
        console.log("routes will be printed on the next line ");
        console.log(routes);
    };

    window.addEventListener('hashchange', router);

    window.location.hash = startingPath;

    return fw;
}