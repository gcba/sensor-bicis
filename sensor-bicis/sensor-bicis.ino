


void setup() {
  pinMode(A0, INPUT);
  Serial.begin(9600);
  //Serial.println(banner);
}

void loop() {
  if (client.available()) {
    c=l;
    l=e;
    e=a;
    a=r;
    r = client.read();
    if (c == 'c' && l== 'l' && e == 'e' && a == 'a' && r == 'r'){
     the_tally = 0;
     Serial.print("cleared");
    }
  }
  lastConnected = client.connected();
  if (!client.connected() && lastConnected) {
    Serial.println("disconnecting.");
    client.stop();
  }
  if(!client.connected() && (millis() - lastConnectionTime > postingInterval) && the_tally > 0) {
    client.stop();
    String reporte="{\"id\":1,\"tiempo\":"+String(millis())+",\"pasadas\":"+String(the_tally)+"}";
    httpRequest(reporte);
  }
  lastConnected = client.connected();
  
  //1 - TUBE IS PRESSURIZED INITIALLY
  int lectura = analogRead(A0);
  float diferencia = (float)lectura / (float)ma;
  if (diferencia > umb) {
    if (strike_number == 0 && is_measuring == 0) { // FIRST HIT
      Serial.println("");
      Serial.println("Rueda delantera. ");
      first_wheel = millis(); 
      is_measuring = 1;
    }
    else{
      Serial.print(strike_number);
      Serial.print("#");
      Serial.print(is_measuring);
      }
    if (strike_number == 1 && is_measuring == 1) { // SECOND HIT
      Serial.println("Rueda trasera.");
      second_wheel = millis();
      is_measuring = 0;
    }
  }else{
    ma = (ma*4+lectura)/5;
  }
  if (diferencia < umb){
    Serial.print("_");
  }
  else if (diferencia > umb && diferencia < 1.2){
    Serial.print("-");
  }
  else if (diferencia > 1.2){
    Serial.print("'");
  }
  
  
  
  
  

  //2 - TUBE IS STILL PRESSURIZED
  while(analogRead(A0) > the_max && is_measuring == 1) { //is being pressed, in all cases. to measure the max pressure.
    the_max = analogRead(A0);
  }

  //3 - TUBE IS RELEASED
  diferencia = (float)analogRead(A0) / (float)ma ;
  if ( diferencia < umb && count_this == 0) { //released by either wheel
    if (strike_number == 0 && is_measuring == 1 && (millis() - first_wheel > the_wheel_delay)) {
      strike_number = 1;
    }
    if (strike_number == 1 && is_measuring == 0 && (millis() - second_wheel > the_wheel_delay) ) {
      count_this = 1;
    }
  }


  //4 - PRESSURE READING IS ACCEPTED AND RECORDED
  if (diferencia < umb && ((count_this == 1 && is_measuring == 0) || ((millis() - first_wheel) > car_timeout) && is_measuring == 1)) { //has been released for enough time.
    the_tally++; 
    Serial.print("Pico maximo = ");
    Serial.println(the_max);
    Serial.println("Pasaron " + String(the_tally) + " bicicletas");
    //Serial.print("time between wheels = ");
    wheel_time = ((second_wheel - first_wheel)/3600000);
    //Serial.println(wheel_time);
    the_speed = (wheel_spacing/1000)/wheel_time;
    if (the_speed > 0 ) {
      Serial.print("Velocidad: ");
      Serial.print(the_speed);
      Serial.println(" km/h");
    }
    else {
      Serial.println("Error de medicion (o peaton)");
    }

    //RESET ALL VALUES
    the_max = 0; 
    strike_number = 0;
    count_this = 0;
    is_measuring = 0;

  }
}




