use diesel::{prelude::*, result::Error};

use crate::models::{
    fetching::{VideoResponse, VideoSnapshot},
    user::{User, user_credentials},
};

pub fn establish_connection(
    username: String,
    password: String,
    database_name: String,
) -> PgConnection {
    /*
     *  Try to establish connection with a database.
     *  WARNING: You should never use this function outside this crate.
     *
     *  Arguments:
     *      username: A username used for connecting to a database.
     *      password: A credentials for a user.
     *
     *  Returns:
     *      Result with connection or error.
     */
    // TODO: For now only localhost
    let db_url = format!("postgres://{username}:{password}@localhost:5431/{database_name}");

    // TODO: Fix it later
    PgConnection::establish(&db_url).unwrap()
}

pub fn insert_user(email: String, login: String, password: String, age: i16) -> bool {
    // Encapsulate this import
    use crate::models::user::{NewUser, User, user_credentials::table};
    let new_account = NewUser::new(email, login, password, age);
    let conn = &mut establish_connection("postgres".into(), "postgres".into(), "USERS_INFO".into());

    match diesel::insert_into(table)
        .values(&new_account)
        .returning(User::as_returning())
        .get_result(conn)
        .ok()
    {
        Some(_) => true,
        None => false,
    }
}

pub fn fetch_user(login_hashed: &String, passwd_hashed: &String) -> Option<User> {
    use crate::models::user::user_credentials::dsl::*;
    // WARNING: Change user, too much privileges
    let conn = &mut establish_connection("postgres".into(), "postgres".into(), "USERS_INFO".into());

    user_credentials
        .filter(username.eq(login_hashed))
        .filter(password.eq(passwd_hashed))
        .select(User::as_select())
        .first(conn)
        .ok()
}

pub fn insert_videos(videos: Vec<VideoResponse>) -> bool {
    use crate::models::fetching::{NewVideo, NewVideoSnapshot, Video, VideoSnapshot};
    use crate::models::fetching::{video_snapshots, videos};

    let conn =
        &mut establish_connection("postgres".into(), "postgres".into(), "GAMES_STATS".into());

    for video in videos {
        let new_vid = diesel::insert_into(videos::table)
            .values(NewVideo { video_id: video.id })
            .returning(Video::as_returning())
            .get_result(conn)
            .ok()
            .unwrap();
        diesel::insert_into(video_snapshots::table)
            .values(NewVideoSnapshot {
                video_id: new_vid.id,
                when_fetched: video.published,
                title: video.title,
                views: video.views,
                description: video.description,
                likes: video.likes,
                dislikes: video.dislikes,
            })
            .returning(VideoSnapshot::as_returning())
            .get_result(conn)
            .ok()
            .unwrap();
    }
    return true;
}
