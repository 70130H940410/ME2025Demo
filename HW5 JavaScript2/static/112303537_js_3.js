function newAns() {
  return Math.floor(Math.random() * 101);
}

let ans=newAns();
console.log(ans);
let guessCount=0;
let time=0;
let stopTimeCount= 0;





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

function timeCount(){
    time=time+0.01;
    //console.log(time.toFixed(2));
    document.getElementById("timeID").innerHTML ="本次遊戲花了:"+time.toFixed(2)+"s";
} 



function func(){

    const n = Number(input.value);
    let today=new Date();
    guessCount++;

    //只有在猜第一次時會觸發計時器
    if(guessCount==1){ 
        stopTimeCount=setInterval(timeCount, 10);
    }
   

    if (n > ans) {
        document.getElementById("display").innerHTML = "太大了，請再試一次。";
        input.value = "";
    }
    else if (n < ans) {
        document.getElementById("display").innerHTML = "太小了，請再試一次。";
        input.value = "";
    }
    else {
        alert("恭喜你，猜對了！答案是 "+ ans+ "，你總共猜了" + guessCount + "次，花了"+time.toFixed(2)+"s");
        ans = newAns();
        console.log(ans);
        guessCount = 0;
        //form.submit();
        clearInterval(stopTimeCount);
        time=0;
        
    }
};



