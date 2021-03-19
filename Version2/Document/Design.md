

# 设计思路



![流程图](DesignFig\fig1.jpg)

## 原始源代码文件

原始源代码文件包括cpp文件和.h文件和makefile等。(只处理cpp文件，其他文件不做处理)

## 预编译

为优化头文件内计算代码，将cpp程序预编译，每个cpp在头部得到头文件内内容，将头文件删除


## 前端部分

前端读取原文件中的cpp文件，如file1.cpp, file2.cpp等，对于每个cpp文件进行静态分析与符号执行，将文件路径、个文件执行路径记录在相应的file1.ir, file2.ir等IR文件中。

将makefile文件中头文件字段去除（此处有疑问）。

####静态分析

- 找出与计算无关代码的位置。

- 确定数值计算部分和无关代码的关系，将代码分段

- 标定输出输入变量，便于符号执行找出trace


####符号执行

符号执行开始时由静态分析标定输入变量和输出变量

符号执行将每个分段中的约束和运算关系找出来



## IR文件

IR文件记录cpp文件的主要信息：

####1. 文件的绝对路径及文件名

采用优化数值计算部分，将优化代码替换回原文件的策略，所以有必要记录原文件位置。

####2. 分段集

在一个cpp文件中，根据一定的条件（分段规则在“仍需讨论的问题”中4和7有说明）将数值代码分成若干个分段，每个分段记录内容：

#####* 起止行号（在原始cpp文件源代码中的位置）

#####* 输入变量(iv1, iv2, iv3)

记录输入变量，以便于优化过程随机生成输入值

#####* 输出变量(ov1, ov2, ov3)

用于后端进行优化过程中的精度对比

#####* trace集

经过前端符号执行后，每个输出变量是一个表达式。一个trace包括约束和一个或多个表达式，表达式可包含循环、矩阵运算等结构，代码形式大致如下:

```c++
if(...){
	ov1 = ...+loop(iv2, iv3, ...)+...; // 整个式子里只出现 ivx
	ov2 = ...;
	...
}
if(...){
    ...
}
```
单条trace内容包括：

* 约束
* 输出变量的表达式

#####* 可后移数值无关代码及对应分段

无关代码表示分段中与数值计算无关的代码部分。在分段代码优化完成后，将无关代码贴在后面该分段后

#####* (暂定不需要)变量名及变量类型

## 后端（待定）

（第一版中优化思路）后端读取IR文件，对每条trace的每个表达式进行优化，优化步骤：

####1. 在约束内生成若干随机点

####2. 等价变换

对IR中每一条trace的每一个表达式进行等价变换。

####3. 变换后稳定检查

稳定后将点与路径都记录下，直至所有点都稳定或者变换次数超出限定最大值

####4. 形成稳定路径

将临近且稳定路径相同的点连接，形成一条在某范围稳定的路径

####5. 将稳定路径转换成代码

将稳定路径转换成代码替换到原文件中。

优化后原cpp文件数和文件名都不发生改变。

#### 将来可能的改进

- 识别iR中循环等结构，进行循环与前后代码的全局优化
- 加入处理循环等结构的规则


##仍需讨论的问题

#### 1. 循环(已解决)

对于循环结构，如果直接进行符号执行提取路径的话，那么路径有可能会非常多，并且每条路径都很有可能非常长，无可读性，无从进行分析和优化。所以对循环进行预处理：

循环的一般形式

```c++
	while(constrain1)
	{
	    statement1;
	    while(){         // 和外层一样
            ...
	    }
	    if(constrain2)
	    {
	        statement2;
	        continue;
	    }
	    f();
	    if(constrain3)
	    {
	        statement3;
	        break;
	    }
	}
```
改写成以下形式：

```c++
	
	while(true)
	{
        if(constraint1){  //将循环条件写进循环体内
            break;
        }
	    statement1;	    
	    while(true){         // 和外层一样
            ... 
	    }
	    if(constrain2){
	        statement2;
	        continue;
	    }
	    f();
	    if(constrain3){
	        statement3;
	        break;
        }
	}
```





1. 改写成通用形式，循环条件写进去

```c++
while(true)
	{
        if(constraint1){
            break1;
        }
	    statement1;	    
	    if(constrain2){
	        statement2;
	        continue;
	    }
	    if(constrain3){
	        statement3;
	        break2;
        }
	}
```
2. 找出所有break与continue的路径，最终循环体中只存在互斥的几条路径

