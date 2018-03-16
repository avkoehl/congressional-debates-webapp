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

function php_distance_request()
{
  var searchwords = document.getElementById("w2w_searchword").value;
  var word = searchwords.split(',')[0].trim();
  var word2 = searchwords.split(',')[1].trim();
  var params = "word=" + word + "&word2=" + word2;
  var base_url = "distance.php";

  document.getElementById("w2w_status").innerHTML = "processing request for word: " + searchwords;
  document.getElementById("wordw2w").innerHTML = "";
  console.log(params);


  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", base_url, true);
  xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlHttp.send(params);

  xmlHttp.onreadystatechange = function ()
  {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    {
      console.log(xmlHttp.responseText);
      document.getElementById("w2w_status").innerHTML = word + " " + word2;
      draww2wplot(xmlHttp.responseText);
    }//if
  }//on readystate change
}





