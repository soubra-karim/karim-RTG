/* A P2P client
It provides the following functions:
- Register the content file to the index server (R)
- Contact the index server to search for a content file (D)
        - Contact the peer to download the file
        - Register the content file to the index server
- De-register a content file (T)
- List the local registered content files (L)
- List the on-line registered content files (O)
*/

#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define QUIT "quit"
#define BUFLEN 100        // Max buffer length
#define SERVER_PORT 14000 // Default server port
#define NAMESIZ 20        // Max size of Peer Name
#define MAXCON 200        // Max number of connections

typedef struct pdu
{
    char type;
    char data[BUFLEN];
} PDU;
PDU rpdu;

struct
{
    int sd;             // Socket Descriptor
    char name[NAMESIZ]; // Content Name
} table[MAXCON];        // Keep track of the registered content
int max_index = 0;      // Index for table

char usr[NAMESIZ];

int s_sock, peer_port;
int fd, nfds;
fd_set rfds, afds;

void registration(int, char *, struct sockaddr_in);
int search_content(int, char *, PDU *, struct sockaddr_in);
int client_download(char *, PDU *, struct sockaddr_in);
void server_download(int, struct sockaddr_in);
void deregistration(int, char *, struct sockaddr_in);
void online_list(int, struct sockaddr_in);
void local_list();
void quit(int, struct sockaddr_in);
void handler();

