#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "protocol.h"

const std::string EXIT_CODE = "_exit_";
const std::string LIST_CODE = "_list_";
const std::string ERROR_CODE = "_null_";

void error(const char *msg)
{
	perror(msg);
	exit(0);
}
std::string to_low(std::string input)
{
	for(int i = 0; i < input.size(); i++)
	{
		input[i] = std::tolower(input[i]);
	}
	return input;
}
std::string get_user_choice()
{
	std::string s;
	std::cout << "What do you want to do?\n1. List\n2. Retrieve\n3. Exit\n";
	std::getline(std::cin, s);
	std::stringstream _stream(s);
	_stream >> s;
	if(s == "1" || to_low(s) == "list")
	{
		s = LIST_CODE;
	}
	else if(s == "2" || to_low(s) == "retrieve")
	{
		std::cout << "Enter file name:\n";
		std::getline(std::cin, s);
		std::stringstream __stream(s);
		__stream >> s;
	}
	else if(s == "3" || to_low(s) == "exit")
	{
		s = EXIT_CODE;
	}
	else return ERROR_CODE;
	return s;
}
int transmit_data(std::string data, int &sockfd, struct sockaddr_in &serv_addr, int &slen)
{
	char buffer[CHUNK_SIZE_];
	bzero(buffer,CHUNK_SIZE_);
	strcpy(buffer, data.c_str());//TODO: Check if correct size
	int n = sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *) &serv_addr, slen);
	if (n < 0) 
	{
		error("ERROR writing to socket");
		return -1;
	}
}
int recieve_data(char* buffer, int &sockfd, struct sockaddr_in &serv_addr, int &slen)//TODO: CHECK 
{
	return recvfrom(sockfd, buffer, CHUNK_SIZE_, 0, (struct sockaddr*) &serv_addr, (socklen_t*) &slen);
}
int recieve_vec(char* buffer, int &sockfd, struct sockaddr_in &serv_addr, int &slen)
{
	recieve_data(buffer, sockfd, serv_addr, slen);
	std::string b(buffer);
	int i = 0;
	while(b != END_OF_TRANSMISSION)
	{
		std::cout << i++ << ". " << b << std::endl;
		recieve_data(buffer, sockfd, serv_addr, slen);
		b = buffer;
	}
	return 0;
}
int recieve_file(char* buffer, int &sockfd, struct sockaddr_in &serv_addr, int &slen)
{
	std::string loc(buffer);
	loc = CLIENT_LOC + loc;
	std::ofstream ofs(loc.c_str(), std::ofstream::out);
	recieve_data(buffer, sockfd, serv_addr, slen);
	std::string b(buffer);
	int i = 0;
	while(b != END_OF_TRANSMISSION)
	{
		ofs << b << std::endl;
		recieve_data(buffer, sockfd, serv_addr, slen);
		b = buffer;
	}
	ofs.close();
	return 0;
}
int init_socket_client(int argc, char *argv[], int &sockfd, int &portno, struct sockaddr_in &serv_addr, int &slen, struct hostent *server)
{
	if (argc < 3) {
	   fprintf(stderr,"usage %s hostname port\n", argv[0]);
	   return -1;
	}
	portno = atoi(argv[2]);
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0)
	{
		error("ERROR opening socket");
		return -1;
	} 
	server = gethostbyname(argv[1]);
	if (server == NULL) {
		fprintf(stderr,"ERROR, no such host\n");
		return -1;
	}
	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	bcopy((char *)server->h_addr, 
		 (char *)&serv_addr.sin_addr.s_addr,
		 server->h_length);
	serv_addr.sin_port = htons(portno);
	return 0;
}
int main(int argc, char *argv[])
{
	int sockfd, portno, n;
	struct sockaddr_in serv_addr;
	int slen = sizeof(serv_addr);
	struct hostent *server;
	char buffer[CHUNK_SIZE_];
	if(init_socket_client(argc, argv, sockfd, portno, serv_addr, slen, server) >= 0)
	{	
		while(1)
		{
			std::string s = get_user_choice();
			if(s == EXIT_CODE)
			{
				std::cout << "Exiting...\n";
				break;
			}
			else if(s == ERROR_CODE)
			{
				std::cout << "Error...\nExiting...\n";
				break;
			}
			else if(s == LIST_CODE)
			{
				transmit_data(LIST_REQ, sockfd, serv_addr, slen);
				recieve_vec(buffer, sockfd, serv_addr, slen);
			}
			else
			{
				transmit_data(GET_REQ, sockfd, serv_addr, slen);
				strcpy(buffer, s.c_str());
				transmit_data(buffer, sockfd, serv_addr, slen);
				recieve_file(buffer, sockfd, serv_addr, slen);
			}
		}
	}
	close(sockfd);
	return 0;
}