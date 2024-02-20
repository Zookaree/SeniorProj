#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define UDP_IP "127.0.0.1"
#define UDP_PORT 2345

int main(int argc, char * argv[])
{
	int server;
	char send_msg[256] = "Sending to server";
	char response[256];
	//create a socket 
	int sockfd;
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	
	//bind to any addr
	struct sockadder_in addr;
	memset((char *)&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	addr.sin_port = htons(UDP_PORT); //requests a port
	
	int conn = connect(server, (struct sockaddr*) &addr,
	 sizeof(addr));
	if(conn == -1)
	{ printf("Error with Connection"); return -1; }
	
	
	/*if (toServer == -1) 
		perror("Error getting adress info");
		
	memcpy(&server_addr, addr_info->ai_addr, 
	addr_info->ai_addrlen);
	server_addr.sin_port = htons(UDP_PORT);
	
	freeaddrinfo(addr_info);*/
	
	//[INSERT COMMANDS TO BE SENT/RECEIVED HERE]
	while(1)
	{
		send(server, send_msg, sizeof(send_msg), 0);
		recv(server, server_response, sizeof(response),0);
		printf("%s", response);
	}
	
	close(sockfd)
	
	return 0;
}
