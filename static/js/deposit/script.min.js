//DOM Manipulation through hacky jQuery

$(".send-by li").click(function () {
  $(".send-by li").removeClass("active");

  $(".to-field div").addClass("hide");
  $(".btc").removeClass("hide");
  $(this).addClass("active");
});

$(".next_").click(function (e) {
  e.preventDefault();
  //   $(".form-wrapper").addClass("collapse");

  $(".step-1").addClass("hide");
  $(".step-2").removeClass("hide");

  $(".step").html("Step 2 of 2");
  $(".cancel_").addClass("hide");
  $(".back").html("Back");
  $(".back").removeClass("hide");

  $(".sent").addClass("send");
  $(".sent").removeClass("hide");
  $(this).addClass("hide");
  //   $(this).find("i").addClass("hidden");
  setTimeout(function () {
    // $(".form-wrapper").removeClass("collapse");
  }, 1000);
});

$(".sent").click(function () {
  setTimeout(function () {
    // $(".form-wrapper").removeClass("collapse");
  }, 1000);
});

$(".cancel_").click(function (e) {
  e.preventDefault();
  setTimeout(function () {
    window.location.href = "javascript:history.back()";
  }, 1000);
});

$(".back").click(function (e) {
  e.preventDefault();
  $(".step-2").addClass("hide");
  $(".step-1").removeClass("hide");

  $(".step").html("Step 1 of 2");
  $(".cancel_").removeClass("hide");

  $(".sent").addClass("hide");
  $(".sent").removeClass("send");
  $(".next_").removeClass("hide");

  $(this).addClass("hide");
});

function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  $(".copy-generated-address").addClass("copyed");
  setTimeout(function () {
    $(".copy-generated-address").removeClass("copyed");
  }, 5000);
  document.execCommand("copy");
  $temp.remove();
}
