# write-my-note
A notes manager with markdown
## Prerequisites
Python 3
#### Environment variables:
WRITE_MY_NOTE_PATH to specify the notes directory

WRITE_MY_NOTE_EDITOR (optional, default=vi) to specify your favorite text/markdown editor
## Usage
```
write-my-note --help


A notes manager with markdown

positional arguments:
  {new,list,find,open}  action
  subject               subject of the note (new note)
  title                 title of the note (new note)
  content               content of the note (new note)

optional arguments:
  -h, --help            show this help message and exit
  -file FILE            markdown file to copy content (new note)
  -text TEXT            text to search (open note)
  --debug               debug mode
  --console             to log to the console, logs to ./output.log otherwise
```