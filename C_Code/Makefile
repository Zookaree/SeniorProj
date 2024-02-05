CFLAGS=-Wall -g -O0 -c
CC=gcc
OBJS=client.o \
	server.o \

all: main

clean:
	rm -f $(OBJS)
	rm main

main: $(OBJS)
	$(CC) $(OBJS) -o main -g

client.o: client_test.c
	gcc $(CLFAGS) client_test.c

server.o: server_test.c
	gcc $(CFLAGS) server_test.c