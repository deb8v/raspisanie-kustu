

# Коллектор расписания КузГТУ

### Используемый API

https://portal.kuzstu.ru/api/

### Лист преподов
https://portal.kuzstu.ru/api/teachers

### Функции
#### 	КЭШ



* modules.getFromCache(URL,expieri),* expieri указан в MS при каждом запросе возвращает искомый файл, при истечении срока или не наличии заново скачивается.

Для настройки папки складирования .bak файлов *modules.cacheDir('docs/yaw')*.



Список SUBSCRIBERS_LIST=["G6265","КСс-211","T17453","Мал"] используется для ограничение размера генерации 



* **makeResponse**("**КС**")*  -- принимает на вход массив групп или преподавателей, фильтрует на копирование и высылает массив на обработку седьмой расой.





![](https://sun9-59.userapi.com/impg/HWuVrffS1upTilK7lcaH1N_fFuwcpD4qXyFWOg/ANgBo9TnxBA.jpg?size=662x236&quality=96&sign=86d79205565441b676e3be210603c01e&type=album)

​	

​	*icalendar.makeCalendar(makeResponse("КСс-211"), 'U:/raspis/my.ics')*

![](https://sun9-64.userapi.com/impg/MzBoDX7eNtNcyP6VuMFpfs53_261gy4n3xiwfQ/RJhmTWjKmfw.jpg?size=1134x560&quality=96&sign=fe2e0420475b341e86d92a753148430f&type=album)

| ![](https://sun9-79.userapi.com/impg/QCB6EqOx-KWt-DFI4Hf6-3DGV-J6fF7ChJHiOQ/lU4BmRAxbwI.jpg?size=747x1600&quality=96&sign=c6be5c2e40a865e2c3e08bf3f9e3583b&type=album) | ![](https://sun9-63.userapi.com/impg/uvd9hBiHdikSebszSilKhnha6gOhNEQHQpNX1g/RW21ESWxFAs.jpg?size=747x1600&quality=96&sign=6211393fa8740ba403062436e3c946db&type=album) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |



###################
Изменения.
20.09.2021
1 - теперь в main для main.compileGroupList() не нужно указывать на конкретный список групп, он берётся из указанных в main.validStatic() объектов

2 - веб апи для поиска  http://localhost:8000/icsshudle/web-api/search?tgt=G6265,T17453  http://localhost:8000/icsshudle/web-api/search?tgt=ук,мал /\ 