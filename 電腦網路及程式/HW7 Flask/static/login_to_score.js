// login-client.js
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('loginBtn');
  const msg = document.getElementById('msg');

  btn.addEventListener('click', async () => {
    msg.textContent = '';
    const username = document.getElementById('Username').value.trim();
    const password = document.getElementById('Password').value;

    if (!username || !password) {
      msg.textContent = '請輸入帳號與密碼';
      return;
    }

    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        const text = await res.text();
        msg.textContent = `伺服器錯誤: ${text}`;
        return;
      }

      const data = await res.json();
      if (data.success) {
        // 登入成功 -> 導到 score.html ，也可以帶 query string
        window.location.href = `score.html?username=${encodeURIComponent(username)}`;
      } else {
        msg.textContent = data.message || '帳號或密碼錯誤';
      }
    } catch (e) {
      console.error(e);
      msg.textContent = '網路錯誤，請稍後再試';
    }
  });
});
