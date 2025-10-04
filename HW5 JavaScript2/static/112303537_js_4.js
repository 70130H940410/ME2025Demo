// -----------------------------------------------------------建立 <table> -----------------------------------------------------------
//建立 <table>
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


//----------------------------------------------------------- checkbox 功能 -----------------------------------------------------------

// (1) 抓節點
/*注意：getElementsByClassName()查找到的是陣列，需要給予index方能使用特定對象
注意：querySelector()查找的是「第一個」符合css屬性的元素，如要尋找所有符合元素，要用querySelectorAll()
*/
const checkAll = table.querySelector("#check_all");
const itemChecks = table.querySelectorAll('.check_item');

// (2) table下方插入一個總計區塊
const totalDiv = document.createElement('p');
totalDiv.innerHTML = `<h3>總計金額：<span id="totalPrice">0</span></h3>`;
document.body.appendChild(totalDiv);

// (3) 重算總金額，加總打勾的金額
function updateTotal() {
    let total = 0;
    itemChecks.forEach(chk => {
        if (chk.checked) {
        const row = chk.closest('tr');
        const subtotal = Number(row.querySelector('.subtotal').textContent);
        total += subtotal;
        }
    });
    document.getElementById('totalPrice').textContent = total;
}

// (4) 同步全選狀態（全部勾選 → 全選打勾；有任一未勾 → 全選取消）
function syncCheckAll() {
  let allChecked = true; 

  itemChecks.forEach(c => {
    if (!c.checked) {
      allChecked = false; // 有任何一個沒勾，就改成 false
    }
  });

  checkAll.checked = allChecked;
}

// (5) 全選：勾/取消 → 全部項目跟著改，並重算
checkAll.addEventListener('change', () => {
    itemChecks.forEach(c => (c.checked = checkAll.checked));
    updateTotal();
});

// (6) 個別 checkbox：每次點擊 → 同步全選狀態 & 重算
itemChecks.forEach(c => {
    c.addEventListener('change', () => {
        syncCheckAll();
        updateTotal();
    });
});



//----------------------------------------------------------- 加減按鈕：更新數量、小計、總計 ----------------------------------------------------------- 

// 工具：更新某一列的計算 (= 單價*數量)
/* 有關children
<tr>
  <td><input type="checkbox" class="check_item"></td>   <!-- children[0] -->
  <td>BENQ 螢幕</td>                                  <!-- children[1] -->
  <td>18</td>                                         <!-- children[2] -->
  <td>5698</td>                                       <!-- children[3] -->
  <td>                                                <!-- children[4] -->
    <button class="minus">-</button>
    <input type="number" class="qty" value="1" min="1" max="18">
    <button class="add">+</button>
  </td>
  <td class="subtotal">5698</td>                      <!-- children[5] -->
</tr>
*/
function updateRowSubtotal(row) {
    const price = Number(row.children[3].textContent); // 第4欄是單價
    const qtyInput = row.querySelector('.qty');
    const qty = Number(qtyInput.value);
    row.querySelector(".subtotal").textContent = price * qty;
}



// 綁定每一列的 + / - 按鈕
table.querySelectorAll('tr').forEach((row, idx) => {
    if (idx === 0) return; // 略過表頭列

    const btnMinus = row.querySelector('.minus');
    const btnAdd   = row.querySelector('.add');
    const qtyInput = row.querySelector('.qty');

    const stockMax = Number(qtyInput.getAttribute('max')); //庫存上限

    // btnAdd
    btnAdd.addEventListener('click', () => {
        let v = Number(qtyInput.value);
        if (v < stockMax) {
        qtyInput.value = v + 1;
        updateRowSubtotal(row);
        updateTotal();
        }
    });

    // btnMinus
    btnMinus.addEventListener('click', () => {
        let v = Number(qtyInput.value);
        if (v > 1) {
        qtyInput.value = v - 1;
        updateRowSubtotal(row);
        updateTotal();
        }
    });
    });



    // 解決input中上下鍵無法更新該raw的總計的計問題
    table.querySelectorAll('.qty').forEach(input => {
    input.addEventListener('input', () => {
        const row = input.closest('tr');
        const stockMax = Number(input.getAttribute('max'));
        let v = Number(input.value);

        // 限制數量範圍
        if (v < 1) {v = 1};
        if (v > stockMax) {v = stockMax};

        input.value = v; // 修正超出範圍的值
        updateRowSubtotal(row); // 更新更新該raw的總計
        updateTotal();          // 更新總金額
    });
});

//----------------------------------------------------------- 結帳按鈕 ----------------------------------------------------------- 
//設定結帳按鈕
const checkoutBtn = document.createElement('button');
checkoutBtn.textContent = '結帳';
document.body.appendChild(checkoutBtn);

checkoutBtn.addEventListener('click', () => {
    const total = Number(document.getElementById('totalPrice').textContent);
    //按下時total金額<=0，不作動作
    if (total <= 0) return; 

    const lines = [];

    itemChecks.forEach(chk => {
        if (!chk.checked) return;

        const row = chk.closest('tr');
        const name = row.children[1].textContent.trim();
        const price = Number(row.children[3].textContent);
        const qtyInput = row.querySelector('.qty');
        const minusBtn = row.querySelector('.minus');
        const addBtn   = row.querySelector('.add');

        const buyQty = Number(qtyInput.value);
        const sub = price * buyQty;
        lines.push(`${name}  x ${buyQty}  = ${sub}`);

    });

    //這裡語法還要再研究一下
    alert(`結帳明細：\n${lines.join('\n')}\n----------------\nTotal：${total}`);

    // 重置
    checkAll.checked = false;
    updateTotal();
 

});




