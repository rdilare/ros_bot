// connect motor controller pins to Arduino digital pins
// motor one
int enA = 10;
int in1 = 9;
int in2 = 8;
// motor two
int in3 = 7;
int in4 = 6;
int enB = 5;

String readString;
int ind1, ind2;
int vA = 0, vB = 0;

void setup()
{
  // set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Serial.begin(115200);

//  Serial.println("ok");
}


void loop()
{
  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == ';') {

      ind1 = readString.indexOf(',');
      vA = (readString.substring(0, ind1)).toInt();
      ind2 = readString.indexOf(',', ind1 + 1);
      vB = (readString.substring(ind1 + 1, ind2)).toInt();


//      Serial.print("From Arduino:");
//      Serial.println(vA);
//      Serial.println(vB);
//      Serial.println("-----------");
      
      drive_motor(vA, vB);
//      Serial.println("ok");
      readString = ""; //clears variable for new input

    }
    else {
      readString += c; //makes the string readString
    }
  }


  //  for (int i = 0; i <= 255 ; i++) {
  //    drive_motor(0, -i);
  //    delay(10);
  //  }
}



void drive_motor(int vA, int vB) {
  char dirA = vA < 0 ? 'B' : 'F';
  char dirB = vB < 0 ? 'B' : 'F';


  if (dirA == 'B') {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  } else if (dirB == 'F') {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  analogWrite(enA, abs(vA));


  if (dirB == 'B') {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } else if (dirB == 'F') {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  analogWrite(enB, abs(vB));

}
