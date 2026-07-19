# MCP NLP Service

基于 MCP (Model Context Protocol) 的全面自然语言处理服务，提供 23 个纯 Python 标准库实现的文本处理工具。

## 特性

- **纯 Python 标准库**：无任何第三方依赖（无需 numpy/pandas/jieba/sklearn）
- **MCP 协议**：基于 `mcp.server.fastmcp`，可作为独立服务或嵌入其他应用
- **中英文双语支持**：所有工具均支持中文和英文文本处理
- **真实算法实现**：每个工具都是完整算法实现，非简单规则匹配

## 快速开始

```bash
# 安装依赖
pip install mcp

# 启动服务
python main.py
```

## 可用工具 (23个)

### 文本预处理
| 工具 | 说明 |
|------|------|
| `sentence_splitter` | 基于规则+统计的中英文分句 |
| `word_tokenizer` | 词典+最大匹配法分词（FMM+BMM） |
| `text_normalizer` | Unicode规范化、全角半角转换、空白清理 |

### 特征提取
| 工具 | 说明 |
|------|------|
| `tfidf_extractor` | TF-IDF特征提取（TF/IDF/TF-IDF排序） |
| `textrank_keywords` | TextRank关键词提取（PageRank迭代收敛） |
| `ngram_extractor` | N-gram语言模型（频率+PMI评估） |

### 文本分析
| 工具 | 说明 |
|------|------|
| `sentiment_analyzer` | 情感分析（正负面词典+否定词+程度副词） |
| `entity_extractor` | 实体提取（人/地/组织/日期/金额/邮箱/电话/网址） |
| `language_detector` | 语言检测（中/英/日/韩/法/德/西/俄/阿） |
| `readability_scorer` | 可读性评分（Flesch-Kincaid+字词复杂度） |

### 文本相似度
| 工具 | 说明 |
|------|------|
| `cosine_similarity` | TF-IDF余弦相似度 |
| `jaccard_similarity` | Jaccard系数（字/词/N-gram三粒度） |
| `edit_distance` | Levenshtein编辑距离（滚动数组DP） |
| `doc_similarity_matrix` | 文档相似度矩阵+层次聚类 |

### 摘要与分类
| 工具 | 说明 |
|------|------|
| `text_summarizer` | TextRank摘要（TF-IDF相似度+PageRank） |
| `text_classifier` | TF-IDF+朴素贝叶斯分类 |
| `kmeans_cluster` | K-Means++文本聚类 |

### 其他工具
| 工具 | 说明 |
|------|------|
| `keyword_frequency` | 词频统计+Zipf定律验证 |
| `collocation_extractor` | PMI+卡方检验搭配提取 |
| `text_generator` | 马尔可夫链N-gram文本生成 |
| `char_frequency_analyzer` | 字符频率+Shannon熵 |
| `document_stats` | 文档综合统计 |
| `stopword_manager` | 停用词管理（中/英+自定义） |

## 使用示例

通过 MCP 客户端调用工具：

```python
from mcp import Client

async with Client("http://localhost:8000") as client:
    # 情感分析
    result = await client.call_tool("sentiment_analyzer", {
        "text": "这个产品非常好用，质量出色！"
    })
    print(result)

    # 关键词提取
    result = await client.call_tool("textrank_keywords", {
        "text": "自然语言处理是人工智能领域的重要方向...",
        "top_k": 10
    })
    print(result)
```

## 项目结构

```
mcp-nlp-service/
  main.py     # MCP NLP 服务主文件（23个工具）
  SKILL.md    # 技能元数据
  README.md   # 项目文档
```
