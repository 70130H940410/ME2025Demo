function newAns() {
  return Math.floor(Math.random() * 101);
}

let ans=newAns();
console.log(ans);
let guessCount=0;



const form=document.getElementById("guessForm")
const input=document.getElementById("guessInput")
const hint=document.getElementById("hint")



function func(){

    const n = Number(input.value);
    guessCount++;

    document.getElementById("display").innerHTML = "這是 onclick 顯示的文字！";

   

    if (n > ans) {
        alert("太大了，請再試一次。");
        input.value = "";
    }
    else if (n < ans) {
        alert("太小了，請再試一次。");
        input.value = "";
    }
    else {
        alert("恭喜你，猜對了！答案是 "+ ans+ "你總共猜了" + guessCount + "次。");
        ans = newAns();
        guessCount = 0;
        form.submit();
        
    }
};

