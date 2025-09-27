document.write('<input type="text" id="inputNum"><br>');

for(let i=0;i<=9;i++){
  document.write('<button onclick="press()"> '+i+' </button>');
  if (i % 3 === 2) document.write("<br>");
}

document.write('<button onclick="clearNum()">clear</button><br>');

let ops = ["+", "-", "*", "/", "(", ")", "="];
for (let op of ops) {
  document.write('<button onclick="press()">' + op + '</button>');
}

function press(){
  
}