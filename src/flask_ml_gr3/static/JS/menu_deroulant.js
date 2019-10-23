/* When the user clicks on the button,
        toggle between hiding and showing the dropdown content */
        function myFunction() {
          document.getElementById("myDropdown").classList.toggle("show");
        }

        // Close the dropdown if the user clicks outside of it
        window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
              var openDropdown = dropdowns[i];
              if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
              }
            }
          }
        }

let menu = document.getElementById('menu')
menu.addEventListener('click', function() {
        menu.style.textAlign = "left";
    },true);

//**************

/*
const mongo = require('mongodb').MongoClient;
let url = "mongodb://localhost:27017/";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  let dbo = db.db("nba_DB");
  //Find all documents in the customers collection:
  db.collection("nba_collection").find({}).toArray(function(err, result) {
    if (err) throw err;
    console.log(result);
    db.close();
  });
});
*/
//let obj = JSON.parse(mycol.find({}));
//document.getElementById("demo").innerHTML = obj.Player + ", " + obj.Age;

let iframe_id = document.getElementsByClassName('iframeMenu');

iframe_id[0].addEventListener('mouseover', function(e) {
    /*iframe_id[0].style.cursor = "pointer";*/
    },true);


/*let win = iframe_id.contentWindow;
let doc = iframe_id.contentDocument? iframe_id.contentDocument: iframe_id.contentWindow.document;

doc.style.cursor = "pointer";*/

