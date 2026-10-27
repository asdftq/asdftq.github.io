(() => {
  'use strict';
  const root = document.querySelector('[data-spinhop-demo]');
  if (!root) return;
  const canvas = root.querySelector('canvas'), ctx = canvas.getContext('2d');
  if (!ctx) return;
  const scoreText = root.querySelector('[data-score]'), bestText = root.querySelector('[data-best]');
  const message = root.querySelector('[data-game-message]'), hopButton = root.querySelector('[data-hop]');
  const shareButton = root.querySelector('[data-share-score]');
  let score = 0, best = 0, angle = -Math.PI / 2, state = 'ready', lastTime = 0, frame = 0, flightStart = 0;
  let takeoff = {x: 0, y: 0};
  try { best = Math.max(0, Math.floor(Number(localStorage.getItem('spinhop.demo.best.v1')) || 0)); } catch {}
  bestText.textContent = String(best);
  const targetAngle = () => -Math.PI / 2 + (score % 3 - 1) * 0.25;
  const point = a => ({x: 210 + Math.cos(a) * 89, y: 280 + Math.sin(a) * 89});
  const wrapped = a => Math.atan2(Math.sin(a), Math.cos(a));
  function circle(x,y,r,color) { ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill(); }
  function draw(now) {
    const elapsed = lastTime ? Math.min((now-lastTime)/1000, 0.05) : 0;
    lastTime=now;
    if (state === 'ready') angle = targetAngle(); // Let the first explicit tap teach the leap.
    if (state === 'playing') angle += elapsed * (1.25 + Math.min(score,20)*.045);
    ctx.clearRect(0,0,420,420);
    ctx.fillStyle='#b6d9d0';ctx.font='12px -apple-system, sans-serif';ctx.textAlign='center';
    ctx.fillText('SIMPLIFIED WEB TIMING DEMO',210,25);
    const target = point(targetAngle());
    ctx.strokeStyle='#344f55';ctx.lineWidth=28;ctx.beginPath();ctx.arc(210,280,89,0,Math.PI*2);ctx.stroke();
    ctx.strokeStyle='#bce98c';ctx.lineWidth=28;ctx.beginPath();ctx.arc(210,280,89,targetAngle()-.29,targetAngle()+.29);ctx.stroke();
    circle(target.x,target.y-87,35,'#698e83');circle(target.x,target.y-87,24,'#9dc783');
    let player=point(angle);
    if(state==='flying') {
      const t=Math.min(1,(now-flightStart)/420);
      player={x:takeoff.x+(target.x-takeoff.x)*t,y:takeoff.y-87*t-52*Math.sin(t*Math.PI)};
      if(t>=1) {
        score++;scoreText.textContent=String(score);
        if(score>best) {best=score;bestText.textContent=String(best);try{localStorage.setItem('spinhop.demo.best.v1',String(best));}catch{}}
        message.textContent=`Landed! Demo score ${score}. Find the next green opening.`;
        angle=Math.PI/2;state='playing';hopButton.textContent='Tap to hop';
      }
    }
    circle(player.x,player.y,13,'#f2e7aa');circle(player.x-4,player.y-3,2,'#183640');circle(player.x+4,player.y-3,2,'#183640');
    ctx.fillStyle='#b6d9d0';ctx.fillText(state==='over'?'MISS · TAP TO TRY AGAIN':'HOP WHEN YOU REACH THE GREEN OPENING',210,391);
    frame=requestAnimationFrame(draw);
  }
  function hop() {
    if(state==='flying') return;
    if(state==='over') {score=0;scoreText.textContent='0';angle=Math.PI/2;state='playing';message.textContent='New run. Wait for the green opening, then hop.';hopButton.textContent='Tap to hop';return;}
    if(Math.abs(wrapped(angle-targetAngle())) <= .29) {
      takeoff=point(angle);flightStart=performance.now();state='flying';message.textContent='Hopping…';
    } else {state='over';message.textContent=`Missed. Demo score ${score}. Try the timing again.`;hopButton.textContent='Try again';}
  }
  hopButton.addEventListener('click',hop);
  canvas.addEventListener('pointerdown',e=>{e.preventDefault();hop();});
  canvas.addEventListener('keydown',e=>{if(e.code==='Space'||e.code==='Enter'){e.preventDefault();hop();}});
  shareButton.addEventListener('click',async()=>{
    const text=`My SpinHop web demo best: ${best} hops. This is a simplified demo score, not an app score.`;
    const url='https://www.asdftq.com/spinhop/';
    try {
      if(navigator.share) {await navigator.share({title:'SpinHop demo score',text,url});}
      else if(navigator.clipboard) {await navigator.clipboard.writeText(`${text} ${url}`);message.textContent='Demo score and link copied.';}
      else {message.textContent=`${text} ${url}`;}
    } catch(error) {if(error.name!=='AbortError')message.textContent=`${text} ${url}`;}
  });
  // Start only when visible and stop animation when leaving the page.
  const start=()=>{cancelAnimationFrame(frame);lastTime=0;if(!document.hidden)frame=requestAnimationFrame(draw);};
  document.addEventListener('visibilitychange',start);
  window.addEventListener('pagehide',()=>cancelAnimationFrame(frame));
  start();
})();
