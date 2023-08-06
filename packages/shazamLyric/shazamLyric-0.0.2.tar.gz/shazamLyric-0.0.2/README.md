# shazamLyric

## Install
```
pip install shazamLyric
```

## Import library 
```
from shazamLyric import *
```

## All code
```
from shazamLyric import *
app = shazamLyric('la belle',3,0,'BR')
print(len(app.key()))
print(app.title())
print(app.subtitle())
print(app.lyrics())
print(app.youtube())
```

## Functions
### Use below code to call functions
```
app = shazamLyric('la belle',3,0,'BR')
```
###### *shazamLyric([text music],[number results],[number offset],[text country])

### Use the code below to get the number of songs
```
print(len(app.key()))
```
### Use the code below to get music code
```
print(app.key())
```
### Use the code below to get music title
```
print(app.title())
```
###### or choose index of list
```
print(app.title()[0])
```
### Use the code below to get music subtitle
```
print(app.subtitle())
```
###### or choose index of list
```
print(app.subtitle()[0])
```
### Use the code below to get music lyrics
```
print(app.lyrics())
```
###### or choose index of list
```
print(app.lyrics()[0])
```
### Use the code below to get youtube link
```
print(app.youtube())
```
###### or choose index of list
```
print(app.youtube()[0])
```

## Links
See my [GitHub](https://github.com/claudiotorresarbe).

