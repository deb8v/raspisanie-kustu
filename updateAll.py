from typing import Counter
import main
main.validStatic()
tl=main.teachersJSON
gl=main.groupsJSON

redownloadList=list();
Counter=0;

print(len(tl),'  ',len(gl))
for i in gl:
    redownloadList.append(i['dept_id'])
    main.getByGroup_ID(i['dept_id'])
    Counter+=1;
    print(Counter,'/',len(redownloadList))
for i in tl:
    redownloadList.append(-int(i['person_id']))
    main.getTeacherShudleByUID(i['person_id'])
    print(Counter,'/',len(redownloadList))

