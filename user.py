import pandas as pd

def df_tweet(user):
    Tweets = []
    neutral_list = []
    negative_list = []
    positive_list = []
    source = []
    follower = []
    screen_name = []
    in_reply_to_status_id = []
    in_reply_to_screen_name = []
    location = []
    friends_count = []
    statuses_count = []
    created_at = []
    created_at_us = []
    status_id = []
    reply = []
    retweet_count = []
    favorite_count = []
    hashtags = []
    user_mentions = []
    
    for tweet in user:
        Tweets.append(tweet.full_text)
        status_id.append(tweet.id_str)
        created_at.append(tweet.created_at)
        source.append(tweet.source)
        in_reply_to_status_id.append(tweet.in_reply_to_status_id_str)
        in_reply_to_screen_name.append(tweet.in_reply_to_screen_name)
        retweet_count.append(tweet.retweet_count)
        favorite_count.append(tweet.favorite_count)
        location.append(tweet.user.location)
        follower.append(tweet.user.followers_count)
        screen_name.append(tweet.user.screen_name)
        friends_count.append(tweet.user.friends_count)
        statuses_count.append(tweet.user.statuses_count)
        created_at_us.append(tweet.user.created_at)

    tw_list = pd.DataFrame()
    tw_list["Tweets"] = Tweets
    tw_list["source"] = source
    tw_list["follower"] = follower
    tw_list["screen_name"] = screen_name
    tw_list["in_reply_to_status_id"] = in_reply_to_status_id
    tw_list["in_reply_to_screen_name"] = in_reply_to_screen_name
    tw_list["location"] = location
    tw_list["friends_count"] = friends_count
    tw_list["statuses_count"] = statuses_count
    tw_list["created_at"] = created_at
    tw_list["created_at_us"] = created_at_us
    tw_list["status_id"] = status_id
    tw_list["retweet_count"] = retweet_count
    tw_list["favorite_count"] = favorite_count
    return (tw_list)
