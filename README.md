# ESVK2Pod


It's utility for convert vk wall records to rss feed, adapted for podcast players. Main idea of this service - to make some instrument for getting public accessible audiobooks and music from vk.com group wall's records to the podcast players like as AnthennaPod for android or any others without logging in or tokens. Also as a DevOps I like when small application has small dependencies and deploy simplicity.



## Dependencies
- python 2.7
- python-lxml
- python-requests


#### Dependencies installation:
  For Debian based operation systems:

```
     sudo apt-get update && sudo apt-get install -y python python-lxml python-requests 
```


  Using python pip:
```
     sudo pip install --upgrade lxml && sudo pip install --upgrade requests # 
```

Maybe you'll need to install libxslt-devel libxml2-devel under RH based systems



## Parameters
There are three parameters to start service
 - 1st parameter - port (default 8080)
 - 2nd parameter - ip address (default localhost)
 - 3th parameter - url prefix and optionally port for audiolink generation
    
    
##### Examples
    ./esvk2pod 
        starts service on port 8080 of localhost
    ./esvk2pod 9000
        starts service on port 9000 of localhost
    ./esvk2pod 9000 192.168.10.20
        starts service on port 9000 of 192.168.10.20 address
    ./esvk2pod 9000 192.168.10.20 yourdomain.com:8000
        starts service on port 9000 of 192.168.10.20 address
        and made urls for getting audio like this
        http://yourdomain.com:8000/vk2podaudio/1234567890abcdef...abcdef.mp3
        It's usefull, if you planning use it behind reverse 
        proxy like Nginx. Sure, you can use IP address
        instead domain name and you can use domain without
        port definition.



## Using examples
You can just append one of the following urls to your podcast player, changing "groupname" to the real name of vk group (for example, try free_audiobooks):

http://localhost:8080/vk2pod/groupname

  Will get 20 records from wall and filter out records that hasn't audio attach, then it will made rss item for each audio attach with content of original record
  
http://localhost:8080/vk2pod/groupname/30

  The same, but it will get 30 records instead 20. Count maximum is 100 at the moment, but if you need more, you can easily fix it in code. :)
  
http://localhost:8080/vk2pod/groupname/30/5

  The same that above example, but with offset of 5 records



## Docker container
You can find Dockerfile in directory docker. Container based on debian:latest. I think, you can change it to ubutu:latest, but I haven't check it yet. Also you can use scripts build-run.sh and stop-remove.sh from docker folder. The first script has one parameter, than is equals of 3th parameters for runnning service. For example, if you frontend has domain name test.com, you can build container with command ./build-run.sh test.com
Attention: container's building will download original code from github instead getting local code from upper level directory.
======


## Notice
This code is provided for free and without any garanties. But you can feel free to send me any feedback to evgeniy.shumilov@gmail.com
