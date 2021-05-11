function updateLike(event) {
  console.log(event);
  console.log(event.parentNode.parentNode);
  console.log(event.parentNode.parentNode.querySelector('.box-total-likes'));
  const likeCount = event.parentNode.parentNode.querySelector('.box-total-likes');
  const likeBtn = event;
    
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