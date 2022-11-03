int port = 3;
char carc = 't';

int tempo = 2186;

void setup() {
  pinMode(port, OUTPUT);
  Serial.begin(9600);

}

void zeraclock (){
  for (int i =0; i<tempo; i++){
    asm("NOP");
  }
}



bool eop (int a){
  return !(a%2);
}

void loop() {
  int contador = 0;
  int soma =0;
  zeraclock();
  digitalWrite(port, 0);
  zeraclock();
  for ( int i =0 ; i<8;i++){
    digitalWrite(port, carc >> i & 0x01);
    soma += carc>>i & 0x01;
    zeraclock();
  }
  
  digitalWrite(port, eop(soma));
  zeraclock();
  digitalWrite(port, 1);
  delay(1000);



  
}
