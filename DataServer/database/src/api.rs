use super::models::user::NewUser;
use axum::{Json, extract};
use chrono::prelude::*;
use reqwest::Client;
use serde_json::{Value, json};
use uuid::Uuid;

const VALID_MESSAGE: bool = true;
const INVALID_ID: u64 = 0x7fffffffffffff;
const INVALID_ID_MESSAGE: &str = "Incorrect id";
const INVALID_SENDER: &str = "Incorrect sender";
const INVALID_RECEIVER: &str = "Incorrect receiver";
const INVALID_CONTENT: &str = "Incorrect content";
const INVALID_CREDENTIALS: &str = "Incorrect credentials";

use crate::{
    models::{
        fetching::{Video, VideoResponse},
        user::User,
    },
    pg::{fetch_user, insert_user, insert_videos},
    requests::{GameForm, LoginContent, Message, MessageStatus, RegisterContent},
};

pub async fn validate_request<T>(payload: &Message<T>) -> Result<bool, String> {
    if payload.id == INVALID_ID {
        return Err(String::from(INVALID_ID_MESSAGE));
    }

    if payload.sender == "" {
        // WARNING: This server should hold globally an array of allowed hosts.
        return Err(String::from(INVALID_SENDER));
    }

    if payload.receiver == "" {
        return Err(String::from(INVALID_RECEIVER));
    }

    match payload.content {
        None => return Err(String::from(INVALID_CONTENT)),
        Some(_) => return Ok(VALID_MESSAGE),
    }
}

pub async fn login(extract::Json(payload): extract::Json<Message<LoginContent>>) -> Json<Value> {
    // TODO: The id should be present in the request
    // WARNING: Success hold to the last minute right before sending.
    let _ = match validate_request(&payload).await {
        Err(err) => return Json(json! {payload.make_message::<String>(err)}),
        Ok(res) => res,
    };

    let content = payload.content.as_ref().unwrap();
    match fetch_user(&content.username, &content.password) {
        None => Json(json! {
            payload.make_message::<String>(String::from(INVALID_CREDENTIALS))
        }),

        Some(_) => Json(json! {payload.make_message::<String>(Uuid::new_v4().into())
        }),
    }
}

pub async fn register(extract::Json(payload): extract::Json<Message<NewUser>>) -> Json<Value> {
    let _ = match validate_request(&payload).await {
        Err(err) => return Json(json! {payload.make_message::<String>(err)}),
        Ok(res) => res,
    };

    let content = payload.content.as_ref().unwrap();
    if !content.validate() {
        return Json(json! {payload.make_message::<String>(String::from(INVALID_CREDENTIALS))});
    }

    match insert_user(
        content.email.clone(),
        content.username.clone(),
        content.password.clone(),
        content.age.clone(),
    ) {
        false => Json(json! {
        payload.make_message::<String>(String::from(INVALID_CREDENTIALS))
        }),

        true => Json(json! {
            payload.make_message::<String>("New user created!".into())
        }),
    }
}

pub async fn request_game(extract::Json(payload): extract::Json<Message<GameForm>>) -> Json<Value> {
    let _ = match validate_request(&payload).await {
        Err(err) => return Json(json! {payload.make_message::<String>(err)}),
        Ok(res) => res,
    };

    let req = Client::new()
        .post("http://localhost:8080/api/search")
        .json(&payload)
        .send()
        .await
        .unwrap();

    let resp: Message<Vec<VideoResponse>> = req.json().await.unwrap();
    let content: Vec<VideoResponse> = resp.content.clone().unwrap();
    insert_videos(content); // TODO: Add error handling 
    Json(json! {resp})
}
