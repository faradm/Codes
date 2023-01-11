#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include "protocol.h"
#include <sys/types.h>
#include <dirent.h>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <sstream>
#include <iostream>
void error(const char *msg)
{
    perror(msg);
    exit(1);
}
int init_socket_server(int argc, char *argv[], int &sockfd, int &portno, struct sockaddr_in &serv_addr)
{
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        return -1;
    }
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    { 
        error("ERROR opening socket");
        return -1;
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    {
        error("ERROR on binding");
        return -1;
    }
    return 0;
}
int transmit_data(char* buffer, int &sockfd, struct sockaddr_in &remaddr, socklen_t &remaddr_len)
{
    return sendto(sockfd, buffer, CHUNK_SIZE_, 0, (struct sockaddr *)&remaddr, remaddr_len);
}
int recieve_data(int &sockfd, char* buffer, int buffer_size, struct sockaddr_in &remaddr, socklen_t &remaddr_len)
{
    bzero(buffer,CHUNK_SIZE_);
    return recvfrom(sockfd, buffer, buffer_size, 0, (struct sockaddr *)&remaddr, &remaddr_len);
}
int transmit_file(std::string file_adr, int &sockfd, char* buffer, struct sockaddr_in &remaddr, socklen_t &remaddr_len)
{
    std::ifstream fin("./files/" + file_adr, std::ifstream::binary);
    int i = 0;
    if(!fin.is_open())
    {
        std::cout << "####@$$@\n";
        return -1;
    }
    while(!fin.eof())
    {
        fin.read(buffer, CHUNK_SIZE_);
        transmit_data(buffer, sockfd, remaddr, remaddr_len);
        std::cout << i++ << "\n";
    }
    strcpy(buffer, END_OF_TRANSMISSION);
    transmit_data(buffer, sockfd, remaddr, remaddr_len);
    return 0;//TODO: Edit
}
int transmit_vec(std::vector<std::string> &vec, int &sockfd, char* buffer, struct sockaddr_in &remaddr, socklen_t &remaddr_len)
{
    for(int i = 0; i < vec.size(); i++)
    {
        strcpy(buffer, vec[i].c_str());
        transmit_data(buffer, sockfd, remaddr, remaddr_len);
    }
    strcpy(buffer, END_OF_TRANSMISSION);
    transmit_data(buffer, sockfd, remaddr, remaddr_len);
}
std::vector<std::string> read_directory()
{
    std::vector<std::string> v;
    DIR* dirp = opendir(SERVER_LOC);
    struct dirent * dp;
    while ((dp = readdir(dirp)) != NULL) {
        v.push_back(dp->d_name);
    }
    closedir(dirp);
    return v;
}
void print_files(std::vector<std::string> &v)
{
    std::cout << "Files:\n";
    for(int i = 0; i < v.size(); i++)
    {
        std::cout << i << ". " << v[i] << std::endl;
    }
}
bool is_digits(const std::string &str)
{
    return str.find_first_not_of("0123456789") == std::string::npos;
}
int find_in_vec(std::vector<std::string> &vec, std::string name)
{
    if(is_digits(name))
    {
        int index = std::stoi(name);
        if(index >= 0 && index < vec.size())
            return index;
        else return -1;
    }
    for(int i = 0; i < vec.size(); i++)
    {
        if(vec[i] == name)
            return i;
    }
    return -1;
}
int main(int argc, char *argv[])
{
    int sockfd, newsockfd, portno;
    char buffer[CHUNK_SIZE_];
    struct sockaddr_in serv_addr;
    struct sockaddr_in remaddr;
    socklen_t remaddr_len = sizeof(remaddr);
    std::vector<std::string> files;
    if(init_socket_server(argc, argv, sockfd, portno, serv_addr) >= 0)
    {
        while(1)
        {
            std::cout << "Waiting...\n";
            if(recieve_data(sockfd, buffer, CHUNK_SIZE_-1, remaddr, remaddr_len) < 0)
            {
                error("Couldn't recieve... Exiting\n");
                break;
            }
            std::string r = buffer;
            if(r == LIST_REQ)
            {
                files = read_directory();
                transmit_vec(files, sockfd, buffer, remaddr, remaddr_len);
            }
            else if(r == GET_REQ)
            {
                if(recieve_data(sockfd, buffer, CHUNK_SIZE_-1, remaddr, remaddr_len) < 0)
                {
                    error("Couldn't recieve... Exiting\n");
                    break;
                }
                files = read_directory();
                r = buffer;
                int file_index = find_in_vec(files, r);
                if(file_index < 0)
                {
                    error("Couldn't find file. Exiting...\n");
                    break;
                }
                transmit_file(files[file_index], sockfd, buffer, remaddr, remaddr_len);
            }
            printf("Here is the message: %s\n",buffer);
        }
        close(sockfd);
    }
}