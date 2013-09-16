#include <SPI.h>
#include <Ethernet.h>

char c = '*';
char l = '*';
char e = '*';
char a = '*';
char r = '*';

const float umb =  1.1; // tolerancia del cambio de presion de 10 %
int ma;
int the_tally; //total amount of sensings.
int latest_minute;
int the_wheel_delay = 50; //number of milliseconds to create accurate readings for cars. prevents bounce.
int car_timeout = 3000;
int the_max = 0;
int is_measuring = 0;
int count_this = 0;
int strike_number = 0;
float wheel_spacing = 1.0668;
float first_wheel = 0.0000000;
float second_wheel= 0.0000000;
float wheel_time = 0.0000000;
float the_speed = 0.0000000;


byte mac[] =  { 0x90, 0xA2, 0xDA, 0x0D, 0x4E, 0x8B };
IPAddress ip(172,29,41,9);
IPAddress dnsserver(172,29,41,2);
IPAddress gw(172,29,41,2);
EthernetClient client;
byte server[] = { 10,10,10,202}; 
unsigned long lastConnectionTime = 0;
boolean lastConnected = false;
const unsigned long postingInterval =  6000;
/*char  banner[] = ""
"   _____  _____          ____\r\n" "  / ____|/ ____|   /\\   |  _ \\   /\\\r\n" " | |  __| |       /  \\  | |_) | /  \\\r\n" " | | |_ | |      / /\\ \\ |  _ < / /\\ \\\r\n" " | |__| | |____ / ____ \\| |_) / ____ \\\r\n" "  \\_____|\\_____/_/   _\\_\\____/_/    \\_\\        ______ _           _         __        _\r\n" "  / ____|     | |   (_)                       |  ____| |         | |       /_/       (_)\r\n" " | |  __  ___ | |__  _  ___ _ __ _ __   ___   | |__  | | ___  ___| |_ _ __ ___  _ __  _  ___ ___\r\n" " | | |_ |/ _ \\| '_ \\| |/ _ \\ '__| '_ \\ / _ \\  |  __| | |/ _ \\/ __| __| '__/ _ \\| '_ \\| |/ __/ _ \\\r\n" " | |__| | (_) | |_) | |  __/ |  | | | | (_) | | |____| |  __/ (__| |_| | | (_) | | | | | (_| (_) |\r\n" "  \\_____|\\___/|_.__/|_|\\___|_|  |_| |_|\\___/  |______|_|\\___|\\___|\\__|_|  \\___/|_| |_|_|\\___\\___/\r\n" "\r\n";
*/
void httpRequest(String data) {
  if (client.connect(server, 5001)) {;
    Serial.println("\nconnecting...");
    client.println("POST /sensor HTTP/1.0");
    client.println("Host: 10.0.0.1");
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

void setup() {
  pinMode(A0, INPUT);
  ma = analogRead(A0);
  Ethernet.begin(mac, ip,dnsserver,gw);
  Serial.begin(9600);
  delay(1000);
  //Serial.println(banner);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  Serial.print("Promedio inicial: ");
  Serial.println(ma);
}

void loop() {
	Serial.print(millis());
	Serial.print("\t");
	Serial.println(analogRead(A0));
}