int main(int argc, char **argv)
{
    int server_port = SERVER_PORT;
    int n;
    struct sockaddr_in server;
    int alen = sizeof(struct sockaddr_in);
    struct hostent *hp;
    char c, *host, name[NAMESIZ];
    struct sigaction sa;

    switch (argc)
    {
    case 2:
        host = argv[1];
        break;
    case 3:
        host = argv[1];
        server_port = atoi(argv[2]);
        break;
    default:
        printf("usage: peer [host] [port]");
        exit(1);
    }

    // UDP connection with index server
    memset(&server, 0, alen);
    server.sin_family = AF_INET;
    server.sin_port = htons(server_port);
    if (hp = gethostbyname(host))
    {
        memcpy(&server.sin_addr, hp->h_addr, hp->h_length);
    }
    else if ((server.sin_addr.s_addr = inet_addr(host)) == INADDR_NONE)
    {
        printf("Can't get host entry\n");
        exit(1);
    }

    // Allocate a socket for the index server
    s_sock = socket(PF_INET, SOCK_DGRAM, 0);
    if (s_sock < 0)
    {
        printf("Can't create a socket\n");
        exit(1);
    }
    if (connect(s_sock, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        printf("Can't connect\n");
        exit(1);
    }

    // Choose a username (used for Peer Name)
    printf("Choose a username\n");
    scanf("%s", usr);

    nfds = 0;
    // Initialize table structure to contain all connected peers
    for (n = 0; n < MAXCON; n++)
    {
        table[n].sd = -1;
    }

    // Setup signal handler
    sa.sa_handler = handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    // Initialization for select()
    FD_ZERO(&afds);        // Clear fd_set
    FD_SET(0, &afds);      // Listening on read descriptor (stdin)
    FD_SET(s_sock, &afds); // Listening on server_socket

    int option;
    while (1)
    {
        printf("Click enter to do another action.\n");
        memcpy(&rfds, &afds, sizeof(rfds));
        if (select(FD_SETSIZE, &rfds, NULL, NULL, NULL) == -1)
        {
            printf("Select error: %s\n", strerror(errno));
            exit(1);
        }

        if (FD_ISSET(0, &rfds))
        { /* Command from the user  */
            printf("Select an option:\n");
            printf("(1) Register content\n");
            //printf("(2) List local content\n");
            printf("(2) List registered content\n");
            printf("(3) Download content\n");
            printf("(4) Deregister content\n");
            printf("(5) Quit\n");
            scanf("%d", &option);

            FILE *fp = NULL;
            char filename[10];

            switch (option)
            {
            case 1:
                printf("You chose Option 1.\n");

                while (fp == NULL)
                {
                    printf("Enter filename to register:\n");
                    scanf("%s", filename);
                    fp = fopen(filename, "rb");
                    if (fp == NULL)
                    {
                        printf("File does not exist, please select another file\n");
                    }
                }

                registration(s_sock, filename, server);
                break;
            case 2:
                printf("You chose Option 2.\n");
                // call online_list() from index server
                online_list(s_sock, server);
                break;
            case 3:
                printf("You chose Option 3.\n");
                // call search_content()
                // call client_download()
                // call registration()
                printf("Enter file name to download:\n");
                scanf("%s", filename);
                PDU *rpdu = malloc(sizeof(PDU));
                bzero(rpdu->data, 100);
                int search_result = search_content(s_sock, filename, rpdu, server);
                if (search_result == 1)
                {
                    printf("ERROR: File not found on index server, please use a valid file name.\n");
                }
                else
                {
                    printf("File found on index server. Requesting download.\n");
                    client_download(filename, rpdu, server);
                    registration(s_sock, filename, server);
                }

                break;
            case 4:
                printf("You chose Option 4.\n");
                while (fp == NULL)
                {
                    printf("Enter filename to de-register:\n");
                    scanf("%s", filename);
                    fp = fopen(filename, "rb");
                    if (fp == NULL)
                    {
                        printf("File does not exist, please select another file\n");
                    }
		        }
		        deregistration(s_sock, filename, server);
                break;
            case 5:
                printf("You chose Option 5.\n");
                quit(s_sock, server);
                exit(0);
            default:
                printf("Invalid option. Please select a number between 1 and 6 inclusive.\n");
            }
        }
        else
        {
            // Download was requested, send file to content client from content server
            printf("A download was requested by another peer, addressing download.\n");
            server_download(s_sock, server);
        }
        printf("\n");
    }
}

void quit(int s_sock, struct sockaddr_in server)
{
char dereg[10];
 	printf("Quitting server, deregistering all content...\n");
	int i;
 	for (i = 0; i < max_index; i++){
		strcpy(dereg, table[i].name);
		printf("Degresitering: %s\n", dereg);
		deregistration(s_sock, dereg, server);	
 	}
	printf("Done\n");
	max_index = 0;
	exit(0);
}


void online_list(int s_sock, struct sockaddr_in server)
{
	PDU *rpdu = malloc(sizeof(PDU));
    bzero(rpdu->data, 100);
    rpdu->type = 'O';
    strcat(rpdu->data, "send list please");
    
	// printf("Registering peer %s \n", usr);
    // printf("Data sent for online list: %s\n", rpdu->data);
    sendto(s_sock, rpdu, sizeof(*rpdu), 0, (const struct sockaddr *)&server, sizeof(server));

    // Recieve acknowledgement of content registration
    PDU recv_pdu;
    int i, n, len;
	char listed_files[100];
	char *token;
    int index=0;
    n=recvfrom(s_sock, &recv_pdu, sizeof(PDU), 0, (struct sockaddr *)&server, &len);
		 if (recv_pdu.type == 'O'){
			printf("Received registered files from index server: \n");
            token = strtok(recv_pdu.data, "|");
            while (token != 0)
            {
				printf("[%d] %s \n", index, token);
              

                token = strtok(0, "|");
                index++;
            }
       }else{
			printf("error listing \n");
		}

}

void server_download(int s_sock, struct sockaddr_in server)
{
    struct sockaddr_in client;
    int descriptor;
    int current_sd;
    int n;
    FILE *file_pointer_server;
    char fname[100];

    for (descriptor = 0; descriptor < MAXCON; descriptor++)
    {

        if (FD_ISSET(table[descriptor].sd, &rfds))
        {
            current_sd = table[descriptor].sd;
            break;
        }
    }
    int client_len = sizeof(client);
    int new_sd = accept(current_sd, (struct sockaddr *)&client, &client_len);
    
	PDU *recv=malloc(sizeof(PDU)) ; // setting up send pdu to content server
    bzero(recv->data, 100);
    char *token;
    int index = 0;
    // gets the file name to be downloaded
    //while (n = read(new_sd, recv, sizeof(PDU)) > 0)
    //{
		n = read(new_sd, recv, sizeof(PDU));
		printf("bytes received %d\n",n);
		printf("CONNECTION TO SERVER DOWNLOAD SUCCESS! \n");
		printf("type received is %c \n",recv->type);
		printf("data is %s\n",recv->data);
        if (recv->type == 'D')
        {
            token = strtok(recv->data, "|");
            while (token != 0)
            {
                if (index == 1)
                {
                    strcpy(fname, token);
                }

                token = strtok(0, "|");
                index++;
            }
        }
    	
	printf("Name of file to open is: %s \n",fname);
    file_pointer_server = fopen(fname, "r");
    PDU resp;
    if (file_pointer_server == NULL)
    {
		printf("file failed to open");
        resp.type = 'E';
        // resp.data = "FILE NOT FOUND";
        strcpy(resp.data, "FILE NOT FOUND");
        write(new_sd, &resp, sizeof(resp));
    }
    else
    {
        while (fgets(resp.data, 100, file_pointer_server) != NULL)
        {
            resp.type = 'C';
            write(new_sd, &resp, sizeof(resp));
        }
        fclose(file_pointer_server);
    }
    (void)close(new_sd);
}

int search_content(int s_sock, char *name, PDU *rpdu, struct sockaddr_in server)
{
    /* Checks if index server has the file, that is to be downloaded
    -communicates to the index server via udp
    -returns 1 if file not found , returns 0 if success
    */

    PDU *spdu = malloc(sizeof(PDU));
    bzero(spdu->data, 100);

    spdu->type = 'S';
    // strcat(spdu->type, 'S'); // type
    strcat(spdu->data, usr); // peer name
    strcat(spdu->data, "|");
    strcat(spdu->data, name); // content name
    printf("Search data sent to index server: %s\n", spdu->data);
    printf("type is: %c \n", spdu->type);
    sendto(s_sock, spdu, sizeof(*spdu), 0, (const struct sockaddr *)&server, sizeof(server));
    int len;
    PDU *recv_pdu;
    int alen = sizeof(server);
    recvfrom(s_sock, rpdu, sizeof(PDU), 0, (struct sockaddr *)&server, &alen);
    printf("Search data received from index server: %s\n", rpdu->data);
    
    if (rpdu->type == 'E')
    {
        printf("Error from search request: %s\n", rpdu->data);
        return 1;
    }
    else
    {
        // type S
        printf("File found! \n");
        printf("Data Received: %s \n", rpdu->data);
        return 0;
    }
}

int client_download(char *name, PDU *pdu, struct sockaddr_in server)
{
    /* Communicates with a content Server
       -connects to content server tcp socket and initiates download.
       -returns 1 if fail, returns 0 if success
   */
    // create file using name , name is content name
    struct sockaddr_in content_server;
    int sd;
    char address[100];
    strcpy(address, pdu->data);
    int index = 0;
    int n;
    char *ip;
    int port;
    PDU spdu; //= malloc(sizeof(PDU)); // setting up send pdu to content server
    bzero(spdu.data, 100);
	char t='D';
    spdu.type='D';
    strcpy(spdu.data, usr); // follows format of ->  D | peer name | content name
    strcat(spdu.data, "|");
    strcat(spdu.data, name);
    // getting ip and port of content server
    char *token;
    token = strtok(address, "|");

    while (token != 0)
    {
        if (index == 2)
        {
            //strcpy(ip, token);
			ip=(char *)token;
        }
        if (index == 3)
        {
            port = atoi(token);
        }
        token = strtok(0, "|");
        index++;
    }
    if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        fprintf(stderr, "Can't create a socket\n");
        exit(1);
    }
    // setup connection
	printf("Setting up connection with content server\n");
	
    bzero((char *)&content_server, sizeof(struct sockaddr_in));
    content_server.sin_family = AF_INET;
    content_server.sin_port = htons(port);
   // strcpy((char *)&content_server.sin_addr, ip);
	int inet_t=inet_aton(ip,(struct in_addr *)&content_server.sin_addr);
	printf("result of inet %d \n",inet_t);
	if(inet_t==0){
		printf("error\n");
	};
    if (connect(sd, (struct sockaddr *)&content_server, sizeof(content_server)) == -1)
    {
        fprintf(stderr, "Can't connect \n");
        exit(1);
    }
	printf("Sending download request to content server with data: %s\n", spdu.data);
	printf("with type %c \n",spdu.type);
    write(sd, &spdu, sizeof(PDU));
    // content server replies with C type
    PDU rpdu;
    FILE *file_pointer;
    file_pointer = fopen(name, "w");
    while (n = read(sd, &rpdu, sizeof(struct pdu)) > 0)
    {
        if (rpdu.type == 'C')
        {
            fputs(rpdu.data, file_pointer);
        }
        else if (rpdu.type == 'E')
        {
            printf("ERROR FILE DOWNLOAD FAILED \n");
            
            fclose(file_pointer);
            remove(name);
            return 1;
        }
    }

    fclose(file_pointer);

    //registration(s_sock, name, server);

    return 0;
}

