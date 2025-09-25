function newAns() {
  return Math.floor(Math.random() * 101);
}

let ans=newAns();
let guessCount=0;


const form=document.getElementById("guessForm")
const input=document.getElementById("guessInput")
const hint=document.getElementById("hint")

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const n = Number(input.value);
    guessCount++;


    if (n > ans) {
        alert("太大了，請再試一次。");
    }
    else if (n < ans) {
        alert("太小了，請再試一次。");
    }
    else {
        alert(`恭喜你，猜對了！答案是 ${ans}，你總共猜了 ${guessCount} 次。`);
        ans = newAns();
        guessCount = 0;
    }
});

