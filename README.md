# ict3204-keystroke-auth-lstm

## Setting Up
### Windows
#### Cloning GitHub Repository (using [vscode](https://code.visualstudio.com/))
1. Press: Ctrl + Shift + P
2. Type: 'Clone' and select 'Git: Clone'
3. Paste `https://github.com/xfortisfye/ict3204-keystroke-auth-lstm`
4. Enter your GitHub credentials & select a location to save the repository

#### Installing Python
1. [Install](https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe) python
2. Set up environment PATH, if not you will not be unable to run `py`/`python` 
    1. Right-click on 'This PC' > Properties > Advance System Settings > Environment Variables
    2. Under System Variable, Select PATH
    3. Click on Edit, enter location. Usually: `C:\Python38\`

> If you are using vscode, relaunch it

#### Installing Dependencies
1. Install virtualenv
```bash
> pip install virtualenv
```
2. Start virtualenv (Linux)
```bash
> source env/bin/activate
```
3. Install pip requirements
```bash
> cd \Path\to\ict3204-keystroke-auth-lstm
> pip install -r requirements.txt
```
### Linux (Debian)
#### Cloning GitHub Repository
```bash
> sudo apt install git -y
> git clone https://github.com/xfortisfye/ict3204-keystroke-auth-lstm
```

### Generating dataset
1. Special thanks to the following git
```bash
> git clone https://github.com/miguelhp89/Keystroke_Dynamics_Gen
```

## Milestones
- [x] Project Outline
- [ ] Prototyping
- [ ] TBD

## Collaborators
| Name            | GitHub                                         | 
| --------------- | ---------------------------------------------- | 
| ** Foo Qi Kai **                  | [@qiikaii](https://github.com/qiikaii) |
| ** Safaraz Bin Sarazli **         | [@chopstigs](https://github.com/chopstigs) |
| ** Muhammad Azfar Bin Adam **     | [@HunterAz](https://github.com/HunterAz) |
| ** Chua Chiang Sheng, Andy **     | [@xfortisfye](https://github.com/xfortisfye) |
| ** Gwee Soon Chai, Christopher ** | [@ManOCoolture](https://github.com/ManOCoolture) |