```c++
while(true){
    if(constraint1){break1;}     //break1路径
    else if(!constraint1&&!constraint2&&constraint3){  //break2路径条件及执行的语句
        statement1;
        statement3;          //根据路径上执行语句可提出变量更新过程（实际的路径情况要更复杂）
        break2;
    }
    else if(!constraint1&&constrain2){
        statement1;
        statement2;       //continue路径，由于是if-else if的形式，continue被自然省略了
    }
    //没有到达任何一个break和continue的路径
    else if(...){
        statement1;
    }
}
```



对于每块（if或者else if块），抽象成(c, s, [b])，循环被表示成{(c, s, [b]), ...}集合

故循环可被写成一下形式：

L -> { (c1, s1, [b1]), (c2, s2, [b2]), ... }

循环在一个具体的上下文中，循环内的变量与程序输入变量有一定的对应关系，记对应关系为A: liv1 = f(iv1,iv2,...), liv2 = f(iv1, iv2, ...), ...

ov1在循环L内的变量更新情况可记为：L<sub>ov1A</sub>

更进一步优化，可将循环内与ov1更新无关的路径去除掉。

-------

例子：

```c++
程序输入变量：pi1, pi2
iv1 = pi1 + pi2;
iv2 = pi1 + 1;
ov1 = iv1 + iv2;
ov2 = 2 * iv1
while(ov1<ov2){         //循环内输入变量iv1,iv2(没有写操作);输出变量ov1,ov2;
    if(ov2<10){
        ov2+=iv2;
        continue;
    }
    if(ov1>20){
        break;
    }
    ov1 = ov1 * iv1;
}

while条件内移:
iv1 = pi1 + pi2;
iv2 = pi1 + 1;
ov1 = iv1 + iv2;
ov2 = 2 * iv1
while(True){
    if(ov1<ov2){break1;} //循环条件移到循环体内
    if(ov2<10){
        ov2 += iv2;
        continue;
    }
    if(ov1>20){
        ov1--;
        --------      //break2路径执行到这里
        break2;
    }
    ov1 = ov1 * iv1;
}

求break和continue的路径，以及不会遇到break和continue的路径
while(True){
    if(ov1<ov2) {break1;}   //第一个break路径
    else if(!(ov1<ov2)&&!(ov2<10)&&(ov1>20)) {//break2路径
    	ov1=ov1-1;
    	break2;
    } 
    else if(!(ov1<ov2)&&(ov2<10)) {//continue路径
    	ov2 = ov2+iv2;
    	//continue;           
    }
    
    //不会遇到break和continue的路径
    else if(!(ov1<ov2)&&!(ov2<10)&&!(ov1>20)){
        ov1 = ov1*iv1;
    }
    else if(...){
    	...
    }
}
```





#### 2. 递归

递归：f1->f2->f3->f1, 形成函数调用环的情况

------

将调用环重写成一个函数

```c++
f(int n){
    if(n<=0){
        return 0;
    }
    return g(n);
}
g(int n){
    n --;
    return f(n-1);
}

改写：
f(int n){
    if(n<=0){
        return 0;
    }
    n--;
    return f(n-1);
}
```



-----



```c++
int f(int n){
    if(constraint1) return 1;
    statement1;
    f(n-1);
    if (constraint2) {
        return 1 + f(n-1);
    }
    if(constraint3){
        statement2;
        if (constraint4) f(n-2);
        statement3;
        return f(n-3);
    }
    return -1;
}
```

根据return找出互斥的几条路径，同时在每条路径中，都找出调用自身的路径

```c++
int f(int n){
    if(constraint1) return 1;
    else if(constraint2）{
        statement1;
        f(n-1);
       	return 1 + f(n-1);
    }
    else if (constraint3) {
        statement1;
    	f(n-1);
    	statement2;
    	if (constraint4) f(n-2);
    	statement3;
    	return f(n-3);
    }
    else {
        statement1;
    	f(n-1);
        return -1;
    }
}
```

recur -> { (c, path, r), ... }, c是条件，path -> {(c, s, f)}, r代表返回值。 其中path代表路径中变量更新和递归调用，中c代表条件，s代表变量更新语句, f代表自我调用

上述例子 -> { （constraint1, {}, 1）, 
（constraint2, { (, statement1, f(n-1)) }, 1+f(n-1)），
（constraint3 , { (, statement1, f(n-1)), (constraint4,  statement2, f(n-2)), (!constraint4, statement2&statement3 , ) , ( , statement4, )}，f(n-3)）
（ , { statement1, f(n-1)}, -1）
}

