# ProyectoFinal

### Sistema de Reciclaje
Se realizó la maqueta de un sistema de reciclaje haciendo distinsión entre botellas de plástico y latas de aluminio.

### Sistema de monitoreo 
Se tiene un sistema de monitoreo para el sistema de reciclaje (botellas-latas). Se usa Raspberry como la computadora del sistema y cuenta con las siguientes características:
1. Lectura de 3 variables físicas diferentes: 
  - Ultrasónico: Comunicación UART (Detecta cualquier elemento que pase por la barrera).
  - Acelerómetro: Comunicación I2C (Detecta movimientos en el servomotor que toma diferentes sentidos dependiendo el material).
  - Inductivo: Comunicación I2C (Detecta si el material es un metal).
2. La lectura de cada sensor debe de aparecer en la matriz de LEDS o en la pantalla OLED.
3. Se incluye una interfaz gráfica para la selección del sensor, la cual se activa al hacer clic en el botón correspondiente. La interfaz gráfica permite de monitorear la medición de cada sensor y lo despliega en una tabla, incluyendo el día y la hora de la medición.
4. Todos los valores son publicados en una aplicación dentro de WIA (wia.io) y se actualizan cada 10 segundos en algún elemento gráfico.
