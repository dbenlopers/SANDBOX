import std.stdio, std.string;

void main(string[] args){
    File file = File("/home/akopp/Desktop/TEST.csv", "r");

    while (!file.eof()) {
        string line = strip(file.readln());
        writeln("read line -> |", line);
    }
}
