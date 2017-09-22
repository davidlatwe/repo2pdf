Repo to PDFs
===

In open-source project devloping, one often needs to read a lot of code so he/she can follow-up.
And sometimes we might want to print the code on paper for reading more freely.

Here I assembled a way to convert the entire project's content to PDF files.
This will convert each file to one PDF and put in an identical folder structure with original project.

If the project is git-controlled, those ignored by `.gitignore` will not be processed, otherwise all file would be converted.
And I use `Pygments` to convert code into HTML, so only `Pygments` supported language will be processed.
> I am not sure about using `.gitignore` as a filter will bring much help because `Pygments` itself will automatically failed with unsupported file extension. But I made it anyway.


## Dependency

#### [Pygments](http://pygments.org/)
```    
$ pip install pygments
```

#### [wkhtmltopdf](https://wkhtmltopdf.org/)

* Debian/Ubuntu:
    ```
    $ sudo apt-get install wkhtmltopdf
    ```
**Warning!** Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from [wkhtmltopdf](http://wkhtmltopdf.org/) site or you can use [this script](https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh).

* Windows and other options: check wkhtmltopdf [homepage](http://wkhtmltopdf.org/) for binary installers


## Usage

For demo, In Bash or CMD, type :

```
$ repo2pdf --demo
```

For task :

```
$ repo2pdf [your_repo_path]
```

For help :

```
$ repo2pdf --help
```


## Ah

Haven't test in unix platform yet.