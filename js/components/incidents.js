function incidents(id){
    var content = `
        <div id="tableWrapper">
            <div id="tableContent">
                <div>This is where the table content would be</div>
                <div>Filler content</div>
                <div>Filler content</div>
                <div>Filler content</div>
            </div>

        </div>`;
    
    document.getElementById(id).innerHTML = content;
}


