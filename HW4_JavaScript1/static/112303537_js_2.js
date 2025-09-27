document.write('<input type="text" id="inputNum"><br>');

for(let i=1;i<=9;i++){
  document.write('<button onclick="press"> '+i+' </button>');
  if (i % 3 === 0) document.write("<br>");
}