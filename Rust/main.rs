
use std::io;

fn main() {
    xy();
    println!("Welcome to guess the numbers");
    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin().read_line(&mut guess)
        .ok()
        .expect("Failed to read line");

    println!("You guessed: {}", guess);
    
}

fn xy() {
    let x = 5;
    let y = 10;
    println!("x and y: {} and {}", x, y);
}
