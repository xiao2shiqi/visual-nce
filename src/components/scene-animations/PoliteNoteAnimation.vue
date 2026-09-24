<script setup lang="ts">
// @ts-nocheck —— 逐帧绘图代码，DOM 操作密集，不做严格类型检查
/**
 * L16 s2 场景动画：警察把纸条塞到雨刷下，抬头微笑（旁白课，嘴始终闭合）。
 * 纯 SVG + JS 绘制；时间轴读取音频当前时间，暂停/拖动/倍速自然跟随。
 * 动作在前 4.4 秒内完成，对应 s2 开始到 s3 换图（约 4.5 秒）。
 */
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps<{ start: number; getTime: () => number }>();
const root = ref<SVGSVGElement | null>(null);
let raf = 0;

onMounted(() => {
  
  const NS = 'http://www.w3.org/2000/svg';
  const $ = (id: string) => root.value!.querySelector('#' + id) as SVGElement;
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  
  // ---- 花盆 ----
  const flowerStems = [];
  [[40, 600, '#e89aa8'], [150, 585, '#f2b3c0'], [255, 570, '#e98fa0']].forEach(([x, y, c], i) => {
    const g = el('g', {}, $('flowers'));
    el('path', { d: `M${x - 28},${y} L${x + 28},${y} L${x + 20},${y + 48} L${x - 20},${y + 48} Z`, fill: '#c98a62', stroke: '#6b4a36', 'stroke-width': 2.5 }, g);
    const stem = el('g', {}, g);
    for (let k = -2; k <= 2; k++) {
      const tx = x + k * 13, ty = y - 40 - Math.abs(k) * -6 - (k % 2 ? 10 : 0);
      el('path', { d: `M${x},${y} Q${x + k * 6},${y - 20} ${tx},${ty}`, fill: 'none', stroke: '#6f9a55', 'stroke-width': 3 }, stem);
      el('ellipse', { cx: tx - 6, cy: ty + 10, rx: 9, ry: 5, fill: '#8fbd6e', transform: `rotate(-30 ${tx - 6} ${ty + 10})` }, stem);
      el('circle', { cx: tx, cy: ty, r: 9, fill: c, stroke: '#a65a6a', 'stroke-width': 1.5 }, stem);
      el('circle', { cx: tx, cy: ty, r: 3, fill: '#f6d67a' }, stem);
    }
    flowerStems.push({ node: stem, x, y, phase: i * 1.7 });
  });
  
  // ---- 手臂 ----
  const arms = $('arms');
  function makeArm() {
    const g = el('g', {}, arms);
    return {
      g,
      upperOutline: el('path', { fill: 'none', stroke: '#4a3f36', 'stroke-width': 76 }, g),
      upper: el('path', { fill: 'none', stroke: '#f2cdae', 'stroke-width': 70 }, g),
      foreOutline: el('path', { fill: 'none', stroke: '#4a3f36', 'stroke-width': 66 }, g),
      fore: el('path', { fill: 'none', stroke: '#f2cdae', 'stroke-width': 60 }, g),
      sleeveOutline: el('path', { fill: 'none', stroke: '#4a3f36', 'stroke-width': 98 }, g),
      sleeve: el('path', { fill: 'none', stroke: '#b9d3e8', 'stroke-width': 92 }, g),
      hand: el('g', {}, g),
    };
  }
  function drawHand(hand, grip) {
    hand.innerHTML = '';
    const s = { stroke: '#4a3f36', 'stroke-width': 3, fill: '#f4d0b2' };
    el('ellipse', { cx: 0, cy: 0, rx: 40, ry: 31, ...s }, hand);
    const curl = grip ? 0.55 : 1;
    [-19, -6, 7, 19].forEach((y, i) => {
      const len = (i === 0 || i === 3 ? 34 : 42) * curl;
      el('rect', { x: 26, y: y - 7, width: len, height: 14, rx: 7, ...s }, hand);
    });
    el('rect', { x: 4, y: 20, width: 34, height: 15, rx: 7.5, transform: 'rotate(35 4 20)', ...s }, hand);
  }
  const armL = makeArm(); // 画面右边那只：抬雨刷（先画，压在下面）
  const armR = makeArm(); // 画面左边那只：拿纸条
  drawHand(armR.hand, true);
  drawHand(armL.hand, false);
  
  // 两段骨骼 IK：肩 → 肘 → 手
  function ik(sx, sy, hx, hy, l1, l2, bendSign) {
    const dx = hx - sx, dy = hy - sy;
    const d = Math.min(Math.hypot(dx, dy), l1 + l2 - 1);
    const a = Math.atan2(dy, dx);
    const b = Math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d));
    const ang = a + bendSign * b;
    return [sx + l1 * Math.cos(ang), sy + l1 * Math.sin(ang)];
  }
  function setArm(arm, sx, sy, hx, hy, bend) {
    const [ex, ey] = ik(sx, sy, hx, hy, 205, 225, bend);
    const up = `M${sx},${sy} L${ex},${ey}`, fo = `M${ex},${ey} L${hx},${hy}`;
    const k = 0.55, slx = sx + (ex - sx) * k, sly = sy + (ey - sy) * k;
    const sl = `M${sx},${sy} L${slx},${sly}`;
    arm.upperOutline.setAttribute('d', up); arm.upper.setAttribute('d', up);
    arm.foreOutline.setAttribute('d', fo); arm.fore.setAttribute('d', fo);
    arm.sleeveOutline.setAttribute('d', sl); arm.sleeve.setAttribute('d', sl);
    const deg = Math.atan2(hy - ey, hx - ex) * 180 / Math.PI;
    arm.hand.setAttribute('transform', `translate(${hx},${hy}) rotate(${deg})`);
  }
  
  // ---- 时间轴 ----
  const ease = t => t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t);
  const seg = (t, a, b) => ease((t - a) / (b - a));
  const lerp = (a, b, k) => a + (b - a) * k;
  const rot = (x, y, cx, cy, deg) => {
    const r = deg * Math.PI / 180, c = Math.cos(r), s = Math.sin(r);
    return [cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c];
  };
  
  function frame() {
    const t = Math.max(0, props.getTime() - props.start);
    const now = t * 1000;
  
    // 0–0.7 抬起雨刷；0.7–2.1 纸条往下塞；2.1–2.5 雨刷落下；2.6–3.1 轻拍；3.2–4.4 抬头微笑
    const lift = seg(t, 0, 0.7) * (1 - seg(t, 2.1, 2.5));
    const slide = seg(t, 0.7, 2.1);
    const release = seg(t, 2.2, 2.6);
    const pat = Math.sin(Math.PI * Math.min(1, Math.max(0, (t - 2.6) / 0.5)));
    const lookUp = seg(t, 3.2, 4.2);
  
    // 雨刷
    const wAng = -7 * lift;
    $('wiper').setAttribute('transform', `rotate(${wAng} 255 738)`);
  
    // 纸条：从高处滑到雨刷下
    const nx = lerp(420, 470, slide), ny = lerp(430, 560, slide), nr = lerp(-10, -4, slide);
    $('note').setAttribute('transform', `translate(${nx},${ny}) rotate(${nr})`);
  
    // 拿纸条的手：跟着纸条走，松手后稍后撤，再轻拍一下
    let hx = nx + 40, hy = ny - 78;
    hx = lerp(hx, 560, release); hy = lerp(hy, 470, release);
    hy += pat * 38; hx -= pat * 10;
    hx = lerp(hx, 640, lookUp); hy = lerp(hy, 520, lookUp);
    drawHandGrip(t);
    setArm(armR, 830, 355, hx, hy, -1);
  
    // 抬雨刷的手：捏着雨刷臂的前端
    const [tipX, tipY] = rot(745, 601, 255, 738, wAng);
    const lx = lerp(tipX + 15, 880, lookUp), ly = lerp(tipY - 12, 630, lookUp);
    setArm(armL, 1120, 370, lx, ly, 1);
  
    // 身体：微微呼吸 + 抬头时直起一点
    const breathe = Math.sin(t * 2.2) * 1.5;
    $('body').setAttribute('transform', `translate(0,${breathe}) rotate(${-2 * lookUp} 1000 700)`);
    $('head').setAttribute('transform', `translate(${6 * lookUp},${breathe - 4 * lookUp}) rotate(${lerp(7, -3, lookUp)} 965 300)`);
  
    // 眼睛：先看纸条（左下），后看向前方；3.9s 和 5.6s 眨眼
    const ix = lerp(-5, -1, lookUp), iy = lerp(4, 0, lookUp);
    const blink = Math.max(bump(t, 3.9, 0.16), bump(t, 5.6, 0.16), bump(t, 1.2, 0.14));
    for (const id of ['eyeL', 'eyeR']) {
      const g = $(id);
      g.querySelector('.iris').setAttribute('transform', `translate(${ix},${iy})`);
      g.querySelector('.lid').setAttribute('transform', `scale(1,${1 - 0.92 * blink})`);
    }
    // 眉毛与嘴：微笑变深（嘴始终闭合）
    const smile = lerp(0.35, 1, lookUp);
    $('mouth').setAttribute('d', `M${925 - 6 * smile},${265 - 4 * smile} Q950,${268 + 12 * smile} ${975 + 6 * smile},${265 - 4 * smile}`);
    $('browL').setAttribute('transform', `translate(0,${-4 * lookUp})`);
    $('browR').setAttribute('transform', `translate(0,${-4 * lookUp})`);
  
    // 花随风摆
    for (const f of flowerStems) {
      const a = Math.sin(now / 900 + f.phase) * 3;
      f.node.setAttribute('transform', `rotate(${a} ${f.x} ${f.y})`);
    }
    raf = requestAnimationFrame(frame);
  }
  let lastGrip = true;
  function drawHandGrip(t) {
    const grip = t < 2.2;
    if (grip !== lastGrip) { drawHand(armR.hand, grip); lastGrip = grip; }
  }
  function bump(t, at, w) { const d = Math.abs(t - at); return d > w ? 0 : 1 - d / w; }
  
  frame();
});

