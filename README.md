# DocuSense
### Project Structure
The structure is inspired by the following:
    • https://docs.python-guide.org/writing/structure/


The hierarchy is as follows:
|.  
├── Makefile         - I come from C, and I still find comfort in the embrace of a Makefile.  
├── README.md        - This is for you, your future self, your colleagues, or, the world.  
├── scripts          - Here, I tend to keep shell scripts or such that I invoke from the Makefile.  
├── src              - Everything you write, the source code of your project, write it here.  
│   └── main.py      - I usually start developing here, it is executable from the beginning; it configures logging and prints a friendly message.
├── storage          - A place for you to store whatever you need.  
│   ├── data         - Data files, databases, program state, etc.  
│   │   └── .gitkeep - .gitkeep - Git does not track empty folders.  
│   └── logs         - Chronicling the silent narrative of your program’s evolution.  
│       └── .gitkeep - .gitkeep - Adding .gitkeep ensures empty folders are preserved.  
├── venv             - A virtual environment for your project, created automatically.  
  
### Requirements
On Ubuntu/Debian (Linux):
Make sure you have Python 3 installed along with the venv module:
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv
```
Even though venv is part of the standard library since Python 3.3, some distros package it separately.

--------------------------------
On macOS:
Python 3 comes pre-installed. To create a virtual environment:
```bash
python3 -m venv venv
```
Or install Python 3 via Homebrew:
```bash
brew install python3
```
Ensure that the folder that contains the 'python' binary is in your PATH.

### Running
There are several ways.  
I will make several assumptions, such as that you have a `python` executable, I developed on ubuntu 24.04 with 
Python 3.12.3
That you have `git` and coreutils :)  
That you have `docker`
```bash
~/ $ git clone https://github.com/ndjuric/docusense.git && cd docusense
~/docusense/ $ python -m venv venv
~/docusense/ $ source venv/bin/activate
(venv) ~/docusense/ $ pip install -r requirements.txt
```

I tend to use tmux or byobu, so at this point I usually split the terminal, spawning a new shell or.. tiling window manager users would just fire up a new terminal instance or.. well not to digress too much.  
Run
```
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1
```

Once docker pulls what is needed and runs elasticsearch, we can go back to the original shell, where our `pwd` output ends in `docusense` or in other words we are in docusense folder. Let's continue.

```bash
(venv) ~/docusense/ $ cd src
(venv) ~/docusense/src $ uvicorn main:app --reload
```
I developed like this, it reloads on change, but you can also run it simply like

```bash
(venv) ~/docusense/src $ python main.py
```

However you decide.. lets spawn a third shell
```bash
~/ $ cd ~/docusense 
~/docusense/ $ source venv/bin/activate
(venv) ~/docusense/ $ make tests
```

I think some explanation is in order, you might've noticed that there is a Makefile in project root, I do come from C and I almost never abandon good tools, and make is one of those tools.
So I tend to use Makefiles.

If you execute `make help` in `~/docusense/` (project root)
It will give you several commands:
```bash
(venv) ~/docusense (main ✗) make help
Available commands:
  make clean_pycache - Clean Python cache
  make tests - Run tests
  make run - Run the application
```

So instead of changing directories you can actually just do everythig from here by executing `make run`, `make tests` etc.
I used pytest for testing and made as many things as possible into classes with more or less low cyclomatic complexity. I set a limit for myself - to finish this in a set number of hours, although I do have limited experience with elastic, and was oh so happy as the last AI winter thawed and the age of actual semantic search dawned. As I read the assignment I wanted to actually *do* everything you wrote, but I did not.. the LLMService is simulated but packages, openai for openai and requests for ollama are there... Also, I've been getting mixed results when running tests in docker-compose environment, which would be the easiest, and when I set up everything step by step yet I started late but I do want to finish today


### UPDATE
I forgot about elasticsearch indexing timeout at test time... I added an endpoint to invoke from tests and refresh the index manually after adding documents.

