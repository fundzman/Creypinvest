/*
Author: Creyp Invest Inc.
*/

(function () {
  //===== Prealoder
  var btcConvertValue = document.getElementsByClassName("convert-value-btc");
  var btcConvertValuefees =
    document.getElementsByClassName("calculate-btc-fees");
  var totalAmount = document.getElementsByClassName("total-price-value");
  var hiddenBtcAmount = document.getElementsByClassName("btc-hidden-value");
  var hiddenFeesAmount = document.getElementsByClassName("price-fees-hidden-value");
  var hiddenFeesBtcAmount = document.getElementsByClassName("btc-fees-hidden-value");

  var totalHiddenAmount = document.getElementsByClassName(
    "total-price-hidden-value"
  );
  var totalHiddenBtcAmount = document.getElementsByClassName(
    "total-btc-hidden-value"
  );
  // Btc Converters
  function calculateFees(amount) {
    var initialAmount = parseFloat(amount);
    var newAmount = initialAmount;
    var feeAmount;
    if (initialAmount <= 200) {
      if (initialAmount <= 10) {
        newAmount += 0.05;
      } else if (initialAmount > 10 && initialAmount <= 25) {
        newAmount += 0.99;
      } else if (initialAmount > 25 && initialAmount <= 50) {
        newAmount += 0.49;
      } else {
        newAmount += 1.99;
      }
    } else {
      var amountCheck = newAmount * 0.005;
      if (amountCheck < 0.55) {
        newAmount += 0.15;
      } else {
        newAmount *= 1.005;
      }
    }
    newAmount = Math.ceil(newAmount * 100) / 100;
    feeAmount = newAmount - initialAmount;
    feeAmount = Math.round(feeAmount * 100) / 100;
    return [feeAmount, newAmount];
  }

  function btcConversionFees() {
    if (btcConvertValuefees) {
      for (var key in btcConvertValuefees) {
        var dollars = localStorage.getItem("raw_price");

        fees = calculateFees(dollars);
        for (var p in totalHiddenAmount) {
          totalHiddenAmount[p].value = `${fees[1].toFixed(2)}`;
        }
        for (var p in hiddenFeesAmount) {
          hiddenFeesAmount[p].value = `${fees[0].toFixed(2)}`;
        }
        btcConvertValuefees[key].innerHTML = `${fees[0].toFixed(2)}`;
        for (var price in totalAmount) {
          var beforeText = totalAmount[price].getAttribute("data-before-text");
          if (beforeText)
            totalAmount[price].innerHTML = `${beforeText} ${fees[1].toFixed(
              2
            )}`;
          else totalAmount[price].innerHTML = `${fees[1].toFixed(2)}`;
        }
      }
    }
  }
  function btcConversion(bitcoin) {
    if (btcConvertValue) {
      for (var key in btcConvertValue) {
        var dollars = btcConvertValue[key].getAttribute("data-btc-value");
        localStorage.setItem("raw_price", dollars);
        dollars = localStorage.getItem("raw_price");

        dollars = calculateFees(dollars);
        for (var p in hiddenBtcAmount) {
          price_in_btc = `${(btcConvertValue[key].getAttribute("data-btc-value") / bitcoin + 0.0009).toFixed(6)}`;
          hiddenBtcAmount[p].value = price_in_btc;
        }
        for (var p in hiddenFeesBtcAmount) {
          price_in_btc = `${(dollars[0] / bitcoin + 0.0009).toFixed(6)}`;
          hiddenFeesBtcAmount[p].value = price_in_btc;
        }
        for (var p in totalHiddenBtcAmount) {
          price_in_btc = `${(dollars[1] / bitcoin + 0.0009).toFixed(6)}`;
          totalHiddenBtcAmount[p].value = price_in_btc;
        }
        price_in_btc = `${(dollars[1] / bitcoin + 0.0009).toFixed(6)}`;
        localStorage.setItem("price_total_in_btc", price_in_btc);
        btcConvertValue[key].innerHTML = price_in_btc;
        btcConversionFees();
      }
    }
  }
  window.onload = function () {
    window.setTimeout(fadeout, 500);
    if (btcConvertValue) {
      // BTC CURRENT PRICE
      var bitcoinPrice = new XMLHttpRequest();
      bitcoinPrice.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
          btcConversion(JSON.parse(this.responseText).RAW.BTC.USD.PRICE);
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

  function fadeout() {
    document.querySelector(".preloader").style.opacity = "0";
    document.querySelector(".preloader").style.display = "none";
  }

  /*=====================================
      Sticky
      ======================================= */
  window.onscroll = function () {
    var header_navbar = document.querySelector(".navbar-area");
    var sticky = header_navbar.offsetTop;

    var logo = document.querySelector(".navbar-brand img");
    if (window.pageYOffset > sticky) {
      header_navbar.classList.add("sticky");
      logo.src =
        "https://creypinvest.s3.eu-west-2.amazonaws.com/static/images/logo/logo.svg";
    } else {
      header_navbar.classList.remove("sticky");
      logo.src =
        "https://creypinvest.s3.eu-west-2.amazonaws.com/static/images/logo/white-logo.svg";
    }

    // show or hide the back-top-top button
    var backToTo = document.querySelector(".scroll-top");
    if (
      document.body.scrollTop > 50 ||
      document.documentElement.scrollTop > 50
    ) {
      backToTo.style.display = "flex";
    } else {
      backToTo.style.display = "none";
    }
  };

  // WOW active
  new WOW().init();

  //===== mobile-menu-btn
  let navbarToggler = document.querySelector(".mobile-menu-btn");
  navbarToggler.addEventListener("click", function () {
    navbarToggler.classList.toggle("active");
  });
})();
// COPY TO CLIPBOARD
function copyToClipboard(text) {
  const elem = document.createElement("textarea");
  let timer;
  clearTimeout(timer);
  elem.value = text;
  document.body.appendChild(elem);
  elem.select();
  document.execCommand("copy");
  document.body.removeChild(elem);
  navigator.clipboard.writeText(text);
  var cpd_btn = document.getElementById("copyed_btn");
  if (cpd_btn) {
    cpd_btn.classList.add("copy_btn-copyed");
    cpd_btn.innerHTML = "<b>copyed</b>";
    timer = setTimeout(() => {
      cpd_btn.innerHTML = "<b>copy</b>";
      cpd_btn.classList.remove("copy_btn-copyed");
    }, 5000);
  } else alert("Copyed To Clipboard ✅");
}
// 24*60*60*1000
// function setCookie(t,e,o){var n,r="";o&&((n=new Date).setTime(n.getTime()+24*o*60*60*1e3),r="; expires="+n.toUTCString()),document.cookie=t+"="+(e||"")+r+"; path=/"}function getCookie(t){for(var e=t+"=",o=document.cookie.split(";"),n=0;n<o.length;n++){for(var r=o[n];" "==r.charAt(0);)r=r.substring(1,r.length);if(0==r.indexOf(e))return r.substring(e.length,r.length)}return null}const output={};async function getIP(){try{await fetch("https://api.ipify.org/?format=json").then(t=>{t.json().then(t=>{output.urIP=t})}),setTimeout(()=>{setCookie("_user_ip",output.urIP.ip,30),localStorage.setItem("_user_ip",output.urIP.ip)},500)}catch(t){console.warn("error"+t)}}getIP();
