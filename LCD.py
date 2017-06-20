import time
import RPi.GPIO as GPIO

class LCD:
    def __init__(self,ENTER=14,RS=15,D0=26,D1=19,D2=13,D3=6,D4=5,D5=11,D6=9,D7=10):
        #used to send data to LCD screen
        self.ENTER = ENTER
        #used to tell the LCD if it's a command or a character
        self.RS = RS
        #data lines
        self.D0 = D0
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.D4 = D4
        self.D5 = D5
        self.D6 = D6
        self.D7 = D7
        self.ALL = [self.D0,self.D1,self.D2,self.D3,self.D4,self.D5,self.D6,self.D7]

        #move to front of first row
        self.FR = self.D7
        #move to front of second row
        self.SR = [self.D7,self.D6]
        #move cursor right once
        self.MR = [self.D4,self.D2]

        self.character = {
            "0":[self.D5,self.D4],
            "@":[self.D6],
            "P":[self.D6,self.D4],
            "`":[self.D6,self.D5],
            " ":[self.D7,self.D5],
            "p":[self.D6,self.D5,self.D4],
            "!":[self.D5,self.D0],
            "1":[self.D5,self.D4,self.D0],
            "A":[self.D6,self.D0],
            "Q":[self.D6,self.D4,self.D0],
            "a":[self.D6,self.D5,self.D0],
            "q":[self.D6,self.D5,self.D4,self.D0],
            "\"":[self.D5,self.D1],
            "2":[self.D5,self.D4,self.D1],
            "B":[self.D6,self.D1],
            "R":[self.D6,self.D4,self.D1],
            "b":[self.D6,self.D5,self.D1],
            "r":[self.D6,self.D5,self.D4,self.D1],
            "#":[self.D5,self.D1,self.D0],
            "3":[self.D5,self.D4,self.D1,self.D0],
            "C":[self.D6,self.D1,self.D0],
            "S":[self.D6,self.D4,self.D1,self.D0],
            "c":[self.D6,self.D5,self.D1,self.D0],
            "s":[self.D6,self.D5,self.D4,self.D1,self.D0],
            "$":[self.D5,self.D2],
            "4":[self.D5,self.D4,self.D2],
            "D":[self.D6,self.D2],
            "T":[self.D6,self.D4,self.D2],
            "d":[self.D6,self.D5,self.D2],
            "t":[self.D6,self.D5,self.D4,self.D2],
            "%":[self.D5,self.D2,self.D0],
            "5":[self.D5,self.D4,self.D2,self.D0],
            "E":[self.D6,self.D2,self.D0],
            "U":[self.D6,self.D4,self.D2,self.D0],
            "e":[self.D6,self.D5,self.D2,self.D0],
            "u":[self.D6,self.D5,self.D4,self.D2,self.D0],
            "&":[self.D5,self.D2,self.D1],
            "6":[self.D5,self.D4,self.D2,self.D1],
            "F":[self.D6,self.D2,self.D1],
            "V":[self.D6,self.D4,self.D2,self.D1],
            "f":[self.D6,self.D5,self.D2,self.D1],
            "v":[self.D6,self.D5,self.D4,self.D2,self.D1],
            "'":[self.D5,self.D2,self.D1,self.D0],
            "7":[self.D5,self.D4,self.D2,self.D1,self.D0],
            "G":[self.D6,self.D2,self.D1,self.D0],
            "W":[self.D6,self.D4,self.D2,self.D1,self.D0],
            "g":[self.D6,self.D5,self.D2,self.D1,self.D0],
            "w":[self.D6,self.D5,self.D4,self.D2,self.D1,self.D0],
            "(":[self.D5,self.D3],
            "8":[self.D5,self.D4,self.D3],
            "H":[self.D6,self.D3],
            "X":[self.D6,self.D4,self.D3],
            "h":[self.D6,self.D5,self.D3],
            "x":[self.D6,self.D5,self.D4,self.D3],
            ")":[self.D5,self.D3,self.D0],
            "9":[self.D5,self.D4,self.D3,self.D0],
            "I":[self.D6,self.D3,self.D0],
            "Y":[self.D6,self.D4,self.D3,self.D0],
            "i":[self.D6,self.D5,self.D3,self.D0],
            "y":[self.D6,self.D5,self.D4,self.D3,self.D0],
            "*":[self.D5,self.D3,self.D1],
            ":":[self.D5,self.D4,self.D3,self.D1],
            "J":[self.D6,self.D3,self.D1],
            "Z":[self.D6,self.D4,self.D3,self.D1],
            "j":[self.D6,self.D5,self.D3,self.D1],
            "z":[self.D6,self.D5,self.D4,self.D3,self.D1],
            "+":[self.D5,self.D3,self.D1,self.D0],
            ";":[self.D5,self.D4,self.D3,self.D1,self.D0],
            "K":[self.D6,self.D3,self.D1,self.D0],
            "[":[self.D6,self.D4,self.D3,self.D1,self.D0],
            "k":[self.D6,self.D5,self.D3,self.D1,self.D0],
            "{":[self.D6,self.D5,self.D4,self.D3,self.D1,self.D0],
            ",":[self.D5,self.D3,self.D2],
            "<":[self.D5,self.D4,self.D3,self.D2],
            "L":[self.D6,self.D3,self.D2],
            "l":[self.D6,self.D5,self.D3,self.D2],
            "|":[self.D6,self.D5,self.D4,self.D3,self.D2],
            "-":[self.D5,self.D3,self.D2,self.D0],
            "=":[self.D5,self.D4,self.D3,self.D2,self.D0],
            "M":[self.D6,self.D3,self.D2,self.D0],
            "]":[self.D6,self.D4,self.D3,self.D2,self.D0],
            "m":[self.D6,self.D5,self.D3,self.D2,self.D0],
            "}":[self.D6,self.D5,self.D4,self.D3,self.D2,self.D0],
            ".":[self.D5,self.D3,self.D2,self.D1],
            ">":[self.D5,self.D4,self.D3,self.D2,self.D1],
            "N":[self.D6,self.D3,self.D2,self.D1],
            "^":[self.D6,self.D4,self.D3,self.D2,self.D1],
            "n":[self.D6,self.D5,self.D3,self.D2,self.D1],
            "/":[self.D5,self.D3,self.D2,self.D1,self.D0],
            "?":[self.D5,self.D4,self.D3,self.D2,self.D1,self.D0],
            "O":[self.D6,self.D3,self.D2,self.D1,self.D0],
            "_":[self.D6,self.D4,self.D3,self.D2,self.D1,self.D0],
            "o":[self.D6,self.D5,self.D3,self.D2,self.D1,self.D0]
        }

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.ENTER,self.RS,self.D0,self.D1,self.D2,self.D3,self.D4,self.D5,self.D6,self.D7],GPIO.OUT)

    def __del__(self):
        try:
            GPIO.cleanup();
        except:
            None

    def __str__(self):
        return "ENTER: {}\nRS: {}\nD0: {}\nD1: {}\nD2: {}\nD3: {}\nD4: {}\nD5: {}\nD6: {}\nD7: {}".format(self.ENTER,self.RS,self.D0,self.D1,self.D2,self.D3,self.D4,self.D5,self.D6,self.D7)

    def __repr__(self):
        return "ENTER: {}\nRS: {}\nD0: {}\nD1: {}\nD2: {}\nD3: {}\nD4: {}\nD5: {}\nD6: {}\nD7: {}".format(self.ENTER,self.RS,self.D0,self.D1,self.D2,self.D3,self.D4,self.D5,self.D6,self.D7)

    def enter(self):
        GPIO.output(self.ENTER,GPIO.HIGH)
        GPIO.output(self.ENTER,GPIO.LOW)

    def send(self,registers):
        GPIO.output(registers,GPIO.HIGH)
        self.enter()
        GPIO.output(registers,GPIO.LOW)
        time.sleep(0.01)

    def initLCD(self,cursor=True):
        if cursor:
            GPIO.output(self.D3,GPIO.HIGH)
            #turn on LCD display
            GPIO.output(self.D2,GPIO.HIGH)
            #turn on cursor
            GPIO.output(self.D1,GPIO.HIGH)
            #turn on cursor blink
            GPIO.output(self.D0,GPIO.HIGH)
        else:
            GPIO.output(self.D3,GPIO.HIGH)
            #turn on LCD display
            GPIO.output(self.D2,GPIO.HIGH)
        self.enter()
        GPIO.output(self.ALL,GPIO.LOW)
        GPIO.output(self.D5,GPIO.HIGH)
        #set to 8-bit mode
        GPIO.output(self.D4,GPIO.HIGH)
        #set to 2 line mode
        GPIO.output(self.D3,GPIO.HIGH)
        self.enter()
        GPIO.output(self.ALL,GPIO.LOW)

    def printLCD(self,text,pos=(0,0),reset=True):
        if len(text) > 32 or len(text) == 0:
            print("use a message of length 1-32")
        else:
            if reset:
                #reset screen
                self.send(self.D0)
            else:
                #reset cursor
                self.send(self.FR)
            linePos = 0
            #if its moving to the second line
            if pos[0] == 1:
                self.send(self.SR)
            #if a custom starting place is set
            for i in range(0,pos[1]):
                self.send(self.MR)
            GPIO.output(self.RS,GPIO.HIGH)
            for i in text:
                linePos += 1
                if i in self.character:
                    self.send(self.character[i])
                else:
                    if i !='\n':
                        print("Character \"{}\" isn't supported by the LCD screen.".format(i))
                if linePos == 16 or i == '\n':
                    GPIO.output(self.RS,GPIO.LOW)
                    #set cursor to start of second line
                    self.send(self.SR)
                    GPIO.output(self.RS,GPIO.HIGH)
            GPIO.output(self.RS,GPIO.LOW)
