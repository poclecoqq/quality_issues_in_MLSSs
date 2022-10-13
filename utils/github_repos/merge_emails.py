from pathlib import Path
from utils import load_emails


def main(folders):
    emails = set()
    crnt_dir = Path(__file__).parent.resolve()
    data_dir = Path(crnt_dir, "data")
    # Read email addresses
    t = 0
    for folder in folders:
        dir = Path(data_dir, folder)
        # There should be only one file matching this regex pattern
        file = next(dir.glob('emails-*.bin'))
        f_emails = load_emails(file)
        emails.update(f_emails)
        print(f'Folder:{folder}. Number of emails:{len(f_emails)}')
        t += len(f_emails)
    print(f'\nTotal number of unique emails: {len(emails)}')
    print(f'Number of duplicate emails: {t-len(emails)}')
    # Save them in a format favorable for the email list
    f_path = Path(data_dir, "out.txt")
    with open(f_path, 'w') as f:
        f.write("\n".join(emails))
    return emails


if __name__ == "__main__":
    folders = ['1665174928', '1665287907']
    main(folders)
