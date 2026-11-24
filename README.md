# Brazo robótico de riego (Webots / webots.cloud)

Un UR5e va al brik de 1 L, "carga" agua y riega los dos conos de terracota, en bucle.

```
brazo-webots/
├── Dockerfile                       # imagen de webots.cloud (R2023b)
├── webots.yml                       # publish: true, type: demo
├── worlds/brazo_riego.wbt           # escena: brazo, jardinera, 2 conos, brik
└── controllers/brazo_riego/brazo_riego.py
```

## Probarlo en local
1. Instala Webots R2023b (o posterior): https://cyberbotics.com
2. `File → Open World…` → `worlds/brazo_riego.wbt` → ▶.

## Publicarlo en webots.cloud
1. Sube **esta carpeta como raíz** de un repo público de GitHub (`webots.yml` y `Dockerfile` deben quedar en la raíz).
2. Ve a https://webots.cloud/simulation → **Add a new simulation**.
3. Pega la URL del mundo, con la rama incluida:
   `https://github.com/<usuario>/<repo>/blob/main/worlds/brazo_riego.wbt`
4. Pulsa en la simulación: se levanta un contenedor con GPU y la ves en el navegador.

La pestaña `/server` de webots.cloud solo informa de los servidores de simulación (los que alojan los contenedores). No hace falta tocarla para publicar.

## Ajustes
- Si el brazo gira hacia el lado contrario a los conos, cambia `PAN_OFFSET` a `math.pi` en el controlador.
- Las alturas se ajustan con los parámetros `lift` y `elbow` de cada `pose_sobre(...)`.
