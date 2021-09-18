import datetime
import json
from ics import Calendar, Event
#rfc5545 iCalendar.
#YYYY-MM-DD HH:mm
callsstring='''09:00-10:30, 10:50-12:20, 13:20-14:50, 15:10-16:40, 17:00-18:30, 18:50-20:20, 20:30-22:00'''.split(', ')
dictCallstring=list();
for i in callsstring:
    dictCallstring.append(i.split('-'))
print(dictCallstring)

rc=json.loads(open('tests/democal.json','r').read())

addresses={
    0:"Корпус 0, улица Демьяна Бедного, 4б",
    1:"Корпус 1, улица Весенняя, 28",
    2:"Корпус 2, улица Дзержинского, 9",
    3:"Корпус 3, Красноармейская улица, 117",
    4:"Корпус 4, улица 50 лет Октября, 19",
    5:"Корпус 5, улица 50 лет Октября, 17",
    6:"Корпус 6, улица Дзержинского, 9Б"
    
}

"""
        name (Optional[str]) – rfc5545 SUMMARY property
        begin (Arrow-compatible) –
        end (Arrow-compatible) –
        duration (Optional[timedelta]) –
        uid (Optional[str]) – must be unique
        description (Optional[str]) –
        created (Arrow-compatible) –
        last_modified (Arrow-compatible) –
        location (Optional[str]) –
        url (Optional[str]) –
        transparent (Optional[bool]) –
        alarms (Optional[Iterable[BaseAlarm]]) –
        attendees (Optional[Iterable[Attendee]]) –
        categories (Optional[Iterable[str]]) –
        status (Optional[str]) –
        organizer (Optional[Organizer]) –
        classification (Optional[str]) –
"""
c = Calendar()
def toAddr(p):
    try:
        a=int(p)
        a=addresses[(a-a%1000)/1000]
    except:
        a=p
    return a
#Выворачиваем весь список содержащий все запрошенные расписания.
for i in rc:
    
    categories=i['name']
    for content in i['content']:
        e = Event()
        e.uid=content['id']
        e.categories=content['subgroup']
        e.name = "["+ content['lesson_number'] +"] "+content['place']+" - "+content['subject'] +", "+content['type']+''
        #e.begin=rc[0]['time']
        begin=content['date_lesson']+" "+dictCallstring[int(content['lesson_number'])-1][0]#без смещения зоны в Z0
        beginD = datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M")-datetime.timedelta(hours=7)

        end=content['date_lesson']+" "+dictCallstring[int(content['lesson_number'])-1][1]#без смещения зоны в Z0
        endD = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")-datetime.timedelta(hours=7)
        
        e.begin= beginD
        
        e.end= endD
        
        e.location=toAddr(content['place'])
        c.events.add(e)
print(c.events)
# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
with open('U:/raspis/my.ics', 'w',encoding='utf8') as my_file:
    my_file.writelines(c)
# and it's done !