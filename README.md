# 基于概念格的文件分类浏览器
------------
@[toc]
## 软件综述
### 1. 基本介绍
本软件是由[概念格(Concept Lattice)](https://baike.baidu.com/item/概念格/3649659?fr=aladdin "概念格(concept lattice)")作为底层数据支持而实现的多标签文件分类浏览器。其解决了传统的目录树结构存在的单一继承的问题，并借助概念格这一强大的理论工具简洁明了的实现了文件的多标签分类问题。
下载源码或关注软件进度：
项目地址：[github](https://github.com/ascodelife/FileM)、[码云gitee](https://gitee.com/an394922886/FileM)、[博客](https://blog.csdn.net/qq_34725782/article/details/102548313)。
### 2. MVC架构图
**开发环境：** Windows10 、[Python3.6](https://www.python.org)  、[Neo4j图数据库](https://neo4j.com/)
**图形库：** [Pyqt5](https://pypi.org/project/PyQt5/)
**附加说明：** 实线表示了部分依赖关系，仅作辅助说明。
![MVC架构图](https://img-blog.csdnimg.cn/20191015210654153.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
## 部分设计简述
下面，将对软件的部分关键设计思想，自底向上的进行简要描述，希望读者能指出设计中的纰漏与改进之处。
### 1. 图数据库(Graph Database)
在本软件中，图数据库主要负责概念格、格转目录树的存储与管理。
#### 1-1. 简要介绍


图数据库(Graph Database)是基于图论实现的一种新型的NoSQL数据库。图论中图的基本元素为节点和边，在图数据库中对应的就是节点和关系。

> 与图形数据库相比，关系模型数据库存在四点缺陷：对象关系的不匹配使得把面向对象的“圆的对象”挤到面向关系的“方的表”中；关系模型静态、刚性、不灵活的本质使得改变schema以满足不断变化的业务需求非常困难；关系模型很不适合表达半结构化的数据———而业界的分析家和研究者都认为半结构化数据是信息管理中的下一个重点；关系模型可以表达面向网络的数据，但是在遍历网络并抽取信息的能力上关系模型非常弱。通过以上分析比较，可以得出结论：当数据量较小且数据对象间关联关系固定时关系数据库可以很好的工作，然而当数据规模庞大，数据对象间的关系复杂且动态变化时，图形数据库则更为合适。[^1]

Neo4j图数据库中基本元素与概念

 1. 节点（Node）
图数据库中一个基本元素，用已表示一个实体记录，就像关系数据库中的一条记录一样。在Neo4j中节点可以包含多个属性（Property）和多个标签（Label），如图1-1所示，
![Node](https://img-blog.csdnimg.cn/20191015215903346.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图1-1 带有属性和标签的节点</font></center>

 2. 关系（Relationship）
同样是图数据库中的基本元素，用于连接两个节点，关系也称为图论的边（Edge）。关系和节点一样可以包含多个属性，但关系只能有一个类型（Type）。如图1-2所示，一个节点可以被多个关系指向或作为关系的起始节点，如图1-3所示，多个关系指向同一节点。特别注意一个节点可以存在指向自己的关系，如图1-4所示。
![Relationship1](https://img-blog.csdnimg.cn/20191015220824570.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图1-2 带有类型和属性的关系</font></center>

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191015221220289.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图1-3 多个关系指向同一节点</font></center>

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191015221108203.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图1-4 关系的起始、结束节点为同一节点</font></center>

 3. 属性
上面提到节点和关系都可以有多个属性。属性是由键值对组成的。属性值可以是基本的数据类型，或者由基本数据类型组成的数组。需要注意的是，属性值没有null的概念，如果一个属性不需要了可以直接将整个键值对都移除。表2-1列出了属性值的基本数据类型。
<center> <font face="黑体">表1-1 属性值类型</font></center>

|类型|说明 |取值范围
|--|--|--|
|boolean  | 布尔值 |true/false
|byte|8位的整数|-128 to 127,inclusive|
|short|16位的整数|-32768 to 32767,inclusive|
|int|32位的整数|-2147483648 to 2147483647,inclusive|
|long|64位的整数|-9223372036854775808 to 9223372036854775807,inclusive|
|float|32位的IEEE 754标准浮点数||
|double|64位的IEEE 754标准浮点数||
|char|16位无符号整数代表的字符|u0000 to uffff(0 to 65535)|
|string|Unicode字符序列||
 4. 路径
当使用节点和关系创建一个图后，在此图中任意两个节点间都是可能存在路径的，如图1-5所示。图中任意两个节点都存在由节点和关系组成的路径，路径也有长度的概念，也就是路径中关系的条数。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191015221342261.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图1-5 路径</font></center>

 5. 遍历（Traversal）
遍历一张图就是按照一定的规则，根据它们之间的关系，依次访问所有相关联的节点的操作。
对于遍历操作不必自己实现，因为Neo4j提供了一套高效的遍历API，可以指定遍历规则，然后让Neo4j自动按照遍历规则遍历并返回遍历结果。遍历规则可以是广度优先也可以是深度优化。

**参考书目：**
 1. 张帜，庞国明，胡佳辉，苏亮.Neo4j权威指南[M].北京:清华大学出版社,2017.
 2. 陈韶健.Neo4j全栈开发[M].北京:电子工业出版社,2017
 3. (美)Ian Roblinson等著.图数据库[M].刘璐，梁越译.北京:人民邮电出版社.

#### 1-2. 概念格的存储

 1. 节点
 用图数据库存储概念格比起存储其他图而言，如：社交图（Social Graph）,兴趣图（Interest Graph）等，同属于不同概念格之间的节点并没有任何关系。因此，一个概念格节点通常只有一个标签，即以其所属格为命名的标签。
 2. 关系
 在概念格中，关系较为简单，通常仅有父子关系，且关系没有属性，因此关系的类型可以命名为孩子（child）或双亲（parent）。
 3. 属性
概念格节点的属性如表2-2所示。
<center> <font face="黑体">表1-2 概念格节点属性</font></center>

| 属性名 | 类型 |说明|必选属性|
|--|--|--|--|
|id | int | 自动生成的唯一的内部标识|是
|extents|list[string]|外延的集合|是
|intents|list[string]|内涵的集合|是
|is_inf|bool|是否是inf节点|否
|is_sup|bool|是否是sup节点|否

#### 1-3. 目录树的存储 
<center> <font face="黑体">表1-3 目录树节点属性</font></center>

| 属性名 | 类型 |说明|必选属性|
|--|--|--|--|
|id | int | 自动生成的唯一的内部标识|是
|concept_id|int|标明该节点来源于概念格的哪个节点|是
|is_obj|bool|true：节点为文件节点，false:该节点为文件夹节点|是
|value|string|节点的值|是
|is_root|bool|标识节点是否是根节点|否

#### 1-4. 存在的改进空间
节点的内部id是由数据库自动生成的身份标识，[在有关资料中称](https://cloud.tencent.com/developer/ask/221534)，不应该使用自动生成的id作为身份标识使用，因为当节点删除时，它是随时可以被重用的，使用id执行查找可能会指向一个完全不同的新的节点数据。
因此，应该自己维护一套索引。
### 2. 数据模型(Data Model)
[数据模型（Data Model）](https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E6%A8%A1%E5%9E%8B/1305623?fr=aladdin)是数据特征的抽象。数据（Data）是描述事物的符号记录，模型（Model)是现实世界的抽象。数据模型从抽象层次上描述了系统的静态特征、动态行为和约束条件，为数据库系统的信息表示与操作提供了一个抽象的框架。数据模型所描述的内容有三部分：数据结构、数据操作和数据约束。
#### 2-1. 简要介绍
<center> <font face="黑体">表2-1 数据模型与说明</font></center>

|数据模型| 说明 |
|--|--|
| FileModel | 文件模型，以json串的形式存储在配置文件中 |
|FileLabelModel|文件标签模型， 以json串的形式存储在配置文件中|
|LatticeModel|概念格模型，以图的形式存储在Neo4j图数据库中
|ConceptNodeModel|概念格节点模型，以节点的形式存储在Neo4j图数据库中
|Lattice2TreeModel|概念格转目录树模型，同LatticeModel
|TreeNodeModel|目录树节点模型，同ConcepNodeModel

#### 2-2. 模型间的依赖关系
如图2-1所示，
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191018023733611.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图2-1 模型间的依赖关系</font></center>
 

#### 2-3. 存在的改进空间
目前FileModel和FilelabelModel主要保存在本地配置文件中，当文件数量和标签数量增长时，频繁读写必定会造成IO上的性能限制，配置文件应该只保存用户界面的一些配置信息，而不应该作为数据存储。
实际上，文件和标签也可以存储在图数据库上，并且也很符合其设计思想。

>  图数据库对于处理呈现出复杂网络结构的标签系统有着明显优于关系型数据库的优势和实用价值。[^2]

大致设计思想如图2-2所示，
![图数据库存储文件和标签](https://img-blog.csdnimg.cn/20191016111537197.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzI1Nzgy,size_16,color_FFFFFF,t_70)
<center> <font face="黑体">图2-2 图数据库存储文件和标签</font></center>

顺带一提的是，文献[^2]也提供了多用户编辑文件标签的设计方法，但显然这不是当前需要改进的重点。

### 3. 核心算法(Core Algorithm)
本软件中使用的核心算法主要有4种，下面将对这些核心算法进行简要阐述。
#### 3-1. 简要介绍
软件中使用的4种核心算法分别来源于3篇文献，具体对应关系参照下表3-1所示，
| 函数名 | 功能 |参考文献|其他说明|
|--|--|--|--|
|  add_concept(ConceptNodeModel)| 在概念格中添加一个新的概念节点，并生成新的概念格。|[^3]|基于对象的概念格渐进式生成算法|
|remove_attribute(attribute:String)|在概念格中移除一个对象属性。|[^4]|渐进式属性消减|
|remove_object(object:String)|在概念格中移除一个对象。|[^4]|渐进式对象消减|
|translate_lattice_to_tree|将已有概念格转为目录树结构。|[^5]|
#### 3-2. 与其他算法的对比及思考
 1. 文献[^3]中给出了基于对象的概念格渐进式生成算法，同时在文献[^6]中给出了基于属性的概念格渐进式生成算法，后者将两种算法进行对比，得出了结论。
 > 在实际的数据表中，数据表的记录( 对象) 的个数会越来越大，而字段( 属性) 的个数往往是有限的。 因此，实际的形式背景大多是对象的个数比属性的个数大得多。这样，在通常情况下，采用基于属性的渐进式生成算法构造概念格会更快些。

在软件实际运行过程中，前期用户会新建大量标签用于文件分类，后期其主要操作是在已有的标签中选择标签对文件进行分类，因此后者的算法可能会带来更好的运行效率。但运行效率不是目前考虑的重点，可以作为今后改进的方向。

 2. 文献[^4]中给出了概念格的属性渐减的算法，因为属性和对象是对偶的，所以我们可以很简单的写出概念格的对象渐减的算法。后人提出了概念格多属性渐减式构造算法[^7]，并给出结论：
 > 本文给出的概念格多属性渐减式构造算法与文献[^4]中的概念格减少单属性渐减式构造算法具有相同的时间复杂度,然而减少多个属性时,文献[^4]的算法需要执行多次,本文算法只需执行一次. 

在软件实际运行过程中，用户极有可能对一批已经失效的文件或标签进行批量删除，此时后者的算法也可以带来更高的运行效率。但依然不是目前考虑的重点。

 3. 沈夏炯等人在文献[^5]中给出了概念格转目录树后用于可视化的基本思想方法，但没有指出文件（资源）在目录树中如何存放。
其学生发表的文献[^8]在其基础上给出了资源的多路径访问算法，经过简单验证，该算法效果可能并不理想或者不适合用于此软件。
因此软件的格转树算法在前者[^5]的基础上，对细节进行优化，并指出了文件在目录树中存储的位置，并以节点的形式存储在图数据库中。通过遍历root节点到所有出度为0的节点（即文件节点）的所有可能路径，来得到文件在目录树中的存放地址。

### 4. 用户操作(User Operation)
#### 4-1. 基本操作介绍

 1. 添加文件
 2. 删除文件
 3. 添加标签
 4. 删除标签
 5. 编辑文件标签
 6. 刷新目录

#### 4-2. 算法调用
<center> <font face="黑体">表4-1 用户操作与算法对应关系</font></center>

|用户操作| 调用算法 |
|--|--|
| 添加文件 | add_concept(ConceptNodeModel) |
| 删除文件 | remove_object(obj_name)|
| 添加标签 |无|
| 删除标签 |remove_attribute(atr_name)|
|编辑文件标签|remove_object(obj_name)->add_concept(ConceptNodeMoel)|
|刷新目录|translate_lattice_to_tree|


#### 4-3. 存在的改进空间
目前的用户界面仅仅是为了验证思想，显然，这是一个用户不友好的界面，我们也一直在寻找和探求更好的利用概念格进行信息检索的策略，如果您有更好的想法，欢迎与我们交流。
## 总结与反思
**个人的不足之处**
 1. 学习和工作效率太低，没有充分利用时间。
 2. 所作工作深度不足，缺乏创新性。
 3. 理论知识储备太少，导致语言表述和实际开发设计过程中遇到不必要的问题。
 
 **改进方向**
 
 1. 做好规划，更合理的分配时间。
 2. 加强理论知识的学习，多看文献多交流多思考。

## 参考文献
[^1]:王余蓝.图形数据库NEO4J与关系据库的比较研究[J].现代电子技术,2012,35(20):77-79.
[^2]: 王慧孜,范炜.图数据库在标签系统中的应用研究[J].数字图书馆论坛,2015(04):21-27.
[^3]: Godin, R. , Missaoui, R. and Alaoui, H. (1995), INCREMENTAL CONCEPT FORMATION ALGORITHMS BASED ON GALOIS (CONCEPT) LATTICES. Computational Intelligence, 11: 246-267. doi:10.1111/j.1467-8640.1995.tb00031.x
[^4]: 张磊,张宏莉,殷丽华,韩道军.概念格的属性渐减原理与算法研究[J].计算机研究与发展,2013,50(02):248-259.
[^5]: 沈夏炯,叶曼曼,甘甜,韩道军.基于概念格的信息检索及其树形可视化[J].计算机工程与应用,2017,53(03):95-99.
[^6]:李云,刘宗田,陈崚,沈夏炯,徐晓华.基于属性的概念格渐进式生成算法[J].小型微型计算机系统,2004(10):1768-1771.
[^7]:马垣,马文胜.概念格多属性渐减式构造[J].软件学报,2015,26(12):3162-3173.
[^8]:甘甜. 基于格结构文件系统的强化学习推荐模型研究及应用[D].河南大学,2016.

