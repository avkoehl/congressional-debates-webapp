function php_frequency_request()
{
  var searchword = document.getElementById("searchword").value;
  var params = "word=" + searchword;
  var base_url = "frequency.php";

  document.getElementById("status").innerHTML = "processing request for word: " + searchword;
  document.getElementById("wordfreq").innerHTML = "";


  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", base_url, true);
  xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlHttp.send(params);

  xmlHttp.onreadystatechange = function ()
  {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    {
      //console.log(xmlHttp.responseText);
      document.getElementById("status").innerHTML = searchword;
      drawlinearplot(xmlHttp.responseText);
    }//if
  }//on readystate change
}

function php_distribution_request()
{
  var searchword = document.getElementById("dist_searchword").value;
  var params = "word=" + searchword;
  var base_url = "distribution.php";

  document.getElementById("dist_status").innerHTML = "processing request for word: " + searchword;
  document.getElementById("worddist").innerHTML = "";


  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", base_url, true);
  xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlHttp.send(params);

  xmlHttp.onreadystatechange = function ()
  {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    {
      //console.log(xmlHttp.responseText);
      document.getElementById("dist_status").innerHTML = searchword;
      drawdistplot(xmlHttp.responseText);
    }//if
  }//on readystate change
}



