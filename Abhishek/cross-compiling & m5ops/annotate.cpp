#include <iostream>
#include <unistd.h>
#include <dirent.h>

#include <gem5/m5ops.h>

//write : it writes the output to standard output
//It reads all the files and folders name in current directory and outputs to std out

int main(){
    m5_work_begin(0, 0);
    write(1, "This will be output to standard out\n", 36);
    m5_work_end(0, 0);

    struct dirent *d;
    DIR *dr;
    dr = opendir(".");
    if (dr!=NULL) {
        std::cout<<"List of Files & Folders:\n";
        for (d=readdir(dr); d!=NULL; d=readdir(dr)) {
            std::cout<<d->d_name<< ", ";
        }
        closedir(dr);
    }
    else {
        std::cout<<"\nError Occurred!";
    }
    std::cout<<std::endl;
}