void deregistration(int s_sock, char *name, struct sockaddr_in server)
{

    PDU *rpdu = malloc(sizeof(PDU));
    bzero(rpdu->data, 100);
    rpdu->type = 'T'; //De register a file name
    strcat(rpdu->data, name);
    strcat(rpdu->data, "|");
    strcat(rpdu->data, usr);
    strcat(rpdu->data, "|");
   // strcat(rpdu->data, inet_ntoa(reg_addr.sin_addr));
    //strcat(rpdu->data, "|");
    //strcat(rpdu->data, port);
    printf("Deregistering peer %s \n",usr);
    printf("Data Sent: %s\n", rpdu->data);
    sendto(s_sock, rpdu, sizeof(*rpdu), 0, (const struct sockaddr *)&server, sizeof(server));


 // Recieve acknowledgement of content deregistration
    PDU recv_pdu;
    int i, n, len, s;
    recvfrom(s_sock, &recv_pdu, sizeof(PDU), 0, (struct sockaddr *)&server, &len);

    if (recv_pdu.type == 'A')
    {	
	printf("File has been deregistered %s \n",name);
        strcpy(table[max_index].name, name);
	int i;
        for (i = 0; i < max_index; i++)
        {
            if (strcmp(table[i].name, name) && s >= nfds) //This finds the filename from the struct and removes it
            {
		strcpy(table[i].name, ""); //This removes file from struct
                nfds = s + 1; 
		table[i].sd = s;
		FD_CLR(s, &afds); //This clears socket
		table[i].sd = -1;			//Remove socket from struct
		close(s);				//Close TCP connection
            }
        }
        
    }
    else
    {
        printf("Error : %s\n", recv_pdu.data);
    }
}

