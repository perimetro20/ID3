import sys

relation = ''
attributes = {}
attribute_list = []
data = []
data_reading = False

for line in sys.stdin:
    if line[0] is not '%':
        line = line.strip()
        if len(line):
            if data_reading:
                line = line.split(',')
                data.append(line)
            elif line.startswith('@relation'):
                line = line.split()
                relation = line[1]
            elif line.startswith('@attribute'):
                line = line[11:]
                line = line.replace('{', "")
                line = line.replace('}', "")
                line = line.replace(',', "")
                line = line.split()
                attribute = line[0]
                attributes[attribute] = line[1:]
                attribute_list.append(attribute)
            elif line.startswith('@data'):
                data_reading = True
