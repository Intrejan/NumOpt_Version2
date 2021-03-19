environment config
==================
Our program run on ubuntu16.04 with python3.6, you can install python3.6 and pip3 on ubuntu16.04 with:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.6
    sudo apt install curl
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3.6 get-pip.py

install antlr4 and python packege antlr4-python3-runtime :

    sudo pip3 install antlr4-python3-runtime==4.7.1
    sudo pip3 install sympy==1.1.1


install clang

    sudo apt install clang


install iRRAM
-------------
安装iRRAM之前，先运行以下命令

    sudo apt install m4
    sudo apt-get install autoconf automake libtool

download [gmp-6.0.0](ftp://ftp.gmplib.org/pub/gmp/gmp-6.0.0.tar.bz2) and [mpfr-3.1.2](https://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.bz2).


first, install gmp-6.0.0

    tar -zxvf gmp-6.0.0.tar.bz2
    cd gmp-6.0.0
    ./configure
    make
    sudo make install

然后安装mpfr-3.1.2

    tar -zxvf mpfr-3.1.2.tar.bz2
    cd mpfr-3.1.2
    ./configure
    make
    sudo make install

最后安装iRRAM

    git clone https://github.com/norbert-mueller/iRRAM.git
    进入iRRAM文件夹
    sudo ./QUICKINSTALL_run_me
    按照提示，三个步骤:
    
        第一个问你用系统装好的gmp和mpfr还是再下载或者用本地的安装包，选择1选项用安装好的gmp和mpfr.
        之后会问你安装在本地还是系统目录下，选择安装到本地
        然后问安装到哪个目录，默认安装到当前iRRAM目录下的installed文件夹内，输入目录或者直接回车使用默认地址。

最后检查代码的Scipt/makefile和Source/backend/config.py中iRRAM_HOME变量是否与你的iRRAM安装位置一致。
需要检查和改动的位置：

    Script/Makefile中第四行的iRRAM_HOME
    Source/backend/config.py中第六行的iRRAM_HOME


run
===
run command in ./Script/:

    sh bench_eval.sh

results
=======
you can get some result files of each case in ./Result/casename, in which there is a file named error.rd that record the errors of the case with optimization and without. 

The optimization generate a new code for the cases, which are in Banary/OptimizedCode/.

What in directory herbieOptimized and irramOptimized are the codes optimized by our program, by herbie and original. The corresponding executable file and points file are stored in Banary/obj/.
