# -*- coding: utf-8 -*-
import re

def is_valid_email(addr):
    #re_email = re.compile(r'\w+\@\w+\.[a-zA-Z]{2,3}')
    re_email = re.compile(r'[0-9a-zA-Z\.\_]+\@\w+\.[a-zA-Z]{2,3}')
    #_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
    if re_email.match(addr):
      return True
    return False

def get_email_name(addr):
    #re_email = re.compile(r'([0-9a-zA-Z\.\_]+)\@\w+\.[a-zA-Z]{2,3}')
    m = re_email.match(addr)
    if m:
      return m.group(1)
    return None

print(is_valid_email('someone@gmail.com'))
print(is_valid_email('bill.gates@microsoft.com'))
print(is_valid_email('bob#example.com'))
print(is_valid_email('mr-bob@example.com'))
print('ok')

#get_email_name('<Tom Paris> tom@voyager.org')
name = get_email_name('tom@voyager.org')
print('email name is : %s' % name)


#re.match(r'<\w+\s\w+>', '<abc abc>')
#re.match(r'\<\w+\w+\>', '<tom paris>')