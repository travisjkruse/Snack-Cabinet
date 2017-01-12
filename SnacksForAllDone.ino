volatile long reader1 = 0;
volatile int reader1Count = 0;

void reader1One(void) {
  reader1Count++;
  reader1 = reader1 << 1;
  reader1 |= 1;
}

void reader1Zero(void) {
  reader1Count++;
  reader1 = reader1 << 1;  
}

void setup()
{
  Serial.begin(9600);
  // Attach pin change interrupt service routines from the Wiegand RFID readers
  attachInterrupt(0, reader1Zero, RISING);//DATA0 to pin 2
  attachInterrupt(1, reader1One, RISING); //DATA1 to pin 3
  delay(500);
  // the interrupt in the Atmel processor mises out the first negitave pulse as the inputs are already high,
  // so this gives a pulse to each reader input line to get the interrupts working properly.
  // Then clear out the reader variables.
  // The readers are open collector sitting normally at a one so this is OK
  for(int i = 2; i<4; i++){
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH); // enable internal pull up causing a one
    digitalWrite(i, LOW); // disable internal pull up causing zero and thus an interrupt
    pinMode(i, INPUT);
    digitalWrite(i, HIGH); // enable internal pull up
  }
  delay(500);
  // put the reader input variables to zero
  reader1 = 0;
  reader1Count = 0;
}

void loop() {
  if(reader1Count >=35){
    int s0=(reader1 >> 0) & 0x1;
    int s1=(reader1 >> 1) & 0x1;
    int s2=(reader1 >> 2) & 0x1;
    int s3=(reader1 >> 3) & 0x1;
    int s4=(reader1 >> 4) & 0x1;
    int s5=(reader1 >> 5) & 0x1;
    int s6=(reader1 >> 6) & 0x1;
    int s7=(reader1 >> 7) & 0x1;
    int s8=(reader1 >> 8) & 0x1;
    int s9=(reader1 >> 9) & 0x1;
    int s10=(reader1 >> 10) & 0x1;
    int s11=(reader1 >> 11) & 0x1;
    int s12=(reader1 >> 12) & 0x1;
    int s13=(reader1 >> 13) & 0x1;
    int s14=(reader1 >> 14) & 0x1;
    int s15=(reader1 >> 15) & 0x1;
    int s16=(reader1 >> 16) & 0x1;
    int s17=(reader1 >> 17) & 0x1;
    long serialNum = s0*pow(2,0)+s1*pow(2,1)+s2*pow(2,2)+s3*pow(2,3)+s4*pow(2,4)+s5*pow(2,5)+s6*pow(2,6)+s7*pow(2,7)+s8*pow(2,8)+s9*pow(2,9)+s10*pow(2,10)+s11*pow(2,11)+s12*pow(2,12)+s13*pow(2,13)+s14*pow(2,14)+s15*pow(2,15)+s16*pow(2,16)+s17*pow(2,17);
    Serial.print("Version 7");
    Serial.print("  ");
    Serial.println(serialNum);

    attachInterrupt(0, reader1Zero, RISING);//DATA0 to pin 2
    attachInterrupt(1, reader1One, RISING); //DATA1 to pin 3
    delay(500);
    for(int i = 2; i<4; i++){
      pinMode(i, OUTPUT);
      digitalWrite(i, HIGH); // enable internal pull up causing a one
      digitalWrite(i, LOW); // disable internal pull up causing zero and thus an interrupt
      pinMode(i, INPUT);
      digitalWrite(i, HIGH); // enable internal pull up
    }
    delay(500);

    reader1 = 0;
    reader1Count = 0;
    serialNum = 0;
  }    
}

