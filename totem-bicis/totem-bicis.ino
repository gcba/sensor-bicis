#include <SPI.h>
#include <Ethernet.h>
#include <avr/wdt.h>

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

byte mac[] =  { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0xe0 };
IPAddress ip(172,29,41,10);
IPAddress gateway(172,29,41,2);
IPAddress mask(255,255,255,0);
EthernetClient client;
byte server[] = { 10,10,10,202}; 
unsigned long lastConnectionTime = 0;
unsigned long lastBarraTime = 0;
unsigned long lastSuccess = 0;
boolean lastConnected = false;
// cada cuanto ir a buscar datos al server
const unsigned long readingInterval =  3000;
// intervalo de update de la barra
const unsigned long barraInterval =  86400000;


void httpRequest() {
  /*wdt_reset();*/
  wdt_disable() ; // los requests tardan mas de 8S por desgracia
  lastConnectionTime = millis();
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
  wdt_reset();
  wdt_enable(WDTO_8S);
}

void cartel(){
  wdt_reset();
  Serial.end();
  digitalWrite(7,LOW);
  delay(1000);
  Serial.begin(9600); 
  delay(4000);
  Serial.print("$1000");
  Serial.println(dMil);
  wdt_reset();
  delay(4000);
  Serial.print("$2");
  Serial.print(uMil);
  Serial.print(cent);
  Serial.print(dec);
  Serial.println(un);
  Serial.flush();
  wdt_reset();
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

void resetear() {
    wdt_enable(WDTO_15MS);  
    for(;;) { };  
}

void setup() {
  wdt_disable();
  // give the ethernet module time to boot up:
  delay(1000);

  /*Serial.println("Acquiring IP address");*/
  /*while(! Ethernet.begin(mac) ) {*/
  /*      Serial.println("Ethernet.begin failed. Retry.");//wait for dhcp*/
  /*   }*/

  Ethernet.begin(mac,ip,gateway,gateway,mask);
  delay(1000);
 
  pinMode(9, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(5, OUTPUT);
  digitalWrite(7,LOW);
  digitalWrite(5,LOW);
  delay(200);
  Serial.begin(9600);
  Serial.flush();
  delay(50);
  digitalWrite(5,HIGH);
  delay(50);
  int i;
  //dot();
  delay(1000);
  Serial.print("$1    $2    ");
  Serial.flush();

  wdt_enable(WDTO_8S);


}

void loop() {
  wdt_reset();
  if (client.available()) {
    dMil = uMil;
    uMil = cent;
    cent = dec;
    dec = un;
    un = char(client.read());
    if (dMil == '#' &&  uMil == '#' && cent == '#' && dec == '#'){
      if (un == '#'){
        dMil = client.read();
        uMil = client.read();
        cent = client.read();
        dec = client.read();
        un = client.read();
        bdec = client.read();
        bun = client.read();
        valor = int(bdec) * 10 + int(bun) - 528;
        if((millis() - lastBarraTime > barraInterval) || lastBarraTime == 0) {
       	  barra();
  	      lastBarraTime=millis();
        };
        if(un1 != un) {
          cartel(); 
          un1 = un;
        }
      }
      if (un == 'R'){
        resetear();
      }
      lastSuccess = millis();
    }
  }
  /*lastConnected = client.connected();*/
  if (!client.connected() && lastConnected) {
    client.stop();
  }
  if(!client.connected() && (millis() - lastConnectionTime > readingInterval)) {
    digitalWrite(9,true);
    
    httpRequest();
    digitalWrite(9,false);
  }
  lastConnected = client.connected();
  if (millis() - lastSuccess > 20000){
    /*resetear();*/
  }

}
