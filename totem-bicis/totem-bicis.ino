#include <SPI.h>
#include <Ethernet.h>

char cMil = '0';
char dMil = '0';
char uMil = '0';
char cent = '0';
char dec = '0';
char un = '0';
long valor = 0;

byte mac[] =  { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0x8B };
IPAddress ip(192,168,1,96);
EthernetClient client;
byte server[] = { 192,168,1,124}; 
unsigned long lastConnectionTime = 0;
boolean lastConnected = false;
const unsigned long readingInterval =  10000;
bool lala = false;

void httpRequest(String data) {
  if (client.connect(server, 8080)) {
    client.println("POST /totem HTTP/1.0");
    client.println("Host: 192.168.1.124");
    client.println("User-Agent: arduino-ethernet");
    client.print("Content-Length: ");
    client.println(data.length());
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println();
    client.println(data);
  } 
  else {
    client.stop();
  }
  lastConnectionTime = millis();
}

String time(){
  long ahora = millis();
  int dia = ahora / 86400000 ;
  int hora = (ahora % dia) / 3600000;
  int minutos = ((ahora % dia) % hora) / 60000 ;
  int segundos = (((ahora % dia) % hora) % minutos) / 1000;
  return String(dia) + ":" + String(hora) + ":" + String(minutos) + ":" + String(segundos);
}

void setup() {
  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  delay(1000);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  if (client.available()) {
    dMil = uMil;
    uMil = cent;
    cent = dec;
    dec = un;
    un = char(client.read());
    if (dMil == '#' &&  uMil == '#' && cent == '#' && dec == '#' && un == '#'){
      dMil = client.read();
      uMil = client.read();
      cent = client.read();
      dec = client.read();
      un = client.read();
      cartel(dMil + uMil + cent + dec + un);
    }
  }
  lastConnected = client.connected();
  if (!client.connected() && lastConnected) {
    client.stop();
  }
  if(!client.connected() && (millis() - lastConnectionTime > random(readingInterval/2,readingInterval))) {
    client.stop();
    String reporte="{\"tiempo\":"+String(time())+",\"valor\":"+String(valor)+"}";
    httpRequest(reporte);
  }
  lastConnected = client.connected();
}
