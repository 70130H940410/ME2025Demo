document.getElementById("second_Project").innerHTML = '範例2:選擇背景顏色';

// 1. 準備顏色陣列
let colorList = ["white","red", "green", "blue", "yellow", "purple"];

// 2. 抓 <select>
let select = document.getElementById("colors");

// 3. 動態生成選項
for (let i = 0; i < colorList.length; i++) {
  let opt = document.createElement("option");
  opt.value = colorList[i];      // 選項的值
  opt.textContent = colorList[i]; // 顯示的文字
  select.appendChild(opt);
}

// 4. 監聽下拉選單改變事件
select.addEventListener("change", () => {
  document.body.style.backgroundColor = select.value;
});
