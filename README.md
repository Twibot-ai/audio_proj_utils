## Command line utils
### Requirements
You need to install ffmpeg, ffprobe to use it.

https://ffmpeg.zeranoe.com/builds/

And then add /bin/ with ffmpeg.exe and ffprobe.exe to your environment

### Help
`python main.py help`

### Dataset creator
How to use:

`python main.py create_dataset <path to all audio> <path to save> <dataset name> <pony_name> <noise level>`

Path arguments:

* All path arguments must be absolute and end with \ (Windows) or / (Linux)
* Wrap your path arguments into ""

Structure inside of all audio samples:
````
├───samples
|   ├───S1
|   │   ├───s1e1
|   │   │   └───Source files
|   │   ├───s1e2
|   │   │   └───Source files
|   │   ├───s1e3
|   │   │   └───Source files
|   │   ├───s1e4
|   │   │   └───Source files
|   │   ├───s1e5
|   │   │   └───Source files
.....
````
Pony name argument:

* Be sure, that it is the same as in audio. For example you need use Twilight instead of Twilight Sparkle

Dataset name argument:

This is the name of directory for you dataset. Could be any, but if you use spaces - wrap argument into ""

Noise level argument:

* Case sensitive
* Could be Noisy, Very Noisy, Clean
* You need separate them with **only comas** if you use not one noise level. Example: "Noisy,Clean"
* Wrap this argument with ""

Example of usage:

`python main.py create_dataset "F:\projects\pony_pre_proj\all" "F:\projects\pony_pre_proj" only_clean Twilight "Clean"`

### Extract only audio of one pony
How to use:

`python main.py separate <path to all audio> <path to save> <name of taget folder> <pony_name>`

Example of usage: 
            
`python main.py separate "F:\projects\pony_pre_proj\all" "F:\projects\pony_pre_proj" twilight_folder Twilight`

All arguments of this command are the same as for dataset creation.
