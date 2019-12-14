var request;

function getRequestObject()      {
   if ( window.ActiveXObject)  {
      return ( new ActiveXObject("Microsoft.XMLHTTP")) ;
   } else if (window.XMLHttpRequest)  {
      return (new XMLHttpRequest())  ;
   } else {
      return (null) ;
   }
}

// Lista wszystkich notatek
function pomiar() {
   document.getElementById('result').innerHTML = '';
   document.getElementById('data').innerHTML = '';

   request = getRequestObject() ;
   request.onreadystatechange = function() {
      if (request.readyState === 4)    {
         document.getElementById('result').innerHTML = request.response;
      }
   };

   request.open("GET", "http://localhost:5000/pomiar/", true);
   request.send(null);
}

// Lista wszystkich notatek z kategorii
function ask_kategoria() {
   let form1 = "<form name='ask'><table>" ;
   form1    += "<tr><td>urzadzenie</td><td><select name=\"urzadzenie\">\n" +
       "  <option value=\"czujnik1\">czujnik1</option>\n" +
       "  <option value=\"czujnik2\">czujnik2</option>\n" +
       "  <option value=\"czujnik3\">czujnik3</option>\n" +
       "  <option value=\"czujnik4\">czujnik4</option>\n" +
       "</select></td></tr>";
   form1    += "<tr><td></td><td><input type='button' value='Sprawdź' onclick='notatki_kategoria(this.form)' ></input></td></tr>";
   form1    += "</table></form>";
   document.getElementById('data').innerHTML = form1;
   document.getElementById('result').innerHTML = '';
}

function notatki_kategoria(form) {
   document.getElementById('result').innerHTML = '';
   document.getElementById('data').innerHTML = '';

   request = getRequestObject() ;
   request.onreadystatechange = function() {
      if (request.readyState === 4) {
         document.getElementById('result').innerHTML = request.response;
      }
   };

   request.open("GET", "http://localhost:5000/pomiar/" + form.urzadzenie.value+"/", true);
   request.send(null);
}

// Lista notatek z kategorii z dat


function ask_kategoria_daty() {
   let form1 = "<form name='ask'><table>" ;
   form1    += "<tr><td>urzadzenie</td><td><select name=\"urzadzenie\">\n" +
       "  <option value=\"czujnik1\">czujnik1</option>\n" +
       "  <option value=\"czujnik2\">czujnik2</option>\n" +
       "  <option value=\"czujnik3\">czujnik3</option>\n" +
       "  <option value=\"czujnik4\">czujnik4</option>\n" +
       "</select></td></tr>";
   form1    += "<tr><td>data1</td><td><input type='text' name='data1' value='data1' ></input></td></tr>";
   form1    += "<tr><td>data2</td><td><input type='text' name='data2' value='data2' ></input></td></tr>";
   form1    += "<tr><td></td><td><input type='button' value='Sprawdź' onclick='notatki_kategoria_daty(this.form)' ></input></td></tr>";
   form1    += "</table></form>";
   document.getElementById('data').innerHTML = form1;
   document.getElementById('result').innerHTML = '';
}

function notatki_kategoria_daty(form) {
   document.getElementById('result').innerHTML = '';
   document.getElementById('data').innerHTML = '';

   request = getRequestObject() ;
   request.onreadystatechange = function() {
      if (request.readyState === 4) {
         document.getElementById('result').innerHTML = request.response;
      }
   };

   URL = "http://localhost:5000/pomiar/" + form.urzadzenie.value+ "/" + form.data1.value + "/" + form.data2.value + "/";
   request.open("GET", URL, true);
   request.send(null);
}

