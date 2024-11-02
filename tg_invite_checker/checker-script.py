import argparse
import os
import regex
import requests
from bs4 import BeautifulSoup

def get_channel_info(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        og_title = soup.find("meta", property="og:title")
        channel_name = og_title['content'] if og_title else "Channel name not found"
        og_description = soup.find("meta", property="og:description")
        channel_description = og_description['content'] if og_description else "Channel description not found"
        subscriber_div = soup.find("div", class_="tgme_page_extra")
        subscriber_count = subscriber_div.get_text(strip=True) if subscriber_div else "Subscriber count not found"
        return channel_name, subscriber_count, channel_description, url
    else:
        print(f'Failed to retrieve the website. Status code: {response.status_code}')
        return None


def read_file(filename: str):
    expired_counter = 0
    alive_counter = 0
    seen = set()
    duplicate_counter = 0
    with open(filename, 'r') as file:
        for line in file:
            link = line.strip().rstrip(')."')
            channel_name, subscriber_count, channel_description, url = get_channel_info(link)
            if channel_name == "Join group chat on Telegram": # invite likely expired
                expired_counter = expired_counter + 1
            elif ((channel_name, channel_description)) in seen:
                duplicate_counter = duplicate_counter + 1
                alive_counter = alive_counter + 1
            else:
                result = channel_name, subscriber_count, channel_description, url
                print(result)
                alive_counter = alive_counter + 1   
                seen.add((channel_name, channel_description))             
    print(f'Total links: {expired_counter+alive_counter}\n'
        f'Expired links: {expired_counter}\n' 
        f'Live links: {alive_counter}\n'
        f'Duplicate channels: {duplicate_counter}')

def main():
    parser = argparse.ArgumentParser(description="Check Telegram invite links")
    parser.add_argument('-f', '--file', type=str, help="Filename/path to file containing Telegram invite links separated by newlines")
    parser.add_argument('-l', '--link', type=str, help="Check an individual Telegram invite link")
    args = parser.parse_args()

    # file path argument
    if args.file:
        if not os.path.isabs(args.file):
            file_path = os.path.join(os.getcwd(), args.file)
        else:
            file_path = args.file
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
            read_file(file_path)
        else:
            print(f"File not found: {file_path}")
    
    # link argument
    if args.link:
        print(f"Link provided: {args.link}")
        return get_channel_info(args.link)

    # default behavior if neither file nor link is provided
    if not args.file and not args.link:
        print("Please provide either a file path or an invite link.")

if __name__ == "__main__":
    main()

