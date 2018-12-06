#define r1 5
#define r2 6
#define r3 7
#define r4 8


void setup() {
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);
  Serial.begin(9600);
}
char read;
void loop() {
  if(Serial.available()){
    read = Serial.read();
    }  
    switch(read){
      case 'l': {
    digitalWrite(r1,0);
    digitalWrite(r2,1);
    digitalWrite(r3,1);
    digitalWrite(r4,0);
        break;
        }
      case 'r': {
    digitalWrite(r1,1);
    digitalWrite(r2,0);
    digitalWrite(r3,0);
    digitalWrite(r4,1);
      break;
      }
      case 'f':{ 
    digitalWrite(r1,1);
    digitalWrite(r2,0);
    digitalWrite(r3,1);
    digitalWrite(r4,0);
        
      break;
      }
      case 'b':{
    digitalWrite(r1,0);
    digitalWrite(r2,1);
    digitalWrite(r3,0);
    digitalWrite(r4,1);

        break;
      }
      case 's':{
    digitalWrite(r1,1);
    digitalWrite(r2,1);
    digitalWrite(r3,1);
    digitalWrite(r4,1);

        break;
      }
    }

}
