const W=124,H=108,CX=62;
function mk(){
  const S={L:new Uint8Array(W*H),P:new Uint8Array(W*H),Z:new Float32Array(W*H),F:new Float32Array(W*H)};
  const box=(cx,cy,rx,ry,f)=>{const x0=Math.max(0,Math.floor(cx-rx-1)),x1=Math.min(W-1,Math.ceil(cx+rx+1)),y0=Math.max(0,Math.floor(cy-ry-1)),y1=Math.min(H-1,Math.ceil(cy+ry+1));for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const u=(x+.5-cx)/rx,v=(y+.5-cy)/ry,q=u*u+v*v;if(q<=1)f(x,y,q,y*W+x);}};
  S.dome=(cx,cy,rx,ry,h,lab,part,z0=0,o={})=>box(cx,cy,rx,ry,(x,y,q,i)=>{if(o.only&&!o.only.includes(S.P[i]))return;S.L[i]=lab;S.P[i]=part;S.Z[i]=z0+h*Math.sqrt(1-q);if(o.fold)S.F[i]=(y+.5-cy)/ry-.45*((x+.5-cx)/rx)**2+1;});
  S.bump=(cx,cy,rx,ry,h,lab,only)=>box(cx,cy,rx,ry,(x,y,q,i)=>{if(!S.L[i])return;if(only&&!only.includes(S.P[i]))return;S.Z[i]+=h*Math.sqrt(1-q);if(lab)S.L[i]=lab;});
  S.interp=(pts,y)=>{if(y<=pts[0][0])return pts[0];for(let k=0;k<pts.length-1;k++){const a=pts[k],b=pts[k+1];if(y<=b[0]){const t=(y-a[0])/(b[0]-a[0]);return a.map((v,j)=>v+(b[j]-v)*t);}}return pts[pts.length-1];};
  S.taper=(pts,lab,part,z0=0)=>{for(let y=Math.floor(pts[0][0]);y<=Math.ceil(pts[pts.length-1][0]);y++){if(y<0||y>=H)continue;const [,hw,h]=S.interp(pts,y+.5);for(let x=0;x<W;x++){const d=(x+.5-CX)/hw;if(Math.abs(d)>1)continue;const i=y*W+x;S.L[i]=lab;S.P[i]=part;S.Z[i]=z0+h*Math.sqrt(1-d*d);}}};
  S.cone=(bx,by,dx,dy,len,w,lab,part,zb)=>{const n=Math.hypot(dx,dy);dx/=n;dy/=n;for(let k=0;k<=len;k+=.3){const hw=w*(1-k/len)+.2;for(let q=-hw;q<=hw;q+=.3){const x=Math.floor(bx+dx*k-dy*q),y=Math.floor(by+dy*k+dx*q);if(x<0||y<0||x>=W||y>=H)continue;const i=y*W+x;S.L[i]=lab;S.P[i]=part;S.Z[i]=zb+1+2.4*(1-k/len)*Math.sqrt(Math.max(0,1-(q/hw)**2));}}};
  S.px=(x,y,lab)=>{if(x>=0&&y>=0&&x<W&&y<H&&S.L[y*W+x])S.L[y*W+x]=lab;};
  S.mirror=()=>{for(let y=0;y<H;y++)for(let x=W/2;x<W;x++){const i=y*W+x,j=y*W+W-1-x;S.L[i]=S.L[j];S.P[i]=S.P[j];S.Z[i]=S.Z[j];S.F[i]=S.F[j];}};
  return S;
}
const h2=(a,b)=>{let n=(a*374761393+b*668265263)|0;n=(n^(n>>>13))*1274126177|0;return ((n^(n>>>16))>>>0)/4294967296;};
function texture(S){
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x,l=S.L[i],p=S.P[i];if(!l)continue;
    if(l===1&&p===1&&Math.abs(x+.5-CX)<14){const rx=x+.5-CX,col=Math.floor((rx+3.5)/7),yy=y+(col&1)*3,u=(((rx+3.5)%7)+7)%7/7,v=((yy%6)+6)%6/6;
      if(u>.14&&u<.86&&v>.16&&v<.84){S.Z[i]+=1.4+1.3*Math.max(0,1-Math.abs(u-.5)*5);}else S.Z[i]-=.8;}
    else if(l===1){const c=5.2,ry=Math.floor(y/c);let b1=9,b2=9;for(let j=ry-1;j<=ry+1;j++){const off=(j&1)*c/2,rr=Math.floor((x-off)/c);for(let k=rr-1;k<=rr+1;k++){const cx=k*c+off+c/2+(h2(k,j)-.5)*1.6,cy=j*c+c/2+(h2(j,k+3)-.5)*1.4,d=Math.hypot(x+.5-cx,y+.5-cy);if(d<b1){b2=b1;b1=d;}else if(d<b2)b2=d;}}
      S.Z[i]+=.6*Math.max(0,1-b1/2.8)-(b2-b1<.7?.35:0);if(h2(x*7+1,y*13+5)<.012&&p===5)S.L[i]=9;}
    else if(l===2){const fr=(S.F[i]*3.2)%1;if(S.F[i]>.9&&fr<.16)S.Z[i]-=1.6;}}
}
const PAL={j:['#060802','#141c08','#22300e','#324414','#43581a','#567020','#6a8628','#7f9c32','#98b440','#b4c858','#d2de7c'],1:['#040802','#0d1c09','#16300f','#204417','#2b581e','#386e26','#47852e','#5a9a36','#73b143','#94c95a','#b6df7c'],2:['#2a1c0c','#46321a','#644a26','#846434','#a48044','#c29c58','#dab870','#ecd08e','#f8e6b2'],3:['#0e0206','#1e040c','#320814','#4c0c1e','#6a1229','#8c1c38','#ae2c4c','#cc4466','#e66884'],4:['#2e2414','#5c4e32','#958452','#c2b282','#e2d6b0','#f6efd8','#fffdf4'],8:['#4e0a1e','#7a1634','#a6284c','#cc4268','#e86a8c','#ff98b0'],5:['#3a0410','#7a0a1e','#be1a34','#f2344e','#ff7a7a']};
function render(S){
  const {L,P,Z}=S,cv=createCanvas(W,H),g=cv.getContext('2d'),im=g.createImageData(W,H),o=im.data;
  const lab=(x,y)=>(x<0||x>=W||y>=H)?0:(y<0?L[x]:L[y*W+x]);
  const zat=(x,y)=>{x=Math.max(0,Math.min(W-1,x));if(y>=H)return -20;if(y<0)y=0;return L[y*W+x]?Z[y*W+x]:Z[y*W+x]-6;};
  const lx=-.5,ly=-.68,lz=.9,ln=Math.hypot(lx,ly,lz);
  const bay=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]];
  const hex=h=>[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x,l=L[i];if(!l)continue;let col=null;
    const z=Z[i],n4=[[x-1,y],[x+1,y],[x,y-1],[x,y+1]];
    const outer=n4.some(([a,b])=>!lab(a,b));
    const gx=Math.max(-4,Math.min(4,(zat(x+1,y)-zat(x-1,y))/2)),gy=Math.max(-4,Math.min(4,(zat(x,y+1)-zat(x,y-1))/2));
    const nx=-gx*.85,ny=-gy*.85,nz=1,nn=Math.hypot(nx,ny,nz),dif=Math.max(0,(nx*lx+ny*ly+nz*lz)/(nn*ln));
    let occ=0;for(const [dx,dy] of [[2,0],[-2,0],[0,2],[0,-2],[2,2],[-2,-2],[2,-2],[-2,2],[3,0],[-3,0],[0,3],[0,-3]]){const d=zat(x+dx,y+dy)-z;if(d>0)occ+=Math.min(d,5);}occ=Math.min(1,occ/22);
    const contact=n4.some(([a,b])=>{if(a<0||b<0||a>=W||b>=H)return false;const j=b*W+a;return L[j]&&P[j]!==P[i]&&Z[j]>z+2.2;});
    let sh=.1+.95*dif-.55*occ;
    if(l===6)col='#120004';else if(l===7)col='#ffffff';else if(l===9)col='#060c04';else if(l===10)col='#080104';
    else{const pal=(l===1&&P[i]===3)?PAL.j:(PAL[l]||PAL[1]),n=pal.length-1;
      if(outer&&l!==4)col=l===3||l===8?pal[0]:'#030602';
      else if(contact&&l!==4&&l!==5)col=pal[l===1?1:0];
      else if(l===5){const ring=n4.some(([a,b])=>{const t=lab(a,b);return t!==5&&t!==6&&t!==7;});col=ring?pal[0]:pal[Math.max(1,Math.min(n,Math.round(sh*n+.6)))];}
      else{if(l===3)sh=sh*.75+.05;if(l===4)sh=sh*.9+.2;if(l===2)sh+=.05;
        const f=Math.max(0,Math.min(.999,sh))*n,lo=Math.floor(f),fr=f-lo,up=(fr>.4&&fr<.6)?(fr*16>bay[y&3][x&3]+4?1:0):(fr>=.6?1:0);col=pal[Math.max(1,Math.min(n,lo+up))];}}
    const [r,gg,b]=hex(col),j=i*4;o[j]=r;o[j+1]=gg;o[j+2]=b;o[j+3]=255;}
  g.putImageData(im,0,0);return cv;
}
function eye(S,cx,cy,r,z){S.dome(cx,cy,r*1.85,r*1.65,6,1,6,z);S.dome(cx,cy,r,r*.92,1.6,5,7,z+5);for(let y=Math.round(cy-r*.75);y<=Math.round(cy+r*.6);y++)S.px(Math.floor(cx),y,6);S.px(Math.floor(cx-r*.45),Math.floor(cy-r*.5),7);S.dome(cx,cy-r*1.45,r*2,r*.7,3,1,8,z+4);}
function neck(S){S.dome(CX,-14,31,46,14,1,1);}
function nuchal(S){S.bump(54,9,5,4,3.2,0,[1]);S.bump(54,1,4.2,3.6,2.6,0,[1]);}
// A · MAW — croc jaws parted, pink gape showing down both sides
function buildA(){const S=mk();neck(S);nuchal(S);
  S.dome(34,45,8.5,11,10,1,2);
  const lo=[[38,34,9],[60,32,8],[82,26,7],[98,19,7]],mo=[[40,30.5,3],[60,29,3],[82,23,3],[96,16,3]],up=[[38,24,13],[60,18.5,12],[80,12.5,11],[92,9.5,11]];
  S.taper(lo,1,3,0);S.dome(CX,101,19,7,8,1,3);
  S.taper(mo,3,12,-6);S.dome(CX,98,15,6,3,3,12,-6);
  S.taper([[44,28,2],[70,25,2],[92,17,2]],8,14,-5);
  for(let y=50;y<=92;y+=7){const w=S.interp(mo,y)[1];S.cone(CX-w+.4,y,1,-.35,4.6,1.6,4,11,-2);}
  [[CX-10,101,.4,-1],[CX-5,102.5,.2,-1]].forEach(([x,y,dx,dy])=>S.cone(x,y,dx,dy,4,1.3,4,11,-2));
  S.taper(up,1,5,1);S.dome(CX,94,11.5,7,12,1,5,1);S.bump(CX,96,7,4.5,2.6,0,[5]);
  for(let y=46;y<=88;y+=7){const w=S.interp(up,y)[1];S.cone(CX-w+.6,y,-1,.35,5,1.7,4,11,6);}
  [[CX-8,98,-.25,1],[CX-3.5,100,0,1]].forEach(([x,y,dx,dy])=>S.cone(x,y,dx,dy,4,1.3,4,11,6));
  S.dome(CX,32,30,20,16,1,4);
  eye(S,45,27,4.6,14);
  S.px(58,96,9);S.px(59,96,9);S.px(58,97,9);
  S.mirror();texture(S);return S;}
