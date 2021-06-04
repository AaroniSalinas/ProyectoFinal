#Librerias
import smbus			
from time import sleep          
import RPi.GPIO as GPIO
import subprocess
from smbus import SMBus
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
 
 
#Contadores 
plastico=0
latas=0
total=0



############################ LCD ############################
# Creacion de la interface i2c
i2c = busio.I2C(SCL, SDA)
 
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
 
# Clear display.
disp.fill(0)
disp.show()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
 
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
 
 
# Load default font.
font = ImageFont.load_default()
bus = SMBus(1)


############################ Sensor Ultrasonico ############################
TRIG = 23 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO = 24 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor
GPIO.setmode(GPIO.BCM)     #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
GPIO.setup(TRIG, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO, GPIO.IN)  #Configuramos el pin ECHO como una salida




############################ Sensor Inductivo ############################

# Pin of Input
GPIOpin = -1
pin = 17

# Initial the input pin
def initialInductive(pin):
  global GPIOpin 
  GPIOpin = pin
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOpin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print("Finished Initiation")
  print(GPIOpin)


############################## Servo ############################
servoPIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(5.8) 



############################ Acelerometro ############################
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47







def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
	
	#Iniciar Inductivo
	initialInductive(pin)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()



def Ultrasonico():
	############################ Sensor Ultrasonico ############################	
	# Ponemos en bajo el pin TRIG y después esperamos 0.5 seg para que el transductor se estabilice
	GPIO.output(TRIG, GPIO.LOW)
	time.sleep(0.5)

	#Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIG,GPIO.LOW)

	# En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
	# Debemos detectar dicho evento para iniciar la medición del tiempo

	while True:
		pulso_inicio = time.time()
		if GPIO.input(ECHO) == GPIO.HIGH:
			break

	# El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
	# En ese momento el sensor pondrá el pin ECHO en bajo.
	# Prodedemos a detectar dicho evento para terminar la medición del tiempo
	while True:
		pulso_fin = time.time()
		if GPIO.input(ECHO) == GPIO.LOW:
			break

	# Tiempo medido en segundos
	duracion = pulso_fin - pulso_inicio

	#Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 343m/s
	distancia = (34300 * duracion) / 2
	
	print( "Distancia: %.2f cm" % distancia)
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	draw.text((x, top + 0), "Distancia: " ,font=font, fill=255) 
	draw.text((x, top + 8), "" + str(distancia), font = font, fill = 255) 
	time.sleep(1)
	disp.image(image)
	disp.show()
	
	global total
	#Suma de total de reciclados
	if(distancia <15):
		 total=total+1;
	
	
	return distancia


def Inductivo():	
	induc=-1
	global latas,plastico
	if(GPIOpin != -1):
		state2 = GPIO.input(GPIOpin)
		if state2 == True :
			if Ultrasonico() <15:
				#No dectectado
				p.ChangeDutyCycle(9)#10
				time.sleep(0.05)
				plastico=plastico+1
				print("Botella")
				induc=1
				draw.text((x, top + 16), "Botella " ,font=font, fill=255) 
				time.sleep(1)
				disp.image(image)
				disp.show()
				p.stop()
			else:
				induc=-1
				
		else:
			if Ultrasonico() <15:
				#Dectectado
				p.ChangeDutyCycle(4.5)#2.5
				time.sleep(0.05)
				latas=latas+1
				induc=0
				print("Lata")
				draw.rectangle((0, 0, width, height), outline=0, fill=0)
				draw.text((x, top + 16), "Lata " ,font=font, fill=255)
				time.sleep(1)
				disp.image(image)
				disp.show()
				p.stop()
			else:
				induc=-1
		
	else:
		print("Please Initial Input Ports")

	return induc

def Acelerometro():

	############################ Acelerometro ############################
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)

	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)



	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0	
	print ( "\tGy=%.2f" %Gy, u'\u00b0') 
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	draw.text((x, top + 20), "Gy " + str(Gy) ,font=font, fill=255)
	time.sleep(1)
	disp.image(image)
	disp.show()	
	return Gy

	
	
if __name__ == "__main__":

	# Imprimimos resultadoen lcd y consola
	#print( "Distancia: %.2f cm" % Ultrasonico())
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	draw.text((x, top + 0), "Distancia: " ,font=font, fill=255) 
	draw.text((x, top + 8), "" + str(Ultrasonico()), font = font, fill = 255) 
	time.sleep(1)
	disp.image(image)
	disp.show()

	if Inductivo() == 1:
		#draw.rectangle((0, 0, width, height), outline=0, fill=0)
		draw.text((x, top + 16), "Botella " ,font=font, fill=255) 
		time.sleep(1)
		disp.image(image)
		disp.show()
	else:
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		draw.text((x, top + 16), "Lata " ,font=font, fill=255)
		time.sleep(1)
		disp.image(image)
		disp.show()		

	
	##Display Acelerometro
	#print ( "\tGy=%.2f" %Acelerometro(), u'\u00b0') 
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	draw.text((x, top + 20), "Gy " + str(Acelerometro()) ,font=font, fill=255)
	time.sleep(1)
	disp.image(image)
	disp.show()	

