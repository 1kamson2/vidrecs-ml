use chrono::Utc;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[repr(u8)]
pub enum MessageStatus {
    Success = 0,
    Failure = 1,
    Pending = 2,
}

#[derive(Deserialize, Serialize)]
pub struct LoginContent {
    pub username: String,
    pub password: String,
}

#[derive(Serialize, Deserialize)]
pub struct RegisterContent {
    pub email: String,
    pub username: String,
    pub password: String,
    pub age: i16,
}
#[derive(Serialize, Deserialize)]
pub struct GameForm {
    pub request: String,
    pub token: String,
}

#[derive(Serialize, Deserialize)]
pub struct Message<T> {
    pub id: u64,
    pub sender: String,
    pub receiver: String,
    pub timestamp: String,
    pub status: MessageStatus,
    pub content: Option<T>,
}

impl<T> Message<T> {
    pub fn new(
        id: u64,
        sender: String,
        receiver: String,
        success: MessageStatus,
        content: T,
    ) -> Self {
        Message {
            id,
            sender,
            receiver,
            timestamp: format!("{}", Utc::now()),
            status: success,
            content: Some(content),
        }
    }

    pub fn make_message<S>(mut self, response: S) -> Message<S> {
        /*
         * Construct Message as response to given request or request to given response.
         * It consumes the entire request making it unusable later.
         *
         *  Arguments:
         *      response: What should be the content of the message.
         *
         *  Returns:
         *      Response to request.
         */

        // We swap the values between sender and receiver.
        // We use sender as receiver and receiver as a sender.
        std::mem::swap(&mut self.sender, &mut self.receiver);
        return Message::<S>::new(
            self.id + 1,
            self.receiver,
            self.sender,
            MessageStatus::Success,
            response,
        );
    }

    pub fn with_id(&mut self, id: u64) -> &mut Self {
        self.id = id;
        self
    }

    pub fn with_sender(&mut self, sender: String) -> &mut Self {
        self.sender = sender;
        self
    }

    pub fn with_receiver(&mut self, receiver: String) -> &mut Self {
        self.receiver = receiver;
        self
    }

    pub fn with_status(&mut self, status: MessageStatus) -> &mut Self {
        self.status = status;
        self
    }

    pub fn with_content(&mut self, content: T) -> &mut Self {
        self.content = Some(content);
        self
    }
}
