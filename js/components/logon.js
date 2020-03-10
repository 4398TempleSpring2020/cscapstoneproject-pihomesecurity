function logon(id){
    var content = `
        <div class="wrapper fadeInDown">
            <div id="formContent">
              <!-- Tabs Titles -->
              <h2 class="active"> Sign In </h2>

              <!-- Icon -->
              <div class="fadeIn first">
                    <img src="logo.png" id="icon" alt="User Icon"/>
              </div>

              <!-- Login Form -->
              <form action="#/incidents">
                    <input type="text" id="login" class="fadeIn second" placeholder="Email">
                    <input type="text" id="password" class="fadeIn third" placeholder="Password">
                    <input type="submit" class="fadeIn fourth" value="Log In">
              </form>

            </div>
        </div>`;

        document.getElementById(id).innerHTML = content;
}


