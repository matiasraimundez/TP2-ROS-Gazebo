# TP2-ROS-Gazebo

Ejecutar la simulación desde `tb3_empty_world/launch`:

```ros2 launch tb3_simulation_launch.py headless:=False```

Para enviarle comandos al robot los mensajes deben estar estampados.

Para teleoperación por teclado ejecutar:

```ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=True```

Para enviar comandos de velocidad ejecutar:

```
ros2 topic pub --rate 1 /cmd_vel geometry_msgs/msg/TwistStamped "twist: {linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.2}}"
```

Para registrar los datos de una ejecución en `logs/log.txt` ejecutar:

```./dump_odom.py > logs/log.txt```

Luego para obtener gráficos ejecutar el script actualizando el `path` del log:

```python3 script.py```
