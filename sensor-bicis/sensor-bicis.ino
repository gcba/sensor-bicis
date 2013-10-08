#include <SPI.h>
#include <Ethernet.h>

char c = '*';
char l = '*';
char e = '*';
char a = '*';
char r = '*';

const int DEBUG = 1;

float ma; // moving average contra el que se comparan los picos de presión
const float umb = 1.25;		// cambio de presion respecto al promedio que tomamos como hit
int conteo;		
int latest_minute;
int delayRueda = 50;
int timeout = 2000;
float lectura = 0;
float dEntreEjes = 0.0010668;
long ultimaLectura = 0;
long ahora = 0;


byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0x8B };

IPAddress ip(172, 29, 41, 10);
IPAddress dnsserver(172, 29, 41, 2);
IPAddress gw(172, 29, 41, 2);
EthernetClient client;
byte server[] = { 10, 10, 10, 202 };
//byte server[] = { 172, 29, 41, 12};

unsigned long lastConnectionTime = 0;
boolean lastConnected = false;
const unsigned long postingInterval = 6000;
/*char  banner[] = ""
"   _____  _____          ____\r\n" "  / ____|/ ____|   /\\   |  _ \\   /\\\r\n" " | |  __| |       /  \\  | |_) | /  \\\r\n" " | | |_ | |      / /\\ \\ |  _ < / /\\ \\\r\n" " | |__| | |____ / ____ \\| |_) / ____ \\\r\n" "  \\_____|\\_____/_/   _\\_\\____/_/    \\_\\        ______ _           _         __        _\r\n" "  / ____|     | |   (_)                       |  ____| |         | |       /_/       (_)\r\n" " | |  __  ___ | |__  _  ___ _ __ _ __   ___   | |__  | | ___  ___| |_ _ __ ___  _ __  _  ___ ___\r\n" " | | |_ |/ _ \\| '_ \\| |/ _ \\ '__| '_ \\ / _ \\  |  __| | |/ _ \\/ __| __| '__/ _ \\| '_ \\| |/ __/ _ \\\r\n" " | |__| | (_) | |_) | |  __/ |  | | | | (_) | | |____| |  __/ (__| |_| | | (_) | | | | | (_| (_) |\r\n" "  \\_____|\\___/|_.__/|_|\\___|_|  |_| |_|\\___/  |______|_|\\___|\\___|\\__|_|  \\___/|_| |_|_|\\___\\___/\r\n" "\r\n";
*/
void httpRequest(String data){
  if (client.connect(server, 8080)) {;
  	Serial.println("\nconnecting...");
  	client.println("POST /sensor HTTP/1.0");
  	client.println("Host: 10.10.10.202");
  	client.println("User-Agent: arduino-ethernet");
  	client.print("Content-Length: ");
  	client.println(data.length());
  	client.println("Content-Type: application/json");
  	client.println("Connection: close");
  	client.println();
  	client.println(data);
  }else{
    client.stop();
  }
  lastConnectionTime = millis();
}

void setup(){
  pinMode(A0, INPUT);
  Ethernet.begin(mac, ip, dnsserver, gw);
  Serial.begin(9600);
  delay(1000);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
 
  for (int i = 0; i < 1000; i++) {
    lectura = (float)analogRead(A0);
    ma = ma + lectura;
  }
  ma=ma/1000;
  Serial.print("Promedio inicial: ");
  Serial.println(ma);
}

