import re

time_re = re.compile(r'(([01]\d|2[0-3]):([0-5]\d):([0-5]\d)|24:00)')

if __name__ == '__main__':
    file_name = 'raw_transcript_sara.txt'
    with open(f'./in/{file_name}', 'r') as f:
        file_content = f.read()
        # Replce time stamps
        file_content = re.sub(time_re, "Interviewer:\t", file_content)
        with open(f'./out/{file_name}', 'w') as f:
            f.write(file_content)
