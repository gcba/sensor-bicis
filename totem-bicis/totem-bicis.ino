#include <SPI.h>
#include <Ethernet.h>

char cMil = '0';
char dMil = '0';
char uMil = '0';
char cent = '0';
char dec = '0';
char un = '0';
char un1 = '0';
char bdec = '0';
char bun = '0';
long valor = 0;

byte mac[] =  { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0x8B };
IPAddress ip(172,29,41,10);
IPAddress gateway(172,29,41,2);
EthernetClient client;
byte server[] = { 10,10,10,202}; 
unsigned long lastConnectionTime = 0;
unsigned long lastBarraTime = 0;
boolean lastConnected = false;
// cada cuanto ir a buscar datos al server
const unsigned long readingInterval =  1000;
// intervalo de update de la barra
const unsigned long barraInterval =  86400000;


void httpRequest() {
  if (client.connect(server, 8080)) {
    client.println("GET /totem HTTP/1.0");
    client.println("Host: 10.10.10.202");
    client.println("User-Agent: arduino-ethernet");
    //client.println("Accept: */*");
    client.println("Connection: close");
    client.println();
  } 
  else {
    client.stop();
  }
  lastConnectionTime = millis();
}

void cartel(){
  Serial.end();
  digitalWrite(7,LOW);
  delay(1000);
  Serial.begin(9600); 
  delay(4000);
  Serial.print("$1000");
  Serial.println(dMil);
  delay(4000);
  Serial.print("$2");
  Serial.print(uMil);
  Serial.print(cent);
  Serial.print(dec);
  Serial.println(un);
  Serial.flush();
}
void dot(){
  Serial.end();
  digitalWrite(7,HIGH);
  delay(100);
  Serial.begin(4800); 
  
  Serial.print("^L^V^9");
  Serial.print("^G");
  Serial.print("^1^0");
  Serial.println("^_");
  Serial.flush();
}

void barra(){
  Serial.end();
  digitalWrite(7,HIGH);
  delay(100);
  Serial.begin(4800); 
  
  Serial.print("^L^V^9");
  int chr=0;
  for(int i=0;i<valor;i++){
      if( (i % 6) == 0) 
      	Serial.print("^G");
      Serial.print("^7^7");
  }
  Serial.println("^_");
  Serial.flush();
}

/* por ahora es horrible esto*/
void animation() {
  int valor1 = valor;
  for (int i =0 ; i<2; i++) {
        valor=100;
	barra();
  	delay(500);
    valor=0;
	barra();
  	delay(500);
  };
  valor = valor1;
  barra();
}



void setup() {
  Ethernet.begin(mac,ip,gateway,gateway);
  digitalWrite(7,LOW);
  digitalWrite(5,LOW);
  delay(50);
  digitalWrite(5,HIGH);
  Serial.begin(9600);
  delay(50);
  int i;
  //dot();
  delay(1000);
  Serial.print("$1    $2    ");
  Serial.flush();
/*
  while(true){
  for (i=1; i<101; i++) {
        valor=i;
	barra();
  	delay(500);
  };
  for (; i>1; i--) {
        valor=i;
	barra();
  	delay(500);
  };
 }
*/

  //animation();
  //Serial.println("$10000");
  //Serial.println("$20000");
  //Serial.print("My IP address: ");
  //Serial.println(Ethernet.localIP());
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
      bdec = client.read();
      bun = client.read();
      //Serial.print(dMil);
      //Serial.print(uMil);
      //Serial.print(cent);
      //Serial.print(dec);
      //Serial.println(un);
      valor = int(bdec) * 10 + int(bun) - 528;
      //Serial.println(valor);

      if((millis() - lastBarraTime > barraInterval) || lastBarraTime == 0) {
     	  barra();
	      lastBarraTime=millis();
      };
      if(un1 != un) {
        // animation();
        cartel(); 
        un1 = un;
      }
    }
  }
  lastConnected = client.connected();
  if (!client.connected() && lastConnected) {
    client.stop();
  }
  if(!client.connected() && (millis() - lastConnectionTime > readingInterval)) {
    httpRequest();
  }
  lastConnected = client.connected();
}
