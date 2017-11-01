Packtpub  ebook downloader
============================================

This is a simple python command to download all your Packtpub purchased books in pdf format. It is simple to use and it downloads all the books one by one to avoid overloading the server with multiple requests.

Dependencies
-------
To use the downloader yo have to install these dependencies. 
* requests 
* beautifulsoup4 
* python-slugify

Usage
-------

This is a line command tool so you can invoke it in this way:

```
python packtpub_download.py user password directory
```


| Parameter 	|                                 Usage                                 	| Required 	|
|:---------:	|:---------------------------------------------------------------------:	|:--------:	|
|    user   	|                            Packtpub username                           	|    Yes   	|
|  password 	|                         Packtpub user password                         	|    Yes   	|
| directory 	| Directory where the books will be downloaded, by default is `./books` 	|    No    	|

Road map
-------
* Avoid download existing books (new mode)
* Unit testing