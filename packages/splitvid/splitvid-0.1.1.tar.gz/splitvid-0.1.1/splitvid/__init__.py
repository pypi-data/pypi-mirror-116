from plumbum import local
from os.path import splitext

ffmpeg = local["ffmpeg"]
ffprobe = local["ffprobe"]


def debug(*args):
    print("[*]", " ".join(map(str,args)))

def get_length(in_file: str) -> float:
    debug("ffprobe", *[
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            in_file,
        ])
    return float(
        ffprobe[
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            in_file,
        ]().strip("\n")
    )

def _get_ext(in_file: str) -> str:
    return splitext(in_file)[1][1:]

def splitvid(in_file: str, out_file: str, start: float, end: float):
    debug("ffmpeg", *["-i", in_file, "-c", "copy", "-ss", start, "-t", end, out_file])
    return ffmpeg["-i", in_file, "-c", "copy", "-ss", start, "-t", end, out_file]

def splitvid_into(in_file: str, out_file_template: str, parts: float):
    if parts < 0:
        raise ValueError("parts has to be > 0")

    length = get_length(in_file)
    step = length / parts
    ext = _get_ext(in_file)

    for i in range(parts):
        splitvid(in_file, out_file_template+ "_"+ str(i) +"."+ext, i*step, (i+1) * step)()

