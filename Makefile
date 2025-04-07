#MakeFile for Coco with a Mame debugger. 
#Created by tazrog 2025


FILE := $(wildcard *.BAS)
NAME := $(basename $(FILE))

DIR := C:\Users\rog\Documents\IVE25

all:	
	C:\\msys64\\usr\\bin\\rm.exe -f $(NAME).DSK	
	decb dskini $(NAME).DSK
	decb copy -0 -t -r $(NAME).BAS $(NAME).DSK,$(NAME).BAS -0 -t -r	
		
	mame coco2b -rompath C:\Users\rog\Documents\Mame\roms -natural -window -ui_active -flop1 $(NAME).DSK 	

clean:
	C:\\msys64\\usr\\bin\\rm.exe -f *.map *.bin *.out *.DSK *.list error.log
	
    	
