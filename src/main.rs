use std::env;
use std::net::{IpAddr, SocketAddr, TcpStream, ToSocketAddrs};
use std::process;
use std::time::{Duration, SystemTime};

const RED: &str = "\x1b[91m";
const GREEN: &str = "\x1b[92m";
const YELLOW: &str = "\x1b[93m";
const BLUE: &str = "\x1b[94m";
const RED_REV: &str = "\x1b[07;91m";
const YELLOW_REV: &str = "\x1b[07;93m";
const DEFCOL: &str = "\x1b[00m";

fn resolve_target(input: &str) -> Result<IpAddr, String> {
    let mut addrs = (input, 0)
        .to_socket_addrs()
        .map_err(|_| "Hostname could not be resolved".to_string())?;

    addrs
        .find(|addr| matches!(addr.ip(), IpAddr::V4(_) | IpAddr::V6(_)))
        .map(|addr| addr.ip())
        .ok_or_else(|| "Hostname could not be resolved".to_string())
}

fn scan_port(target: IpAddr, port: u16) -> bool {
    let timeout = Duration::from_secs(1);
    let socket_addr = SocketAddr::new(target, port);
    TcpStream::connect_timeout(&socket_addr, timeout).is_ok()
}

fn main() {
    println!("\t{YELLOW_REV}[ PORT SCANNER ]{DEFCOL}");

    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!(
            "{RED_REV}[ Error : Invalid amount of arguments, target hostname required ]{DEFCOL}"
        );
        eprintln!("Usage: cargo run -- <hostname-or-ip>");
        process::exit(1);
    }

    let target_input = &args[1];
    let target = match resolve_target(target_input) {
        Ok(ip) => ip,
        Err(err) => {
            eprintln!("{RED_REV}[ Error : {err} ]{DEFCOL}");
            process::exit(1);
        }
    };

    println!("{}", "-".repeat(50));
    println!("[{YELLOW}${DEFCOL}] Scanning target : {GREEN}{target}{DEFCOL}");
    println!(
        "[{YELLOW}${DEFCOL}] Scanning started at : {BLUE}{:?}{DEFCOL}",
        SystemTime::now()
    );
    println!("{}", "-".repeat(50));

    let mut open_ports = Vec::new();

    for port in 1..=65535u16 {
        if scan_port(target, port) {
            println!("[{GREEN}!{DEFCOL}] Port {YELLOW}{port}{DEFCOL} : {GREEN}open{DEFCOL}");
            open_ports.push(port);
        } else {
            println!("[{RED}!{DEFCOL}] Port {YELLOW}{port}{DEFCOL} : {RED}closed{DEFCOL}");
        }
    }

    println!(
        "\n[ Number of open ports found on target server : {YELLOW}{}{DEFCOL} ]",
        open_ports.len()
    );
}
