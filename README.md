# telegram-uploader

(wip) A telegram uploader to upload files with GUI.

## How it works?

Any file path passed to the program are selected to upload.
The chats to upload the files to can be selected in the GUI.

## Requirements:

- Python 3.8+
- api_id and api_hash from telegram. [How?](https://core.telegram.org/api/obtaining_api_id)

## Setup:

- Change `api_id` and `api_hash` in `creds.sample.py`.

- Rename `creds.sample.py` to `creds.py`.

- Create a virtual environment, activate it and install requirements  
    ``` 
    python -m venv .venv 
    . ./.venv/bin/activate
    pip install -r requirements.txt 
    ```

- Generate session file.
    ```
    python generate_session.py
    ```
    and follow the on screen instructions. After the script is finished. Paste
    the file path it generates in `creds.py` for `session_path`.

    Note: Phone number should include country code
    
## Usage:

Append the path of files you want to upload after the program:

```
python app.py /tmp/abcd.jpeg /tmp/boomer.png /etc/gcc
```

## File Manager Integration:

### Thunar (Linux)

- Get the full python path inside the virtual environment
- Get the full path to `app.py` 
- In thunar, go to `Edit` - `Configure Custom Actions` - `Add a new custom action`
- Under `Basic`, give it a name and in command field use this syntax:
    ```
    /path/to/.venv/bin/python /path/to/app.py %F
    ```
- Under `Appearance Conditions` choose everything except `Directories`. Press OK.
- Now you can use this program straight from your file manager.

## Todo:

- [ ] Interactive initial setup
- [ ] Proper command line parameters