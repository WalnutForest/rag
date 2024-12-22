# 项目文档

## 一. 项目简介

本项目是一个基于streamlit和llama_index的对话web应用，可以实现知识库搭建，问答系统功能。

知识库搭建：用户可以上传自己的知识库，或者使用默认的知识库，进行知识库的搭建。

<img alt="img_1.png" src="md_images\知识库演示.png"/>

问答系统：用户可以输入问题，系统会依据知识库返回答案。

<img alt="img.png" src="md_images\对话演示.png"/>

## 二. 部署运行流程

### 使用conda的部署流程

创建conda环境

```shell
conda create -n env_name python=3.10.15
conda activate env_name
```

依据requirements.txt安装依赖包

```shell
pip install -r requirements.txt
```

下载项目文件，可以直接下载压缩包，也可以从github上下载

```shell
git clone https://github.com/WalnutForest/rag.git
```

根据提示输入项目临时token：
```text
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
```

进入项目文件夹

```shell
cd Rag
```

运行streamlit

```shell
streamlit run hello.py
```


