#include <wiringPi.h> //WIRING PI USES BCM GPIO RPI4 PLACEMENTS
#include <stdio.h>
#include <stdint.h>

#define JOYSTICK_PIN_X 0 //X-axis connected to WPI GPIO 0 (GPIO 17)
#define MOTOR_PWM_PIN 1 //PWM pin connected to motor GPIO 1 (GPIO 18)
#define JOYSTICK_MAX 1023 	//Max JS val
#define JOYSTICK_MIN 0		//Mine JS val
#define PWM_MIN 1100		//Reversal Motor Val
#define PWM_MAX 1900		//Forward Motor Val
#define NEUTRAL_PWM 1500	//Neutral Motor Val

int wiringPiSetup(void);

int main(int argc, char * argv[])
{
	if (wiringPiSetup() == -1)
	{
		printf("WiringPi Setup Error\n");
		return -1;
	}
	
	pinMode(MOTOR_PWM_PIN, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);//Set PWM Mode to Mark Space mode
	pwmSetRange(20000);		//Set PWM ranfe to 20 ms (might need to turn this down)
	pwmSetClock(192); 		//Set PWM clock to 50Hz
	
	int joystickVal = 0;
	
	while (1)
	{
		joystickVal = analogRead(JOYSTICK_PIN_X);
		//mapping JS val to PWM
		int pwmVal = map(joystickVal, JOYSTICK_MIN, JOYSTICK_MAX, PWM_MIN, PWM_MAX);
		
		//output PWM to control the motor
		pwmWrite(MOTOR_PWM_PIN, pwmVal);
		
		printf("Joystick X-axis val: %d, PWM Val: %d\n", joystickVal, pwmVal);
		
		delay(50);
	}
	
	return 0;
}
