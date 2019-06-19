import smtplib, ssl
import praw
import datetime
now = datetime.datetime.now()
redditLink = "https://www.reddit.com"

def get_submission_matches(target_file):
    sub = 'NintendoSwitchDeals'
    game_list = get_targets_list(target_file)

    reddit = praw.Reddit(client_id = 'your_client_id',
                         client_secret = 'your_client_secret',
                         username = 'your_username',
                         password = 'your_password',
                         user_agent = "reddit Parser")


    subreddit = reddit.subreddit(sub)
    new_subreddit = subreddit.new(limit=10)

    output_submissions = []
    for submission in new_subreddit:
        if not (submission.stickied):
            for game in game_list:
                if game in submission.title.lower():
                    output_submissions.append(submission)
    return output_submissions


def get_targets_list(target_file):
    targets_list = []
    with open(target_file, 'r') as searchfile:
        for line in searchfile:
            lineStripped = line.strip()
            targets_list.append(lineStripped)
    return targets_list


def convert_submissions_to_string(submissions):
    out_string = ""
    for submission in submissions:
        out_string += submission.title + "\n"
        out_string += redditLink+submission.permalink + "\n\n"
    return out_string


def get_archived_submissions():
    archived_list = []
    with open('history.txt', 'r') as searchfile:
        for line in searchfile:
            lineStripped = line.strip()
            archived_list.append(lineStripped)
    return archived_list


def append_history_file(submissions_list):
    with open('history.txt', 'a') as historyfile:
        for submission in submissions_list:
            historyfile.write(redditLink + submission.permalink + "\n")


def append_logs_file():
    with open('logs.txt', 'a') as logs:
        logs.write(now.strftime("%Y-%m-%d %H:%M:%S ") + "Parser_NS.py\n")


def filter_new_submissions(new_submissions, archived_submissions):
    final_list = []
    for submission in new_submissions:
        current = redditLink + submission.permalink
        if (current) not in archived_submissions:
            final_list.append(submission)
    return final_list


def get_email_list():
    email_list = []
    with open('emailList.txt', 'r') as searchfile:
        for line in searchfile:
            lineStripped = ''.join(line.split())
            lineStripped = lineStripped.split(",")
            email_list.append(lineStripped)
    return email_list


def send_email(receiver_email, out_string):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "your_sender_email@gmail.com"
    password = 'your_sender_email_password'

    if(len(out_string) > 0):
        out_string = out_string.encode('ascii', 'ignore').decode('ascii')
        message = """\
        Subject: Switch Deals!
        

{}""".format(out_string)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


def main(receiver_email, target_file):
    subreddit_submissions = get_submission_matches(target_file)
    archived_submissions = get_archived_submissions()
    filtered_submissions = filter_new_submissions(subreddit_submissions, archived_submissions)
    if(len(filtered_submissions) != 0):
        output_string = convert_submissions_to_string(filtered_submissions)
        send_email(receiver_email, output_string)
        append_history_file(filtered_submissions)


if __name__ == '__main__':
    email_list = get_email_list()
    for email in email_list:
        main(email[0], email[1])
    append_logs_file()
