// 建立 <table> 元素
const table = document.createElement("table");
table.border = "1";
table.width = "600px";

// 模擬商品資料
const products = [
    { name: "BENQ 螢幕", stock: 18, price: 5698 },
    { name: "3M 無痕掛勾", stock: 89, price: 179 },
    { name: "DJI MINI 4 Pro", stock: 23, price: 31969 }
];

// 建立第一raw
/*觀念
反引號 ` 是現代 JavaScript 處理字串的「升級版」寫法。
它能讓你輕鬆插入變數、換行、做運算、產生 HTML，幾乎完全取代 ' 和 " 的用途。
*/
const header = document.createElement("tr");
    header.innerHTML = `
    <th><input type="checkbox" id="check_all"></th>
    <th>商品名稱</th>
    <th>商品庫存</th>
    <th>單價</th>
    <th>數量</th>
    <th>總計</th>`;
table.appendChild(header);

// 迴圈產生每一列
/*
products → 一個陣列（array），裡面有多個商品。
.forEach(...) → 陣列的方法，會依序「取出每一個元素」。
p => { ... } → 箭頭函式，表示「每取出一個元素，就把它暫時放進變數 p」。
*/
products.forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td><input type="checkbox" class="check_item"></td>
        <td>${p.name}</td>
        <td>${p.stock}</td>
        <td>${p.price}</td>
        <td>
        <button class="minus">-</button>
        <input type="number" class="qty" value="1" min="1" max="${p.stock}">
        <button class="add">+</button>
        </td>
        <td class="subtotal">${p.price}</td>
    `;
  table.appendChild(tr);
});

// 把整個表格加進畫面
document.getElementById("container").appendChild(table);



/*
1.插入變數---------------------------------------------------

let name = "典儒";

// 舊寫法
let old = "Hello, " + name + "!";

// 新寫法
let modern = `Hello, ${name}!`;

console.log(old);    // Hello, 典儒!
console.log(modern); // Hello, 典儒!

2.跨行字串---------------------------------------------------

// 舊寫法（錯誤，不能換行）
let text1 = "第一行
第二行";  //  會報錯

// 舊寫法（勉強用 \n）
let text2 = "第一行\n第二行";

// 新寫法（正確又清晰）
let text3 = `
第一行
第二行
`;

3.插入運算---------------------------------------------------

let price = 200;
let qty = 3;

// 舊寫法
let oldTotal = "小計：" + (price * qty) + "元";

// 新寫法
let newTotal = `小計：${price * qty}元`;

console.log(oldTotal); // 小計：600元
console.log(newTotal); // 小計：600元

4.插入 HTML 結構---------------------------------------------------

let name = "滑鼠";
let price = 499;

// 舊寫法
let html1 = "<tr><td>" + name + "</td><td>" + price + "</td></tr>";

// 新寫法
let html2 = `
<tr>
  <td>${name}</td>
  <td>${price}</td>
</tr>
`;

*/