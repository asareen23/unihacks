const colors = ['#00b4d8', '#fde4cf', '#ffcfd2', '#f1c0e8', '#a3c4f3', '#90dbf4', '#8eecf5', '#98f5e1', '#b9fbc0'];
const lists = document.querySelectorAll('li#tag')
for (let i = 0; i < lists.length; i++) {
    let random_color = colors[Math.floor(Math.random() * colors.length)];
    console.log(lists[i])
    lists[i].style.backgroundColor = random_color;
}