var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img1 = document.getElementById("image1");
var img2 = document.getElementById("image2");
var img3 = document.getElementById("image3");
var img1_slide = document.getElementById("image1_slide");
var img2_slide = document.getElementById("image2_slide");
var img3_slide = document.getElementById("image3_slide");
var img4_slide = document.getElementById("image4_slide");
var img_poster = document.getElementById("poster");
var modalImg = document.getElementById("modal_image");
var captionText = document.getElementById("caption");

setOnClickListener(img1);
setOnClickListener(img2);
setOnClickListener(img3);
setOnClickListener(img1_slide);
setOnClickListener(img2_slide);
setOnClickListener(img3_slide);
setOnClickListener(img4_slide);
setOnClickListener(img_poster);

function setOnClickListener(imageVariable) {
  imageVariable.onclick = function () {
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
  };
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
};
