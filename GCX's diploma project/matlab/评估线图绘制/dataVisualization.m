clc; clear all

num = xlsread('myData.xlsx');
stairs(num(1,:),num(2,:),'LineWidth',0.7),hold on
stairs(num(3,:),num(4,:),'LineWidth',0.7),hold on
stairs(num(5,:),num(6,:),'LineWidth',0.7),hold on
stairs(num(7,:),num(8,:),'LineWidth',0.7)

title('回合得分曲线'),xlabel('episode'),ylabel('reward')
set(gca,'xticklabel',get(gca,'xtick'));  % 关闭 Y 轴的科学计数法
legend('a','b','c','d')
grid on