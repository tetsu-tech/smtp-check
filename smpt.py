# import dns
import dns.resolver
import smtplib
import time
import pandas as pd

def get_domains(filename: str):
    try:
        print ("Trying to open file ", filename)
        with open(filename) as f:
            domains = [line.rstrip() for line in f]
    except:
        print("Error while loading", filename)
        sys.exit("IO error")
    else:
        print (len(domains), "addresses loaded...starting mx lookup.\n\n")

    return domains

def get_mxrecord(domain):
    try:
        answers = dns.resolver.resolve(domain.split("@",1)[1], 'MX')
    except Exception as e:
        error_message = f'[get_mxrecord error] ${e}'
        print (error_message)
        return { 'mxRecord': error_message, 'domain': domain }
    
    print('answers[0].exchange.to_text()', answers[0].exchange.to_text())
    mxRecord = answers[0].exchange.to_text()
    return { 'mxRecord': mxRecord, 'domain': domain }

def get_mxrecords_from_domains(domains):
    result = []
    for domain in domains:
        data = get_mxrecord(domain)
        result.append(data)
    return result

def check_mxrecord(data):
    print('---data', data)
    server = smtplib.SMTP(data['mxRecord'], 25) # 接続先サーバー, ポート番号
    hello_result = server.ehlo()
    # print('hello_result', hello_result)
    mail_result = server.mail('tetete1118@gmail.com') # MAIL FROMに指定するアドレス
    # print('mail_result', mail_result)
    rcpt_result = server.rcpt(data['domain']) 
    print('rcpt_result', rcpt_result[0])
    time.sleep(.200)


filename = 'emails.txt'
domains = get_domains(filename=filename)
    
time.sleep(1)

results = get_mxrecords_from_domains(domains=domains)
print('results', results)

for result in results:
    if not result['mxRecord'].startswith('[get_mxrecord error]'):
        check_mxrecord(result)
