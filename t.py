import tweepy
import requests

# Twitter APIの
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# LINE Notifyのトークン
line_notify_token = 'YOUR_LINE_NOTIFY_TOKEN'

# LINE Notifyに通知を送る関数
def send_line_notify(message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    requests.post(line_notify_api, headers=headers, data=data)

# Twitterのフォローイベントハンドラ
class FollowStreamListener(tweepy.StreamListener):
    def on_event(self, event):
        if event['event'] == 'follow':
            user_id = event['source']['id_str']
            user_screen_name = event['source']['screen_name']
            message = f'{user_screen_name}さんがフォローしました！'
            send_line_notify(message)

# Twitter APIの認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# フォローイベントをリッスンするストリーム
stream_listener = FollowStreamListener()
stream = tweepy.Stream(auth=auth, listener=stream_listener)

# 特定のユーザのフォローイベントをフィルタリング
follow_user_id = 'TARGET_USER_ID'
stream.filter(follow=[follow_user_id], is_async=True)
