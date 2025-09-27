document.write('<input type="text" id="inputNum"><br>');

for(let i=0;i<=9;i++){
  document.write('<button onclick="press(\''+i+'\')"> '+i+' </button>');
  if (i % 3 === 2) document.write("<br>");
}

document.write('<button onclick="press(\'clear\')">clear</button><br>');

let ops = ["+", "-", "*", "/", "(", ")", "="];
for (let op of ops) {
  document.write('<button onclick="press(\''+op+'\')">' + op+ '</button>');
}

//筆記:press(\' '+op+' \') 這樣的寫法就是 → 幫每個按鈕生成一個 onclick 事件，按下去會呼叫 press(某個符號)。//

function press(valueInput){
  const displayOnScreen = document.getElementById("inputNum");
  console.log(displayOnScreen);

  if (valueInput === "clear") {
    displayOnScreen.value = "";
  }
  else if (valueInput === "=") {
      let ans = eval(displayOnScreen.value);
      alert(displayOnScreen.value + " = " + ans);
      displayOnScreen.value = ans;
    
  }
  else{
    displayOnScreen.value = displayOnScreen.value + valueInput;
  }
}

  
