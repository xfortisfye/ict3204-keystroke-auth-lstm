# ict3204-secure-analytics

## Table of Contents <!-- omit in toc -->
- [Setting Up](#setting-up)
  - [Windows](#windows)
    - [Cloning GitHub Repository (using vscode)](#cloning-github-repository-using-vscode)
    - [Installing Python](#installing-python)
    - [Installing Dependencies](#installing-dependencies)
    - [Setting up GNU Make](#setting-up-gnu-make)
  - [Linux (Debian)](#linux-debian)
    - [Cloning GitHub Repository](#cloning-github-repository)
- [Running the Project](#running-the-project)
  - [Option 1: Using GNU Make](#option-1-using-gnu-make)
- [Milestones](#milestones)
- [Collaborators](#collaborators)

## Setting Up
### Windows
#### Cloning GitHub Repository (using [vscode](https://code.visualstudio.com/))
1. Press: Ctrl + Shift + P
2. Type: 'Clone' and select 'Git: Clone'
3. Paste `https://github.com/ehandywhyy/ict3204-secure-analytics`
4. Enter your GitHub credentials & select a location to save the repository

#### Installing Python
1. [Install](https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe) python
2. Set up environment PATH, if not you will not be unable to run `py`/`python` 
    1. Right-click on 'This PC' > Properties > Advance System Settings > Environment Variables
    2. Under System Variable, Select PATH
    3. Click on Edit, enter location. Usually: `C:\Python38\`

> If you are using vscode, relaunch it

#### Setting up GNU Make
1. [Install](https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=nchc&download=) Make for Windows
2. Set up environment PATH, if not you will not be unable to run `make`
   1. Right-click on 'This PC' > Properties > Advance System Settings > Environment Variables
   2. Under System Variable, Select PATH
   3. Click on Edit, enter Make location. Usually: `C:\Program Files (x86)\GnuWin32\bin`

### Linux (Debian)
#### Cloning GitHub Repository
```bash
> sudo apt install git -y
> git clone https://github.com/ehandywhyy/ict3204-secure-analytics
```

## Running the Project
### Option 1: Using GNU Make
1. To run the program
```bash
> cd \Path\to\software-engineering-project
> make
```
2. To clean compiled files (.pyc)
```bash
> make clean
```

## Milestones
- [x] Project Outline
- [ ] Prototyping
- [ ] TBD

## Collaborators
| Name            | GitHub                                         | 
| --------------- | ---------------------------------------------- | 
| ** Foo Qi Kai **               | [@](https://github.com/) |
| ** Safaraz Bin Sarazli **            | [@](https://github.com/)       |
| ** Muhammad Azfar Bin Adam **            | [@](https://github.com/)         |
| ** Chua Chiang Sheng, Andy **   | [@ehandywhyy](https://github.com/ehandywhyy)  |
| ** Gwee Soon Chai, Christopher ** | [@](https://github.com/)     |
