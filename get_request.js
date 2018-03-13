function frequency_request()
{
  var searchword = document.getElementById("searchword").value;
  var params = "word=" + searchword;
  var http = new XMLHttpRequest();
  //var base_url = "http://localhost:5000/frequency?"
  var base_url = "http://ds.lib.ucdavis.edu:5000/frequency?"
    var url = base_url + params;

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function ()
  {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    {
      drawplot(xmlHttp.responseText);
    }//if
  }//on readystate change
  xmlHttp.open("GET", url, true);
  xmlHttp.send(null);
}


function php_request()
{
  var searchword = document.getElementById("searchword").value;
  var params = "word=" + searchword;
  var base_url = "frequency.php";


  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", base_url, true);
  xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlHttp.send(params);

  xmlHttp.onreadystatechange = function ()
  {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    {
      console.log(xmlHttp.responseText);
      drawplot(xmlHttp.responseText);
    }//if
  }//on readystate change
}


