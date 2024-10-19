#include <iostream>
#include <string>
#include <fstream> //file handling
#include <vector> //to store lines of the file
#include <dirent.h> //directory handling

void listFiles(){
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

std::string autocomplete(const std::vector<std::string>& files, const std::string& input) {
    std::vector<std::string> matches;

    //check for matches based on input
    for (const auto& file : files) {
        if (file.find(input) == 0) { //match if the file name starts with the input
            matches.push_back(file);
        }
    }

    //if theres only one match, return it
    if (matches.size() == 1) {
        return matches[0]; //return the matched file name
    } else if (matches.size() > 1) {
        std::cout << "Possible matches:" << std::endl;
        for (const auto& match : matches) {
            std::cout << " - " << match << std::endl; //display possible matches
        }
    }

    return ""; //return empty if no unique match found
}


int main(){
    //variable to store the user input
    std::string input;
    std::vector<std::string> fileLines; //vector to store lines of the file
    std::vector<std::string> files; //vector to store the file names

    std::cout << "Algorithmia" << std::endl;
    std::cout << "':q' to exit." << std::endl;
    std::cout << "':of <filename>' to open a file." << std::endl;
    std::cout << "':lfs' to list files in the current directory." << std::endl;

    //main loop to keep the IDE running and take user commands
    while (true){
        //display the prompt symbol '>' and wait for user inpuit
        std::cout << "> ";
        std::getline(std::cin, input); //read the entire line of input                               

        //check if the user entered the quit command
        if (input == ":q"){
            break; //exit the loop
        }else if(input == ":lfs"){
            listFiles(); //list files
        }else if (input.substr(0, 4) == ":of ") {
            std::string filename = input.substr(4); //get the filename from the command

            //ff the user has not entered a filename, prompt for one
            if (filename.empty()) {
                std::cout << "Please enter the filename: ";
                std::getline(std::cin, filename);
            }

            //try to autocomplete the filename
            std::string autocompleted = autocomplete(files, filename);
            if (!autocompleted.empty()) {
                filename = autocompleted; //use the autocompleted filename
            }

            if (filename.empty()) {
                std::cout << "Please provide a filename." << std::endl;
            } else {
                openFile(filename, fileLines);
                displayFile(fileLines);
            }
        } else {
            std::cout << "Command: " << input << std::endl; //echo other commands
        }
    }
    

    std::cout << "exiting algorithmia..." << std::endl;  
    return 0;
}
