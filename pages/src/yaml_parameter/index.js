// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img1 = document.getElementById("diagram_section_image");
var img2 = document.getElementById("title_section_image");
var img3 = document.getElementById("nodes_section_image");
var img4 = document.getElementById("groups_section_image");
var img5 = document.getElementById("connections_section_image");
var modalImg = document.getElementById("modal_image");
var captionText = document.getElementById("caption");

setOnClickListener(img1)
setOnClickListener(img2)
setOnClickListener(img3)
setOnClickListener(img4)
setOnClickListener(img5)

function setOnClickListener(imageVariable) {
  imageVariable.onclick = function () {
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
  }
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
}