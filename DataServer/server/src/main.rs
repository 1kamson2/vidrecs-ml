use axum::routing::post;
use axum::{Router, body::Body, response::Json, routing::get};
use clap::Parser;
use database::api::{_fill_up, login, register, request_game};
use database::requests::Message;
use serde_json::{Value, json};

#[derive(Parser)]
struct StartupCfg {
    host: String,
    port: String,
}

#[tokio::main]
async fn main() {
    let args: StartupCfg = StartupCfg::parse();
    assert!(args.host.len() != 0, "You didn't provide hostname.");
    assert!(args.port.len() == 4, "You didn't provide correct port.");

    let router: Router<_> = Router::new()
        .route("/api/login", post(login))
        .route("/api/register", post(register))
        .route("/api/request_game", post(request_game))
        .route("/api/admin/fillup", post(_fill_up))
        .route("/api/sync", get(not_implemented))
        .route("/api/check_health", get(not_implemented))
        .route("/api/echo", get(not_implemented));

    let listener = tokio::net::TcpListener::bind(format!("{}:{}", args.host, args.port))
        .await
        .unwrap();
    axum::serve(listener, router).await.unwrap();
}

async fn not_implemented() -> Json<Value> {
    Json(json!({"content": "Not implemented, sorry!"}))
}
