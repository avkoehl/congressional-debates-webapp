function openTab(event, tabName) {
  var i, tab, tablink;
  tab = document.getElementsByClassName("tab");
  tablink = document.getElementsByClassName("tablink");

  for (i =0; i < tab.length; i++)
  {
    tab[i].style.display="none";
  }
  for (i=0; i < tablink.length; i++)
  {
    tablink[i].className = tablink[i].className.replace("active", "");
  }

  document.getElementById(tabName).style.display="block";
  event.currentTarget.className += " active";
 }



