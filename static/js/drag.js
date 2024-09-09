const chatbox = document.querySelector('.chatbox');

let isDragging = false;
let startX, startY, offsetX, offsetY;

chatbox.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    offsetX = chatbox.offsetLeft;
    offsetY = chatbox.offsetTop;
});

document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;

    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;

    const newOffsetX = offsetX + deltaX;
    const newOffsetY = offsetY + deltaY;

    chatbox.style.left = `${newOffsetX}px`;
    chatbox.style.top = `${newOffsetY}px`;
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});
