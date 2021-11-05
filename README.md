# pretix_ggroups

Pretix and gmail don't really like to play together, for larger events eventually sending mails via SMTP fails.  
To circumvent this one can use google groups to send out bulk-emails, this script generates csv output which can be imported by the google groups bulk import.

## Preparations

1. Edit the group_mail, organizer and event variables in `pretix_ggroups.py` to suit your needs
2. Prepare your environment

```bash
python3 -m venv venv
source venv bin activiate
pip install -r requirements.txt
```

## Usage

```bash
export PRETIX_API_TOKEN=<your API token>
./pretix_ggroups.py > attendees.csv
```
