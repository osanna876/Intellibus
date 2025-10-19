#include <iostream>
#include <string>
#include <algorithm>


using namespace std;

string classifyUrgency(string text) { 

    transform(text.begin(), text.end(), text.begin(), ::tolower);

    
    if (text.find("help") != string::npos ||
        text.find("trapped") != string::npos ||
        text.find("urgent") != string::npos ||
        text.find("emergency") != string::npos)
        return "Critical";

    
    else if (text.find("fire") != string::npos ||
             text.find("flood") != string::npos ||
             text.find("injury") != string::npos ||
             text.find("accident") != string::npos)
        return "High";

    
    else
        return "Low";
}

int main() {
    string input;
    cout << "Enter a description of the situation:\n> ";
    getline(cin, input);

    string level = classifyUrgency(input);
    cout << "\nUrgency Level: " << level << endl;

    return 0;
}
  