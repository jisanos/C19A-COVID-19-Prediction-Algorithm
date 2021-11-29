# C19A (CIPA) COVID-19 Prediction Algorithm (CAPSTONE Project)

Repository for CIPA Capstone project in which is pre-processed, visualized and modeled a machine learning algorithm that can predict future cases of the spread.

## Abstract
We analyzed JHU COVID-19 data, pre-processed, visualized and modeled a machine learning algorithm that can predict future cases of the spread. This was done using python and various third-party data analysis libraries.  We also generated synthetic data to test our modeled algorithm against it and attempt to see how the spread might continue in the future. 

The source code of this project is licensed under the GPLv3, allowing for an open-source development and community approach to what is a global issue. 

## Purpose
Due to the recent surge of COVID-19 cases, we believe that this pandemic will remain afloat for longer than expected, and we do not see enough tools that can help us see the evolution of the spread of the pandemic in the future. Thus, we decided that it would be beneficial to work on developing a model that can predict future cases of COVID-19 based on pre-existing data. Hopefully, this can let us better observe how the virus behaves under different conditions and help with formulating future prevention strategies. 

## Objectives
Our objective with this project is to attempt to model a machine learning algorithm able to predict future cases of COVID-19. To do this we must use valid publicly available pre-existing data that we must analyze, pre-process, and visualize. After this we may begin testing different algorithms, that can properly project accurate predictions, or create our algorithm if the existing ones are not good enough.

## Libraries and Languages

* Python with various Data Science libraries such as:
   * pandas 
   * matplotlib 
   * Others

Disclaimer: These libraries already come with the Anaconda package.    

## Getting Started

### installing
To run the scrypts, you will need anaconda to access Spyder or download spyder separately. 
Link for downloading anaconda: https://www.anaconda.com/products/individual
Link for downloading spyder: https://www.spyder-ide.org/

### Requisites for Spyder
* Will required a system with Windows, MacOS or linux.
* Python 2.7 or >=3.3
* PyQt5 >=5.2 or PyQt4 >=4.6.0 (PyQt5 is recommended).
* Qtconsole >=4.2.0 – for an enhanced Python interpreter.
* Rope >=0.9.4 and Jedi <http://jedi.jedidjah.ch/en/latest/> 0.8.1 – for code completion, go-to-definition and calltips on the Editor.
* pyflakes – for real-time code analysis.
* Sphinx – for the Help pane rich text mode and to get our documentation.
* Pygments >=2.0 – for syntax highlighting and code completion in the Editor of all file types it supports.
* Pylint – for static code analysis.
* Pep8 – for style analysis.
* Psutil – for memory/CPU usage in the status bar.
* Nbconvert – to manipulate Jupyter notebooks on the Editor.
* Qtawesome >=0.4.1 – for an icon theme based on FontAwesome.
* Pickleshare – To show import completions on the Editor and Consoles.
* PyZMQ – To run introspection services on the Editor asynchronously.
* QtPy >=1.1.0 – To run Spyder with PyQt4 or PyQt5 seamlessly.
* Chardet >=2.0.0– Character encoding auto-detection in Python.
* Numpydoc Used by Jedi to get return types for functions with Numpydoc docstrings.
### Requisites for Anaconda
* Will required a system with Windows, MacOS or linux.
* License: Free use and redistribution under the terms of the EULA for Anaconda Individual Edition.
* Operating system: Windows 8 or newer, 64-bit macOS 10.13+, or Linux, including Ubuntu, RedHat, CentOS 7+, and others.
* If your operating system is older than what is currently supported, you can find older versions of the Anaconda installers in our archive that might work for you. See Using Anaconda on older operating systems for version recommendations.
* System architecture: Windows- 64-bit x86, 32-bit x86; MacOS- 64-bit x86; Linux- 64-bit x86, 64-bit aarch64 (AWS Graviton2 / arm64), 64-bit Power8/Power9, s390x (Linux on IBM Z & LinuxONE).
* Minimum 5 GB disk space to download and install.

On Windows, macOS, and Linux, it is best to install Anaconda for the local user, which does not require administrator permissions and is the most robust type of installation. However, if you need to, you can install Anaconda system wide, which does require administrator permissions.

## Import all of the data to the top level directory (this project's dir)

Cases and Deaths:

`git clone https://github.com/CSSEGISandData/COVID-19.git "./CSSE_C-19"`

Vaccinations, Testing:

`git clone https://github.com/govex/COVID-19.git "./CCI_C-19"`

Alternate branch of CCI containing US State Level Policy Tracker:

`git clone -b govex_data https://github.com/govex/COVID-19.git "./CCI_C-19_Policies"`

[Weather Data](https://storage.googleapis.com/covid19-open-data/v3/weather.csv)

## Built with
* Anaconda 
* Spyder

## Authors
* Hector G. Sanchez Mercado - [jisanos](https://github.com/jisanos)

* Rayniel Ramirez Albizu - [RaynielRamirezz](https://github.com/RaynielRamirezz)

## Third-Party libraries

* pandas 

* numpy 

* faker 

* matplotlib 

* seaborn 

* sklearn 

* geopy 

* folium 

* nltk 

* wordcloud 

* gensim 

## Dictionary
CSSE: Johns Hopkins Center for Systems Science and Engineering

CCI: Johns Hopkins Centers for Civic Impact

WHO: World Health Organization
