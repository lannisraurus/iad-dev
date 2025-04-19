
# IAD - Project I - Arduino Interface

**Duarte Tavares [105920], João Camacho [106224], Jorge Costa [106891], Margarida Saraiva [106994]**  
**2025**

---

## 1. UI

In this communication project between the Arduino and the Raspberry Pi, a Python application was created for the Raspberry Pi with which the user can interact. The application includes:

- A log, which shows the commands that have already been used and displays error messages if something goes wrong;
- A text box where a variety of commands can be entered (submitted either by pressing “Enter” or using the “Run” button below the box);
- A Run button to submit commands;
- An Interrupt button to stop an acquisition that is already in progress;
- A Commands button that opens a new window listing all available commands and their purposes;
- A Graph button that opens a new window displaying a graph with the acquired data.

---

## 2. Features

When the application opens, the log shows setup information about processes that occur immediately at startup: the Raspberry Pi scans and lists the available ports, then tries to determine if they are valid for communication. If valid ports are found, one is selected and opened for communication.

In the editable text box, the Raspberry Pi processes the input by using spaces as separators between words—the first word being the keyword identifying the command, and the remaining words as parameters. An exception is made for quoted strings, which are treated as a single element. The box also features auto-complete (using the Tab key) and command history navigation (using the up and down arrows).

---

## 3. Communication

Three types of commands are distinguished: internal, external, and mixed.

- **Internal Commands**:  
  Involve only the Raspberry Pi, with no communication to the Arduino (e.g., listing available ports, renaming graph axes, etc.).

- **External Commands**:  
  Require a connection to the Arduino and are processed entirely on the Arduino. If the Raspberry Pi doesn’t recognize a command, it assumes it is external and sends it to the Arduino, which either returns an error or executes it and sends back results (e.g., changing the Arduino pin used for acquisition).

- **Mixed Commands**:  
  Use functionalities of both the Arduino and Raspberry Pi. For example, the “acquire plot” command sends several “acquire” commands to the Arduino and then uses the Raspberry Pi to draw the graph.

Specific mixed commands were implemented for the circuit set up at the group’s workstation, such as the “discharge curve” command – see Fig. 1.

---

## 4. Program Execution

Before starting the program, it's recommended to connect the Arduino to the Raspberry Pi via USB, with the breadboard circuit already set up and properly connected to the Arduino. The program is run from the terminal with:

```bash
python3 main.py
```

It is advised that the first action be to view the available commands in the “Commands” window, accessible via the corresponding button.

---

## References

1. [PyQt documentation](https://doc.qt.io/qtforpython-5/contents.html)  
2. [pyqtgraph documentation](https://pyqtgraph.readthedocs.io/en/latest/index.html)  
3. [pyserial documentation](https://pyserial.readthedocs.io/en/latest/)  
4. [Arduino language reference](https://docs.arduino.cc/language-reference/)  
5. [KiCad EDA Suite](https://www.kicad.org/)  

---
