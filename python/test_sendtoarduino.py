import serial
from CodeCompanionView import CodeCompanionView
from random import randint

view = CodeCompanionView()
view.rgb = [randint(0,255),randint(0,255),randint(0,255)]
view.screen = ['Heres hoping', 'this works']

s = serial.Serial('/dev/tty.usbmodem1a1211', 9600)
print '%s\n' % view.json
s.write('%s\n' % view.json)
# s.write("\n");


#while 1:
#	print s.readline()



# AKIAIOKVNDG55GOKRUUA
# Hi6vk8DrKO1USRWZjEwiDUVUuo8BA7sREdXaQjFT

# Friendly color 210 100 200

  # String tryString = String(jsonString);
  # tryString.replace("\\", "");
  # jsonString = tryString.c_str();
