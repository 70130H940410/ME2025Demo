const div_byid=document.getElementById('div_1');
const div_byclassname=document.getElementsByClassName('div_class');
const div_qry=document.querySelector('.div_class');
const div_qryA=document.querySelectorAll('.div_class');

div_byid.style.backgroundColor="green";
div_byclassname[0].style.backgroundColor="pink";
//只能選一個//

for (let i = 0; i < div_byclassname.length; i++) {
  div_byclassname[i].style.backgroundColor = "pink";
}

for (let div of div_byclassname) {
  div.style.backgroundColor = "pink";
}
//用迴圈i判斷，或者用let ...of...

div_qry.style.backgroundColor='purple';
div_qryA[1].style.backgroundColor='red';

div_byid.classList.add('test');
div_byid.setAttribute('onclick','alert("hi")');
//

let new_element = document.createElement('input');
new_element.type= 'button';
new_element.value= 'create by js';
div_byid.appendChild(new_element);

//
div_byid.addEventListener('click',alert)
