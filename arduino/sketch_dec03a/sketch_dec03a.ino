void setup() {
  pinMode(4, OUTPUT);
  tone(4, 523);
  delay(100);
  tone(4, 659);
  delay(100);
  tone(4, 784);
  delay(100);
  tone(4, 659);
  delay(100);
  tone(4, 523);
  delay(100);
  tone(4, 0, 1);

  delay(1000);
  for(int i=0; i<10; i++){
    tone(4, 3135, 200);
    delay(300);
  }
  for(int i=3135+10; i>0; i-=10){
    tone(4, i);
    delay(1);
  }
  tone(4, 0, 1);
  delay(1000);
}

void loop() {  
}
