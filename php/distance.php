<?php

  $word = $_POST['word'];
  $word2 = $_POST['word2'];
  $baseurl = "http://localhost:5000/distance?word=";
  $url = $baseurl.$word."&word2=".$word2;
  $curl = curl_init($url);
  $result=curl_exec($curl);
  curl_close($curl);

 ?>
