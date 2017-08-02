# CozmoRest
Rest Server to control Cozmo remotely 

## TO START THE SERVER
  cd rest_env\Scripts <br>
  activate <br>
  cd .. <br>
  cd tutorial <br>
  python manage.py runserver (localhost and 8001) <br>
  python manage.py runserver 0.0.0.0:<your_port> (to customize listen address and listen port) <br>

## STARTUP SCRIPT:
  /home/pi/CozmoRest/startRestServer.sh

## INVOKE COZMO COMMANDS:
  Calling the RPI:  http://your_address:port/snippets/  (IP and Port has been set in startRestServer.sh)<br>
  Calling API Platform Gateway: http://192.168.0.69:8011/Cozmo or http://new.proxy.digitalpracticespain.com:18001/Cozmo
  

## COZMO CUSTOM CODE
  All commands and variables can be check at rest_env\tutorial\snippets\views.py <br>
  All cozmo related code is also in that file


  