void registration(int s_sock, char *name, struct sockaddr_in server)
{
    /* Register a content to the index server
        - Create a TCP socket for other peers to download
        - Add TCP socket descriptor and content name to local list
        - Register the content to the index server via UDP
        - Update nfds (number of file descriptors)
    */
    int s;
    // Create a stream socket
    if ((s = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    { // Create TCP socket for content
        fprintf(stderr, "Can't create a socket\n");
        exit(1);
    }

    // Bind an address to the socket
    struct sockaddr_in reg_addr; // TCP Socket Address
    bzero((char *)&reg_addr, sizeof(struct sockaddr_in));
    reg_addr.sin_family = AF_INET;
    reg_addr.sin_port = htons(0); // Is 0 correct?
    reg_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(s, (struct sockaddr *)&reg_addr, sizeof(reg_addr)) == -1)
    {
        fprintf(stderr, "Can't bind name to socket\n");
        exit(1);
    }

    // Queue upto max 5 connect requests
    listen(s, 5);

    char port[10];
    int alen = sizeof(struct sockaddr_in);
    getsockname(s, (struct sockaddr *)&reg_addr, &alen); // Get socket address information
    sprintf(port, "%d", ntohs(reg_addr.sin_port));       // Get port of socket and put into string

    PDU *rpdu = malloc(sizeof(PDU));
    bzero(rpdu->data, 100);
    rpdu->type = 'R';
    strcat(rpdu->data, name);
    strcat(rpdu->data, "|");
    strcat(rpdu->data, usr);
    strcat(rpdu->data, "|");
    strcat(rpdu->data, inet_ntoa(reg_addr.sin_addr));
    strcat(rpdu->data, "|");
    strcat(rpdu->data, port);
	// printf("Registering peer %s \n", usr);
    printf("Registration data sent to index server: %s\n", rpdu->data);
    sendto(s_sock, rpdu, sizeof(*rpdu), 0, (const struct sockaddr *)&server, sizeof(server));

    // Recieve acknowledgement of content registration
    PDU recv_pdu;
    int i, n, len;
    recvfrom(s_sock, &recv_pdu, sizeof(PDU), 0, (struct sockaddr *)&server, &len);

    if (recv_pdu.type == 'A')
    {
        strcpy(table[max_index].name, name);
	int i;
        for (i = 0; i < max_index; i++)
        {
            if (strcmp(table[i].name, "") && s >= nfds)
            {
                nfds = s + 1;
            }
        }
        table[max_index].sd = s;
        FD_SET(s, &afds);
        max_index++;
    }
    else
    {
        printf("Error: %s\n", recv_pdu.data);
    }
}

void handler()
{
    //quit(s_sock);
}