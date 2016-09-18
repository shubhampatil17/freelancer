#include <iostream>	//for io tasks
#include <fcntl.h>	//for O_ flags
#include <sys/mman.h>	//for mmap (memory mapping)
#include <unistd.h>	//for sleep and ftruncate
#include <mutex>	//for mutex variable

using namespace std;

//access permissions
#define PERMISSIONS 0777


int main(int argc, char* argv[]){

	//default structure to be placed in shared memory. Mutex + Integer
	struct shm_buffer{
		mutex mtx;
		int value;
	};

	int shm_fd = shm_open("/testSHM", O_RDWR|O_CREAT, PERMISSIONS);	//open shared memory
	//1 : Name of the shared memory
	//2 : Read-write flags (O_ flags)
	//3 : Access permission

	if(shm_fd == -1){
		cout<<"Error : Shared Memory creation failed ! Aborting ...\n";
		return 0;
	}

	cout<<"Success : Shared Memory created successfully !\n";

	//expand shared memory to the size of shm_buffers
	ftruncate(shm_fd, sizeof(struct shm_buffer));
	
	//map shared memory to process area
	void* shm_base_addr = (struct shm_buffer*)mmap(NULL, sizeof(struct shm_buffer), PROT_READ|PROT_WRITE, MAP_SHARED, shm_fd, 0);
	//1 : start address of memory segment. NULL : let system choose it.
	//2 : Size of memory segment in bytes
	//3 : Memory read-write protection flags
	//4 : Sharing flag. MAP_SHARED : Share segment with other process. MAP_PRIVATE : keep segment private
	//5 : Shared memory descriptor
	//6 : Offset in the memory segment

	if(shm_base_addr == MAP_FAILED){
		cout<<"Error: mmap mapping failed ! Aborting ...\n";
		return 0;
	}	

	//Point shm_buffer to the base address of shared memory
	struct shm_buffer* buffer =  (struct shm_buffer*)shm_base_addr;
	
	buffer->value = 1000000;
	cout<<"Status : Current value in Shared Memory ="<<buffer->value<<"\n";
	cout<<"Status : Waitng for shm2.cpp to update the value ...\n";

	while(true){

		//buffer->mtx.lock();	//lock mutex
		if(buffer->value == 2000000){
			//buffer->mtx.unlock();
			break;			
		}

		//buffer->mtx.unlock();	//unlock mutex
	}

	cout<<"Status : Updated value in Shared Memory ="<<buffer->value<<"\n";

	//unmap memory segment from process area
	munmap(shm_base_addr, sizeof(struct shm_buffer));
	//1 : base address of shared memory
	//2 : size of memory to unmap

	shm_unlink("/testSHM");	//release shared memory

	return 0;
}