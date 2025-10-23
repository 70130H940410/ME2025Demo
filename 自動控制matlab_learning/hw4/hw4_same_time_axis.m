set(0,'DefaultFigureColor','w');
%% 第一題impulse input 
%% (i) 一階系統  G(s)=a/(s+a)   a=1,3,6
figure; hold on; grid on;
a_list = [1 3 6];
Tfinal = 5;                 % 一階衰減很快，5 s 夠看
dt = 0.001;                 % 時間解析度
t = 0:dt:Tfinal;
for k = 1:numel(a_list)
    a = a_list(k);
    sys = tf(a,[1 a]);
    % 只畫在同一張圖
    [y,tt] = impulse(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(i) Impulse Response of First-Order Systems');
xlabel('Time (s)'); ylabel('Amplitude');
legend('a=1','a=3','a=6','Location','best');
xlim([0 Tfinal]); hold off;

%% (ii) 二階無阻尼  b=0,  wn=0.5, 2
figure; hold on; grid on;
b = 0;
wn_list = [0.5 2];

% 為了同一張圖共用時間軸：
T_low  = 2*pi/min(wn_list);          % 最慢週期
T_high = 2*pi/max(wn_list);          % 最快週期
Tfinal = 10*T_low;                   % 看 ~10 個慢週期
dt     = T_high/200;                 % 對最快頻率每週期取 ≥200 點
t      = 0:dt:Tfinal;

for k = 1:numel(wn_list)
    wn  = wn_list(k);
    sys = tf(wn^2,[1 2*b*wn wn^2]);
    [y,tt] = impulse(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(ii) Impulse Response of 2nd-Order (Undamped, b=0)');
xlabel('Time (s)'); ylabel('Amplitude');
legend('\omega_n=0.5','\omega_n=2','Location','best');
xlim([0 Tfinal]); hold off;

%% (iii) 二階欠阻尼  b=0.2,  wn=0.5, 2
figure; hold on; grid on;
b = 0.2;
wn_list = [0.5 2];

% 欠阻尼也用同樣的時間/解析度策略
T_low  = 2*pi/min(wn_list);
T_high = 2*pi/max(wn_list);
Tfinal = 10*T_low;
dt     = T_high/200;
t      = 0:dt:Tfinal;

for k = 1:numel(wn_list)
    wn  = wn_list(k);
    sys = tf(wn^2,[1 2*b*wn wn^2]);
    [y,tt] = impulse(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(iii) Impulse Response of 2nd-Order (Underdamped, b=0.2)');
xlabel('Time (s)'); ylabel('Amplitude');
legend('\omega_n=0.5','\omega_n=2','Location','best');
xlim([0 Tfinal]); hold off;

%% 第二題step input 
%% (i) 一階系統  G(s)=a/(s+a)   a=1,3,6
figure; hold on; grid on;
a_list = [1 3 6];
Tfinal = 5;                 % 一階衰減很快，5 s 夠看
dt = 0.001;                 % 時間解析度
t = 0:dt:Tfinal;
for k = 1:numel(a_list)
    a = a_list(k);
    sys = tf(a,[1 a]);
    % 只畫在同一張圖
    [y,tt] = step(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(i) Step Response of First-Order Systems');
xlabel('Time (s)'); ylabel('Amplitude');
legend('a=1','a=3','a=6','Location','best');
xlim([0 Tfinal]); hold off;

%% (ii) 二階無阻尼  b=0,  wn=0.5, 2
figure; hold on; grid on;
b = 0;
wn_list = [0.5 2];

% 為了同一張圖共用時間軸：
T_low  = 2*pi/min(wn_list);          % 最慢週期
T_high = 2*pi/max(wn_list);          % 最快週期
Tfinal = 10*T_low;                   % 看 ~10 個慢週期
dt     = T_high/200;                 % 對最快頻率每週期取 ≥200 點
t      = 0:dt:Tfinal;

for k = 1:numel(wn_list)
    wn  = wn_list(k);
    sys = tf(wn^2,[1 2*b*wn wn^2]);
    [y,tt] = step(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(ii) Step Response of 2nd-Order (Undamped, b=0)');
xlabel('Time (s)'); ylabel('Amplitude');
legend('\omega_n=0.5','\omega_n=2','Location','best');
xlim([0 Tfinal]); hold off;

%% (iii) 二階欠阻尼  b=0.2,  wn=0.5, 2
figure; hold on; grid on;
b = 0.2;
wn_list = [0.5 2];

% 欠阻尼也用同樣的時間/解析度策略
T_low  = 2*pi/min(wn_list);
T_high = 2*pi/max(wn_list);
Tfinal = 10*T_low;
dt     = T_high/200;
t      = 0:dt:Tfinal;

for k = 1:numel(wn_list)
    wn  = wn_list(k);
    sys = tf(wn^2,[1 2*b*wn wn^2]);
    [y,tt] = step(sys,t);
    plot(tt,y,'LineWidth',1.2);
end
title('(iii) Step Response of 2nd-Order (Underdamped, b=0.2)');
xlabel('Time (s)'); ylabel('Amplitude');
legend('\omega_n=0.5','\omega_n=2','Location','best');
xlim([0 Tfinal]); hold off;