// Wstawianie rekordow do bazy
// function podajdane(){
//    let form1 = "<form name='ask'><table>" ;
//    form1    += "<tr><td>urzadzenie</td><td><select id='selu' name=\"urzadzenie\" onchange='podajdane()'>\n" +
//        "  <option value=\"czujnik1\">czujnik1</option>\n" +
//        "  <option value=\"czujnik2\">czujnik2</option>\n" +
//        "  <option value=\"czujnik3\">czujnik3</option>\n" +
//        "  <option value=\"czujnik4\">czujnik4</option>\n" +
//        "</select></td></tr>";
//
//    let value = document.getElementById('selu').value;
//
//    if(value === "czujnik1") {
//        form1 += "<tr><td>temp</td><td><input type='text' name='dane' value='temp' ></input></td></tr>";
//        form1 += "<tr><td></td><td><input type='button' value='Dodaj' onclick='notatki_kategoria_daty(this.form)' ></input></td></tr>";
//        form1 += "</table></form>";
//    }
//    else if(value === "czujnik2") {
//        form1 += "<tr><td>cisnienie</td><td><input type='text' name='dane' value='cisnienie' ></input></td></tr>";
//        form1 += "<tr><td></td><td><input type='button' value='Dodaj' onclick='notatki_kategoria_daty(this.form)' ></input></td></tr>";
//        form1 += "</table></form>";
//    }
//    else if(value === "czujnik3") {
//        form1 += "<tr><td>predkosc</td><td><input type='text' name='dane' value='predkosc' ></input></td></tr>";
//        form1 += "<tr><td></td><td><input type='button' value='Dodaj' onclick='notatki_kategoria_daty(this.form)' ></input></td></tr>";
//        form1 += "</table></form>";
//    }
//    else if(value === "czujnik3") {
//        form1 += "<tr><td>wysokosc</td><td><input type='text' name='dane' value='wysokosc' ></input></td></tr>";
//        form1 += "<tr><td></td><td><input type='button' value='Dodaj' onclick='notatki_kategoria_daty(this.form)' ></input></td></tr>";
//        form1 += "</table></form>";
//    }
//
//    document.getElementById('data').innerHTML = form1;
//    document.getElementById('result').innerHTML = '';
// }

function ins_form() {
   let form1 = "<form name='add'><table>" ;
   form1    += "<tr><td>urzadzenie</td><td><select id='selu' name=\"urzadzenie\">\n" +
       "  <option value=\"czujnik1\">czujnik1</option>\n" +
       "  <option value=\"czujnik2\">czujnik2</option>\n" +
       "  <option value=\"czujnik3\">czujnik3</option>\n" +
       "  <option value=\"czujnik4\">czujnik4</option>\n" +
       "</select></td></tr>";
   form1 += "<tr><td>dane</td><td><input type='text' name='dane' value='dane' ></input></td></tr>";
   form1 += "<tr><td></td><td><input type='button' value='Dodaj' onclick='insert(this.form)' ></input></td></tr>";
   form1 += "</table></form>";
   document.getElementById('data').innerHTML = form1;
   document.getElementById('result').innerHTML = '';
}

function insert(form)  {
    let row = {};
    row.urzadzenie = form.urzadzenie.value;
    let data = {}

    data.dane = form.dane.value;


    row.dane = data;

    let txt = JSON.stringify(row);

    document.getElementById('result').innerHTML = '';
    document.getElementById('data').innerHTML = '';
    request = getRequestObject() ;
    request.onreadystatechange = function() {
       if (request.readyState === 4 && request.status === 200 )    {
          document.getElementById('result').innerHTML = request.response;
       }
    };

    URL = "http://localhost:5000/pomiar/" + form.urzadzenie.value+"/";
    request.open("POST", URL, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(txt);
}

// Usuwanie rekordow z bazy danych
function ask_urzadzenie_data() {
   let form1 = "<form name='ask'><table>" ;
   form1    += "<tr><td>urzadzenie</td><td><select name=\"urzadzenie\">\n" +
       "  <option value=\"czujnik1\">czujnik1</option>\n" +
       "  <option value=\"czujnik2\">czujnik2</option>\n" +
       "  <option value=\"czujnik3\">czujnik3</option>\n" +
       "  <option value=\"czujnik4\">czujnik4</option>\n" +
       "</select></td></tr>";
   form1    += "<tr><td>data1</td><td><input type='text' name='data1' value='data1' ></input></td></tr>";
   form1    += "<tr><td>data2</td><td><input type='text' name='data2' value='data2' ></input></td></tr>";
   form1    += "<tr><td></td><td><input type='button' value='Usuń' onclick='_delete(this.form)' ></input></td></tr>";
   form1    += "</table></form>";
   document.getElementById('data').innerHTML = form1;
   document.getElementById('result').innerHTML = '';
}

function _delete(form) {
    let urzadzenie = form.urzadzenie.value;
    let data1 = form.data1.value;
    let data2 = form.data2.value;

    document.getElementById('result').innerHTML = '';
    document.getElementById('data').innerHTML = '';

    request = getRequestObject() ;
    request.onreadystatechange = function() {
       if (request.readyState === 4 )    {
           document.getElementById('result').innerHTML = request.response;
       }
    };

    URL = "http://localhost:5000/pomiar/" + urzadzenie + "/" + data1 + "/" + data2 + "/";
    request.open("DELETE", URL, true);
    request.send(null);
}
