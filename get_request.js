function frequency_request()
{
  var searchword = document.getElementById("searchword").value;
  var params = "word=" + searchword;
  var http = new XMLHttpRequest();
  var base_url = "http://localhost:5000/frequency?"
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

