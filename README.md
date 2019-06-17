# SimpleCoverDownloader
Download the album art if cover.jpg is not in the directory.

## Tutorial
The software help us to search/download the album art automatically. The flow is:

* **Select a directory** where music files are.

* ~~Select which searching engines to be used.~~ (Not installed yet)

* The program walks through whole the directory and gets a list showing which folder **not have the cover.jpg file (assume 1 album 1 folder)**.

* Using **keyword (Album and Artist)** to Search the relative image.

* ~~Show searching results for manual judgment (optional).~~ (Not installed yet)

* **Save (optional)** the image in the music folder.

## Screen Shot
Main window

![Imgur](https://i.imgur.com/uc0wqtQ.png)

Processing window

![Imgur](https://i.imgur.com/P8XDj8o.png)

## Reference Library
* requests
* tinytag
* BeautifulSoup
* Pillow
* PyQt5
