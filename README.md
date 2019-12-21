# write-my-note
A notes manager with markdown
## Prerequisites
Python 3
#### Environment variables:
- WMN_PATH (required, notes repository path)

- WMN_EDITOR (optional, specify your favorite text/markdown editor, default="vi")
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