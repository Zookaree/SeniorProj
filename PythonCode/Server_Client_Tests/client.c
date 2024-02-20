#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define UDP_IP "127.0.0.1"
#define UDP_PORT 2345

int main(int argc, char * argv[])
{
	//create a socket 
	int sockfd;
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	
	//bind to any addr
	struct sockadder_in addr;
	memset((char *)&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	addr.sin_port = htons(0); //requests a port
	
	bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
	
	//get server address
	struct addrinfo hints;
	struct addrinfo * addr_info;
	struct sockaddr_in server_addr;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	
	if(getaddrinfo(UDP_IP, NULL, &hints, &addr_info) != 0)
		perror("Error getting adress info");
		
	memcpy(&server_addr, addr_info->ai_addr, addr_info->ai_addrlen);
	server_addr.sin_port = htons(UDP_PORT);
	
	freeaddrinfo(addr_info);
	
	//[INSERT COMMANDS TO BE SENT/RECEIVED HERE]
	while(1)
	{
		
	}
	
	close(sockfd)
	
	return 0;
}
