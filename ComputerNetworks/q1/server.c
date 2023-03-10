#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    int sockfd, newsockfd, portno;
    socklen_t clilen;
    char buffer[256];
    struct sockaddr_in serv_addr, cli_addr;
    struct sockaddr_in remaddr;
    socklen_t remaddr_len = sizeof(remaddr);
    int n;
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
            sizeof(serv_addr)) < 0) 
            error("ERROR on binding");
    //listen(sockfd,5);
    //clilen = sizeof(cli_addr);
    //  newsockfd = accept(sockfd, 
    //              (struct sockaddr *) &cli_addr, 
    //              &clilen);
    //  if (newsockfd < 0) 
    //       error("ERROR on accept");
    bzero(buffer,256);
    n = recvfrom(sockfd, buffer, 255, 0, (struct sockaddr *)&remaddr, &remaddr_len);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("Here is the message: %s\n",buffer);
    close(sockfd);
    return 0; 
}