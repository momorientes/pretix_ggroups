#!/usr/bin/env python3

import os
import re

import requests

api_base = "https://pretix.eu/api/v1"

# the google groups mail address
group_mail = "denog13@denog.de"
# pretix event organizer
organizer = "denog"
# pretix event name
event = "denog13"


def main():
    results = api_get_all_pages(
        f"{api_base}/organizers/{organizer}/events/{event}/orders/"
    )
    attendee_emails = []

    for order in results:
        for position in order["positions"]:
            if (
                position["attendee_email"]
                and position["attendee_email"] not in attendee_emails
            ):
                if not position["attendee_email"].endswith("gmail.com"):
                    attendee_emails.append(position["attendee_email"])
                # gmail doesn't allow to subscribe userse with plussed emails to be subscribed to groups, so we remove the plussed part
                else:
                    mail = re.sub(r"\+[^@]+", "", position["attendee_email"])
                    attendee_emails.append(mail)

    print("Group Email [Required],Member Email,Member Type,Member Role")
    for mail in attendee_emails:
        print(f"{group_mail},{mail},,")


def api_get_all_pages(url: str, results: list = []) -> list:
    """Recursive function to get all pages of an API endpoint
    Args:
        url: the full URL to get
        results: a list of all existing results to return (for recursion)
    Returns: All pages results as list
    """
    headers = {"Authorization": f"Token {os.environ.get('PRETIX_API_TOKEN')}"}
    data = requests.get(url, headers=headers).json()
    if data["results"]:
        results += data["results"]
        if data["next"]:  # handle pagination by recursing
            api_get_all_pages(data["next"], results=results)

    return results


if __name__ == "__main__":

    if not os.environ.get("PRETIX_API_TOKEN"):
        raise EnvironmentError("No PREITX_API_TOKEN provided")

    main()
