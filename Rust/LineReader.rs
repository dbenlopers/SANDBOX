use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let f = match File::open("/home/akopp/Desktop/TEST.csv") {
        Ok(f) => f,
        Err(..) => panic!("Boom"),
    };
    let reader = BufReader::new(&f);

    for line in reader.lines() {
        let mut print = line.unwrap();
        println!("{:?}", print);
    }
}
