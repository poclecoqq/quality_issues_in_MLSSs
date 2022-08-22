import pathlib
import os
import re

if __name__ == "__main__":
    crnt_path = pathlib.Path(__file__).parent.resolve()

    ans = ''
    with open(crnt_path/'in.txt') as f:
        for l in f.read().split('\n'):
            if len(l) == 0:
                ans += '\n'
            else:
                res = re.search(
                    '^(Interviewee:|Interviewer [1-3]:|Interviewer:)', l)
                if res:
                    speaker_name = res.group(0)
                else:
                    l = speaker_name + ' ' + l
                ans += l + '\n'

    out_path = crnt_path/"out"
    os.makedirs(out_path, exist_ok=True)
    with open(out_path/'out.txt', 'w+') as f:
        f.write(ans)
