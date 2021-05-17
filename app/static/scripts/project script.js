// This function update likes
const likeCount = document.getElementById('like-count');
const likeBtn = document.getElementById('like-btn');
// let firstLoadState = likeBtn.classList.contains('active');
// let newLoadState = firstLoadState;

function updateLike() {
  if (likeBtn.classList.contains('active')) {
    likeCount.innerHTML--;
    newLoadState = false;
  }
  else {
    likeCount.innerHTML++;
    newLoadState = true;
  }

  likeBtn.classList.toggle('active');
}

// For Carousel
let counter = 1;
let totalSlides = document.querySelectorAll('.manual-btn').length;
setInterval(function(){
  document.getElementById('radio' + counter).checked = true;
  counter++;
  if (counter > totalSlides) {
    counter = 1;
  }
}, 3000);  // Change slide every 3s



// // only submit form if the status change when user leaves the webpage
// window.onbeforeunload =  function() {
//   if (newLoadState != firstLoadState) {
//     console.log("Different")
//     // return "DIFFERENT";
//   } else {
//     console.log("Same")
//     // return "SAME";
//   }
// };