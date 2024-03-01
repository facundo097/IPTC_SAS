% Matlab® Example: Synchronous Buck Converter
% TB06, page 93

% Parameters from the plant:
clc 

L = 470*10^-6;
rL = 91.8*10^-3;
C = 470*10^-6;
rC = 20*10^-3;

% This example shows how to develop the small-signal control-to-output transfer
% functions Gvu(z) and Giu(z) usingMatlab®. First, define the converter state-space
% matrices:

A1 = [ -(rC+rL)/L -1/L; 1/C 0 ];
A0 = A1;
b1 = [ 1/L rC/L; 0 -1/C ];
b0 = [ 0 rC/L; 0 -1/C];
c1 = [1 0; rC 1];
c0 = c1;

% Define the reference conditions
Vg=24;
Io=3.6;
D=0.5;
Dprime=1-D;

tcntrl=8*10^-6;
Ts=8*10^-6; %fs = 125kHz

Tdpwm=D*Ts;
td=tcntrl+Tdpwm;
Nr=1;
fs=1/Ts;

% Next, evaluate X↓ according to Table 3.1. The expm method can be used to numerically
% evaluate the matrix exponential:
% This assumes that matrices A1 and A0 are invertible, which is always the case as long 
% as parasitic components (rC, rL) are included in themodeling step.

A1i = A1^-1;
A0i = A0^-1;
Xdown = ((eye(2)-expm(A1*D*Ts)*expm(A0*Dprime*Ts))^-1)*(-expm(A1*D*Ts)*A0i*(eye(2)-expm(A0*Dprime*Ts))*b0+-A1i*(eye(2)-expm(A1*D*Ts))*b1)*[Vg;Io];

% Then, construct small-signal model matrices Φ, γ, and δ as per Table 3.1:

Phi = expm(A0*(Ts-td))*expm(A1*D*Ts)*expm(A0*(td-D*Ts))
gamma = expm(A0*(Ts-td))*((A1-A0)*Xdown + (b1-b0)*[Vg;Io])*Ts
delta = c0

% Finally, extract the control-to-output transfer functions Gvu(z) and Giu(z) by converting
% the state-space representation (Φ, γ, δ) into Matlab® transfer function objects.
% First, build a state-space object usingmethod ss and then the transfer function objects
% using tf:

sys_v = ss(Phi,gamma,delta(2,:),0,Ts);
Gvuz = tf(sys_v)

sys_i = ss(Phi,gamma,delta(1,:),0,Ts);
Giuz = tf(sys_i)




% Set the size of the plot window
fig_i = figure;
set(fig_i, 'Position', [100, 100, 1000, 600]); % [left, bottom, width, height]
bode(sys_i)
title('Bode Diagram for the Current');
uiwait(fig_i);
fig_v = figure;
set(fig_v, 'Position', [100, 100, 1000, 600]); % [left, bottom, width, height]
bode(sys_v)
title('Bode Diagram for the Voltage');

%Gvd=(Vg*(1+7.5*10^-6*s))/(30*10^-6*s^2+2.1*10^-5*s+1);