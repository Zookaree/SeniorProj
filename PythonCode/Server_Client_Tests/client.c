#include <sys/socket.h>
#include <netinet/in.h>
//#include <pigpio.h>
//#include <signal.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <wiringPi.h> 
#include <arpa/inet.h>

//#define UDP_IP "127.0.0.1"
#define UDP_IP "192.168.1.119"
#define UDP_PORT 9931
#define JOYSTICK_PIN_X 17 	//GPIO 17
#define MOTOR_PWM_PIN 12 	//GPIO 12
#define PWM_MIN 1100		//Full Reversal Motor Val
#define PWM_MAX 1900		//Full Forward Motor Val
#define NEUTRAL_PWM 1500	//Neutral Motor Val

//PHY pin 29, 31, 37
#define LED0_GPIO 5
#define LED1_GPIO 6
#define LED2_GPIO 26

int checkVal = 0;
int pwmVal = 0;
int loopVal = 1500;

//Substitute map function from Arduino's map
//Allows in_min to be out_min and in_max to be out_max and in
//between values to be those values
int map(int x, int in_min, int in_max, int out_min, int out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void process_commands(int sock, struct sockaddr_in *server_addr)
{
	char cmd[200]; 		//Command array
	char response[4096];//Response array 
	int status = 0;		
	int recv_len = 0;
	//int slen = sizeof(server_addr);
	int last = 0;
	
	//char *token = 0;	
	char copy[200];		//Copy of Command Array
	char joystickStr[64];
	printf("cmd> ");
	
	while (fgets(cmd, sizeof(cmd), stdin) != NULL)
	{
		//trimming trailing newline
		last = strlen(cmd) - 1;
		if (cmd[last] == '\n')
			cmd[last] = 0;
		strcpy(copy, cmd);
		//token = strtok(cmd, " ");
		if (strcmp(cmd, "exit") == 0)
			break;
		else if (strcmp(cmd, "test") == 0)
		{
			printf("Printing 'test' statement: ");
			status = sendto(sock, cmd, strlen(cmd), 0, //Checks the value of status
				(struct sockaddr *)server_addr, sizeof(*server_addr));
			if (status < 0) //If status is less than one then we've failed the status check
			{
				perror("send to server failed");
				exit(1);
			}
			//This will receive the length of the command from the server talking back to the client
			recv_len = recvfrom(sock, response, sizeof(response), 0, NULL, NULL);
			//if the length was less than 0, then we have a problem
			if (recv_len < 0)
			{
				perror("recv from server failed");
				exit(1);
			}
			
			//null terminate the string
			response[recv_len] = 0;
			printf("%s\n", response);
			
		}
		else if (strcmp(cmd, "run") == 0) //This is our Run Command for WALL-C
		{
			status = sendto(sock, cmd, strlen(cmd), 0,
					(struct sockaddr *)server_addr, sizeof(*server_addr));
			if (status < 0)
			{
				perror("send to server failed");
				exit(1);
			}
			while (1)
			{
				//printf("Printing 'run' statement: ");
				
				recv_len = recvfrom(sock, response, sizeof(response), 0, NULL, NULL);
				
				if (recv_len < 0)
				{
					perror("recv from server failed");
					exit(1);
				}
				//Joystick Code using WiringPi
				int joystickVal = digitalRead(JOYSTICK_PIN_X);
				if (joystickVal == 1)
				{
					if (loopVal > 1500)
						loopVal -= 25;
					checkVal = -1;
				}
				else if (joystickVal == 0 && checkVal == -1)
					loopVal += 25;
				
				pwmVal = map(joystickVal, 0, 1023, loopVal, PWM_MAX);
				
				pwmWrite(MOTOR_PWM_PIN, pwmVal); //PWMWrite is Arduino taken implemented into C
				
				printf("Joystick X-axis val: %d, PWM Val: %d\n", joystickVal, pwmVal);
				
				//null terminate the string
				response[recv_len] = 0;
				//printf("%s\n", response);
				
				sprintf(joystickStr, "%d", pwmVal);
				int sendVar = sendto(sock, joystickStr, sizeof(joystickStr), 
				0, (struct sockaddr*)server_addr, sizeof(*server_addr));
				
				if(sendVar < 0)
				{
					perror("PWMVal sent has failed\n");
					exit(1);
				}
			}
		}
		else
		{
			perror("Invalid Command");
			exit(1);
		}
		printf("cmd> ");
	}
}

int main(int argc, char * argv[])
{
	int gpioResult = 0;
	//create a socket 
	int sockfd;
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	
	//bind to any addr
	struct sockaddr_in myaddr;
	memset((char *)&myaddr, 0, sizeof(myaddr));
	myaddr.sin_family = AF_INET;
	myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	myaddr.sin_port = htons(UDP_PORT); //requests a port
	
	bind(sockfd, (struct sockaddr *)&myaddr, sizeof(myaddr));
	
	// get the server's address
	struct addrinfo hints;
	struct addrinfo *addr;
	
	struct sockaddr_in server_addr;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	
	if (getaddrinfo(UDP_IP, NULL, &hints, &addr) != 0)
		perror("Error getting address info:");
		
	memcpy(&server_addr, addr->ai_addr, addr->ai_addrlen);
	server_addr.sin_port = htons(UDP_PORT);
	
	freeaddrinfo(addr);

	//Checks if WiringPi is set up
	if (wiringPiSetupGpio() == -1)
	{
		printf("WiringPi Setup Error\n");
		return -1;
	}
	
	//Arduino esque things used from WiringPi that sends the mode
	//of the pins assigned (17 and 12 respectively)
	pinMode(JOYSTICK_PIN_X, INPUT);
	//gpioSetMode(JOYSTICK_PIN_X, PI_INPUT);
	pinMode(MOTOR_PWM_PIN, PWM_OUTPUT);
	//gpioSetMode(MOTOR_PWM_PIN, PI_INPUT);
	pinMode(LED0_GPIO, OUTPUT);
	pinMode(LED1_GPIO, OUTPUT);
	pinMode(LED2_GPIO, OUTPUT);
	
	process_commands(sockfd, &server_addr);
	
	close(sockfd);
	
	return 0;
}
