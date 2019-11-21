# Tornado MVC(Model View Controller)

A light weight MVC Framework based on Tornado Web Server with Twitter Bootstrap installed.

# Simple Installation

This project uses oficial [Twitter Bootstrap](https://github.com/twbs/bootstrap) dependency. Once you have clonend this porject, you need to update the dependencies.

1. Get the project into your working directory and update the dependecies:

    ```bash
    git clone https://github.com/luisjba/tornado-mvc

    cd tornado-mvc

    git submodule update --init --recursive
    ```
2. Install the requirements from requirements.txt file using pip:
    ```bash
    pip install -r requirements.txt
    ```
3. Build the mvc to install the submodules:
    ```bash
    make
    ```
# Running Tornado Web Server

The controllers are located in the `controllers` directory with the    [home controller](controllers/home_controller.py) as example. The view files are located in `views` directory with a [base layout](views/layouts/base.html) to be used as a template. By default, each controller try to load the views looking for its controller name   inside the `views` direcotry and then the view name according the action name (the prefix of each RequestHandler inside the controller). For the action index in the home controlle there is the  [index view](views/home/index.html) located at `views/home/index.html`

By default the framework load the index action of the home controller. Run the server with the following command:

    python app.py

The Tornado Web Server runs at 8888 port, you can browse at [localhost:8888](http://localhost:8888). If you want to run the Tornado Web Server at a custom port, use the flag `-p` followed by the port number you want to use. For example if you want tu run in the port 8080, run the following command:

    python app.py -p 8080




# Controllers and Actions as RequestHandler

The Tornado MVC Framework find for controllers files in the directory `controllers` and assing the name 

## Donate

If this project was usefull to you and want to thanks me you can buy me a cup of coffe.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GVCZHZPGL7E2U&source=url)

[![Donate QR Code](https://github.com/luisjba/docker-sagecell/raw/master/images/Donate_QR_Code.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GVCZHZPGL7E2U&source=url)