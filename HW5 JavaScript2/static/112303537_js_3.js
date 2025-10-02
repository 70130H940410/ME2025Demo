function newAns() {
  return Math.floor(Math.random() * 101);
}

let ans=newAns();
console.log(ans);
let guessCount=0;



const form=document.getElementById("guessForm")
const input=document.getElementById("guessInput")
const hint=document.getElementById("hint")

/*計時器

let time=0;

setInterval(timeCount, 1000)

function timeCount(){
    time++;
    console.log(time)
}    
    */






function func(){

    const n = Number(input.value);
    const today=new Date();
    guessCount++;



    
   

    if (n > ans) {
        document.getElementById("display").innerHTML = "太大了，請再試一次。";
        input.value = "";
    }
    else if (n < ans) {
        document.getElementById("display").innerHTML = "太小了，請再試一次。";
        input.value = "";
    }
    else {
        alert("恭喜你，猜對了！答案是 "+ ans+ "你總共猜了" + guessCount + "次，花了");
        ans = newAns();
        guessCount = 0;
        form.submit();
        
    }
};



