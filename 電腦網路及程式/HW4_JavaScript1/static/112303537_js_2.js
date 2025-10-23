document.write('<input type="text" id="inputNum"><br>');

for(let i=0;i<=9;i++){
  document.write('<button style="margin:5px;" onclick="press(\''+i+'\')"> '+i+' </button>');
  if (i % 3 === 2) document.write("<br>");
}

//筆記:這邊margin加下來後，css跟html寫法需要再複習//

document.write('<button style="margin:5px;" onclick="press(\'clear\')">clear</button><br>');

let ops = ["+", "-", "*", "/", "(", ")", "=","←"];
for (let op of ops) {
  document.write('<button style="margin:5px;" onclick="press(\''+op+'\')">' + op+ '</button>');
}

//筆記:press(\' '+op+' \') 這樣的寫法就是 → 幫每個按鈕生成一個 onclick 事件，按下去會呼叫 press(某個符號)。//

function press(valueInput){
  const displayOnScreen = document.getElementById("inputNum");
  

  if (valueInput === "clear") {
    displayOnScreen.value = "";
  }
  else if (valueInput === "=") {
      let ans = eval(displayOnScreen.value);
      alert(displayOnScreen.value + " = " + ans);
      displayOnScreen.value = ans;
    
  }
  else if (valueInput === "←") {
    displayOnScreen.value = displayOnScreen.value.slice(0, -1);
  }
  //作業外的刪除鍵//
  else{
    displayOnScreen.value = displayOnScreen.value + valueInput;
  }
  console.log(displayOnScreen.value);
}

  
