#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <wiringPi.h> 

#define UDP_IP "127.0.0.1"
#define UDP_PORT 2345

#define JOYSTICK_PIN_X 17 	//GPIO 17
#define MOTOR_PWM_PIN 12 	//GPIO 12
#define PWM_MIN 1100		//Reversal Motor Val
#define PWM_MAX 1900		//Forward Motor Val
#define NEUTRAL_PWM 1500	//Neutral Motor Val

int checkVal = 0;
int pwmVal = 0;

//Substitute map function from Arduino's map
//Allows in_min to be out_min and in_max to be out_max and in
//between values to be those values
int map(int x, int in_min, int in_max, int out_min, int out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void process_commands(int sock, struct sockaddr_in *server_addr)
{
	char cmd[200];
	char response[4096];
	int status = 0;
	int recv_len = 0;
	int last = 0;
	char *token = 0;
	char copy[200];
	printf("cmd> ");
	
	while (fgets(cmd, sizeof(cmd), stdin) != NULL)
	{
		//trimming trailing newline
		last = strlen(cmd) - 1;
		if (cmd[last] == '\n')
			cmd[last] = 0;
		strcpy(copy, cmd);
		token = strtok(cmd, " ");
		if (strcmp(cmd, "exit") == 0)
			break;
		else if (strcmp(cmd, "test") == 0)
		{
			printf("Printing 'test' statement: ");
			status = sendto(sock, cmd, strlen(cmd), 0,
				(struct sockaddr *)server_addr, sizeof(*server_addr));
			if (status < 0)
			{
				perror("send to server failed");
				exit(1);
			}
			
			recv_len = recvfrom(sock, response, sizeof(response), 0, NULL, NULL);
			
			if (recv_len < 0)
			{
				perror("recv from server failed");
				exit(1);
			}
			
			//null terminate the string
			response[recv_len] = 0;
			printf("%s\n", response);
			
		}
		else if (strcmp(cmd, "run") == 0)
		{
			while (1)
			{
				printf("Printing 'run' statement: ");
				status = sendto(sock, cmd, strlen(cmd), 0,
					(struct sockaddr *)server_addr, sizeof(*server_addr));
				if (status < 0)
				{
					perror("send to server failed");
					exit(1);
				}
				
				recv_len = recvfrom(sock, response, sizeof(response), 0, NULL, NULL);
				
				if (recv_len < 0)
				{
					perror("recv from server failed");
					exit(1);
				}
				
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
				
				//null terminate the string
				response[recv_len] = 0;
				printf("%s\n", response);
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
	
	pinMode(JOYSTICK_PIN_X, INPUT);
	pinMode(MOTOR_PWM_PIN, PWM_OUTPUT);
	
	process_commands(sockfd, &server_addr);
	
	close(sockfd);
	
	return 0;
}
