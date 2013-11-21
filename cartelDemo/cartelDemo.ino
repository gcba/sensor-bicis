#include <SPI.h>
#include <Ethernet.h>

int numero=12345;
int valor=0;

byte mac[] =  { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0x8B };
IPAddress ip(192,168,1,96);
EthernetClient client;
byte server[] = { 10,10,10,202}; 
unsigned long lastConnectionTime = 0;
boolean lastConnected = false;
const unsigned long readingInterval =  1000;

void cartel(){
  Serial.end();
  digitalWrite(7,LOW);
  delay(4000);
  Serial.begin(9600); 
  delay(4000);
  if (numero < 10000){
    Serial.println("$10000");
  }else{
    Serial.println("$1000"+ String(numero/10000));
  }
  int segundo= numero % 10000;
  String pre = "";
  if (segundo<10){
    pre = "000";
  }else if (segundo<100){
    pre = "00";
  }else if (segundo<1000){
    pre = "0";
  }
  delay(4000);
  Serial.println("$2" + pre + String(segundo));
}

void barra(){
  Serial.end();
  digitalWrite(7,HIGH);
  delay(500);
  Serial.begin(4800); 
  
  Serial.print("^L^V^9");
  Serial.print("^G");
  int chr=0;
  for(int i=0;i<valor;i++){
    if(chr < 6){
      Serial.print("^7^7");
      chr++;
    }else{
      Serial.print("^G^7^7");
      chr=0;
    }
  }
  Serial.print("^_");
}


void setup() {
  Serial.begin(9600); 
  delay(100);
  digitalWrite(5,LOW);
  delay(100);
  digitalWrite(5,HIGH);
}

void loop() {
  numero++;
  valor++;
  delay(4000);
  cartel();
  barra();
}
