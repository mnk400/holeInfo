install: 
			@mkdir tmp
			@cp src/holeinfo.py tmp
			@mv tmp/holeinfo.py tmp/holeinfo
			@chmod +x tmp/holeinfo
			@sudo cp tmp/holeinfo /usr/local/bin
			@rm -r tmp

uninstall:  
			@sudo rm /usr/local/bin/holeinfo
