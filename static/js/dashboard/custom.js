$(function () {
  "use strict";

  $(".preloader").fadeOut();
  // this is for close icon when navigation open in mobile view
  $(".nav-toggler").on("click", function () {
    $("#main-wrapper").toggleClass("show-sidebar");
    $(".nav-toggler i").toggleClass("ti-menu");
  });
  $(".search-box a, .search-box .app-search .srh-btn").on("click", function () {
    $(".app-search").toggle(200);
    $(".app-search input").focus();
  });

  // ==============================================================
  // Resize all elements
  // ==============================================================
  $("body, .page-wrapper").trigger("resize");
  $(".page-wrapper").delay(20).show();

  //****************************
  /* This is for the mini-sidebar if width is less then 1170*/
  //****************************
  var setsidebartype = function () {
    var width = window.innerWidth > 0 ? window.innerWidth : this.screen.width;
    if (width < 1170) {
      $("#main-wrapper").attr("data-sidebartype", "mini-sidebar");
    } else {
      $("#main-wrapper").attr("data-sidebartype", "full");
    }
  };
  $(window).ready(setsidebartype);
  $(window).on("resize", setsidebartype);
});
window.onload = function () {
  if (bitcoin_toggler) {
    // BTC CURRENT PRICE
    var bitcoinPrice = new XMLHttpRequest();
    bitcoinPrice.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        btcConverter(JSON.parse(this.responseText).RAW.BTC.USD.PRICE);
      }
    };
    bitcoinPrice.open(
      "GET",
      "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD",
      true
    );
    bitcoinPrice.send();
  }
};

function toggleNavDropDown() {
    document.getElementById("dropdownMenu").classList.toggle("show");
  };
