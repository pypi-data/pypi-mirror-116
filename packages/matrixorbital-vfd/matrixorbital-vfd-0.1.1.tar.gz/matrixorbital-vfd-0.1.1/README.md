# MatrixOrbital-VFD

I2C display driver for Matrix Orbital VFDs.

_unofficial, not affiliated with [Matrix Orbital Corp](https://www.matrixorbital.com/)_

### Install

```shell
pip install matrixorbital-vfd
```

### Usage

```python
from matrixorbital_vfd import VFD, Brightness

with VFD(1, 0x2e) as vfd:
	vfd.clear()
	vfd.brightness(Brightness.HIGH)
	vfd.write('Hello, world!')
```

### Functions

- `VFD.display(True/False)`  
  turn on/off display

- `VFD.home()`  
  move cursor to home position 0x0

- `VFD.position(column, row)`  
  move cursor to specified column/row position

- `VFD.move('left'/'right')`  
  move cursor left/right 1 column

- `VFD.clear()`  
  clear screen

- `VFD.brightness(Brightness.MEDIUM or 'MEDIUM')`  
  set brightness to specified level

- `VFD.cursor(True/False)`  
  enable/disable block (blinking) cursor

- `VFD.wrap(True/False)`  
  enable/disable line wrapping

- `VFD.scroll(True/False)`  
  enable/disable auto line scrolling

- `VFD.write('text')`  
  write text to display