onUnmounted(() => cancelAnimationFrame(raf));
</script>

<template>
  <svg ref="root" class="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 1376 768">
  <defs>
    <!-- 水彩：边缘轻微抖动 + 纸纹 -->
    <filter id="pn-wobble" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="4" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="pn-paper">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="9" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.40  0 0 0 0 0.33  0 0 0 0.55 0"/>
    </filter>
    <filter id="pn-bloom">
      <feTurbulence type="fractalNoise" baseFrequency="0.006" numOctaves="2" seed="2" result="b"/>
      <feColorMatrix in="b" type="matrix" values="0 0 0 0 1  0 0 0 0 0.97  0 0 0 0 0.9  0 0 0 0.35 0"/>
    </filter>
    <linearGradient id="pn-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#b9d9ee"/><stop offset="1" stop-color="#eef6fa"/>
    </linearGradient>
    <linearGradient id="pn-hood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#cdb08e"/><stop offset="1" stop-color="#a88460"/>
    </linearGradient>
    <linearGradient id="pn-glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#9fb6c4" stop-opacity=".45"/><stop offset="1" stop-color="#c9d7df" stop-opacity=".2"/>
    </linearGradient>
    <linearGradient id="pn-shirt" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#c9def0"/><stop offset="1" stop-color="#a6c4dc"/>
    </linearGradient>
    <clipPath id="pn-glassClip"><path d="M0,168 L392,160 L826,588 L0,640 Z"/></clipPath>
  </defs>

  <!-- ===== 街景（静态） ===== -->
  <g filter="url(#pn-wobble)" stroke="#6b5c4c" stroke-width="2" stroke-linejoin="round">
    <rect x="-10" y="-10" width="1400" height="800" fill="url(#pn-sky)" stroke="none"/>
    <!-- 远处街道 -->
    <path d="M430,400 L1376,380 L1376,768 L0,768 L0,430 Z" fill="#e7e2d9" stroke="none"/>
    <path d="M1100,420 L1376,470 L1376,520 L1060,440 Z" fill="#dcd5ca"/>
    <!-- 左侧木楼 -->
    <rect x="-10" y="-10" width="520" height="470" fill="#f0d9aa"/>
    <g stroke="#c9ad7c" stroke-width="1.5">
      <path d="M40,0 V460 M90,0 V460 M140,0 V460 M190,0 V460 M240,0 V460 M290,0 V460 M340,0 V460 M390,0 V460 M440,0 V460"/>
    </g>
    <rect x="30" y="40" width="130" height="120" fill="#cfe0ea"/>
    <rect x="210" y="40" width="130" height="120" fill="#d6e5ee"/>
    <rect x="30" y="230" width="140" height="200" fill="#c5d8e3"/>
    <rect x="220" y="230" width="140" height="200" fill="#cddde7"/>
    <path d="M400,110 L510,90 L510,200 L400,215 Z" fill="#e2c894"/>
    <!-- 玻璃楼 -->
    <rect x="505" y="-10" width="200" height="400" fill="#cbdae4"/>
    <g stroke="#9fb3c0" stroke-width="1.5">
      <path d="M505,60 H705 M505,130 H705 M505,200 H705 M505,270 H705 M505,340 H705 M570,0 V390 M640,0 V390"/>
    </g>
    <path d="M520,20 L560,20 L530,380 L505,380 Z" fill="#fff" opacity=".35" stroke="none"/>
    <!-- 远景楼 -->
    <rect x="700" y="110" width="120" height="290" fill="#f3e3c4"/>
    <g fill="#d3e2ea" stroke="#b9a785" stroke-width="1">
      <rect x="715" y="135" width="26" height="36"/><rect x="760" y="135" width="26" height="36"/>
      <rect x="715" y="200" width="26" height="36"/><rect x="760" y="200" width="26" height="36"/>
      <rect x="715" y="265" width="26" height="36"/><rect x="760" y="265" width="26" height="36"/>
    </g>
    <rect x="820" y="170" width="70" height="230" fill="#ece0cc"/>
    <!-- 右侧楼 -->
    <rect x="1180" y="-10" width="210" height="440" fill="#efd8b6"/>
    <g fill="#cfe0ea" stroke="#b39a74" stroke-width="1.5">
      <rect x="1205" y="30" width="55" height="75"/><rect x="1290" y="30" width="55" height="75"/>
      <rect x="1205" y="140" width="55" height="75"/><rect x="1290" y="140" width="55" height="75"/>
      <rect x="1205" y="250" width="55" height="75"/><rect x="1290" y="250" width="55" height="75"/>
    </g>
    <rect x="1180" y="340" width="210" height="90" fill="#d9c3a0"/>
    <!-- 小树 -->
    <rect x="812" y="300" width="8" height="90" fill="#8a6d4d"/>
    <circle cx="816" cy="285" r="36" fill="#a9c98a"/>
    <circle cx="840" cy="300" r="24" fill="#9cbf7c"/>
  </g>

  <!-- 街边花盆（会随风轻摆） -->
  <g id="flowers" filter="url(#pn-wobble)"></g>

  <!-- ===== 车：车内 + 玻璃 ===== -->
  <g filter="url(#pn-wobble)" stroke="#4d4540" stroke-width="2.5" stroke-linejoin="round">
    <g clip-path="url(#pn-glassClip)">
      <path d="M0,560 Q380,520 830,560 L830,700 L0,700 Z" fill="#6f5d4e" opacity=".85"/>
      <path d="M150,640 A150,120 0 0 1 450,640" fill="none" stroke="#3f3834" stroke-width="16"/>
      <path d="M0,300 L70,300 L90,640 L0,640 Z" fill="#5c5550" opacity=".7"/>
      <path d="M0,168 L392,160 L826,588 L0,640 Z" fill="url(#pn-glass)" stroke="none"/>
      <path d="M160,170 L250,170 L60,640 L-20,640 Z" fill="#fff" opacity=".28" stroke="none"/>
      <path d="M300,170 L340,170 L170,640 L140,640 Z" fill="#fff" opacity=".18" stroke="none"/>
    </g>
    <!-- 车顶与 A 柱 -->
    <path d="M-10,110 Q200,95 420,120 L430,160 L0,170 Z" fill="#b89a78"/>
    <path d="M392,160 L430,150 L880,580 L826,588 Z" fill="#8f7960"/>
    <path d="M0,168 L392,160 L826,588 L0,640" fill="none" stroke="#3f3b38" stroke-width="12"/>
    <!-- 后视镜 -->
    <path d="M180,172 V225" stroke="#555" stroke-width="6"/>
    <rect x="110" y="222" width="150" height="50" rx="14" fill="#8e969b"/>
    <!-- 机盖 -->
    <path d="M-10,640 L826,588 Q1100,580 1390,610 L1390,780 L-10,780 Z" fill="url(#pn-hood)"/>
    <path d="M620,720 Q1000,690 1376,720" fill="none" stroke="#e7d4bb" stroke-width="5" opacity=".8"/>
  </g>

  <!-- 纸条（在雨刷下面） -->
  <g id="note" filter="url(#pn-wobble)">
    <path d="M-130,-88 L130,-88 L136,88 L-126,92 Z" fill="#fdfcf7" stroke="#6e6a62" stroke-width="2.5"/>
    <path d="M-120,-80 L125,-80 L128,-60 L-118,-60 Z" fill="#000" opacity=".03" stroke="none"/>
  </g>

  <!-- 雨刷 -->
  <g id="wiper" filter="url(#pn-wobble)" stroke="#3a3a3c" stroke-linecap="round">
    <line x1="255" y1="738" x2="520" y2="614" stroke-width="18"/>
    <line x1="255" y1="738" x2="520" y2="614" stroke="#a9adb2" stroke-width="10"/>
    <line x1="290" y1="632" x2="760" y2="600" stroke-width="10"/>
    <line x1="290" y1="632" x2="760" y2="600" stroke="#c9ccd0" stroke-width="4"/>
    <circle cx="255" cy="738" r="16" fill="#555" stroke-width="3"/>
  </g>
  <g filter="url(#pn-wobble)" stroke="#3a3a3c" stroke-linecap="round">
    <line x1="585" y1="700" x2="700" y2="640" stroke-width="16"/>
    <line x1="585" y1="700" x2="700" y2="640" stroke="#a9adb2" stroke-width="8"/>
    <line x1="620" y1="624" x2="850" y2="604" stroke-width="9"/>
    <circle cx="585" cy="700" r="14" fill="#555" stroke-width="3"/>
  </g>

  <!-- ===== 警察 ===== -->
  <g id="cop" filter="url(#pn-wobble)" stroke="#4a3f36" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
    <g id="body">
      <!-- 躯干 -->
      <path d="M770,330 Q960,262 1165,300 Q1230,420 1260,700 L840,700 Q800,500 770,330 Z" fill="url(#pn-shirt)"/>
      <path d="M1000,300 Q1030,500 1010,700" fill="none" stroke="#8fb0c9" stroke-width="3"/>
      <path d="M880,420 L960,410 L962,470 L884,478 Z" fill="#b3cde2"/>
      <path d="M1050,405 L1130,400 L1136,462 L1054,468 Z" fill="#b3cde2"/>
      <!-- 领口 -->
      <path d="M915,295 L965,350 L1005,285 Z" fill="#f0c9a8"/>
      <path d="M905,290 L965,352 L940,380 L890,305 Z" fill="#d8e7f3"/>
      <path d="M1015,282 L965,352 L995,372 L1035,298 Z" fill="#d8e7f3"/>
      <!-- 肩章 -->
      <path d="M800,318 L895,292 L905,318 L812,346 Z" fill="#2f4a73"/>
      <path d="M1040,288 L1150,300 L1146,326 L1036,314 Z" fill="#2f4a73"/>
      <path d="M1120,298 L1124,322" stroke="#e1b64c" stroke-width="5"/>
      <!-- 右臂臂章 -->
      <path d="M1150,380 L1215,370 L1225,430 L1185,460 L1160,430 Z" fill="#2f4a73"/>
      <circle cx="1188" cy="412" r="12" fill="#e1b64c" stroke-width="2"/>
    </g>

    <!-- 头（整体可转动） -->
    <g id="head">
      <path d="M925,250 L1005,250 L1010,300 L920,300 Z" fill="#eac2a0"/>
      <ellipse cx="1045" cy="205" rx="18" ry="28" fill="#f2cdae"/>
      <path d="M870,170 Q868,280 955,300 Q1035,300 1045,190 Z" fill="#f5d4b6"/>
      <!-- 金发 -->
      <path d="M868,150 Q875,120 925,118 L1050,120 Q1062,160 1045,195 Q1030,150 990,148 Q930,150 900,160 Q880,165 872,190 Z" fill="#ecc66f"/>
      <!-- 腮红 -->
      <ellipse cx="895" cy="240" rx="20" ry="11" fill="#f0a591" opacity=".45" stroke="none"/>
      <ellipse cx="1005" cy="240" rx="20" ry="11" fill="#f0a591" opacity=".45" stroke="none"/>
      <!-- 眉毛 -->
      <path id="browL" d="M890,178 Q910,168 930,176" fill="none" stroke="#b58a3c" stroke-width="5"/>
      <path id="browR" d="M968,176 Q990,168 1010,178" fill="none" stroke="#b58a3c" stroke-width="5"/>
      <!-- 眼睛 -->
      <g id="eyeL" transform="translate(912,203)">
        <g class="lid"><ellipse rx="15" ry="12" fill="#fff" stroke-width="2.5"/><g class="iris"><circle r="8" fill="#4f7fb4" stroke="none"/><circle r="4" fill="#1d2a3a" stroke="none"/><circle cx="-2.5" cy="-3" r="2" fill="#fff" stroke="none"/></g></g>
      </g>
      <g id="eyeR" transform="translate(988,203)">
        <g class="lid"><ellipse rx="15" ry="12" fill="#fff" stroke-width="2.5"/><g class="iris"><circle r="8" fill="#4f7fb4" stroke="none"/><circle r="4" fill="#1d2a3a" stroke="none"/><circle cx="-2.5" cy="-3" r="2" fill="#fff" stroke="none"/></g></g>
      </g>
      <!-- 鼻子 -->
      <path d="M948,210 Q940,238 952,245" fill="none" stroke="#c9967a" stroke-width="3"/>
      <!-- 嘴：全程闭着，只改变笑的弧度 -->
      <path id="mouth" d="M925,265 Q950,272 975,265" fill="none" stroke="#9a5a4a" stroke-width="4"/>
      <!-- 帽子 -->
      <path d="M835,105 Q830,45 960,30 Q1100,28 1105,95 L1080,128 Q960,112 850,132 Z" fill="#fbfbf8"/>
      <path d="M850,105 Q960,88 1082,98 L1080,135 Q960,122 852,140 Z" fill="#2c4670"/>
      <path d="M852,140 Q960,122 1080,135 Q1040,170 940,168 Q860,168 820,160 Z" fill="#1f2226"/>
      <path d="M870,150 Q960,140 1040,150" fill="none" stroke="#5a5f66" stroke-width="3"/>
      <circle cx="960" cy="92" r="22" fill="#e3b94f"/>
      <path d="M960,78 V106 M946,92 H974" stroke="#2c4670" stroke-width="4"/>
    </g>
  </g>

  <!-- 手臂（JS 每帧重算，两段骨骼 IK） -->
  <g id="arms" filter="url(#pn-wobble)" stroke-linecap="round" stroke-linejoin="round"></g>

  <!-- 纸纹与水彩晕染，最上层 -->
  <rect width="1376" height="768" filter="url(#pn-bloom)" style="mix-blend-mode:soft-light" pointer-events="none"/>
  <rect width="1376" height="768" filter="url(#pn-paper)" opacity=".35" style="mix-blend-mode:multiply" pointer-events="none"/>
</svg>
</template>
