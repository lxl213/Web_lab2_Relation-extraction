# Web_lab2_Relation-extraction
# Exp2:

### **Author:**

- **骆霄龙 PB18151853**
- **张越群 PB17051070**

## 程序概要：

对数据集实现了两种不同模型下的关系抽取，分别为基于TF-IDF与逻辑回归模型和BiLSTM模型实现。 并进行了模型融合 与预测结果的可视化与分析。

## 功能实现:

#### Model1:TF-IDF

- 主要利用sklearn的`TfidfVectorizer`和`LogisticRegression(solver='liblinear')`实现。 通过将训练数据用TfidfVectorizer编码后对`LogisticRegression(solver='liblinear')` 生成的模型进行训练。参数则使用默认参数。 随后对编码后的测试数据预测即可。

#### Model2:BiLSTM

- 模型参数: 其中Embedding层的embedding_size = 100。

<img src="/Users/xiaolongluo/Desktop/exp2/resource/model.png" alt="model" style="zoom:50%;" />

- 重要函数: 在源文件中已给出注释

## 环境相关:

- 编程语言: python3.6
- 开发工具:Jupyter notebook
- 依赖的库：
  - tensorflow
  - numpy
  - sklearn
  - keras
  - Matplotlib

- 运行方式: 直接运行jupyter notebook即可
