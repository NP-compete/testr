#!/usr/bin/python
import os

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Web Chat Program</title>'
print '<script language="javascript" type="text/javascript" src="../lib/jquery-1.7.2.min.js"></script>'
print "<script language='javascript' type='text/javascript' src='../lib/web_chat.js'></script>"
print '<script language="javascript" type="text/javascript" src="../lib/spin.js"></script>'
print '</head>'
print "<body  onunload='unload()'>"
print '<h2>This is my first chat program</h2>'
print "<p>start chat</p>"
print "<div id='msg_div'></div>"
print "<input type='text' id='remote_ip'/>"
print "<button type='button' onclick='connect_remote()'>Connect</button>"
print "<input type='text' id='message'/>"
print "<button type='button' onclick='send_message()'>Send Message!</button>"
os.system('./cgi-bin/chat_server.py &')
print '</body>'
print '</html>'