// B · CROWN
function buildB(){const S=mk();neck(S);nuchal(S);
  for(const [a,len,w] of [[205,15,3.2],[184,17,3.6],[163,14,3.1],[226,11,2.6],[143,10,2.6]]){const r=a*Math.PI/180;S.cone(CX+Math.cos(r)*27,30+Math.sin(r)*17,Math.cos(r),Math.sin(r),len,w,4,10,8);}
  S.dome(34,44,8.5,11,10,1,2);
  const lo=[[38,26,9],[60,20.5,8],[80,14.5,7],[96,11,7]],up=[[38,24,13],[60,18.5,12],[80,12.5,11],[94,9.5,11]];
  S.taper(lo,1,3,0);S.dome(CX,98,13,8,8,1,3);
  S.taper(up,1,5,1);S.dome(CX,97,11.5,7,12,1,5,1);S.bump(CX,99,7,4.5,2.6,0,[5]);
  for(let y=46,k=0;y<=92;y+=4.5,k++){const w=S.interp(up,y)[1];S.cone(CX-w+.6,y,-.9,k%2?.7:-.7,3.4,1.3,4,11,6);}
  S.cone(CX-10.5,89,-.35,-1,6.5,1.9,4,11,8);
  S.dome(CX,32,30,20,16,1,4);
  eye(S,45,27,4.4,14);eye(S,49,41,2.8,12);
  S.px(58,99,9);S.px(59,99,9);S.px(58,100,9);
  S.mirror();texture(S);return S;}
