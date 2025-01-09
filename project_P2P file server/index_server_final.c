/* Index Server 
Message types:
R - used for registration
A - used by the server to acknowledge the success of registration
Q - used by chat users for de-registration
D - download content between peers (not used here)
C - Content (not used here)
S - Search content
L - Location of the content server peer
E - Error messages from the Server
*/

#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>

#define MSG1 "Cannot find content"
#define BUFLEN 100
#define NAMESIZ 20
#define MAX_NUM_CON 200

typedef struct entry {
    char usr[NAMESIZ]; // Peer Name
    struct sockaddr_in addr; // Address of content
    int downloads; // Number of downloads
    struct entry *next; // Other Content Servers
} ENTRY;

typedef struct {
    char name[NAMESIZ]; // Content Name
    ENTRY *head;
} LIST;
LIST list[MAX_NUM_CON];
int max_index = 0;

typedef struct {
    char type;
    char data[BUFLEN];
} PDU;
PDU tpdu;

void search(int, char *, struct sockaddr_in);
void registration(int, char *, struct sockaddr_in);
void deregistration(int, char *, struct sockaddr_in);
int isEntryNULL(int);

int main(int argc, char *argv[]) {
    int port = 3000;
    struct sockaddr_in sin; // Server socket
	struct sockaddr_in fsin; // Peer socket
	int alen = sizeof(struct sockaddr_in); // Address length
    char name[NAMESIZ], usr[NAMESIZ];
    PDU rpdu;

    int n;
    for (n = 0; n < MAX_NUM_CON; n++)
        list[n].head = NULL;

    switch (argc) {
		case 1:
			break;
		case 2:
			port = atoi(argv[1]);
			break;
		default:
			fprintf(stderr, "usage: index_server [port]\n");
	}

    // Specify socket settings
	memset(&sin, 0, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_addr.s_addr = INADDR_ANY;
	sin.sin_port = htons(port);

	// Setup UDP socket
    int s;
	s = socket(AF_INET, SOCK_DGRAM, 0);
	if (s < 0) {
		printf("Can't create socket");
		exit(1);
	}

	// Bind the socket
	if (bind(s, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
		printf("Failed to bind socket to port");
	}

    while (1) {
        if ((n = recvfrom(s, &rpdu, sizeof(PDU), 0, (struct sockaddr *)&fsin, &alen)) < 0) {
            printf("recvfrom error: n=%d\n", n);
        }

        printf("Received Data of Type: %c\n", rpdu.type);

        if (rpdu.type == 'R') {
            registration(s, rpdu.data, fsin);
        } else if (rpdu.type == 'S') {
            search(s, rpdu.data, fsin);
        } else if (rpdu.type == 'O') {
            // Read from content list and send to client
            PDU *opdu = malloc(sizeof(PDU));
            bzero(opdu->data, 100);
            opdu->type = 'O';
            char content[100];
            bzero(content, 100);
	    int i;
            for (i = 0; i < max_index; i++) {
                if (!isEntryNULL(i) && strstr(content, list[i].name) == NULL) {
                    strcat(opdu->data, list[i].name);
                    strcat(opdu->data, "|");
                    strcat(content, list[i].name);
                }
            }
            sendto(s, opdu, sizeof(*opdu), 0, (const struct sockaddr *)&fsin, sizeof(fsin));
        } else if (rpdu.type == 'T') {
            deregistration(s, rpdu.data, fsin);
        } else {
            printf("Error: Invalid type recieved\n");
        }
        printf("\n");
    }
    return 0;
}

void search(int s, char *data, struct sockaddr_in addr) {
    printf("Recieved search request with data: %s\n", data);
    char *sep = strtok(data, "|"); // Peer Name
    char peer[20];
    strcpy(peer, sep);
    // strcpy(list[max_index].name, contentName);

    char contentName[20]; // Content Name
    sep = strtok(NULL, "|");
    strcpy(contentName, sep);

    int i = 0;
    int found = 0;
    int found_index = 0;
    int minDownloads = 999;
    while (i < max_index) {
        if (!isEntryNULL(i) && strcmp(contentName, list[i].name) == 0 && list[i].head->downloads < minDownloads) {
            found_index = i;
            minDownloads = list[i].head->downloads;
            found = 1;
        }
        i++;
    }
    if (found == 1) {
        printf("Found registered content");
        PDU *spdu = malloc(sizeof(PDU));
        bzero(spdu->data, 100);
        spdu->type = 'S';
        strcat(spdu->data, list[found_index].name);
        strcat(spdu->data, "|");
        strcat(spdu->data, list[found_index].head->usr);
        strcat(spdu->data, "|");
        strcat(spdu->data, inet_ntoa(list[found_index].head->addr.sin_addr));
        strcat(spdu->data, "|");
        char port[10];
        sprintf(port, "%d", ntohs(list[found_index].head->addr.sin_port));
        strcat(spdu->data, port);
        printf("Search data to be returned to peer: %s \n", spdu->data);
        sendto(s, spdu, sizeof(*spdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
        list[found_index].head->downloads += 1;
    } else {
        PDU *epdu = malloc(sizeof(PDU));
        bzero(epdu->data, 100);
        epdu->type = 'E';
        strcpy(epdu->data, "Content not found!");
        sendto(s, epdu, sizeof(*epdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
    }
    // Print contents of list
    void printEntry(ENTRY *entry) {
        printf("User: %s\n", entry->usr);
        printf("IP Address: %s\n", inet_ntoa(entry->addr.sin_addr));
        printf("Port: %d\n", ntohs(entry->addr.sin_port));
        printf("Downloads: %d\n", entry->downloads);
    }
    void printList(LIST *list) {
        printf("Content Name: %s\n", list->name);
        
        ENTRY *current = list->head;
        while (current != NULL) {
            printf("Entry:\n");
            printEntry(current);
            current = current->next;
        }
    }
    for (i = 0; i < max_index; i++) {
        printf("List %d:\n", i);
        printList(&list[i]);
        printf("\n");
    }
}

void deregistration(int s, char *data, struct sockaddr_in addr) {
printf("Data Recieved from deregistration: %s\n", data);
    char *sep = strtok(data, "|"); // Content Name
    char contentName[20];
    strcpy(contentName, sep);
    strcpy(list[max_index].name, contentName); //Might not need this

    char peer[20]; // Peer Name
    sep = strtok(NULL, "|");
    strcpy(peer, sep); //Variable for peer name, important

    int i = 0;
    int found = 0;

	
    while (!found && i < max_index) {
        if (!isEntryNULL(i) && strcmp(contentName, list[i].name) == 0 && strcmp(peer, list[i].head->usr) == 0) {
            printf("Found content to deregister: %s\n", contentName);
            // Found the content which is registered, need to remove it
	    strcpy(list[i].name, ""); //This should replace that content with NULL, therefore removing it
            found = 1;
        } else {
            printf("Content not registered %s and %s\n", contentName, list[i].name);
        }
        i++;
    }
    if (found == 1) {
	//This is where we remove that filename from the list change from adding to removing omehow?

        //max_index++; dont change the max index when removing, just remove form the list just ignore for now

        PDU *apdu = malloc(sizeof(PDU));
        bzero(apdu->data, 100);
        apdu->type = 'A';
        strcpy(apdu->data, "File has been deregistered!\n");
        sendto(s, apdu, sizeof(*apdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
	
    } else {
        
	//Final code if file is not registered
	PDU *epdu = malloc(sizeof(PDU));
        bzero(epdu->data, 100);
        epdu->type = 'E';
        strcpy(epdu->data, "File is not registered, therefore cannot be removed");
        sendto(s, epdu, sizeof(*epdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
    }
}

void registration(int s, char *data, struct sockaddr_in addr) {
    printf("Data Recieved from Registration: %s\n", data);

    char *sep = strtok(data, "|"); // Content Name
    char contentName[20];
    strcpy(contentName, sep);
    strcpy(list[max_index].name, contentName);

    char peer[20]; // Peer Name
    sep = strtok(NULL, "|");
    strcpy(peer, sep);

    int i = 0;
    int found = 0;
    // Find out if there is existing content and peer already registered
    while (!found && i < max_index) {
        if (!isEntryNULL(i) && strcmp(contentName, list[i].name) == 0 && strcmp(peer, list[i].head->usr) == 0) {
            printf("Found existing content: %s", contentName);
            // Need to add new content server to content
            found = 1;
        } else {
            // No match found yet
            // printf("No match between %s and %s, %s, and %s\n", contentName, list[i].name, peer, list[i].head->usr);
        }
        i++;
    }

    if (found == 1) {
        // Found an existing content and peer already registered, so sending an error
        PDU *epdu = malloc(sizeof(PDU));
        bzero(epdu->data, 100);
        epdu->type = 'E';
        strcpy(epdu->data, "Peer and file already registered");
        sendto(s, epdu, sizeof(*epdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
    } else {
        ENTRY *entry = malloc(sizeof(ENTRY));
        list[max_index].head = entry;
        list[max_index].head->downloads = 0;
        strcpy(entry->usr, peer);

        sep = strtok(NULL, "|"); // IP Address
        inet_aton(sep, (struct in_addr *)&entry->addr.sin_addr);

        int portNum;
        sep = strtok(NULL, "|");  // Port Number
        sscanf(sep, "%d", &portNum);
        entry->addr.sin_port = htons(portNum);

        printf("Port Number: %d\n", portNum);
        printf("Content Name: %s\n", list[max_index].name);
        printf("Peer Name: %s\n", entry->usr);
        printf("Port %d\n", ntohs(entry->addr.sin_port));

        max_index++;

        PDU *apdu = malloc(sizeof(PDU));
        bzero(apdu->data, 100);
        apdu->type = 'A';
        strcpy(apdu->data, "File has been registered!");
        sendto(s, apdu, sizeof(*apdu), 0, (const struct sockaddr *)&addr, sizeof(addr));
    }
}

int isEntryNULL(int i) {
    // Make sure that there is no content available
    return (!strcmp(list[i].name, "") && list[i].head == NULL);
}