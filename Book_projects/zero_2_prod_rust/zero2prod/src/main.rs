use std::net::TcpListener;
use zero2prod::run;

#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
    let listener = TcpListener::bind("127.0.0.1:0").expect("Failed to bind random port");
    let address = listener.local_addr().unwrap();
    println!("runing server on: http://{address}");
    run(listener)?.await
}
