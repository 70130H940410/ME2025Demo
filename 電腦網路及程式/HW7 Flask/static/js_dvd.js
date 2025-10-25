const dvd = document.querySelector('.dvd-logo');
const obstacleEl = document.querySelector('.login-card');   // ← 白色輸入框外層卡片

// ===== 可調參數 =====
const SPEED_MIN = 140;
const SPEED_MAX = 260;
const BOUNCE_JITTER = 0.4;   // ±約 23°
const BUFFER = 10;           // 與白框的緩衝距離（可增大讓圖更早反彈）
// ====================

let x = 100, y = 100;
let vx = (Math.random() * (SPEED_MAX - SPEED_MIN) + SPEED_MIN) * (Math.random() < 0.5 ? 1 : -1);
let vy = (Math.random() * (SPEED_MAX - SPEED_MIN) + SPEED_MIN) * (Math.random() < 0.5 ? 1 : -1);
let last = performance.now();

function randomHue() {
  dvd.style.filter = `hue-rotate(${Math.floor(Math.random()*360)}deg) drop-shadow(0 0 15px white)`;
}

function getObstacleRect() {
  if (!obstacleEl) return null;
  const r = obstacleEl.getBoundingClientRect();
  // 擴大／縮小反彈區域，可用 BUFFER 微調
  return {
    left:  r.left  - BUFFER,
    top:   r.top   - BUFFER,
    width: r.width + BUFFER*2,
    height:r.height+ BUFFER*2
  };
}

function update(now) {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;

  const W = window.innerWidth;
  const H = window.innerHeight;
  const w = dvd.offsetWidth;
  const h = dvd.offsetHeight;

  x += vx * dt;
  y += vy * dt;

  let bounced = false;

  // 邊界反彈
  if (x <= 0)          { x = 0;     vx = Math.abs(vx);  bounced = true; }
  else if (x + w >= W) { x = W - w; vx = -Math.abs(vx); bounced = true; }

  if (y <= 0)          { y = 0;     vy = Math.abs(vy);  bounced = true; }
  else if (y + h >= H) { y = H - h; vy = -Math.abs(vy); bounced = true; }

  // 白色輸入框（login-card）碰撞反彈
  const obs = getObstacleRect();
  if (obs) {
    const ox = obs.left, oy = obs.top, ow = obs.width, oh = obs.height;

    const overlapX = Math.max(0, Math.min(x + w, ox + ow) - Math.max(x, ox));
    const overlapY = Math.max(0, Math.min(y + h, oy + oh) - Math.max(y, oy));

    if (overlapX > 0 && overlapY > 0) {
      // 根據最小滲入軸反彈
      if (overlapX < overlapY) {
        if (x + w/2 < ox + ow/2) { x = ox - w - 0.5; vx = -Math.abs(vx); }
        else                     { x = ox + ow + 0.5; vx =  Math.abs(vx); }
      } else {
        if (y + h/2 < oy + oh/2) { y = oy - h - 0.5; vy = -Math.abs(vy); }
        else                     { y = oy + oh + 0.5; vy =  Math.abs(vy); }
      }
      bounced = true;
    }
  }

  // 反彈後隨機角度/速度擾動
  if (bounced) {
    const speed = Math.hypot(vx, vy);
    const newSpeed = Math.min(SPEED_MAX, Math.max(SPEED_MIN, speed + (Math.random()*60 - 30)));
    const angle = Math.atan2(vy, vx) + (Math.random() - 0.5) * BOUNCE_JITTER;
    vx = Math.cos(angle) * newSpeed;
    vy = Math.sin(angle) * newSpeed;
    randomHue();
  }

  dvd.style.transform = `translate(${x}px, ${y}px)`;
  requestAnimationFrame(update);
}

requestAnimationFrame(update);
