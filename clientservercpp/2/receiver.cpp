#include <iostream>	//for io tasks
#include <fstream>	//for file handling
#include <string>	//for string manipulation
#include <unistd.h>	//for timed sleep

#include <fcntl.h>	//for O_flags
#include <sys/stat.h>	//for mode attributes
#include <mqueue.h>	//for message queue

using namespace std;

//permissions and message priority
#define PERMISSIONS 0655
#define PRIORITY 0


int main(int argc, char* argv[]){

	//default queue attributes
	struct mq_attr attr;
	attr.mq_maxmsg = 10;
	attr.mq_msgsize = 8192;

	if(argc !=2){
		cout<<"Receiver : Error in input !\n";
		cout<<"Usage:"<<argv[0]<<" <filename>\n";
	}else{

		ofstream fp(argv[1], ios::out|ios::trunc);
		string content;

		mqd_t mqd = mq_open("/testQueue", O_RDONLY|O_CREAT, PERMISSIONS, &attr);	//open message queue
		//1 : Name of message queue, should start with "/"
		//2 : Read-write flags(O_flags)
		//3 : Read-write permissions
		//4 : Queue attributes object

		if(mqd == -1){
			cout<<"Error(Receiver) : Message queue creation failed. Aborting ...\n";
			return 0;
		}

		cout<<"Receiver process receiving content ...\n";

		char buffer[8192];
		int status = mq_receive(mqd, buffer, 8192, PRIORITY);
			//1 : message queue descriptor
			//2 : buffer address
			//3 : length of buffer
			//4 : priority of message, 0 is lowest


		if(status == -1){
			cout<<"Error(Receiver) : Failed to receive content ...\n";
		}else{
			fp << buffer;
			cout<<"Content written to "<<argv[1]<<" successfully ! Receiver process now exiting ...\n";
		}

		mq_close(mqd);	//close message queue
		mq_unlink("/testQueue");	//delete message queue
		fp.close();	//close file
	}

	return 0;
}