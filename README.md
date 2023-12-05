# CSNETWK-FileTransferMP

## Instructions

### Starting a server

``` bash
py Server.py <ip address> <port>
```



### Starting a client

#### CLI
```bash
py Client.py
```

#### GUI
```bash
py View.py
```

If there is a need to clear `/Server/Files`, make sure to also clear the list of files in FileList.json (for GUI implementation)


### Uploading a file through CLI
If the file is in `./Client/Uploads`,
```bash
/store Uploads/<YOUR-FILE-NAME-HERE>
```

### Uploading a file through GUI
Make sure the file needed to upload is in `./Client/Uploads`, as the program only accepts files from this directory.


### Commands List for CLI
- **/join** \<IP Address\> \<Port Number\> - Connect to the server application

- **/?** - Request command help to output all Input Syntax commands for references

- **/leave** - Disconnect to the server application

- **/register** \<handle\> - Register a handle to the server

- **/store** \<filename\> - Send a file to the server

- **/dir** - Request the directory file list from the server

- **/get** \<filename\> - Request a file from the server

