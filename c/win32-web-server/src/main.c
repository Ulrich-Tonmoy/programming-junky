#include <winsock2.h>
#include <Windows.h>
#include <stdio.h>

int main() {
    WSADATA wsadata;
    if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0) {
        printf("WSAStartup failed with error: %d\n", WSAGetLastError());
        return 1;
    }

    SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
    if (s == INVALID_SOCKET) {
        printf("socket failed with error: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(3000);

    if (bind(s, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        printf("bind failed with error: %d\n", WSAGetLastError());
        closesocket(s);
        WSACleanup();
        return 1;
    }

    if (listen(s, 10) == SOCKET_ERROR) {
        printf("listen failed with error: %d\n", WSAGetLastError());
        closesocket(s);
        WSACleanup();
        return 1;
    }

    printf("Server http://localhost:3000/ \n");

    SOCKET client = accept(s, NULL, NULL);
    if (client == INVALID_SOCKET) {
        printf("accept failed with error: %d\n", WSAGetLastError());
        closesocket(s);
        WSACleanup();
        return 1;
    }

    char request[4096] = {0};
    int bytes_received = recv(client, request, sizeof(request) - 1, 0);
    if (bytes_received == SOCKET_ERROR) {
        printf("recv failed with error: %d\n", WSAGetLastError());
        closesocket(client);
        closesocket(s);
        WSACleanup();
        return 1;
    }
    request[bytes_received] = '\0';

    // Print the request
    // for (size_t i = 0; i < sizeof(request); i++) {
    //     printf("%c", request[i]);
    // }

    if (strncmp(request, "GET / ", 6) == 0) {
        FILE* f = fopen("index.html", "rb");
        if (f == NULL) {
            printf("Failed to open index.html\n");
            const char* error_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found";
            send(client, error_response, strlen(error_response), 0);
            closesocket(client);
            closesocket(s);
            WSACleanup();
            return 1;
        }

        char buffer[4096];
        size_t total_bytes_sent = 0;
        while (TRUE) {
            size_t bytes_read = fread(buffer, 1, sizeof(buffer), f);
            if (bytes_read == 0) {
                break;
            }

            int bytes_sent = send(client, buffer, bytes_read, 0);
            if (bytes_sent == SOCKET_ERROR) {
                printf("send failed with error: %d\n", WSAGetLastError());
                fclose(f);
                closesocket(client);
                closesocket(s);
                WSACleanup();
                return 1;
            }
            total_bytes_sent += bytes_sent;
        }

        printf("Sent %zu bytes from index.html\n", total_bytes_sent);
        fclose(f);
    } else {
        printf("Unsupported request type: %s\n", request);
        const char* error_response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nUnsupported request";
        send(client, error_response, strlen(error_response), 0);
    }

    closesocket(client);
    WSACleanup();

    return 0;
}