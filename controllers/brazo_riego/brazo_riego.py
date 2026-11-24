"""Controlador del UR5e: va al brik, "carga" agua y riega los dos conos de terracota.

Movimiento en espacio articular con interpolación coseno (arranque y parada suaves).
Sin dependencias externas: solo la API `controller` de Webots.
"""
import math

from controller import Robot

JOINTS = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

# Si el brazo gira hacia el lado contrario a los conos, cambia a math.pi.
PAN_OFFSET = 0.0

# Posiciones (x, y) en metros respecto a la base del brazo, igual que en el .wbt
CONOS = {"cono_1": (0.6, 0.2), "cono_2": (0.6, -0.2)}
BRIK = (-0.1, 0.55)

HOME = [0.0, -math.pi / 2, 0.0, -math.pi / 2, 0.0, 0.0]


def pose_sobre(x, y, lift, elbow):
    """Pose con la herramienta apuntando hacia abajo sobre el punto (x, y)."""
    pan = math.atan2(y, x) + PAN_OFFSET
    wrist1 = -math.pi / 2 - (lift + elbow)  # mantiene la herramienta vertical
    return [pan, lift, elbow, wrist1, -math.pi / 2, 0.0]


robot = Robot()
ts = int(robot.getBasicTimeStep())
motors = [robot.getDevice(name) for name in JOINTS]
for m in motors:
    m.setVelocity(m.getMaxVelocity())

current = HOME[:]


def step():
    if robot.step(ts) == -1:
        raise SystemExit


def mover(objetivo, segundos):
    global current
    inicio = current[:]
    n = max(1, int(segundos * 1000 / ts))
    for i in range(1, n + 1):
        s = 0.5 - 0.5 * math.cos(math.pi * i / n)
        for k, m in enumerate(motors):
            m.setPosition(inicio[k] + (objetivo[k] - inicio[k]) * s)
        step()
    current = objetivo[:]


def esperar(segundos):
    for _ in range(int(segundos * 1000 / ts)):
        step()


def regar(segundos):
    """Simula el riego girando la muñeca (como una regadera)."""
    base = current[:]
    for giro in (0.6, -0.6, 0.6, 0.0):
        mover(base[:5] + [giro], segundos / 4)


for m, q in zip(motors, HOME):
    m.setPosition(q)
esperar(1.0)

while True:
    print("→ Brik: cargando agua")
    mover(pose_sobre(*BRIK, lift=-1.45, elbow=1.25), 2.5)
    esperar(1.0)

    for nombre, (x, y) in CONOS.items():
        print(f"→ {nombre}: regando")
        mover(pose_sobre(x, y, lift=-1.4, elbow=1.1), 2.5)   # aproximación por arriba
        mover(pose_sobre(x, y, lift=-1.2, elbow=1.4), 1.2)   # baja sobre el cono
        regar(2.0)
        mover(pose_sobre(x, y, lift=-1.4, elbow=1.1), 1.0)   # sube

    print("→ Casa")
    mover(HOME, 2.5)
    esperar(1.5)
