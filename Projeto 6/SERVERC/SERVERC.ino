int port = 3;
int tempomeio = 2186*0.5;
int tempo = 2186;


void setup() {

  pinMode(port, INPUT);
  Serial.begin(9600);
}

void zerameio(){
  for (int i =0; i<tempomeio; i++){
    asm("NOP");

  }
}

void zeratudo(){
  for (int i =0; i<tempo; i++){
    asm("NOP");
  }
}




void loop() {
  

  while (digitalRead(port)==1){
    
  }
  
  byte valor = 0x00;
  zeratudo();
  zerameio();

  for (int i=0;i<8;i++){
       valor|= digitalRead(port)<<i;
       zeratudo();
  }
  zeratudo();
  digitalRead(port);
  zeratudo();
  digitalRead(port);
  char c = valor;
  Serial.println(c);

}
//97
//1100001
