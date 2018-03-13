<?php

  $word = $_POST['word'];
  $baseurl = "http://localhost:5000/frequency?word=";
  $url = $baseurl.$word;
  $curl = curl_init($url);
  $result=curl_exec($curl);
  curl_close($curl);

 ?>
