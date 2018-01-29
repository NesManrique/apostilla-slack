from requests.sessions import Session
from slackclient import SlackClient
import argparse
from time import sleep
import os
import datetime
from pytz import timezone

def main():
    parser = argparse.ArgumentParser(description="Sends message to slack channel if page is up.")
    parser.add_argument(
        '-c',
        '--channel',
        required=False,
        default='#apostilla',
        help='Channel where the message will be posted. Default: #apostilla'
    )
    parser.add_argument(
        '-u',
        '--url',
        required=False,
        default='citaslegalizaciones.mppre.gob.ve',
        help='URL to check. Defaults to citaslegalizaciones.mppre.gob.ve'
    )
    parser.add_argument(
        '-t'
        '--timezone',
        required=False,
        default='America/Bogota',
        help='Timezone for the dates. Defaults to America/Bogota'
    )
    parser.add_argument(
        '-s',
        '--sleeptime',
        required=False,
        default=300,
        help='Amount of seconds to wait to check if the page is up again. Default: 300.'
    )
    parser.add_argument(
        '-d',
        '--downtime',
        required=False,
        default=360,
        help=('Amount of minutes to send a summary msg to the channel for how long we '
              'have been checking and the page is still down. Default: 360 (6 hours).')
    )
    args = parser.parse_args()
    try:
        slack_token = os.environ["SLACK_API_TOKEN"]
    except Exception as e:
        print('Environment variable SLACK_API_TOKEN is not defined')
        exit(1)
    sc = SlackClient(slack_token)
    req_session = Session()
    url = 'https://isitup.org/{0}.json'.format(args.url)

    start_t = datetime.datetime.now(timezone(args.timezone))
    while True:
        try:
            response = req_session.get(url)
            response.raise_for_status()
        except Exception as e:
            sc.api_call(
              "chat.postMessage",
              channel=args.channel,
              text="Lmao, isitup.com is the one that is down!!"
            )
            sleep(args.sleeptime)
            continue
        else:
            jsonR = response.json()
            if jsonR['status_code'] == 1:
                sc.api_call(
                  "chat.postMessage",
                  channel=args.channel,
                  text=":thumbsup: The page *http://{0}* is *UP*!!".format(args.url)
                )
                sleep(args.sleeptime)
                start_t = datetime.datetime.now(timezone(args.timezone))
            elif jsonR['status_code'] == 2:
                end_t = datetime.datetime.now(timezone(args.timezone))
                elapsed = end_t - start_t
                if elapsed > datetime.timedelta(minutes=args.downtime):
                    sc.api_call(
                      "chat.postMessage",
                      channel=args.channel,
                      text=(":disappointed: I am sorry to report that *http://{0}* has been *down* for more "
                            "than {1} minutes (counted since: {2})").format(args.url,args.downtime,start_t.strftime("%Y-%m-%d %H:%M"))
                    )
                    start_t = datetime.datetime.now(timezone(args.timezone))
                sleep(args.sleeptime)
            elif jsonR['status_code'] == 3:
                print('*{}* does not appear to be a valid domain.'.format(args.url))
                print("Please enter both the domain name AND the suffix (ex: *amazon.com* or *whitehouse.gov*).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...\n")
        exit(0)