每次递归，选择其中一个进行执行



#### 3. 矩阵

矩阵的操作在代码中体现为一到多层的循环，从循环最内层开始抽取，提取出操作信息，判断能否进行下一步的优化。对于行操作或者列操作，我们用数学上的区间符号来表示范围，开区间用小括号"()"表示，闭区间用"[]"表示。有多个循环，则标定从最内层循环开始的循环层数。

例如A[i0:i1)<sup>2</sup>[j0:j1)<sup>1</sup> = B[i0:i1)<sup>2</sup>[j0:j1)<sup>1</sup> + C[i0:i1)<sup>2</sup>[j0:j1)<sup>1</sup>表示

```
for (int i = i0;i < i1;i++) {
    for (int j = j0;j < j1;j++) {
        A[i][j] = B[i][j] + C[i][j];
    }
}
```

若提取到一定层数，不能够再向上提取（循环条件为已提取循环的下标），可用范围标识，例如：

A[i:i1)<sup>2</sup>[j0:j1)<sup>1</sup> = B[i:i1)<sup>2</sup>[j0:j1)<sup>1</sup> + C[i0:i1)<sup>2</sup>[j0:j1)<sup>1 </sup>for i in [0, n];



矩阵操作典型场景：

```c++
//交换i，j两行操作, A[i][0:n), A[j][0:n) = A[j][0:n), A[i][0:n)
for (int p = 0;p < n;p++) {
    //A[i][p], A[j][p] = A[j][p], A[i][p]
    int tmp = A[i][p];
    A[i][p] = A[j][p];
    A[j][p] = tmp;
}

```

```c++
//C = A + B (m*n阶)
for (int i = 0;i < m;i++) { //C = A + B
    for (int j = 0;j < n;j++) { //C[i][0:n) = A[i][0:n) + B[i][0:n)
        C[i][j] = A[i][j] + B[i][j]; //元素相加
    }
}

//C = A * B (m阶)
for(int i = 0; i < m; i++) {   //C = A * B
    for(int j = 0; j < m; j++) {   //C[i][0:m) = A[i][0:m] · B
        for(int k = 0; k < m; k++) { //C[i][j] = A[i][0:m] · B[0:m][j]
            C[i][j] += A[i][k] * B[k][j];
        }
    }    
}    
```



-----



高斯消去代码

```c++
//消下三角(n * n+1)
for(int i=0;i<n;i++) {   //从第一行开始
    //优化后此处应加上选出k列绝对值最大的元素所在的行
    for(int j = i+1;j<n;j++) { //  rowi之下的每一行 - alpha*rowi
        for(int k = i;k<n;k++) {    // rowj - alpha*rowi
            A[j][k] -= A[j][i] / A[i][i] * A[i][k];  
        }
    }
}

//回代
for(i = n-1;i >= 0;i--)
{
    for(j = i+1;j < n;j++)
    {
        A[i][n] -= A[i][j]*X[j];
    }
    X[i] = A[i][n] / A[i][i];
} 
```

优化后代码

```c++
//消元
for(int i=0;i<n;i++) {   //从第一行开始

    //优化，将最大行移动到当前行
    int maxr = i;
    for (int p = i+1;p < n;p++) {
        maxr = A[p][i] > A[maxr][i] ? p: maxr; 
    }
    for (int p = 0;p < n;p++) {
        int tmp;
        tmp = A[i][p];
        A[i][p] = A[maxr][p];
        A[maxr][p] = tmp;
    }

    for(int j = i+1;j<n;j++) { //  rowi之下的每一行 - alpha*rowi
        for(int k = i;k<n;k++) {    // rowj - alpha*rowi
            A[j][k] -= A[j][i] / A[i][i] * A[i][k];  
        }
    }
}

//回代
for(i = n-1;i >= 0;i--)
{
    for(j = i+1;j < n;j++)
    {
        A[i][n] -= A[i][j]*X[j];
    }
    X[i] = A[i][n] / A[i][i];
} 
```



-----

提取思路还是一层一层来，

