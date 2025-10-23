num = [1];
den = [1,2];
figure(1);step (num,den); grid on ;

num2 = [1,1];
den2 = [1,0.5,4];
figure(2); step (num2,den2); grid on;

num = [1];
den = [1,2];
figure(3);impulse (num,den); grid on ;

num2 = [1,1];
den2 = [1,0.5,4];
figure(4);impulse (num2,den2); grid on;
