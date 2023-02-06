# Discord 채팅 내역을 GPT-2의 fine-tuning을 위한 txt파일로 변환.

import csv #.csv 파일을 읽어오기 위한 라이브러리.
import re #정규표현식을 위한 라이브러리.

def removeURL(TEXT): #data에 있는 url, MarkDown 또는 PATH를 제외함.
    TEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', TEXT, flags=re.MULTILINE)
    TEXT = re.sub('^```(?:py|python)\n([\s\S]*?)```$', '', TEXT, flags=re.MULTILINE)
    TEXT = re.sub('^.*\.(com|py)$', '', TEXT, flags=re.MULTILINE)
    TEXT = re.sub('^([a-zA-Z]):[\\\/]((?:[^<>:"\\\/\|\?\*]+[\\\/])*)([^<>:"\\\/\|\?\*]+)\.([^<>:"\\\/\|\?\*\s]+)$', '', TEXT, flags=re.MULTILINE)
    return(TEXT)

def createDATA(input, hazusu): #.csv File PATH, ['Discord User ID1', "Discord User ID2",...]
    f = open(input,'r', encoding="UTF-8") #encoding="UTF-8" 부분을 빼면 한글 Windows 환경에서 작동하지 않음.
    rdr = csv.reader(f)
    lid = ""
    mjr = ""
    i = 0
    saishu = []
    final = ""

    for line in rdr:
        if line[0] in hazusu: #제외 대상에 있는 ID가 보낸 메세지는 학습하지 않음.
            pass
        if line[0] == lid:
            mjr += " " + removeURL(line[3])
            lid = line[0]

        else:
            if lid == "":
                mjr += removeURL(line[3])
                lid = line[0]
            else:
                if re.match(('^[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9\s\d]+$'), mjr):
                    saishu.append([mjr])
                    mjr = removeURL(line[3])
                    lid = line[0]
                else:
                    mjr = removeURL(line[3])
                    lid = line[0]

    for ll in saishu: #입력과 출력을 구분해서 변수에 저장.
        i += 1
        if(i%2==1): #i가 홀수라면
            final += "<s>" + ll[0] + "[SEP]"
        else: #i가 짝수라면
            final += ll[0] + "</s>"

    f = open("data.txt",'w', encoding="UTF-8") #data.txt에 최종 결과를 기록함. 마찬가지로 encoding="UTF-8" 부분을 빼면 한글 Windows 환경에서 작동하지 않음.
    f.write(final)
    f.close()
