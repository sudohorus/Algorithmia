#include <iostream>
#include <string>
#include <fstream> //file handling
#include <vector> //to store lines of the file
#include <dirent.h> //directory handling
#include <termios.h>
#include <unistd.h>

enum Mode { NAVIGATION, INSERTION };

//disable buffered input and set terminal to capture key presses immediately
void setRawMode(bool enable){
    static struct termios oldt, newt;
    if (enable){
        tcgetattr(STDIN_FILENO, &oldt); //save terminal settings
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO); //disable canonical mode and echo
        tcsetattr(STDIN_FILENO, TCSANOW, &newt); //set new terminal settings
    }else{
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt); //restore original terminal settings
    }
}

void listFilesDirectory(){
    DIR *dir;
    struct dirent *ent;
    dir = opendir("."); //open the current directory
    if (dir != nullptr){
        std::cout << "files in the current directory: " << std::endl;
        while ((ent = readdir(dir)) != nullptr){
            std::cout << " - " << ent->d_name << std::endl; //print each file name
        }
        closedir(dir); //close the directory
    }else{
        std::cout << "[ERROR] Could not open the current directory." << std::endl;
    }
}

void openFile(const std::string& filename, std::vector<std::string>& lines){
    std::ifstream file(filename); //open the file
    if (!file){
        std::cout << "[ERROR] Opening file: " << filename << std::endl;
        return;
    }

    std::string line;
    lines.clear(); //clear existing lines
    while (std::getline(file, line)){
        lines.push_back(line); //store each line in the vector
    }
    file.close(); //close file
}

void displayFile(const std::vector<std::string>& lines){
    for (const auto& line : lines){
        std::cout << line << std::endl; //print each line
    }
}

void saveFile(const std::string& filename, const std::vector<std::string>& lines){
    std::ofstream file(filename);
    if (!file){
        std::cout << "[ERROR] Error on saving file: " << filename << std::endl;
        return;
    }

    for (const auto& line : lines){
        file << line << std::endl;
    }
    file.close();
    std::cout << "File saved: " << filename << std::endl;
}

void editFile(std::vector<std::string>& lines){
    std::cout << "Entering INSERT mode (press ESC to got back to NAVIGATION mode)" << std::endl;
    setRawMode(true); //enable raw mode to capture individual key presses
    std::string newLine;
    while(true){
        char ch;
        read(STDIN_FILENO, &ch, 1); //capture single character
        
        if (ch == 27){ //ESC key
            break;
        }else if (ch == '\n'){ //enter key
            lines.push_back(newLine);
            newLine.clear();
            std::cout << std::endl;
        }else{
            newLine.push_back(ch);
            std::cout << ch;
        }
    }
    setRawMode(false); //disable raw mode after editing
}

int main(){
    //variable to store the user input
    std::string input;
    std::vector<std::string> fileLines; //vector to store lines of the file
    std::string currentFile;
    std::vector<std::string> files; //vector to store file names
    Mode mode = NAVIGATION; //start in navigation mode

    std::cout << "Algorithmia" << std::endl;
    std::cout << "':q' to exit." << std::endl;
    std::cout << "':of <filename>' to open a file." << std::endl;

    std::cout << "':lfs' to list files in the current directory." << std::endl;

    //main loop to keep the IDE running and take user commands
    while (true){
        if (mode == NAVIGATION){
            std::cout << "> ";
            std::getline(std::cin, input);

            if(input == ":q"){
                break;
            }else if(input.substr(0, 4) == ":of"){
                std::string filename = input.substr(4); //get the filename from the command
                
                //if the user has no entered a filename, prompt for one
                if (filename.empty()){
                    std::cout << "Please enter the filename: ";
                    std::getline(std::cin, filename);
                }

                if (filename.empty()){
                    std::cout << "[ERROR] Please provide a filename." << std::endl;
                }else{
                    openFile(filename, fileLines);
                    displayFile(fileLines);
                }
            }else if(input == ":w" && !currentFile.empty()){
                saveFile(currentFile, fileLines);
            }else if(input == ":lfs"){
                listFilesDirectory();
            }else if(input == "i"){
                mode = INSERTION;
            }else{
                std::cout << "[ERROR] Unknown command: " << input << std::endl; 
            }
        }else if(mode == INSERTION){
            editFile(fileLines);
            mode = NAVIGATION;
        }
    }
    

    std::cout << "exiting algorithmia..." << std::endl;  
    return 0;
}
