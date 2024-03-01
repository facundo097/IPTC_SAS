%clear all
%clc

simOut = sim("Controllers_Simulation");
t = simOut.tout;

figure(1)
plot(t, simOut.V_out, 'LineWidth', 1.5, 'color', 'r')
set(gcf, 'Position', [300 300 1000 600])
grid on
title("Respuesta al escalón unitario del control PID", 'FontSize', 20) 
xlabel('Tiempo (s)', 'FontSize', 14) 
ylabel('Tensión (V)', 'FontSize', 14) 
set(gca, 'FontSize', 12);
xlim([-0.0001, 0.0018])
ylim([0, 1.2])

figure(2)
plot(t, simOut.V_out, 'LineWidth', 1.5, 'color', 'r')
set(gcf, 'Position', [300 300 1000 600])
grid on
title("Respuesta al escalón unitario del control PID", 'FontSize', 20) 
xlabel('Tiempo (s)', 'FontSize', 14) 
ylabel('Tensión (V)', 'FontSize', 14) 
set(gca, 'FontSize', 12);
xlim([-0.001, 0.02])
ylim([0, 1.2])

figure(3)
plot(t, simOut.I_out, 'LineWidth', 1.5, 'color', 'r')
set(gcf, 'Position', [300 300 1000 600])
grid on
title("Respuesta al escalón unitario del control PI", 'FontSize', 20)
xlabel('Tiempo (s)', 'FontSize', 14)
ylabel('Corriente (A)', 'FontSize', 14)
set(gca, 'FontSize', 12);
xlim([-0.0001, 0.0016])
ylim([0, 1.2])

figure(4)
plot(t, simOut.I_out, 'LineWidth', 1.5, 'color', 'r')
set(gcf, 'Position', [300 300 1000 600])
grid on
title("Respuesta al escalón unitario del control PI", 'FontSize', 20)
xlabel('Tiempo (s)', 'FontSize', 14)
ylabel('Corriente (A)', 'FontSize', 14)
set(gca, 'FontSize', 12);
xlim([-0.001, 0.05])
ylim([0, 1.2])