void loop(){
  if (client.available()) {
  	c = l;
  	l = e;
  	e = a;
  	a = r;
  	r = client.read();
  	if (c == 'c' && l == 'l' && e == 'e' && a == 'a' && r == 'r') {
  	    conteo = 0;
  	  //  Serial.print("cleared");
  	  }
    }
    lastConnected = client.connected();
    if (!client.connected() && lastConnected) {
  	  Serial.println("disconnecting.");
  	  client.stop();
    }
    if (!client.connected()	
    && (millis() - lastConnectionTime > postingInterval) 
    && conteo > 0
    ) {
    	client.stop();
    	String reporte =
    	    "{\"id\":1,\"tiempo\":" + String(millis()) + ",\"pasadas\":" +
    	     String(conteo) + "}";
      httpRequest(reporte);
    }
    lastConnected = client.connected();



//SENSADO
    lectura = (4 * lectura + analogRead(A0)) / 5; // "suavizo" las lecturas de a 5 para eliminar algo de ruido.

    float diferencia = (float) lectura / (float) ma;
    if (diferencia > umb) {
    	ahora = millis();
      if (ahora-ultimaLectura < timeout  &&  ahora-ultimaLectura > delayRueda){
		    conteo++;
        //Serial.print("bici: ");
        //Serial.print(dEntreEjes*3600000/(ahora-ultimaLectura));
        //Serial.println("km/h");
      }
      ultimaLectura = millis();
    }else{
      ma = (ma * 1000 + lectura) / 1001;
    }
    


    Serial.print(lectura);
    Serial.print("\t");
    Serial.print(millis());
    Serial.print("\t");
    Serial.println(diferencia);

/*CODIGO VIEJO
    //1 - TUBE IS PRESSURIZED INITIALLY
    lectura = analogRead(A0);
    float diferencia = (float) lectura / (float) ma;
    if (diferencia > umb) {
	if (DEBUG) {
	    Serial.print("ma: ");
	    Serial.print(ma);
	    Serial.print(" lectura: ");
	    Serial.print(lectura);
	    Serial.print(" diferencia: ");
	    Serial.println(diferencia);
	}
	if (strike_number == 0 && is_measuring == 0) {	// FIRST HIT
	    Serial.println("");
	    Serial.println("Rueda delantera. ");
	    first_wheel = millis();
	    is_measuring = 1;
	}
	if (strike_number == 1 && is_measuring == 1) {	// SECOND HIT
	    Serial.println("Rueda trasera.");
	    second_wheel = millis();
	    is_measuring = 0;
	}
    }else{
	ma = (ma * 30 + lectura) / 31;
    }
	//2 - TUBE IS STILL PRESSURIZED
	while (analogRead(A0) > the_max && is_measuring == 1) {	//is being pressed, in all cases. to measure the max pressure.
	the_max = analogRead(A0);
    }

    //3 - TUBE IS RELEASED
    diferencia = (float) analogRead(A0) / (float) ma;
    if (diferencia < umb && count_this == 0) {	//released by either wheel
	if (strike_number == 0 && is_measuring == 1
	    && (millis() - first_wheel > the_wheel_delay)) {
	    strike_number = 1;
	}
	if (strike_number == 1 && is_measuring == 0
	    && (millis() - second_wheel > the_wheel_delay)) {
	    count_this = 1;
	}
    }

    //4 - PRESSURE READING IS ACCEPTED AND RECORDED
    if (diferencia < umb && ((count_this == 1 && is_measuring == 0)
			     || ((millis() - first_wheel) > car_timeout) && is_measuring == 1)) {	//has been released for enough time.
	conteo++;
	Serial.print("Pico maximo = ");
	Serial.println(the_max);
	Serial.println("Pasaron " + String(conteo) + " bicicletas");
	//Serial.print("time between wheels = ");
	wheel_time = ((second_wheel - first_wheel) / 3600000);
	//Serial.println(wheel_time);
	the_speed = (wheel_spacing / 1000) / wheel_time;
	if (the_speed > 0) {
	    Serial.print("Velocidad: ");
	    Serial.print(the_speed);
	    Serial.println(" km/h");
	}else{
	    Serial.println("Error de medicion (o peaton)");
	}

	//RESET ALL VALUES
	the_max = 0;
	strike_number = 0;
	count_this = 0;
	is_measuring = 0;

    }*/
}
