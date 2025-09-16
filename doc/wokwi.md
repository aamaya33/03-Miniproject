## Wokwi Installation 

The reason that introduced was because I found it annoying that I couldn't really know what my stuff is doing without the board, so this is set up to make the developer experience better 

### Installation 
- Install `Wokwi for VS Code` Extension
- Press F1 and select "Wokwi: Request a new License" which will redirect you to a link on your browser 
- make a free account if needed and click on `GET YOUR LICENSE`

### Running Wokwi
- run `pip install mpremote`
- when simulator is running, open a command prompt and type `python -m mpremote connect port:rfc2217://localhost:4000 run src/main.py`
- make sure to NOT tab out of the simulator tab otherwise the simulator will pause and the command will timeout
- WARNING IT CAN BE EXTREMELY LOUD

### Modifying the diagram.json file 
This is extremely annoying since they have this interactive editor that just doesn't work and is behind a paywall. To be able to access the json file directly, you'll need to change it from `diagram.json` to anything else (e.g. `diagrams.json`) and make your changes there. 