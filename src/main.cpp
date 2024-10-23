#include <iostream>
#include <fstream>
#include <string>
#include <ncurses.h>
#include <vector>

void save_file(const std::string &filename, const std::vector<std::string> &lines) {
    std::ofstream file(filename);
    if (file.is_open()) {
        for (const auto &line : lines) {
            file << line << std::endl;
        }
        file.close();
    } else {
        std::cerr << "[ERROR]Could not save file " << filename << std::endl;
    }
}

void show_help(){
    printw("Commands:\n");
    printw(":w   - Save File\n");
    printw(":q   - Leave editor\n");
    printw(":q!  - Leave without save\n");
    printw(":h   - Show help menu (this menu)\n");
    printw("Press any key to continue...\n");
    refresh();
    getch(); // Aguarda uma tecla para voltar
}

//argc vai contar o número de argumentos passados na linha de comando
//argv é o vetor que c ontem os argumentos passados
//o primeiro argumento (argv[0]) é sempre o nome do programa
int main(int argc, char* argv[]){
    //ele verifica se o usuario passou o nome do arquivo como argumento
    //se o usuario nao passou o nome do arquivo, imprime uma mensagem de uso e encerra
    if(argc < 2){
        std::cout << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1; //caso retorna 1, ele indica que o programa foi encerrado com erro
    }

    //inicializando a biblioteca ncurses
    initscr(); //inicia o modo ncurses
    cbreak(); //desativa o buffer de linha, recebemos as entradas imediatamente
    keypad(stdscr, TRUE); //habilita o uso de teclas especiais como setas
    noecho(); //impede que o input do usuario seja mostrado na tela automaticamente
    curs_set(1); //mostra o cursor

    //cria um objeto ifstream (input file stream) para abrir o arquivo no modo leitura
    std::ifstream file(argv[1]); //argv[1] é o nome do arquivo passado pelo usuario
    if (!file.is_open()){ //verifica se o arquivo foi aberto com sucesso
        //se o arquivo nao puder ser aberto, imprime uma mensagem de erro
        endwin(); //encera ncurses antes de sair
        std::cout << "[ERROR]Could not open file " << argv[1] << std::endl;
        return 1; //retorna 1 que indica erro
    }
    //cria uma variavel para armazenar cada linha do arquivo e a posição do cursos
    std::vector<std::string> lines;
    std::string line;

    //exibe o conteudo do arquivo na tela
    while(std::getline(file, line)){
        lines.push_back(line); //imprime linha
    }
    file.close();

    //movimentação do cursos
    int row = 0, col = 0;
    int top_line = 0; //linha superior visivel
    int max_lines = LINES - 1; //quantidade de linhas visiveis no terminal, -1 para a linha de comandos

    //funcao para "desenhar" o conteudo visivel na tela
    auto draw_screen = [&](int top_line){
        clear(); //limpa a tela
        for (int i = 0; i < max_lines - 1; ++i){ //deixa uma linha para comandos no final
            if (top_line + i < lines.size()){
                mvprintw(i, 0, "%s", lines[top_line + i].c_str());
            }
        }
        move(row, col); //move o cursor para posição atual
        refresh(); //atualiza a tela
    };

    //desenha a tela pela primeira vez
    draw_screen(top_line);

    int ch;
    std::string command; //variavel de comando
    bool command_mode = false; //flag para o modo de comando

    while ((ch = getch()) != 'q') {
        if (command_mode) {
            if (ch == '\n') { //executa o comando ao pressionar Enter
                if (command == "w") { //comando para salvar
                    save_file(argv[1], lines);
                }
                command.clear(); //limpa o comando
                command_mode = false; //sai do modo de comando
            } else if (ch == 27) { //ESC para sair do modo de comando
                command.clear(); //limpa o comando
                command_mode = false; //sai do modo de comando
            } else {
                command += ch; //adiciona caractere ao comando
            }
        } else {
            switch (ch) {
                case KEY_UP:
                    if (row > 0) {
                        row--;
                    } else if (top_line > 0) {
                        top_line--;
                    }
                    break;
                case KEY_DOWN:
                    if (row < max_lines - 1 && top_line + row + 1 < lines.size()) {
                        row++;
                    } else if (top_line + max_lines < lines.size()) {
                        top_line++;
                    }
                    break;
                case KEY_LEFT:
                    if (col > 0) col--;
                    break;
                case KEY_RIGHT:
                    if (col < COLS - 1) col++;
                    break;
                case ':': //entrar no modo de comando
                    command_mode = true;
                    command.clear(); //limpa o comando
                    break;
                case 'e': { //entrar no modo de edição (opcional)
                    std::string &current_line = lines[top_line + row];
                    int original_col = col;
                    echo(); //mostra o que o usuário digita
                    while (true) {
                        clear(); //limpa a tela
                        for (int i = 0; i < max_lines; ++i) {
                            if (top_line + i < lines.size()) {
                                mvprintw(i, 0, "%s", lines[top_line + i].c_str());
                            }
                        }
                        mvprintw(max_lines, 0, ": %s", command.c_str()); //mostra o comando na linha de comando
                        move(row, col); //move o cursor
                        refresh(); //atualiza a tela

                        ch = getch();
                        if (ch == 27) { //ESC para sair do modo de edição
                            break;
                        } else if (ch == KEY_BACKSPACE || ch == 127) { //backspace para remover
                            if (col > 0) {
                                col--;
                                current_line.erase(current_line.begin() + col);
                            }
                        } else if (ch == KEY_DC) { //deletar
                            if (col < current_line.size()) {
                                current_line.erase(current_line.begin() + col);
                            }
                        } else if (ch == KEY_HOME) {
                            col = 0; //move para o início da linha
                        } else if (ch == KEY_END) {
                            col = current_line.size(); //move para o final da linha
                        } else if (ch == '\n') { //enter para nova linha (opcional)
                            lines.insert(lines.begin() + top_line + row + 1, ""); //insere uma nova linha
                            row++;
                            col = 0; //move para a nova linha
                        } else if (isprint(ch)) { //verifica se o caractere é imprimível
                            current_line.insert(current_line.begin() + col, ch); //insere o caractere na posição
                            col++; //move o cursor para a direita
                        }

                        if (col > current_line.size()) {
                            col = current_line.size(); //ajusta o cursor se for maior que a linha
                        }
                    }
                    noecho(); //esconde o que o usuário digita
                    break;
                }
            }
        }

        draw_screen(top_line);
        if (command_mode) {
            mvprintw(max_lines, 0, ": %s", command.c_str()); //mostra o comando na linha de comando
        }
    }
    //encerra o modo ncurses e restaura o terminal
    endwin();
    //return 0, indica o fim do programa com sucesso
    return 0;
}