// C · POUCH — croc with bloated throat sacs, jaws ajar, tongue lolling
function buildC(){const S=mk();neck(S);nuchal(S);
  S.dome(29,66,17,16,10,2,15,0,{fold:true});
  S.dome(35,45,8.5,11,10,1,2);
  const lo=[[40,25,9],[64,20,8],[88,13.5,7]],up=[[40,23,13],[62,17,12],[82,11.5,11]];
  S.taper(lo,1,3,0);S.dome(CX,92,13,6.5,8,1,3);
  S.dome(CX,88,11,6,2,3,12,-3);
  S.taper(up,1,5,1);S.dome(CX,84,10.5,6.5,12,1,5,1);S.bump(CX,86,6.5,4,2.5,0,[5]);
  for(let y=46,k=0;y<=82;y+=4.5,k++){const w=S.interp(up,y)[1];S.cone(CX-w+.6,y,-.9,k%2?.7:-.7,3.2,1.3,4,11,6);}
  for(const x of [54,58])S.cone(x+.5,89,0,1,3,1.1,4,11,4);
  S.dome(CX,32,32,22,16,1,4);
  eye(S,43,25,5.6,13);
  [[50,16],[56,26],[48,38],[40,34],[54,40]].forEach(([x,y])=>S.bump(x,y,1.6,1.6,1.6,0,[4]));
  S.px(58,86,9);S.px(59,86,9);
  S.mirror();texture(S);
  for(let i=0;i<S.L.length;i++)if(S.P[i]===15&&S.F[i]<.78)S.L[i]=1;
  for(let i=0;i<=20;i++){const t=i/20,x=66+5*t+2*Math.sin(t*5),y=91+14*t,r=4.2-1.5*t;S.dome(x,y,r,r,3,8,14,6);}
  S.bump(68,97,1,6,-1.2,0,[14]);
  return S;}
