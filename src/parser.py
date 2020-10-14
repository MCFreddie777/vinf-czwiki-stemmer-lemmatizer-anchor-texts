import regex

def parse_xml_file(in_file_path,out_file_path):
    with open(in_file_path,"r", encoding='UTF-8') as in_file, open(out_file_path,"w+",encoding='UTF-8') as out_file:
        for line in in_file:
            parse_anchors_from_line(line,out_file)

def parse_anchors_from_line(line,out_file):
    expression = '\[\[([\p{L}\p{Po}\p{Pi}\p{Pf}\p{Ps}\p{Pc}\p{Pd}\p{Sk}\p{So}\p{C}\p{N}\p{Z}})=>]+)\|?([\p{L}\p{Po}\p{Pi}\p{Pf}\p{Ps}\p{Pc}\p{Pd}\p{Sk}\p{So}\p{C}\p{N}\p{Z}})=>]+)?\]\]'
    line_matches = regex.findall(expression,line)
    if len(line_matches) > 0:
        for regex_match in line_matches:
            items = list(filter(None,regex_match))
            for index,item in enumerate(items):
                out_file.write(f"\"{item}\"{',' if index != len(items)-1 else ''}")
            out_file.write('\n')
