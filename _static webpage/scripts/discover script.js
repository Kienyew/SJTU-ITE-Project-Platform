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


document.addEventListener("mousemove", parallex);
function parallex(e) {
  const obj = this.querySelector("#discover-background");
  const speed = 3;  // Maybe randomize speed ?
  const x = (window.innerWidth - e.pageX * speed) / 100;
  const y = (window.innerHeight - e.pageY * speed) / 100;

  obj.style.transform = `scale(1.1) translateX(${x}px) translateY(${y}px)`
}
