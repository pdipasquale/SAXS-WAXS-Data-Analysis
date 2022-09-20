logdir = "./livelogfile.log" #input location of log file
biglog = open(logdir, 'r')
contents = biglog.readlines()
type(contents)
num_lines = len(contents)
print(["Number of lines:", str(num_lines)])
rows = list(range(0, num_lines-1))

split_header = contents[0].split(" ")
idx = split_header.index('chanh_filename')
print(split_header[idx+2])

# Worst way to find DFs but i'm using it for now
DFs = []
i = 0
for row in rows:
    row_n = contents[row]
    split_lines = row_n.split(" ") # splits up the logfile line using spaces as a delimeter
    fname = str(split_lines[idx+2])
    if 'dark' in fname:
        DFs.append(row)
        i = i + 1
print('Dark Field Images at:' + str(DFs))
print('Confirm this by checking frames in the tif directory please....')
#fname_column = list(find_all(split_header, 'chanh_filename'))