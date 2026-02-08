#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include<ctime>
using namespace std;

int main(){
    // list of words
    vector<string> words = {"hangman","hello","useful","abcdeffg","nopes","important"};
    // ASCII draw of  the hangman
    vector<vector<string>> stages = {

    {   "+--+",
        "|  |",
        "   |",
        "   |",
        "   |",
        "   |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
        "   |",
        "   |",
        "   |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
        "|   |",
        "   |",
        "   |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
       "/|   |",
        "   |",
        "   |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
       "/|\\   |",
        "    |",
        "    |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
       "/|\\   |",
       "/    |",
        "    |",
        "****",
    },

    {   "+--+",
        "|  |",
        "0   |",
       "/|\\   |",
       "/ \\    |",
        "    |",
        "****",
    }  

    };

    // choose the random word
    srand(time(0));
    int index = rand() % words.size();
    string word = words[index];

    // length of hidden words in the form of blanks
    vector<string> hidden_word(word.size(), "_");

    int lives =6;

    while (lives>0){
        
        // show hidden words
        for (string ch : hidden_word) {
            cout << ch << " ";
        }
        cout<<endl;
        
        // guess the character everytime
        char ch;
        cout<<"Guess the character";
        cin>>ch;

        // check if character is there in the word guessed overall
        if (word.find(ch) != string::npos) {
            // check the indexing of the character 
            for (int i=0;i<word.size();i++){
                if (word[i]== ch){
                    hidden_word[i] = string(1, ch);
                    cout<<"correct guess"<<endl;
                }
            }
        }
        else{
            lives--;
            cout<<"Wrong guess! Lives left: "<<lives<<endl;
            for (string line : stages[6 - lives]) {
                cout << line << endl;
            }
        }

        bool won = true;
        for (string c : hidden_word) {
            if (c == "_") {
                won = false;
                break;
            }
        }

        if (won) {
            cout << "You won! The word was: " << word << endl;
            break;   // exit the loop
        }
    }

    if (lives == 0){
        cout<<"You lose!!"<<endl;
    }
    return 0;
}