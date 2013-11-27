import time
#import wiringpi
#import RPi.GPIO as GPIO
#GPIO driver for Raspberry PI
 
class Printer:
    #drivers should work untill 400kHz
    #period is 1.0/400000.0
    #high duration = 1.0/800000.0
    #low duration  = 1.0/800000.0 = 0.00000125
    #MAXDELAY = 0.0005
    MAXDELAY = 500 #cycles in wait loop (BUSY WAIT)
    # 400 khz max MINDELAY = 0.00000125
    #MINDELAY = 0.000002
    MINDELAY = 1 #cycles in wait loop (BUSY WAIT)
    delays = []
    
    EASE_SIZE = 20 #equals 20 mm canvas space
    # tested to work MINDELAY = 0.0001

    
    def calculateDelays(self):
        for i in range(self.EASE_SIZE):
            delay = self.MAXDELAY*( 1 - (float(i)/float(self.EASE_SIZE))) + self.MINDELAY;
            self.delays.append(int(delay))
        self.delays.append(1)
        
        print 'delays',self.delays  
    
    def __init__(self,file_base_name):
    
        self.RAW_OUTPUT = open('layer0.dat', 'w')
        self.layercounter = 0
        L_clk = 5   #header pin 5 
        L_dir = 3   #header pin 3 
        R_dir = 7   #header pin 7
        R_clk  = 8   #header pin 8
        Solenoid = 10  #header pin 10
        self.leftChannel = [L_clk, L_dir]
        self.rightChannel = [R_clk,R_dir]
        self.printerHead = [Solenoid]
        self.lastdirs =[0,0]
        
        """
        wiringpi.wiringPiSetup()
        
        wiringpi.pinMode(L_clk,1)
        wiringpi.pinMode(L_dir,1)
        wiringpi.pinMode(R_clk,1)
        wiringpi.pinMode(R_dir,1)
        wiringpi.pinMode(Solenoid,1)
        """
        """
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(L_clk,GPIO.OUT)
        GPIO.setup(L_dir,GPIO.OUT)
        GPIO.setup(R_dir,GPIO.OUT)
        GPIO.setup(R_clk,GPIO.OUT)
        GPIO.setup(Solenoid,GPIO.OUT)
        """
        self.calculateDelays()
        
    def saveLayer(self):
        self.finalize();
        self.layercounter +=1
        self.RAW_OUTPUT = open('layer'+str(self.layercounter)+'.dat', 'w')
        

        
    def printBatch(self, cmds, currentIndex, totalLength):
        #if(float(currentIndex)/float(totalLength)) > 0.5: 
        if((totalLength - currentIndex) < currentIndex):
            delta = totalLength - currentIndex
        else:
            delta = currentIndex
        # currentIndex is which mm in a total line of length totalLength
        # cmds is all python generated from json stepping instructions to move a single mm on canvas
        
        # for long sweeps between layers speed remains low there is only one instruction currentindex = 0 for the whole sweep
        # create exception putting delta over ease size to max transport speed long generated sweep have manu more cmds than STEP_PER_MM value
        # 12.5 mm linespacing * 42.55 steps per mm is cmds generated btween lines these should be low speed to its the treshold to go fast or not
        #print 'len(cmds)',len(cmds)
        """
        if len(cmds)>4400: #14*43 tunred out to be to low
            delta = self.EASE_SIZE + 1
        
        
        for cmd in cmds:
            #self.executeInstruction(cmd, delta)
            self.logCmdsToFile(cmd, delta)
        """
        gencmds = len(cmds)
        CMDCOUNT=0
        if gencmds > 1000: #14*43 tunred out to be to low
            #all generated transison steps
            for cmd in cmds:
                if((gencmds - CMDCOUNT) < CMDCOUNT):
                    delta = int((gencmds - CMDCOUNT)/43.0)
                else:
                    delta = int(CMDCOUNT/43.0)
                CMDCOUNT = CMDCOUNT + 1
                #delta = self.EASE_SIZE + 1
                self.logCmdsToFile(cmd, delta)
        else:
            for cmd in cmds:
                self.logCmdsToFile(cmd, delta)  
    
    def logCmdsToFile(self,cmd,delta):
        self.RAW_OUTPUT.write(str(cmd[0])+','+str(cmd[1])+','+str(cmd[2])+','+str(delta)+'\n')
        
    def finalize(self):
        self.RAW_OUTPUT.close() 
    
    def executeInstruction(self, cmd, delta):
        self.stepEngine(0, cmd[0], delta) #left engine
        self.stepEngine(1, cmd[1], delta) #right engine
        self.driveSolenoid(cmd[2]) #penhead
    
    def wait(self,count):
        while count:
            count = count -1
        
    def stepEngine(self, engine, cmd, delta):
        if(cmd==0):
            return
        # rudimentary easing motor speeds 
        if delta > self.EASE_SIZE:
            #20 mm traveled go max speed
            delay = self.MINDELAY
        else:
            #transistion from MAXDELAY to MINDELAY based on the calculated delta value
            #delay = self.MAXDELAY*( 1 - (float(delta)/float(self.EASE_SIZE))) + self.MINDELAY;
            delay = self.delays[delta]
            #delay = self.MINDELAY  
        #print 'delay: ', delay  
        
        if(engine==1):
            channel  = self.leftChannel
            cmd = -1*cmd
        else:
            channel  = self.rightChannel
            #cmd = -1*cmd
        #direction toggle   
        #print 'writing digitalpin'
        if cmd!=self.lastdirs[engine]:
            if cmd<0 :
                pass
                #wiringpi.digitalWrite(channel[1],0)
                #GPIO.output(channel[1],False)
            else:
                pass
                #wiringpi.digitalWrite(channel[1],1)
                #GPIO.output(channel[1],True)
        #print 'digitalwrite done'
        self.lastdirs[engine]=cmd
        #stepclockpulse one HIGH, followed by a LOW 
        #wiringpi.digitalWrite(channel[0],1)
        #GPIO.output(channel[0],True)
        #time.sleep(delay)
        #if engine==0:
        #   print 'engine: ',engine,'delay: ',delay,'delta',delta
        self.wait(delay)
        #wiringpi.digitalWrite(channel[0],0)
        #GPIO.output(channel[0],False)
        #time.sleep(delay)
        self.wait(delay)
        
    def driveSolenoid(self,cmd):
        if cmd==0:
            return
        if(cmd<0):
            pass
            #pen up, solenoid should be switched on in our design
            #wiringpi.digitalWrite(self.printerHead[0],1)
            #GPIO.output(self.printerHead[0],True)
        else:
            pass
            #pen down
            #wiringpi.digitalWrite(self.printerHead[0],0)
            #GPIO.output(self.printerHead[0],False)