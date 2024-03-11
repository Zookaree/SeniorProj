#include <wiringPi.h> //WIRING PI USES BCM GPIO RPI4 PLACEMENTS
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

#define JOYSTICK_PIN_X 17 //X-axis connected to WPI GPIO 0 (GPIO 17)
#define MOTOR_PWM_PIN 12 //PWM pin connected to motor GPIO 1 (GPIO 18)
#define JOYSTICK_MAX 1023 	//Max JS val
#define JOYSTICK_MIN 0		//Mine JS val
#define PWM_MIN 1100		//Reversal Motor Val
#define PWM_MAX 1900		//Forward Motor Val
#define NEUTRAL_PWM 1500	//Neutral Motor Val

int map(int x, int in_min, int in_max, int out_min, int out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

int main(void)
{
	if (wiringPiSetupGpio() == -1)
	{
		printf("WiringPi Setup Error\n");
		return -1;
	}
	
	pinMode(JOYSTICK_PIN_X, INPUT);
	pinMode(MOTOR_PWM_PIN, PWM_OUTPUT);
	
	int checkVal = 0;
	int pwmVal = 0;
	
	while(1)
	{
		int joystickVal = digitalRead(JOYSTICK_PIN_X);
		if (joystickVal == 1)
		{
			pwmVal = map(joystickVal, 0, 1023, 1500, PWM_MAX);
			checkVal = -1;
		}
		else if (joystickVal == 0 && checkVal == -1)
			pwmVal = map(joystickVal, 0, 1023, 1600, PWM_MAX);

		pwmWrite(MOTOR_PWM_PIN, pwmVal);
		
		printf("Joystick X-axis val: %d, PWM Val: %d\n", joystickVal, pwmVal);
		
		usleep(50000);
	}
	
	return 0;
}
