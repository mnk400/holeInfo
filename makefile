install: 
			@mkdir tmp
			@cp src/holeInfo.py tmp
			@mv tmp/holeInfo.py tmp/holeinfo
			@sudo cp tmp/holeinfo /usr/local/bin
			@rm -r tmp

uninstall:  
			@sudo rm /usr/local/bin/holeinfo
