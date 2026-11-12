import csv
import matplotlib.pyplot as plt

path = 'log_ej4.txt'

with open(path, newline='') as log:
    log_reader = csv.reader(log, delimiter='\t')
    
    time = []
    pos_x = []
    pos_y = []
    orien = []
    vel_l = []
    vel_a = []
    for row in log_reader:
        x, y, yaw, v, e = [float(f) for f in row[1:6]]
        sec = int(row[0][32:42])
        nanos = int(row[0][52:-1])
        t = sec + 10**-9 * nanos
        time.append(t)
        pos_x.append(x)
        pos_y.append(y)
        orien.append(yaw)
        vel_l.append(v)
        vel_a.append(e)

    time0 = [t - time[0] for t in time]

    plt.figure(figsize=(8, 8))
    plt.plot(pos_x, pos_y, label='Recorrido', linewidth=1)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Camino del robot')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.savefig('ej5/a-camino.png', dpi=150, bbox_inches='tight')

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(4, 10))
    plt.subplots_adjust(hspace=0.3)

    ax1.plot(time0, pos_x, label='x', linewidth=1)
    ax1.set_xlabel('t [s]')
    ax1.set_ylabel('x [m]')
    ax1.set_title('Coord. x respecto al tiempo')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(time0, pos_y, label='y', linewidth=1)
    ax2.set_xlabel('t [s]')
    ax2.set_ylabel('y [m]')
    ax2.set_title('Coord. y respecto al tiempo')
    ax2.legend()
    ax2.grid(True)

    ax3.plot(time0, orien, label='Orientación', linewidth=1)
    ax3.set_xlabel('t [s]')
    ax3.set_ylabel('yaw [rad]')
    ax3.set_title('Orientación respecto al tiempo')
    ax3.legend()
    ax3.grid(True)

    fig.savefig('ej5/b-trayectoria.png', dpi=150, bbox_inches='tight')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 8))
    plt.subplots_adjust(hspace=0.3)

    ax1.plot(time0, vel_l, label='v', linewidth=1)
    ax1.set_xlabel('t [s]')
    ax1.set_ylabel('v [m/s]')
    ax1.set_title('Velocidad lineal respecto al tiempo')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(time0, vel_a, label='w', linewidth=1)
    ax2.set_xlabel('t [s]')
    ax2.set_ylabel('w [rad/s]')
    ax2.set_title('Velocidad angular respecto al tiempo')
    ax2.legend()
    ax2.grid(True)

    fig.savefig('ej5/c-velocidad.png', dpi=150, bbox_inches='tight')