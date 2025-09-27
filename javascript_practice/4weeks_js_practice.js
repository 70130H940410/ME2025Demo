const today=new Date();
console.log(today.getHours());
console.log(today.toLocaleTimeString());







/////////////////////////////////////////////

switch(3){
    case 1:
       console.log(-12); 
    break;
    case 3:
       console.log(-8); 
    break;
    default:
        console.log("default");
    break;
}

/////////////////////////////////////////////

let i=1;

if(i>=1){
    console.log(i*i);
    i++;
}
else if(i==5){
    console.log("5");
    i++;
}
else{
    console.log("");
    i++;
}

/////////////////////////////////////////////

for(let i=0;i<=5;i++){
    console.log(i)
}


while(0){
    console.log("")
}


/////////////////////////////////////////////


function func(par1,par2){
    console.log(par1+par2)
}

func("hello","world")


/////////////////////////////////////////////


console.log(30+"40.5")
console.log(30+40.5)

/////////////////////////////////////////////

console.log("hello");

var test = 0;
console.log(typeof(test));

function testing(){

}

let array=[1,2,3]
