# write-my-note
A markdown notes manager with Github

You can link your notes repository with your Github account
## Prerequisites
- Python 3
- pip
- install dependencies `pip install -r requirements.txt`
- #### Environment variables:
    - WMN_PATH (required, notes repository path)
    - WMN_EDITOR (optional, specify your favorite text/markdown editor, default="vi")
    - WMN_GIT_TOKEN (optional, GitHub access token)
    - WMN_GIT_NAME (optional, Github user name)
    - WMN_GIT_EMAIL (optional, Github user email)
    - WMN_LOG (optional, specify the logs path)
## Usage
```
write-my-note --help


A notes manager with markdown

positional arguments:
          {new,list,find,open,remove}
                                action
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
### Notes
- For a Github usage, you can prefix the subject with '_' for local files that you don't want to be uploaded,
so they'll be ignored.
E.g. [...] new _localnote hello world
- For a Github usage, for the 'open' action, if the note has been modify in the editor,
then its modifications are pushed to your Github repository
- If a subject contains spaces, they are replaced with '-' char.
So be careful to use this char for 'open' and 'remove' action.