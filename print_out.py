import subprocess
import time

IS_EMULATION = False
TEXT_SIZE_MULTIPLIER = 2
MUSIC_FILE = "./lyrics/Rick Astley - Never Gonna Give You Up (Official Music Video).mp4"
LYRIC_FILE = "./lyrics/Rick-Astley-Never-Gonna-Give-You-Up.lrc"


WIDTH_LIMIT = 32 // TEXT_SIZE_MULTIPLIER
LINE_BUFFER_LIMIT = 1 + (6 // TEXT_SIZE_MULTIPLIER)
assert TEXT_SIZE_MULTIPLIER in (0, 1, 2, 3, 4, 5, 6, 7, 8), 'Invalid text size'

if __name__ == '__main__':
    with open(LYRIC_FILE) as f:
        #assert f.read(1) == '\ufeff', 'Unexpected header'
        f.read(3)
        raw_lines = f.read()
    raw_lines = raw_lines.split('\n')

    lines_times = []
    lines = []
    for raw_line in raw_lines:
        if not raw_line: continue
        line = raw_line[10:]
        if line == 'www.RentAnAdviser.com': continue

        assert raw_line[0] == '['
        m = int(raw_line[1:3])
        assert raw_line[3] == ':'
        s = int(raw_line[4:6])
        assert raw_line[6] == '.'
        cs = int(raw_line[7:9])
        assert raw_line[9] == ']'
        lines_times.append(cs + 100 * (s + 60 * m))

        words = line.split()[::-1]
        split_line = []
        this_line = []
        while words:
            if len(words[-1]) > WIDTH_LIMIT:
                # Commit existing word if any
                if this_line: split_line.append(' '.join(this_line))
                # Split word across multiple lines
                while len(words[-1]) > WIDTH_LIMIT:
                    split_line.append(words[-1][:WIDTH_LIMIT-1] + '-')
                    words[-1] = words[-1][WIDTH_LIMIT-1:]
                continue
            this_line.append(words.pop())
            new_line = ' '.join(this_line)
            if len(new_line) == WIDTH_LIMIT:
                split_line.append(new_line)
                this_line.clear()
            elif len(new_line) > WIDTH_LIMIT:
                words.append(this_line.pop())
                split_line.append(' '.join(this_line))
                this_line.clear()
        if this_line: split_line.append(' '.join(this_line))
        lines.append(tuple(split_line))

    timed_lines = [(time, line) for time, lines in zip(lines_times, lines) for line in lines]
    for _ in range(LINE_BUFFER_LIMIT):
        timed_lines.append((None, ''))

    if IS_EMULATION:
        print_buffer = []
        def tprint(line):
            print_buffer.append(line)
            if len(print_buffer) >= LINE_BUFFER_LIMIT:
                print(print_buffer.pop(0))
    else:
        with open('LPT1:', 'wb') as f:
            f.write(bytearray([0x1D, 0x21, 0x11 * (TEXT_SIZE_MULTIPLIER - 1)]))
            f.flush()
        def tprint(line):
            with open('LPT1:', 'wb') as f:
                f.write(line.encode('ascii') + b'\n')
                f.flush()

    subprocess.Popen([r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe', MUSIC_FILE])
    #import os
    #os.system(f'explorer.exe "{MUSIC_FILE}"')
    #time.sleep(0.4)
    start = time.time()

    for _, line in timed_lines[:LINE_BUFFER_LIMIT-1]:
        tprint(line)

    for i, (_, line) in enumerate(timed_lines[LINE_BUFFER_LIMIT-1:]):
        time_to_print = timed_lines[i][0]

        target_time = start + time_to_print / 100
        while (now := time.time()) + 0.01 < target_time:
            remaining = target_time - now
            if remaining > 1:
                time.sleep(1)
            else:
                time.sleep(remaining)

        tprint(line)