```c++
//A{i+1,n}[i:n] -= A{i+1,n}[i] / A[i][i] * A[i][i:n) for i in (0,n) -> Gauss Elimination
for(int i=0;i<n;i++) {   //从第一行开始,[)表示第一层提取，{}表示第二层提取
    //继续提取，A[i+1,n)2[i:n)1 -= A[i+1,n)2[i] / A[i][i] * A[i][i:n)1
    for(int j = i+1;j<n;j++) {
        //提取最内层信息，A[j][i:n)1 -= A[j][i] / A[i][i] * A[i][i:n)1, 
        for(int k = i;k<n;k++) {
            A[j][k] -= A[j][i] / A[i][i] * A[i][k];  
        }
    }
}
//A[j][k] -= A[j][i] / A[i][i] * A[i][k]，k∈(i,n)，j∈(i+1,n),i∈（0,n）

//回代
//{A[i][n] -= A[i][i+1:n) * X[i+1:n), X[i] = A[i][n] / A[i][i] } for i in [n-1:0];
for(i = n-1;i >= 0;i--) {
    //A[i][n] -= A[i][i+1:n) * X[i+1:n)
    for(j = i+1;j < n;j++) { 
        A[i][n] -= A[i][j] * X[j];
    }
    X[i] = A[i][n] / A[i][i];
} 
```

提取后的消下三角： A[i+1,n)<sup>2</sup>[i:n)<sup>1</sup> -= A\[i+1,n)<sup>2</sup>[i] / A\[i\][i] * A\[i\]\[i:n)<sup>1</sup> for i in [0, n);

回代代码表示为：( A\[i\]\[n\] -= A\[i\]\[i+1:n) * X[i+1:n), X[i] = A\[i\]\[n\] / A\[i\]\[i\] ) for i in [n-1, 0];

优化后： { Ri(A) <-> Rmax(A) by R[i], A[i+1,n)<sup>2</sup>>[i:n)<sup>1</sup> -= A\[i+1,n)<sup>2</sup>>[i] / A\[i\][i] * A\[i\]\[i:n)<sup>1</sup> } for i in [0, n);  { A\[i\]\[n\] -= A\[i\]\[i+1:n) * X[i+1:n), X[i] = A\[i\]\[n\] / A\[i\]\[i\] } for i in [n-1, 0];

代码：

```c++
//消元
for(int i=0;i<n;i++) {   //从第一行开始

    //Ri <-> Rmaxr
    //优化，将最大行移动到当前行
    int maxr = i;
    for (int p = i+1;p < n;p++) {
        if (A[p][i] > A[maxr][i]) maxr = p;
    }
    for (int p = 0;p < n;p++) {
        int tmp = A[i][p];
        A[i][p] = A[maxr][p];
        A[maxr][p] = tmp;
    }

    for(int j = i+1;j<n;j++) { //  rowi之下的每一行 - alpha*rowi
        for(int k = i;k<n;k++) {    // rowj - alpha*rowi
            A[j][k] -= A[j][i] / A[i][i] * A[i][k];
        }
    }
}


//回代
for(i = n-1;i >= 0;i--)
{
    for(j = i+1;j < n;j++)
    {
        A[i][n] -= A[i][j]*X[j];
    }
    X[i] = A[i][n] / A[i][i];
} 
```



#### 4. 交替代码(已解决)

代码中可能含有用到中间结果的代码，此时需要将代码分段优化。比如输出一个变量，这个时候要把代码分段，分段的位置可以是这个输出变量语句的前一个对该变量的写操作之后，或者是输出变量语句后面第一个对该变量的写操作之前。

例如：

```c++
...
c = a + b
//可以在此处分割
output(c)
e = c + d
//或者在此处分割
c++
...
```

output(c)输出c的中间结果，在下一次与上一次的c的写操作之间将代码分割开，`output(c)`就是交替代码

将代码从与数值计算无关的地方分段（考虑靠前还是靠后切），记录到每个分段中无关代码（控制台输出等不参与优化的代码）信息，待优化后将其放在优化后代码的后面。

最理想的方式，增加一倍的复杂度，对于每一个分段，两种方式都试一下，确定一个比较好的方式

#### 5.trace集表达方式(根据循环的处理方式确定)
```
 if(constrain){
    ov1=...;
    ov2=...;
    ...
}
```
or
```
ov1 = ...if(constrain1)
ov2 = ...if(constrain2)
...
```
哪种好一些（或许第一种比较好一些，避免条件异构的问题）

#### 6.需优化的代码在头文件.h里(暂时已解决)

编译预处理先做掉，使原始项目的每一个cpp都已经带上了头文件，直接优化预处理后的cpp。

#### 7.数值计算分段依赖于非数值计算的数据 (已解决)
非数值计算的部分如果依赖数值计算结果的话，和4.交替代码的处理类似，分段分裂。

如果非数值计算的部分不需要数值计算的分段结果，可以将它移到分段之前，并将非数值计算部分的输出数据作为当前分段的一个输入。  