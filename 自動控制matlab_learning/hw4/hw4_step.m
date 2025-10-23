% 一階系統
a = [1,3,6];
for i = 1:length(a)
    system = tf(a(i), [1 a(i)]);
    figure;
    step(system);grid on;
    title(['Step Response: a = ' num2str(a(i))]);
    %MATLAB 中，字串（string）和數字（numeric）不能直接相加。
end

% 二階系統 (b, wn)
%params是一個矩陣(matrix)，用來儲存多組系統參數
params = [0.0 0.5;
          0.0 2;
          0.2 0.5;
          0.2 2];
for i = 1:size(params,1)
    b = params(i,1); wn = params(i,2);
    system = tf(wn^2, [1 2*b*wn wn^2]);

    % 手動設定時間軸（依頻率調整：頻率越高，Δt越小）
    Tfinal = 40;% 看前 40 秒
    dt = 0.005;% 取樣時間
    t = 0:dt:Tfinal;

    figure;
    step(system);grid on;
    title(['Step Response: b = ' num2str(b) ',  ω_n = ' num2str(wn)]);
    xlim([0 Tfinal]);% 防止自動把時間軸拉很長
end