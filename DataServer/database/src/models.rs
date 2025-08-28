use sha2::{Digest, Sha256};

pub mod user {
    use diesel::{
        self, Selectable,
        prelude::{Insertable, Queryable},
    };
    use serde::{Deserialize, Serialize};

    diesel::table! {
        user_credentials (id) {
            id -> BigSerial,
            email ->Varchar,
            username -> Varchar,
            password -> Varchar,
            age -> SmallInt,
        }
    }

    #[derive(Debug, Selectable, Queryable)]
    #[diesel(table_name = user_credentials)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct User {
        pub id: i64,
        pub email: String,
        pub username: String,
        pub password: String,
        pub age: i16,
    }

    #[derive(Serialize, Deserialize, Debug, Insertable)]
    #[diesel(table_name = user_credentials)]
    pub struct NewUser {
        pub email: String,
        pub username: String,
        pub password: String,
        pub age: i16,
    }

    impl NewUser {
        pub fn new(email: String, login: String, passwd: String, age: i16) -> Self {
            /*
             *  Create an instance of User.
             *
             *  Arguments:
             *      email: user's email
             *      login: user's login
             *      passwd: user's passwd
             *      age: user's age
             */
            let mut hashed: Vec<String> = super::hash_fields_sha256(vec![passwd, login, email]);
            NewUser {
                email: hashed.pop().unwrap(),
                username: hashed.pop().unwrap(),
                password: hashed.pop().unwrap(),
                age,
            }
        }

        pub fn validate(&self) -> bool {
            return self.username.len() > 8 && self.password.len() > 8;
        }
    }
}

pub mod fetching {
    use chrono::{DateTime, NaiveDateTime, Utc};
    use diesel::{
        self, Selectable,
        prelude::{Insertable, Queryable},
    };
    use serde::{Deserialize, Serialize};
    use std::time::SystemTime;

    diesel::table! {
        videos (id) {
            id -> BigSerial,
            video_id ->Char,
        }
    }

    #[derive(Debug, Selectable, Queryable)]
    #[diesel(table_name = videos)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct Video {
        pub id: i64,
        pub video_id: String,
    }

    #[derive(Serialize, Deserialize, Debug, Insertable)]
    #[diesel(table_name = videos)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct NewVideo {
        pub video_id: String,
    }

    diesel::table! {
        video_snapshots (id) {
            id -> BigSerial,
            video_id ->BigInt,
            when_fetched -> Timestamp,
            title-> Varchar,
            views -> Bigint,
            description -> Varchar,
            likes ->Bigint,
            dislikes -> Bigint,
        }
    }

    #[derive(Selectable, Queryable)]
    #[diesel(table_name = video_snapshots)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct VideoSnapshot {
        pub id: i64,
        pub video_id: i64,
        pub when_fetched: NaiveDateTime,
        pub title: String,
        pub views: i64,
        pub description: String,
        pub likes: i64,
        pub dislikes: i64,
    }

    #[derive(Serialize, Deserialize, Insertable)]
    #[diesel(table_name = video_snapshots)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct NewVideoSnapshot {
        pub video_id: i64,
        pub when_fetched: NaiveDateTime,
        pub title: String,
        pub views: i64,
        pub description: String,
        pub likes: i64,
        pub dislikes: i64,
    }

    diesel::table! {
        comments (comment_id) {
            comment_id -> BigSerial,
            video_id -> Char,
            who_commented -> Char,
            content -> Char,
            when_posted -> Timestamp
        }
    }

    #[derive(Serialize, Deserialize, Insertable, Clone)]
    #[diesel(table_name = comments)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct NewComment {
        pub video_id: String,
        pub who_commented: String,
        pub content: String,
        pub when_posted: NaiveDateTime,
    }

    #[derive(Serialize, Selectable, Queryable)]
    #[diesel(table_name = comments)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct Comment {
        pub comment_id: i64,
        pub video_id: String,
        pub who_commented: String,
        pub content: String,
        pub when_posted: NaiveDateTime,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct FetchedComment {
        pub who_commented: String,
        pub content: String,
        pub when_posted: NaiveDateTime,
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct VideoResponse {
        pub id: String,
        pub channelid: String,
        pub published: NaiveDateTime,
        pub title: String,
        pub views: i64,
        pub description: String,
        pub likes: i64,
        pub dislikes: i64,
        pub thumbnail: String,
        pub comments: Vec<FetchedComment>,
    }

    diesel::table! {
        thumbnails (id) {
            id -> BigSerial,
            video_id -> Char,
            thumbnail_path -> Char,
        }
    }

    #[derive(Serialize, Deserialize, Insertable)]
    #[diesel(table_name = thumbnails)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct NewThumbnail {
        pub video_id: String,
        pub thumbnail_path: String,
    }

    #[derive(Serialize, Selectable, Queryable)]
    #[diesel(table_name = thumbnails)]
    #[diesel(check_for_backend(diesel::pg::Pg))]
    pub struct Thumbnail {
        pub id: i64,
        pub video_id: String,
        pub thumbnail_path: String,
    }
}

fn hash_fields_sha256(fields: Vec<String>) -> Vec<String> {
    /*
     *  Helper function for field hashing.
     *
     *  Arguments:
     *      fields: Vector of fields to be hashed
     *
     *  Returns:
     *      Vector hashed by SHA256 algorithm, the fields are returned
     *      in the same order as they were passed
     */
    fields
        .into_iter()
        .map(|field| {
            let mut hasher = Sha256::new();
            hasher.update(field);
            let hash_result = hasher.finalize();
            format!("{:x}", hash_result)
        })
        .collect()
}
