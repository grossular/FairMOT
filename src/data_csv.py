import glob

for f in glob.glob('../../lighttrack/data/GNE/Go_North_East/**/*.mp4', recursive=True):
    print(f)