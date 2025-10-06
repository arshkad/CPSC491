// ignore this, it doesn't work well at the moment
// const background = document.getElementById('background');
// const colors = ["#93c5fd","#f9a8d4","#86efac","#fde047","#fca5a5","#d8b4fe","#a5b4fc","#c4b5fd"];

// const rows = Math.ceil(window.innerHeight /40);
// const cols = Math.ceil(window.innerWidth /40);

// for(let i = 0; i < rows * cols; i++) {
//   const box = document.createElement('div');
//   box.classList.add('box');

//   // Temporary hover color
//   box.addEventListener('mouseenter', () => {
//     box.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
//   });

//   box.addEventListener('mouseleave', () => {
//     box.style.backgroundColor = 'transparent'; // reset
//   });

//   background.appendChild(box);
// }

// // Optional: adjust boxes on window resize
// window.addEventListener('resize', () => {
//   background.innerHTML = '';
//   const rows = Math.ceil(window.innerHeight / 40);
//   const cols = Math.ceil(window.innerWidth / 40);
//   for(let i = 0; i < rows * cols; i++) {
//     const box = document.createElement('div');
//     box.classList.add('box');
//     box.addEventListener('mouseenter', () => {
//       box.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
//     });
//     box.addEventListener('mouseleave', () => {
//       box.style.backgroundColor = 'transparent';
//     });
//     background.appendChild(box);
//   }
// });
