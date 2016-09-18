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
		cout<<"Sender : Error in input !\n";
		cout<<"Usage:"<<argv[0]<<" <filename>\n";
	}else{

		ifstream fp(argv[1], ios::in);

		if(!fp.is_open()){
			cout<<"Sender(Error) : File doesn't exit ! Aborting ...\n";
			return 0;
		}

		string content((istreambuf_iterator<char>(fp)),(istreambuf_iterator<char>()));	
		fp.close();

		mqd_t mqd = mq_open("/testQueue", O_WRONLY|O_CREAT, PERMISSIONS, &attr);	//open message queue
		//1 : Name of message queue, should start with "/"
		//2 : Read-write flags(O_flags)
		//3 : Read-write permissions
		//4 : Queue attributes object

		if(mqd == -1){
			cout<<"Sender(Error) : Message queue creation failed. Aborting ...\n";
			return 0;
		}

		while(true){
			cout<<"Sender : Sender process is sending content of"<<argv[1]<<"\n";
			int status = mq_send(mqd, content.c_str(), content.length(), PRIORITY);	//send message
			//1 : message queue descriptor
			//2 : message content (char *)
			//3 : length of content
			//4 : priority of message, 0 is lowest

			if(status == -1){
				cout<<"Sender (Error) : Failed to send content. Retrying in 3 secs ...\n";
				sleep(3);
			}else{
				cout<<"Sender : Sender process sent content successfully !\n";
				cout<<"Message Content :\n"<<content<<"\n";
				cout<<"Sender : Sender process now exiting ...\n";
				break;
			}
		}

		mq_close(mqd);	//close message queue
	}

	return 0;
}