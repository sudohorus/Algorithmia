#include <iostream>
#include <string>
#include <fstream> //file handling
#include <vector> //to store lines of the file

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


int main(){
    //variable to store the user input
    std::string input;
    std::vector<std::string> fileLines; //vector to store lines of the file

    std::cout << "Algorithmia" << std::endl;
    std::cout << "':q' to exit." << std::endl;
    std::cout << "':of <filename>' to open a file." << std::endl;

    //main loop to keep the IDE running and take user commands
    while (true){
        //display the prompt symbol '>' and wait for user inpuit
        std::cout << "> ";
        std::getline(std::cin, input); //read the entire line of input

        //check if the user entered the quit command
        if (input == ":q"){
            break; //exit the loop
        }else if(input.substr(0, 4) == ":of "){
            std::string filename = input.substr(4); //get the filename
            if(filename.empty()){
                std::cout << "[ERROR] Please provide a filename." << std::endl;
            }else{
                openFile(filename, fileLines); //open the file and read lines
                displayFile(fileLines); //display the content of the file
            }                                        
        }else{
            std::cout << "Command: " << input << std::endl; //echo other commands
        }
    }

    std::cout << "exiting algorithmia..." << std::endl;  
    return 0;
}
