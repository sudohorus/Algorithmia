#include <iostream>
#include <string>

int main(){
    //variable to store the user input
    std::string input;

    //initial message
    std::cout << "Algorithmia" << std::endl;
    std::cout << "':q' to exit" << std::endl;

    //main loop to keep the IDE running and take user commands
    while (true){
        //display the prompt symbol '>' and wait for user inpuit
        std::cout << "> ";
        std::getline(std::cin, input); //read the entire line of input

        //check if the user entered the quit command
        if (input == ":q"){
            break; //exit the loop
        }

        //for now, simply echo the command back to the user
        std::cout << "Command: " << input << std::endl;
    }

    //exit message when the ide is closed
    std::cout << "exiting algorithmia..." << std::endl;
    return 0;
}
