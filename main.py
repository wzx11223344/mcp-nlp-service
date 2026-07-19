#!/usr/bin/env python3
"""
MCP NLP Service — A comprehensive NLP processing server using the MCP protocol.
Provides 23 text processing tools implemented with pure Python standard library only.
"""
import re
import math
import json
import random
import collections
import hashlib
import unicodedata
from typing import List, Dict, Tuple, Set, Optional, Any
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nlp-service")

# ========================================================================
# BUILT-IN DICTIONARIES
# ========================================================================

# ---- Chinese Stopwords ----
_CHINESE_STOPWORDS = """
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你
会 着 没有 看 好 自己 这 他 她 它 们 那 这个 那个 什么 怎么 如何
因为 所以 但是 而且 然后 如果 虽然 虽然 不过 或者 还是 只是 可是
不是 就是 而是 而是 并且 或者 或者 除了 不仅 不但 不管 无论
把 被 让 给 对 从 在 到 于 向 和 与 同 跟 比 按 按照 根据 据
通过 经过 凭借 用 以 为 为了 因为 由于 对于 关于 至于 除了
作为 当作 沿着 顺着 朝 往 在 当 正在 已经 曾经 刚 刚刚 才 就
便 再 又 也 还 都 只 只要 只有 除非 除了 无论 不管 任凭 哪怕
竟然 居然 果然 自然 当然 显然 其实 实际上 本来 原来 根本 丝毫
几乎 差不多 大约 大致 大概 可能 也许 或许 应该 应当 必须 一定
的确 确实 真正 完全 十分 非常 特别 尤其 比较 相当 稍微 略微
很 极 太 最 更 越 更加 越发 愈 愈加 颇 极其 极为 格外 分外
个 只 条 件 种 样 些 点 些 次 回 趟 遍 番 阵 场 顿 口 下 次 位
吗 呢 啊 吧 呀 啦 哦 嗯 哈 哇 哟 罢了 而已 而已 罢了 算了
来 去 上 下 前 后 里 外 内 中 间 旁 左右 上下 以前 以后 以来
以外 之内 之间 之前 之后 上面 下面 前面 后面 里面 外面 旁边
这里 那里 哪里 这边 那边 哪边 这些 那些 哪些 这么 那么 怎么
谁 什么 哪 哪儿 哪里 哪些 怎么 怎样 怎么样 为什么 如何 何等
几 多少 多么 多 少 几多 几何 几时 多会儿 多久 多长 多大
我 你 您 他 她 它 我们 你们 他们 她们 它们 咱们 自己 本人
本人 咱 俺 大家 大伙 大家 诸位 各位 本人 本身 自个 自我
这 那 哪 此 彼 该 本 某 各 另 别的 其他 其余 任何 所有 一切
整个 全部 凡是 任何 有的 某些 有些 什么 一切 任何 所有 全部
""".split()

_CHINESE_STOPWORDS = set(w for w in _CHINESE_STOPWORDS if w.strip())

_ENGLISH_STOPWORDS = set("""
a about above after again against all am an and any are as at be because
been before being below between both but by can did do does done due during
each few for from further had has have having here hereinafter hereby herein
hereof hereon hereto hereunto hereupon herewith how however if in into is it
its itself just like many me might more most much must my myself no nor not
now of on once only or other our ours ourselves out over own per quite rather
really same shall she should show side since so some such than that the their
them themselves then there thereby therein thereof thereon thereto thereunto
thereupon therewith these they this those through thus to too under until up
upon us very was we were what when where whereby wherein whereof whereon
whereto whereunto whereupon wherever whether which while whither who whom
whose why with within without would yes yet you your yours yourself yourselves
""".split())

# ---- Sentiment Dictionaries ----

_CHINESE_POSITIVE = set("""
好 优秀 出色 漂亮 美丽 精彩 完美 棒 极好 绝妙 卓越 杰出 非凡 伟大 光荣
正确 对 喜欢 爱 热爱 赞赏 欣赏 赞美 赞扬 称赞 夸奖 满意 开心 快乐 高兴
幸福 甜蜜 温馨 和谐 团结 进步 发展 成功 胜利 成就 突破 创新 领先 优势
先进 繁荣 富强 昌盛 兴旺 发达 健康 安全 稳定 和平 友好 善良 真诚 诚信
可靠 踏实 认真 勤奋 努力 坚强 勇敢 乐观 积极 主动 热情 大方 慷慨 宽容
理解 支持 帮助 贡献 奉献 牺牲 保护 关怀 体贴 温柔 温暖 光明 希望 梦想
前途 未来 美好 经典 著名 知名 一流 顶级 高级 专业 权威 正宗 地道 纯粹
聪明 智慧 机灵 敏锐 灵活 能干 高效 方便 实用 舒适 轻松 自由 新鲜 活力
丰富 多彩 全面 完整 清晰 明确 简单 容易 快速 及时 准确 精确 深入 透彻
感动 震撼 激动 兴奋 喜悦 欣慰 自豪 骄傲 羡慕 佩服 尊敬 崇拜 信任 放心
推荐 值得 适合 流行 时尚 潮流 热门 火爆 抢手 畅销 好评 优质 实惠 划算
便宜 省钱 节约 环保 节能 绿色 天然 有机 健康 养生 滋补 营养 美味 可口
香甜 鲜美 酥脆 嫩滑 爽口 解渴 清凉 消暑 保暖 御寒 舒适 透气 柔软 光滑
细腻 精致 典雅 高贵 豪华 奢华 气派 气度 风度 品味 格调 情调 浪漫 诗意
""".split())

_CHINESE_NEGATIVE = set("""
差 坏 糟 烂 臭 破 旧 脏 乱 差劲 恶劣 糟糕 失败 错误 缺点 缺陷 毛病 问题
困难 艰难 艰苦 辛苦 痛苦 悲伤 难过 伤心 悲哀 哀伤 忧愁 忧郁 郁闷 烦恼
烦躁 焦虑 担心 恐惧 害怕 惊慌 紧张 不安 不满 讨厌 厌恶 憎恨 仇恨 怨恨
愤怒 生气 恼火 气愤 暴怒 疯狂 崩溃 绝望 失落 沮丧 灰心 消极 悲观 失望
懒惰 虚伪 虚假 欺骗 欺诈 诈骗 撒谎 说谎 隐瞒 掩盖 掩饰 伪装 假装 做作
傲慢 偏见 歧视 轻视 鄙视 蔑视 侮辱 羞辱 嘲笑 讽刺 挖苦 讥讽 打击 压制
压迫 剥削 掠夺 侵占 侵犯 侵略 破坏 摧毁 毁灭 损害 伤害 危害 威胁 危险
危机 紧急 危急 严重 沉重 惨重 重大 巨大 庞大 臃肿 繁琐 复杂 麻烦 啰嗦
肮脏 龌龊 卑鄙 下流 无耻 下贱 低俗 庸俗 粗俗 粗鲁 暴力 残忍 凶残 狠毒
阴险 狡猾 奸诈 贪婪 自私 吝啬 小气 计较 嫉妒 羡慕 恨 怨 仇 冤 愤怒
紧张 拥挤 嘈杂 吵闹 喧嚣 混乱 无序 落后 倒退 退化 衰落 衰败 腐败 腐烂
腐朽 陈旧 过时 落后 原始 野蛮 粗暴 僵硬 死板 呆板 枯燥 乏味 无聊 空虚
寂寞 孤独 孤单 冷漠 冷淡 冷酷 无情 残忍 残酷 苛刻 严厉 严格 死板 僵化
漏洞 隐患 风险 危机 故障 崩溃 失灵 失效 停摆 停滞 受阻 受阻 延期 延误
亏损 赤字 负债 破产 倒闭 萎缩 下滑 下跌 贬值 缩水 损失 浪费 消耗 耗费
""".split())

_ENGLISH_POSITIVE = set("""
good great excellent wonderful fantastic amazing awesome beautiful brilliant
outstanding superb perfect magnificent splendid remarkable exceptional
terrific fabulous marvelous delightful lovely pleasant nice fine grand
superior impressive stunning breathtaking glorious exquisite elegant
charming graceful beautiful lovely pretty handsome gorgeous cute adorable
lovely wonderful happy glad cheerful joyful merry delighted pleased satisfied
grateful thankful blessed lucky fortunate successful prosperous thriving
flourishing booming growing improving advancing progressing developing
innovative creative original unique special extraordinary incredible
remarkable notable noteworthy significant important valuable useful helpful
beneficial advantages benefits positive optimistic hopeful bright promising
brilliant smart intelligent wise clever bright sharp quick fast efficient
effective productive powerful strong robust solid stable secure safe reliable
durable lasting timeless classic popular famous renowned celebrated admired
respected honored praised loved adored treasured cherished valued appreciated
enjoyable entertaining amusing fun exciting thrilling fascinating engaging
captivating inspiring motivating uplifting encouraging heartwarming touching
moving emotional passionate enthusiastic energetic vibrant lively dynamic
generous kind caring compassionate gentle warm friendly hospitable welcoming
""".split())

_ENGLISH_NEGATIVE = set("""
bad worse worst terrible awful horrible dreadful horrible horrible nasty
ugly unpleasant disagreeable poor inferior substandard unsatisfactory
inadequate deficient flawed defective broken damaged ruined destroyed
wrecked spoiled rotten decayed decomposed corrupt rotten foul disgusting
revolting repulsive offensive repugnant abhorrent detestable loathsome
hateful horrible awful terrible dreadful frightful ghastly hideous grim
gloomy bleak dreary dismal somber melancholy sorrowful sad unhappy miserable
distressed anguished grief stricken hurt wounded pained suffering agonizing
tormenting torturous painful excruciating unbearable intolerable unendurable
difficult hard tough challenging problematic troublesome vexing annoying
irritating frustrating aggravating infuriating maddening enraging anger
furious wrathful irate livid indignant resentful bitter spiteful vengeful
cruel brutal vicious ferocious savage barbaric inhumane heartless ruthless
merciless pitiless relentless unyielding stubborn obstinate rigid inflexible
harsh stern severe strict demanding exacting苛刻 rigorous stringent tough
dangerous risky hazardous perilous precarious unsafe unstable insecure
weak fragile frail delicate vulnerable susceptible prone liable subject
failure defeat loss setback reversal decline deterioration worsening
corruption decay rot decomposition putrefaction pollution contamination
poison toxic hazardous harmful damaging destructive detrimental injurious
hurtful damaging ruinous catastrophic disastrous calamitous devastating
tragic fatal lethal deadly mortal terminal incurable hopeless desperate
negative pessimistic cynical skeptical doubtful uncertain unclear vague
ambiguous confusing misleading deceptive false untrue incorrect wrong
error mistake fault flaw defect shortcoming weakness limitation drawback
""".split())

_BOOSTER_WORDS = {
    # Extreme boosters (weight 2.0)
    "极": 2.0, "极其": 2.0, "极为": 2.0, "极度": 2.0, "极端": 2.0,
    "绝对": 2.0, "完全": 2.0, "十分": 2.0, "非常": 2.0, "特别": 2.0,
    "尤其": 2.0, "格外": 2.0, "分外": 2.0, "万分": 2.0, "无比": 2.0,
    "超级": 2.0, "超": 2.0, "巨": 2.0, "爆": 2.0, "炸": 2.0,
    "extremely": 2.0, "absolutely": 2.0, "completely": 2.0, "totally": 2.0,
    "utterly": 2.0, "thoroughly": 2.0, "entirely": 2.0, "perfectly": 2.0,
    "very": 2.0, "really": 2.0, "highly": 2.0, "deeply": 2.0, "greatly": 2.0,
    # Moderate boosters (weight 1.5)
    "很": 1.5, "挺": 1.5, "好": 1.5, "蛮": 1.5, "颇": 1.5, "较": 1.5,
    "比较": 1.5, "相当": 1.5, "还算": 1.5, "quite": 1.5, "rather": 1.5,
    "pretty": 1.5, "fairly": 1.5, "somewhat": 1.5,
    # Weak boosters (weight 1.2)
    "有点": 1.2, "有些": 1.2, "稍微": 1.2, "略微": 1.2, "一点": 1.2,
    "a bit": 1.2, "a little": 1.2, "slightly": 1.2, "barely": 1.2,
}

_NEGATION_WORDS = {
    "不": -1, "没": -1, "没有": -1, "别": -1, "不要": -1, "不用": -1,
    "并非": -1, "不是": -1, "不能": -1, "不会": -1, "不行": -1, "不可以": -1,
    "从不": -1, "从没": -1, "从未": -1, "毫不": -1, "毫无": -1, "绝非": -1,
    "决不": -1, "绝不": -1, "并未": -1, "尚未": -1, "不大": -1, "不太": -1,
    "not": -1, "no": -1, "never": -1, "none": -1, "nothing": -1, "nobody": -1,
    "nowhere": -1, "neither": -1, "nor": -1, "cannot": -1, "can't": -1,
    "don't": -1, "doesn't": -1, "didn't": -1, "won't": -1, "wouldn't": -1,
    "couldn't": -1, "shouldn't": -1, "isn't": -1, "aren't": -1, "wasn't": -1,
    "weren't": -1, "haven't": -1, "hasn't": -1, "hadn't": -1, "ain't": -1,
}

# ---- Entity Dictionaries ----
_CHINESE_SURNAMES = set("""
赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜
戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳丰鲍史唐
费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄
和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁
杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍
虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚
程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓
牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙
叶幸司韶郜黎蓟溥印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双
闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍郤璩桑桂濮牛寿通边扈燕冀郏浦尚农
温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘
匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空
曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳
夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠
公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车
颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦
段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门
""".strip())

_COMMON_MALE_NAMES = set("""
伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元
全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林
有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江
超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士
以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘
""".strip())

_COMMON_FEMALE_NAMES = set("""
秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素
云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍
茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁
梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠
柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝丽阳
""".strip())

_COMMON_PLACE_SUFFIXES = set("""
市省区县镇乡村街道路大道街巷弄楼栋号室组屯里庄桥沟港湾岛山岭峰
江河流域海湖泊塘水库园林园场厂站所店馆院中心大厦广场公园花园
""".strip())

_COMMON_ORG_SUFFIXES = set("""
公司集团集团厂矿局处部委办厅局所站社院中心中心中心银行大学学院
学校中学小学幼儿园医院研究院研究所设计院协会学会商会工会妇联
委员会理事会董事会监事会集团股份有限有限责任股份有限集团有限
""".strip())

# ---- Common Chinese words for tokenization ----
_COMMON_CHINESE_WORDS = set("""
我们 他们 它们 她们 你们 自己 自己 什么 怎么 怎样 如何 为什么 哪个 哪些 哪里
因为 所以 虽然 但是 而且 并且 或者 如果 即使 尽管 不管 无论 不仅 不但 除了
可以 能够 应该 必须 需要 可能 也许 大概 或许 一定 肯定 当然 确实 的确 实在
已经 曾经 正在 将要 马上 立刻 顿时 忽然 突然 逐渐 渐渐 慢慢 快快 始终 一直
所有 一切 全部 整个 完全 全部 部分 许多 很多 大量 少数 一些 有点 有些 每个
之间 之前 之后 之上 之下 之中 之内 之外 前后 左右 上下 以来 以后 以前 现在
今天 明天 昨天 早上 晚上 中午 下午 上午 时候 时间 分钟 小时 天 月 年 周
工作 学习 生活 生产 发展 建设 管理 服务 经济 文化 教育 科技 技术 科学 研究
社会 国家 世界 国际 国内 市场 企业 公司 政府 组织 机构 系统 项目 产品 服务
问题 答案 结果 原因 方法 方式 过程 关系 影响 作用 意义 价值 水平 程度 规模
方面 领域 方向 范围 内容 形式 状态 条件 情况 形势 趋势 特点 特征 性质 本质
主要 重要 关键 核心 基本 基础 根本 重大 严重 必要 必要 充分 有效 直接 间接
进行 参加 参与 开展 实现 完成 达到 通过 采用 利用 应用 使用 运用 发挥 加强
提高 增加 减少 降低 保持 维持 保证 确保 促进 推动 推进 带动 引导 指导 领导
表示 说明 表明 反映 反应 指出 提出 提到 规定 确定 决定 制定 建立 形成 成为
认为 以为 觉得 感到 感觉 意识 注意 关注 重视 强调 突出 集中 统一 协调 配合
全面 深入 广泛 普遍 通常 常见 典型 特殊 特别 尤其 非常 十分 相当 比较 相对
绝对 完全 彻底 根本 基本 大致 大约 大概 几乎 将近 接近 超过 以上 以下 以内
第一 第二 第三 首先 其次 然后 最后 同时 此外 另外 总之 综上 综上所述 例如 比如
了解 理解 认识 熟悉 掌握 懂得 明白 清楚 知道 发现 发明 创造 创新 改革 开放
人民 群众 百姓 公民 成员 人员 人士 人口 人力 人才 人物 人选 人 事 物 时间
经济 政治 文化 社会 生态 文明 精神 物质 意识 存在 运动 变化 发展 联系 矛盾
统一 对立 相互 彼此 之间 之中 之中 其中 各自 分别 不同 相同 相似 相反 相对
人类 自然 宇宙 世界 地球 环境 资源 能源 信息 数据 知识 经验 理论 实践 实际
能力 素质 质量 效率 效益 效果 成果 成就 成绩 收获 得到 获得 取得 实现 完成
好 坏 大 小 多 少 长 短 高 低 深 浅 宽 窄 厚 薄 重 轻 快 慢 早 晚 先 后
新 旧 老 年轻 古老 现代 当代 古代 原始 传统 民族 民间 官方 正式 非正式
这个 那个 哪个 这些 那些 哪些 这里 那里 哪里 这边 那边 这边 这边 那边
上来 下来 进来 出来 回来 过来 起来 上去 下去 进去 出去 回去 过去 上去
不能 不会 不行 不可以 不可能 不得 不必 不用 无须 无需 未必 尚未 不曾
代表 参加 参与 参观 参考 参谋 参照 对比 针对 对象 对方 对手 对等 对称
发挥 发扬 发展 发掘 发现 发动 发射 发布 发生 发达 发明 发放 发行 发表
""".split())

# ---- Language detection ----
_CHINESE_RANGE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
_JAPANESE_RANGE = re.compile(r'[\u3040-\u309f\u30a0-\u30ff]')
_KOREAN_RANGE = re.compile(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]')
_ARABIC_RANGE = re.compile(r'[\u0600-\u06ff\u0750-\u077f]')
_CYRILLIC_RANGE = re.compile(r'[\u0400-\u04ff\u0500-\u052f]')
_DEVANAGARI_RANGE = re.compile(r'[\u0900-\u097f]')
_THAI_RANGE = re.compile(r'[\u0e00-\u0e7f]')

_ENGLISH_COMMON = set("the be to of and a in that have i it for not on with he as at".split())
_CHINESE_COMMON = set("的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到".split())
_JAPANESE_COMMON = set("の に を は が た で て と し れ さ ある いる する なる ない この".split())
_KOREAN_COMMON = set("이 그 그녀 의 에 는 가 을 를 도 에서 하다 있다 되다 보다".split())
_FRENCH_COMMON = set("le de la les et un une des dans pour sur avec par est sont".split())
_GERMAN_COMMON = set("der die das und den dem des ein eine einer eines einem".split())
_SPANISH_COMMON = set("el la los las de del con por para una un que es son".split())
_RUSSIAN_COMMON = set("и в на с не по от из у за о как что это".split())
_ARABIC_COMMON = set("في من على إلى عن كان مع هذا هذه ذلك".split())

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def _is_chinese_char(ch: str) -> bool:
    """Check if a character is Chinese."""
    return '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' or '\uf900' <= ch <= '\ufaff'

def _is_english_word(word: str) -> bool:
    """Check if a string is an English word (all ASCII letters)."""
    return bool(re.fullmatch(r'[a-zA-Z]+', word))

def _words(text: str) -> List[str]:
    """Simple English word tokenizer (split on whitespace/punctuation)."""
    return re.findall(r'[a-zA-Z]+', text)

def _chinese_chars(text: str) -> List[str]:
    """Extract Chinese characters from text."""
    return list(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', text))

def _is_punctuation(ch: str) -> bool:
    return bool(re.match(r'[,.!?;:\'"()\[\]{}<>《》，。！？；：""''（）【】、\-\—…·\s\n\r\t\\/]', ch))

# ---- Dictionary-based tokenizer (Maximum Matching) ----
_CHINESE_DICT: Set[str] = set()
_CHINESE_LONGEST = 4

def _ensure_chinese_dict():
    """Ensure the Chinese dictionary is initialized."""
    global _CHINESE_DICT, _CHINESE_LONGEST
    if not _CHINESE_DICT:
        _CHINESE_DICT = set(_COMMON_CHINESE_WORDS)
        _CHINESE_DICT.update(_CHINESE_SURNAMES)
        _CHINESE_DICT.update(_COMMON_MALE_NAMES)
        _CHINESE_DICT.update(_COMMON_FEMALE_NAMES)
        _CHINESE_DICT.update(_COMMON_PLACE_SUFFIXES)
        _CHINESE_DICT.update(_COMMON_ORG_SUFFIXES)
        _CHINESE_DICT.update(_CHINESE_POSITIVE)
        _CHINESE_DICT.update(_CHINESE_NEGATIVE)
        _CHINESE_LONGEST = max(len(w) for w in _CHINESE_DICT) if _CHINESE_DICT else 4

def _fmm_tokenize(text: str, custom_dict: Optional[Set[str]] = None) -> List[str]:
    """Forward Maximum Matching tokenization."""
    _ensure_chinese_dict()
    dictionary = custom_dict | _CHINESE_DICT if custom_dict else _CHINESE_DICT
    max_word_len = max((len(w) for w in dictionary), default=_CHINESE_LONGEST)
    tokens = []
    i = 0
    while i < len(text):
        matched = False
        for j in range(min(max_word_len, len(text) - i), 0, -1):
            word = text[i:i + j]
            if word in dictionary:
                tokens.append(word)
                i += j
                matched = True
                break
        if not matched:
            tokens.append(text[i])
            i += 1
    return tokens

def _bmm_tokenize(text: str, custom_dict: Optional[Set[str]] = None) -> List[str]:
    """Backward Maximum Matching tokenization."""
    _ensure_chinese_dict()
    dictionary = custom_dict | _CHINESE_DICT if custom_dict else _CHINESE_DICT
    max_word_len = max((len(w) for w in dictionary), default=_CHINESE_LONGEST)
    tokens = []
    i = len(text)
    while i > 0:
        matched = False
        for j in range(max_word_len, 0, -1):
            if i - j < 0:
                continue
            word = text[i - j:i]
            if word in dictionary:
                tokens.append(word)
                i -= j
                matched = True
                break
        if not matched:
            tokens.append(text[i - 1:i])
            i -= 1
    tokens.reverse()
    return tokens

def _mm_tokenize(text: str, custom_dict: Optional[Set[str]] = None) -> List[str]:
    """Maximum matching tokenization (FMM + BMM disambiguation)."""
    fmm = _fmm_tokenize(text, custom_dict)
    bmm = _bmm_tokenize(text, custom_dict)
    # Choose the one with fewer tokens (better segmentation)
    if len(fmm) <= len(bmm):
        return fmm
    # If equal length, choose the one with fewer single-character tokens
    fmm_single = sum(1 for t in fmm if len(t) == 1 and _is_chinese_char(t[0]))
    bmm_single = sum(1 for t in bmm if len(t) == 1 and _is_chinese_char(t[0]))
    return fmm if fmm_single <= bmm_single else bmm

def _tokenize_mixed(text: str, custom_dict: Optional[Set[str]] = None) -> List[str]:
    """Tokenize mixed Chinese-English text."""
    tokens = []
    # Split text into Chinese and non-Chinese segments
    segments = re.split(r'([\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+)', text)
    for seg in segments:
        if not seg:
            continue
        if re.fullmatch(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+', seg):
            # Chinese segment
            tokens.extend(_mm_tokenize(seg, custom_dict))
        else:
            # Non-Chinese segment: split on whitespace/punctuation
            eng_tokens = re.findall(r'[a-zA-Z]+|[0-9]+|[^\s\w]', seg)
            tokens.extend(eng_tokens)
    return tokens

# ---- TF-IDF helpers ----
def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    """Compute term frequency for a list of tokens."""
    total = len(tokens)
    if total == 0:
        return {}
    freq: Dict[str, int] = {}
    for t in tokens:
        t_lower = t.lower()
        freq[t_lower] = freq.get(t_lower, 0) + 1
    return {word: count / total for word, count in freq.items()}

def _compute_idf(documents: List[List[str]]) -> Dict[str, float]:
    """Compute inverse document frequency across documents."""
    N = len(documents)
    df: Dict[str, int] = {}
    for doc in documents:
        seen = set()
        for t in doc:
            t_lower = t.lower()
            if t_lower not in seen:
                df[t_lower] = df.get(t_lower, 0) + 1
                seen.add(t_lower)
    return {word: math.log((N + 1) / (count + 1)) + 1 for word, count in df.items()}

def _tfidf_vectorize(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    """Compute TF-IDF vector for a document."""
    tf = _compute_tf(tokens)
    return {word: tf_val * idf.get(word, 1.0) for word, tf_val in tf.items()}

def _cosine_sim(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    all_keys = set(vec1.keys()) | set(vec2.keys())
    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0
    for key in all_keys:
        v1 = vec1.get(key, 0.0)
        v2 = vec2.get(key, 0.0)
        dot += v1 * v2
        norm1 += v1 * v1
        norm2 += v2 * v2
    norm1 = math.sqrt(norm1)
    norm2 = math.sqrt(norm2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def _page_rank(graph: Dict[int, Set[int]], max_iter: int = 100, d: float = 0.85, tol: float = 1e-6) -> Dict[int, float]:
    """PageRank algorithm on a graph represented as adjacency sets."""
    n = len(graph)
    if n == 0:
        return {}
    scores = {i: 1.0 / n for i in graph}
    for _ in range(max_iter):
        new_scores = {}
        diff = 0.0
        for i in graph:
            rank_sum = 0.0
            for j, neighbors in graph.items():
                if i in neighbors:
                    rank_sum += scores[j] / max(len(neighbors), 1)
            new_scores[i] = (1 - d) / n + d * rank_sum
            diff += abs(new_scores[i] - scores[i])
        scores = new_scores
        if diff < tol:
            break
    return scores

# ---- Build word co-occurrence graph for TextRank ----
def _build_cooccur_graph(tokens: List[str], window: int = 2) -> Dict[int, Dict[int, float]]:
    """Build a weighted co-occurrence graph."""
    graph: Dict[int, Dict[int, float]] = {}
    for i, tok in enumerate(tokens):
        if tok not in graph:
            graph[tok] = {}
        for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
            if i == j:
                continue
            neighbor = tokens[j]
            graph[tok][neighbor] = graph[tok].get(neighbor, 0) + 1
    return graph

# ---- N-grams ----
def _extract_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    """Extract n-grams from a token list."""
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

# ---- PMI ----
def _pmi(count_xy: int, count_x: int, count_y: int, total: int) -> float:
    """Compute Pointwise Mutual Information."""
    if count_x == 0 or count_y == 0:
        return 0.0
    p_xy = count_xy / total
    p_x = count_x / total
    p_y = count_y / total
    if p_x <= 0 or p_y <= 0 or p_xy <= 0:
        return 0.0
    return math.log(p_xy / (p_x * p_y))

# ---- Chi-square ----
def _chi_square(a: int, b: int, c: int, d: int) -> float:
    """Compute chi-square statistic for collocation discovery.
    a = count of (w1, w2) together
    b = count of w1 without w2
    c = count of w2 without w1
    d = count of neither
    """
    total = a + b + c + d
    if total == 0:
        return 0.0
    expected_a = (a + b) * (a + c) / total
    if expected_a == 0:
        return 0.0
    chi2 = (a - expected_a) ** 2 / expected_a
    if b + d > 0:
        expected_b = (a + b) * (b + d) / total
        if expected_b > 0:
            chi2 += (b - expected_b) ** 2 / expected_b
    if c + d > 0:
        expected_c = (c + d) * (a + c) / total
        if expected_c > 0:
            chi2 += (c - expected_c) ** 2 / expected_c
        expected_d = (c + d) * (b + d) / total
        if expected_d > 0:
            chi2 += (d - expected_d) ** 2 / expected_d
    return chi2

# ========================================================================
# MCP TOOLS — TEXT PREPROCESSING
# ========================================================================

@mcp.tool()
def sentence_splitter(text: str) -> str:
    """Split text into sentences using rule-based plus statistical heuristics.

    Supports Chinese (。！？) and English (.!?) sentence boundaries.
    Handles abbreviations (Mr., Dr., U.S.A.), decimal numbers (3.14),
    ellipsis (...), and common exceptions.
    """
    if not text:
        return json.dumps({"sentences": [], "count": 0}, ensure_ascii=False, indent=2)

    # Abbreviations that should not trigger sentence splitting
    abbreviations = {
        'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr', 'st', 'ave', 'blvd',
        'dept', 'est', 'govt', 'inc', 'ltd', 'co', 'corp', 'vs', 'etc',
        'e.g', 'i.e', 'a.m', 'p.m', 'viz', 'al', 'vol', 'pp', 'ch', 'ex',
        'approx', 'apt', 'bldg', 'capt', 'col', 'cpt', 'gen', 'gov',
        'lt', 'maj', 'rep', 'rev', 'sen', 'sgt', 'adm', 'cmdr', 'cpl',
        'sir', 'dame', 'lord', 'lady', 'hon', 'esq', 'phd', 'md', 'ba',
        'ma', 'llb', 'bsc', 'msc', 'dphil', 'ed', 'asst', 'assoc', 'dept',
        'dist', 'natl', 'org', 'univ', 'usu'
    }

    # Split on sentence-terminating punctuation
    # Pattern: sentence boundary punctuation followed by space/capital letter/Chinese character
    patterns = [
        # Chinese sentence endings
        (r'[。！？]', 'zh'),
        # English sentence endings (must be followed by space+uppercase or end of string)
        (r'[.!?](?=\s+[A-Z"\'(\[{])', 'en'),
        (r'[.!?](?=\s*$)', 'en-end'),
        # Newline-based sentence boundary
        (r'\n\s*\n', 'para'),
        # Ellipsis followed by space+capital
        (r'…(?=\s*[A-Z\u4e00-\u9fff])', 'ellipsis'),
    ]

    # First split by paragraph boundaries
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    all_sentences = []

    for para in paragraphs:
        if not para:
            continue
        # Tokenize the paragraph into candidate sentences
        # Use a character-by-character approach for robustness
        candidates = []
        current = []
        i = 0
        while i < len(para):
            ch = para[i]
            current.append(ch)

            # Check for Chinese sentence endings
            if ch in '。！？':
                # Check if it's not part of an abbreviation or special usage
                candidates.append(''.join(current).strip())
                current = []
                i += 1
                continue

            # Check for English . ! ?
            if ch in '.!?':
                # Look ahead to determine if this is really a sentence boundary
                # Check for abbreviation
                word_before = ''.join(re.findall(r'[a-zA-Z]+', ''.join(current[-20:])))

                # Skip abbreviations
                if word_before.lower() in abbreviations:
                    i += 1
                    continue

                # Skip decimal numbers and abbreviations with multiple dots
                if ch == '.':
                    # Check if preceded by a digit (decimal number)
                    if current and len(current) >= 2 and current[-2].isdigit():
                        # Look ahead: if followed by digit, it's a decimal
                        if i + 1 < len(para) and para[i + 1].isdigit():
                            i += 1
                            continue
                    # Check for patterns like U.S.A, Ph.D.
                    if i + 1 < len(para) and para[i + 1] == '.':
                        i += 1
                        continue
                    # Check for common initial patterns like "A. Smith"
                    if len(word_before) == 1 and word_before.isalpha():
                        i += 1
                        continue

                # Now check if this is a real sentence boundary
                # Look at next non-whitespace character
                next_char = ''
                j = i + 1
                while j < len(para) and para[j].isspace():
                    j += 1
                if j < len(para):
                    next_char = para[j]

                is_boundary = False
                if not next_char:
                    is_boundary = True  # End of text
                elif next_char.isupper() or _is_chinese_char(next_char):
                    is_boundary = True  # Followed by uppercase or Chinese char
                elif next_char in '"\'"''「『（([{':
                    is_boundary = True  # Followed by opening quote/bracket

                if is_boundary:
                    candidates.append(''.join(current).strip())
                    current = []
                i += 1
                continue

            i += 1

        # Add any remaining text
        if current:
            remaining = ''.join(current).strip()
            if remaining:
                candidates.append(remaining)

        all_sentences.extend(candidates)

    # Clean up empty and very short sentences (likely fragments)
    final_sentences = []
    for s in all_sentences:
        s = s.strip()
        if len(s) < 1:
            continue
        # Remove leading/trailing punctuation
        s = s.strip(' \t\n\r')
        final_sentences.append(s)

    if not final_sentences:
        final_sentences = [text.strip()]

    result = {
        "sentences": final_sentences,
        "count": len(final_sentences),
        "total_chars": len(text),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def word_tokenizer(text: str, method: str = "mm", custom_words: str = "") -> str:
    """Tokenize Chinese and mixed-language text using dictionary-based maximum matching.

    Supports Forward Maximum Matching (FMM), Backward Maximum Matching (BMM),
    and combined (MM) with disambiguation. Include custom words separated by commas.
    """
    custom_dict = None
    if custom_words.strip():
        custom_dict = set(w.strip() for w in custom_words.split(',') if w.strip())

    tokens = _tokenize_mixed(text, custom_dict)

    # Collect token statistics
    unique_tokens = len(set(tokens))
    token_freq = collections.Counter(tokens)
    top_tokens = token_freq.most_common(20)

    result = {
        "tokens": tokens,
        "token_count": len(tokens),
        "unique_tokens": unique_tokens,
        "vocabulary_richness": round(unique_tokens / max(len(tokens), 1), 4),
        "top_tokens": [{"token": t, "count": c} for t, c in top_tokens],
        "method": method,
        "custom_words_count": len(custom_dict) if custom_dict else 0,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def text_normalizer(text: str, lowercase: bool = True, normalize_unicode: bool = True) -> str:
    """Normalize text: Unicode normalization, full/half-width conversion,
    whitespace cleanup, and optional case unification.
    """
    original = text
    if normalize_unicode:
        text = unicodedata.normalize('NFKC', text)

    # Full-width to half-width conversion
    full_to_half = {}
    for code in range(0xFF01, 0xFF5F):
        full_to_half[chr(code)] = chr(code - 0xFEE0)
    full_to_half['　'] = ' '  # Full-width space
    text = text.translate(str.maketrans(full_to_half))

    # Normalize whitespace: collapse multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize newlines
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace
    text = text.strip()

    # Remove zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)

    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('「', '"').replace('」', '"')

    # Normalize dashes
    text = re.sub(r'[—–−]', '-', text)

    # Case unification
    if lowercase:
        text = text.lower()

    changes = []
    if original != text:
        changes.append("Text was modified during normalization")

    result = {
        "original_length": len(original),
        "normalized_length": len(text),
        "normalized": text,
        "changes": changes,
        "lowercase_applied": lowercase,
        "unicode_normalization": normalize_unicode,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ========================================================================
# MCP TOOLS — FEATURE EXTRACTION
# ========================================================================

@mcp.tool()
def tfidf_extractor(text: str, documents: str = "") -> str:
    """Extract TF-IDF features from text. If additional documents are provided
    (one per line), IDF is computed across the full corpus; otherwise, the
    input text is treated as a single document with simulated IDF.
    """
    tokens = _tokenize_mixed(text)
    tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)]

    if not tokens:
        return json.dumps({"error": "No tokens found"}, ensure_ascii=False, indent=2)

    doc_lines = [d.strip() for d in documents.split('\n') if d.strip()] if documents.strip() else []
    all_docs: List[List[str]] = [tokens]

    for line in doc_lines:
        line_tokens = _tokenize_mixed(line)
        line_tokens = [t.lower() for t in line_tokens if t.strip() and not _is_punctuation(t)]
        if line_tokens:
            all_docs.append(line_tokens)

    idf = _compute_idf(all_docs)
    tfidf = _tfidf_vectorize(tokens, idf)
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)

    result = {
        "corpus_size": len(all_docs),
        "vocabulary_size": len(idf),
        "top_features": [{"term": term, "score": round(score, 6)}
                         for term, score in sorted_tfidf[:50]],
        "total_features": len(tfidf),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def textrank_keywords(text: str, top_k: int = 10, window: int = 2,
                      max_iter: int = 100, damping: float = 0.85) -> str:
    """Extract keywords using the TextRank algorithm.

    Builds a word co-occurrence graph from a sliding window, runs PageRank
    iteration until convergence, and returns top-K ranked keywords.
    """
    tokens = _tokenize_mixed(text)
    tokens = [t.lower() for t in tokens if len(t.strip()) > 1 and not _is_punctuation(t)
              and t not in _CHINESE_STOPWORDS and t.lower() not in _ENGLISH_STOPWORDS]

    if len(tokens) < 2:
        return json.dumps({"error": "Insufficient tokens for TextRank (need at least 2)"},
                          ensure_ascii=False, indent=2)

    # Build co-occurrence graph
    graph = _build_cooccur_graph(tokens, window)

    # Run PageRank
    scores = _page_rank(graph, max_iter, damping)

    # Sort and get top-K
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    # Compute convergence info
    result = {
        "keywords": [{"word": word, "score": round(score, 6)}
                     for word, score in sorted_words],
        "graph_nodes": len(graph),
        "graph_edges": sum(len(neighbors) for neighbors in graph.values()),
        "window_size": window,
        "damping_factor": damping,
        "iterations": max_iter,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def ngram_extractor(text: str, n: int = 2, top_k: int = 30) -> str:
    """Extract N-gram language model features.

    Computes unigram/bigram/trigram frequency statistics and evaluates
    collocation strength using Pointwise Mutual Information (PMI).
    """
    tokens = _tokenize_mixed(text)
    tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)]

    if len(tokens) < n:
        return json.dumps({"error": f"Insufficient tokens for {n}-gram extraction"},
                          ensure_ascii=False, indent=2)

    # Extract n-grams
    ngrams = _extract_ngrams(tokens, n)
    ngram_counts = collections.Counter(ngrams)

    total_ngrams = len(ngrams)
    total_tokens = len(tokens)

    # For PMI calculation, get unigram counts
    unigrams = _extract_ngrams(tokens, 1)
    unigram_counts = collections.Counter(unigrams)
    unigram_total = len(unigrams)

    # Compute PMI for top n-grams
    pmi_scores = []
    for ng, count in ngram_counts.most_common(top_k * 3):
        if n == 2:
            w1, w2 = ng
            c1 = unigram_counts.get((w1,), 1)
            c2 = unigram_counts.get((w2,), 1)
            pmi_val = _pmi(count, c1, c2, total_tokens)
            pmi_scores.append({
                "ngram": ' '.join(ng),
                "count": count,
                "frequency": round(count / total_ngrams, 6),
                "pmi": round(pmi_val, 4),
            })
        else:
            pmi_scores.append({
                "ngram": ' '.join(ng),
                "count": count,
                "frequency": round(count / total_ngrams, 6),
            })

    pmi_scores.sort(key=lambda x: (-x['count'], -x.get('pmi', 0)))
    pmi_scores = pmi_scores[:top_k]

    result = {
        "n": n,
        "total_tokens": total_tokens,
        "total_ngrams": total_ngrams,
        "unique_ngrams": len(ngram_counts),
        "top_ngrams": pmi_scores,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ========================================================================
# MCP TOOLS — TEXT ANALYSIS
# ========================================================================

@mcp.tool()
def sentiment_analyzer(text: str) -> str:
    """Analyze sentiment using built-in positive/negative dictionaries,
    negation word handling, and booster word amplification.

    Returns sentiment scores for Chinese and English text in [0, 1] range,
    where 0 = most negative, 0.5 = neutral, 1 = most positive.
    """
    tokens = _tokenize_mixed(text)
    tokens_clean = [t for t in tokens if t.strip()]

    pos_score = 0.0
    neg_score = 0.0
    total_words = len(tokens_clean)
    negation_active = False
    booster = 1.0
    negation_window = 3  # How far negation affects following words
    negation_countdown = 0

    pos_matches = []
    neg_matches = []
    booster_matches = []

    for token in tokens_clean:
        tok_lower = token.lower()

        # Check negation
        if tok_lower in _NEGATION_WORDS:
            negation_active = not negation_active
            negation_countdown = negation_window
            continue

        # Check booster
        if tok_lower in _BOOSTER_WORDS:
            booster = _BOOSTER_WORDS[tok_lower]
            booster_matches.append(token)
            continue

        # Determine polarity
        is_positive = False
        is_negative = False
        weight = 1.0

        if _is_chinese_char(token[0]):
            if token in _CHINESE_POSITIVE:
                is_positive = True
            elif token in _CHINESE_NEGATIVE:
                is_negative = True
        else:
            if tok_lower in _ENGLISH_POSITIVE:
                is_positive = True
            elif tok_lower in _ENGLISH_NEGATIVE:
                is_negative = True

        # Apply negation and booster
        if negation_active:
            weight = -booster
            if is_positive:
                neg_score += abs(weight)
                neg_matches.append(token)
            elif is_negative:
                pos_score += abs(weight)
                pos_matches.append(token)
        else:
            if is_positive:
                pos_score += booster
                pos_matches.append(token)
            elif is_negative:
                neg_score += booster
                neg_matches.append(token)

        # Reset booster after use
        booster = 1.0
        negation_countdown -= 1
        if negation_countdown <= 0:
            negation_active = False

    # Compute final sentiment score [0, 1]
    total = pos_score + neg_score
    if total == 0:
        sentiment_score = 0.5
        sentiment_label = "neutral"
    else:
        sentiment_score = pos_score / total
        if sentiment_score > 0.6:
            sentiment_label = "positive"
        elif sentiment_score < 0.4:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

    # Intensity
    intensity = min(1.0, total / max(total_words, 1) * 3)
    if intensity > 0.7:
        intensity_label = "strong"
    elif intensity > 0.3:
        intensity_label = "moderate"
    else:
        intensity_label = "weak"

    result = {
        "sentiment_score": round(sentiment_score, 4),
        "sentiment_label": sentiment_label,
        "intensity": round(intensity, 4),
        "intensity_label": intensity_label,
        "positive_score": round(pos_score, 4),
        "negative_score": round(neg_score, 4),
        "positive_matches": pos_matches[:20],
        "negative_matches": neg_matches[:20],
        "booster_matches": booster_matches[:10],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def entity_extractor(text: str) -> str:
    """Extract named entities using regular expressions, rule-based patterns,
    and dictionary matching. Supports: person names, locations, organizations,
    dates, currency amounts, emails, phone numbers, and URLs.
    """
    entities: Dict[str, List[Dict[str, Any]]] = {
        "person": [],
        "location": [],
        "organization": [],
        "date": [],
        "amount": [],
        "email": [],
        "phone": [],
        "url": [],
        "other": [],
    }

    seen: Set[str] = set()

    def _add_entity(cat: str, text: str, start: int, end: int, confidence: float = 0.8):
        key = f"{cat}:{text}:{start}"
        if key not in seen:
            seen.add(key)
            entities[cat].append({
                "text": text,
                "start": start,
                "end": end,
                "confidence": confidence,
            })

    # ---- Email ----
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for m in re.finditer(email_pattern, text):
        _add_entity("email", m.group(), m.start(), m.end(), 0.95)

    # ---- URL ----
    url_pattern = r'https?://[^\s<>"\'\[\]{}|\\^`]+'
    for m in re.finditer(url_pattern, text):
        _add_entity("url", m.group(), m.start(), m.end(), 0.95)

    # ---- Phone numbers ----
    phone_patterns = [
        (r'1[3-9]\d{9}', 0.90),  # Chinese mobile
        (r'\+\d{1,3}[-\s]?\d{1,14}', 0.85),  # International
        (r'0\d{2,3}[-\s]?\d{7,8}', 0.80),  # Chinese landline
        (r'\(\d{3}\)\s?\d{3}-\d{4}', 0.85),  # US format (555) 123-4567
        (r'\d{3}-\d{3}-\d{4}', 0.80),  # US format 555-123-4567
    ]
    for pattern, conf in phone_patterns:
        for m in re.finditer(pattern, text):
            _add_entity("phone", m.group(), m.start(), m.end(), conf)

    # ---- Currency amounts ----
    amount_patterns = [
        (r'[¥￥$€£]?\d+(?:\.\d+)?\s*(?:元|美元|欧元|英镑|块|毛|分|万|亿)?', 0.85),
        (r'(?:元|美元|欧元|英镑|块|毛|分|万|亿)\s*\d+(?:\.\d+)?', 0.85),
    ]
    for pattern, conf in amount_patterns:
        for m in re.finditer(pattern, text):
            _add_entity("amount", m.group(), m.start(), m.end(), conf)

    # ---- Dates ----
    date_patterns = [
        (r'\d{4}[-/\.年]\d{1,2}[-/\.月]\d{1,2}[日号]?', 0.90),
        (r'\d{4}[-/\.年]\d{1,2}[月]?', 0.85),
        (r'\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}', 0.80),
        (r'(?:今|去|明|前|后|大前|大后)(?:天|日|年|月|周)', 0.80),
        (r'(?:星期[一二三四五六日天]|周[一二三四五六日天])', 0.85),
        (r'(?:January|February|March|April|May|June|July|August|'
         r'September|October|November|December)\s+\d{1,2},?\s+\d{4}', 0.90),
        (r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|'
         r'September|October|November|December)\s+\d{4}', 0.90),
        (r'\d{1,2}/\d{1,2}/\d{2,4}', 0.80),
    ]
    for pattern, conf in date_patterns:
        for m in re.finditer(pattern, text):
            _add_entity("date", m.group(), m.start(), m.end(), conf)

    # ---- Person names (Chinese) ----
    _ensure_chinese_dict()
    tokens = _tokenize_mixed(text)
    for i, tok in enumerate(tokens):
        if len(tok) >= 2 and all(_is_chinese_char(c) for c in tok):
            # Check if first character is a surname
            if tok[0] in _CHINESE_SURNAMES:
                # Full name (2-3 chars)
                if 2 <= len(tok) <= 3:
                    if len(tok) == 2:
                        other = tok[1]
                    else:
                        other = tok[1] + tok[2]
                    # Check if remaining chars look like name characters
                    if all(c in _COMMON_MALE_NAMES or c in _COMMON_FEMALE_NAMES
                           or _is_chinese_char(c) for c in other):
                        idx = text.find(tok)
                        if idx >= 0:
                            _add_entity("person", tok, idx, idx + len(tok), 0.75)

    # ---- English person name patterns ----
    for m in re.finditer(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', text):
        # Avoid matching locations and organizations wrongly
        parts = m.group().split()
        if 2 <= len(parts) <= 4 and all(p[0].isupper() for p in parts):
            _add_entity("person", m.group(), m.start(), m.end(), 0.70)

    # ---- Locations ----
    # Chinese location patterns
    loc_patterns = [
        (r'(?:[^\s,，。的]{2,}(?:省|市|区|县|镇|乡|村|街道|路|大道|街|巷|里|庄|桥|港|湾|岛|山|岭|峰|江|河|湖|海|泊|塘|水库|园|林))',
         0.75),
    ]
    for pattern, conf in loc_patterns:
        for m in re.finditer(pattern, text):
            _add_entity("location", m.group(), m.start(), m.end(), conf)

    # Country and major city names
    major_locations = {
        "中国": 0.95, "美国": 0.95, "英国": 0.95, "法国": 0.95, "德国": 0.95,
        "日本": 0.95, "韩国": 0.95, "印度": 0.90, "俄罗斯": 0.95, "澳大利亚": 0.90,
        "北京": 0.90, "上海": 0.90, "广州": 0.90, "深圳": 0.90, "杭州": 0.85,
        "成都": 0.85, "武汉": 0.85, "南京": 0.85, "西安": 0.85, "重庆": 0.85,
        "天津": 0.85, "香港": 0.90, "台北": 0.85, "东京": 0.85, "纽约": 0.85,
        "伦敦": 0.85, "巴黎": 0.85, "柏林": 0.85, "悉尼": 0.80, "首尔": 0.80,
    }
    for loc, conf in major_locations.items():
        idx = 0
        while True:
            idx = text.find(loc, idx)
            if idx < 0:
                break
            _add_entity("location", loc, idx, idx + len(loc), conf)
            idx += len(loc)

    # ---- Organizations ----
    org_patterns = [
        (r'[^\s,，。的]{2,}(?:公司|集团|局|处|部|委|办|厅|所|站|社|院|中心|大学|学院|银行|协会|学会|商会|委员会)',
         0.70),
        (r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|Ltd|Corp|LLC|PLC|LLP|Co))\.?',
         0.75),
    ]
    for pattern, conf in org_patterns:
        for m in re.finditer(pattern, text):
            _add_entity("organization", m.group(), m.start(), m.end(), conf)

    # Filter and deduplicate results
    filtered = {k: v[:20] for k, v in entities.items() if v}
    total = sum(len(v) for v in filtered.values())

    result = {
        "entities": filtered,
        "total_entities": total,
        "entity_types_found": list(filtered.keys()),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def language_detector(text: str) -> str:
    """Detect language using Unicode ranges, common word frequencies,
    and n-gram features. Supports: Chinese, English, Japanese, Korean,
    French, German, Spanish, Russian, Arabic, and mixed-language detection.
    """
    if not text.strip():
        return json.dumps({"error": "Empty text"}, ensure_ascii=False, indent=2)

    sample = text[:5000]  # Use first 5000 chars for efficiency

    # Unicode range counts
    chinese_chars = len(_CHINESE_RANGE.findall(sample))
    japanese_chars = len(_JAPANESE_RANGE.findall(sample))
    korean_chars = len(_KOREAN_RANGE.findall(sample))
    arabic_chars = len(_ARABIC_RANGE.findall(sample))
    cyrillic_chars = len(_CYRILLIC_RANGE.findall(sample))
    latin_chars = len(re.findall(r'[a-zA-Z]', sample))
    digits = len(re.findall(r'[0-9]', sample))
    total_identified = chinese_chars + japanese_chars + korean_chars + arabic_chars + cyrillic_chars + latin_chars + digits

    # Word-level analysis
    words_en = set(re.findall(r'[a-zA-Z]+', sample.lower()))
    words_zh = set(_chinese_chars(sample))
    bigrams_en = set()
    for i in range(len(sample) - 1):
        if sample[i].isalpha() and sample[i + 1].isalpha():
            bigrams_en.add(sample[i:i + 2].lower())

    # Score each language
    scores: Dict[str, float] = {}

    # Chinese
    zh_score = chinese_chars / max(total_identified, 1) * 100
    if words_zh:
        common_zh = len(words_zh & _CHINESE_COMMON)
        zh_score += common_zh * 5
    scores["Chinese"] = zh_score

    # Japanese (has both CJK + kana)
    ja_score = japanese_chars / max(total_identified, 1) * 100
    jp_words = set(re.findall(r'[\u3040-\u309f\u30a0-\u30ff]+', sample.lower()))
    if jp_words:
        common_jp = len(set(''.join(jp_words).split()) & _JAPANESE_COMMON)
        ja_score += common_jp * 5
    scores["Japanese"] = ja_score

    # Korean
    ko_score = korean_chars / max(total_identified, 1) * 100
    scores["Korean"] = ko_score

    # Arabic
    ar_score = arabic_chars / max(total_identified, 1) * 100
    scores["Arabic"] = ar_score

    # Russian/Cyrillic
    ru_score = cyrillic_chars / max(total_identified, 1) * 100
    ru_words = set(re.findall(r'[а-яА-ЯёЁ]+', sample.lower()))
    if ru_words:
        common_ru = len(ru_words & _RUSSIAN_COMMON)
        ru_score += common_ru * 5
    scores["Russian"] = ru_score

    # English/Latin
    en_score = 0.0
    if latin_chars > 0:
        en_score = latin_chars / max(total_identified, 1) * 100
        common_en = len(words_en & _ENGLISH_COMMON)
        en_score += common_en * 5

        # Check for French/German/Spanish common words
        fr_hits = len(words_en & _FRENCH_COMMON)
        de_hits = len(words_en & _GERMAN_COMMON)
        es_hits = len(words_en & _SPANISH_COMMON)

        # French
        if fr_hits > de_hits and fr_hits > es_hits and fr_hits >= 2:
            scores["French"] = en_score + fr_hits * 5
            scores["English"] = en_score
        # German
        elif de_hits > fr_hits and de_hits > es_hits and de_hits >= 2:
            scores["German"] = en_score + de_hits * 5
            scores["English"] = en_score
        # Spanish
        elif es_hits > fr_hits and es_hits > de_hits and es_hits >= 2:
            scores["Spanish"] = en_score + es_hits * 5
            scores["English"] = en_score
        else:
            scores["English"] = en_score

    # Normalize scores
    max_score = max(scores.values()) if scores else 1
    normalized = {lang: round(s / max_score * 100, 2) for lang, s in scores.items()}

    # Sort languages by score
    ranked = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
    top_lang = ranked[0][0] if ranked else "unknown"

    # Build language distribution
    lang_dist = {lang: score for lang, score in ranked if score > 5}
    total_score = sum(lang_dist.values())

    # Determine confidence
    if len(ranked) >= 2:
        margin = ranked[0][1] - ranked[1][1]
        if margin > 40:
            confidence = "high"
        elif margin > 20:
            confidence = "medium"
        else:
            confidence = "low"
    else:
        confidence = "high"

    result = {
        "detected_language": top_lang,
        "confidence": confidence,
        "language_scores": ranked,
        "language_distribution": lang_dist,
        "script_analysis": {
            "chinese_chars": chinese_chars,
            "japanese_chars": japanese_chars,
            "korean_chars": korean_chars,
            "cyrillic_chars": cyrillic_chars,
            "arabic_chars": arabic_chars,
            "latin_chars": latin_chars,
            "digits": digits,
        },
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def readability_scorer(text: str) -> str:
    """Score text readability using Flesch-Kincaid formula, average word/character
    lengths, and sentence complexity metrics.
    """
    sentences = json.loads(sentence_splitter(text))["sentences"]
    num_sentences = len(sentences)

    tokens = _tokenize_mixed(text)
    words = [t for t in tokens if t.strip() and not _is_punctuation(t)]
    num_words = len(words)

    # Chinese character count
    chinese_chars_count = len(_chinese_chars(text))
    # English syllable estimation (simple heuristic: count vowel groups)
    def _count_syllables(word: str) -> int:
        word = word.lower()
        if not re.search(r'[aeiou]', word):
            return max(1, len(re.findall(r'[a-z]', word)))
        vowels = re.findall(r'[aeiouy]+', word)
        count = len(vowels)
        # Adjust for silent e
        if word.endswith('e') and count > 1:
            count -= 1
        # Minimum 1 syllable
        return max(1, count)

    total_syllables = sum(_count_syllables(w) for w in words if _is_english_word(w))

    # Flesch Reading Ease (English)
    if num_sentences > 0 and num_words > 0:
        avg_words_per_sentence = num_words / num_sentences
        avg_syllables_per_word = total_syllables / max(num_words, 1)
        flesch_ease = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
        flesch_ease = max(0, min(100, flesch_ease))
    else:
        avg_words_per_sentence = 0
        avg_syllables_per_word = 0
        flesch_ease = 0

    # Chinese readability score (approximate)
    if chinese_chars_count > 0 and num_sentences > 0:
        avg_chars_per_sentence = chinese_chars_count / num_sentences
        # Simplified Chinese readability (lower = more complex)
        chinese_readability = max(0, 100 - avg_chars_per_sentence * 3)
    else:
        avg_chars_per_sentence = 0
        chinese_readability = 0

    # Grade level interpretation
    if flesch_ease >= 90:
        grade_level = "Very Easy (5th grade)"
        reading_level = "Very Easy"
    elif flesch_ease >= 80:
        grade_level = "Easy (6th grade)"
        reading_level = "Easy"
    elif flesch_ease >= 70:
        grade_level = "Fairly Easy (7th grade)"
        reading_level = "Fairly Easy"
    elif flesch_ease >= 60:
        grade_level = "Standard (8th-9th grade)"
        reading_level = "Standard"
    elif flesch_ease >= 50:
        grade_level = "Fairly Difficult (10th-12th grade)"
        reading_level = "Fairly Difficult"
    elif flesch_ease >= 30:
        grade_level = "Difficult (College)"
        reading_level = "Difficult"
    else:
        grade_level = "Very Difficult (College Graduate)"
        reading_level = "Very Difficult"

    # Character entropy
    char_freq: Dict[str, int] = {}
    for ch in text:
        char_freq[ch] = char_freq.get(ch, 0) + 1
    total_chars = len(text)
    entropy = 0.0
    for freq in char_freq.values():
        p = freq / total_chars
        entropy -= p * math.log2(p)

    # Lexical diversity
    unique_words = len(set(w.lower() for w in words if w.strip()))
    lexical_diversity = unique_words / max(num_words, 1)

    result = {
        "flesch_reading_ease": round(flesch_ease, 2),
        "flesch_grade_level": grade_level,
        "reading_level": reading_level,
        "avg_words_per_sentence": round(avg_words_per_sentence, 2),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2),
        "chinese_readability_score": round(chinese_readability, 2) if chinese_chars_count > 0 else None,
        "avg_chars_per_sentence": round(avg_chars_per_sentence, 2),
        "lexical_diversity": round(lexical_diversity, 4),
        "character_entropy": round(entropy, 4),
        "sentence_count": num_sentences,
        "word_count": num_words,
        "char_count": total_chars,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ========================================================================
# MCP TOOLS — TEXT SIMILARITY
# ========================================================================

@mcp.tool()
def cosine_similarity(text1: str, text2: str) -> str:
    """Compute cosine similarity between two texts using TF-IDF vectors.

    Tokenizes both texts, computes TF-IDF vectors, and returns the
    cosine similarity score (0-1 range where 1 = identical vectors).
    """
    tokens1 = _tokenize_mixed(text1)
    tokens2 = _tokenize_mixed(text2)
    tokens1 = [t.lower() for t in tokens1 if t.strip() and not _is_punctuation(t)]
    tokens2 = [t.lower() for t in tokens2 if t.strip() and not _is_punctuation(t)]

    if not tokens1 or not tokens2:
        return json.dumps({
            "similarity": 0.0,
            "error": "One or both texts have no tokens after processing",
        }, ensure_ascii=False, indent=2)

    # Compute IDF across both documents
    idf = _compute_idf([tokens1, tokens2])
    vec1 = _tfidf_vectorize(tokens1, idf)
    vec2 = _tfidf_vectorize(tokens2, idf)

    sim = _cosine_sim(vec1, vec2)

    # Find common terms
    common_terms = set(tokens1) & set(tokens2)
    unique_to_1 = set(tokens1) - set(tokens2)
    unique_to_2 = set(tokens2) - set(tokens1)

    result = {
        "cosine_similarity": round(sim, 6),
        "interpretation": f"{'High' if sim > 0.7 else 'Moderate' if sim > 0.4 else 'Low'} similarity",
        "text1_terms": len(tokens1),
        "text2_terms": len(tokens2),
        "common_terms": len(common_terms),
        "unique_to_text1": len(unique_to_1),
        "unique_to_text2": len(unique_to_2),
        "jaccard_coefficient": round(len(common_terms) / max(len(set(tokens1) | set(tokens2)), 1), 6),
        "top_common_terms": sorted(common_terms, key=lambda x: vec1.get(x, 0) * vec2.get(x, 0), reverse=True)[:15],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def jaccard_similarity(text1: str, text2: str, granularity: str = "word") -> str:
    """Compute Jaccard similarity coefficient between two texts.

    Supports three granularities:
    - 'char': Character-level comparison
    - 'word': Word-level comparison
    - 'ngram': N-gram (character trigram) comparison
    """
    if granularity == "char":
        set1 = set(text1)
        set2 = set(text2)
        label = "characters"
    elif granularity == "ngram":
        n = 3
        set1 = set(text1[i:i + n] for i in range(len(text1) - n + 1))
        set2 = set(text2[i:i + n] for i in range(len(text2) - n + 1))
        label = f"character {n}-grams"
    else:  # word
        tokens1 = _tokenize_mixed(text1)
        tokens2 = _tokenize_mixed(text2)
        set1 = set(t.lower() for t in tokens1 if t.strip() and not _is_punctuation(t))
        set2 = set(t.lower() for t in tokens2 if t.strip() and not _is_punctuation(t))
        label = "words"

    intersection = set1 & set2
    union = set1 | set2

    if not union:
        jaccard = 0.0
    else:
        jaccard = len(intersection) / len(union)

    dice = 2 * len(intersection) / max(len(set1) + len(set2), 1)

    result = {
        "jaccard_similarity": round(jaccard, 6),
        "dice_coefficient": round(dice, 6),
        "granularity": label,
        "set1_size": len(set1),
        "set2_size": len(set2),
        "intersection_size": len(intersection),
        "union_size": len(union),
        "common_items": sorted(intersection)[:20],
        "unique_to_text1": sorted(set1 - set2)[:20],
        "unique_to_text2": sorted(set2 - set1)[:20],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def edit_distance(text1: str, text2: str) -> str:
    """Compute Levenshtein edit distance between two texts using
    rolling-array dynamic programming (O(m*n) time, O(min(m,n)) space).
    """
    m, n = len(text1), len(text2)

    # Ensure text2 is the shorter one for space efficiency
    if m < n:
        text1, text2 = text2, text1
        m, n = n, m

    # Rolling array DP
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if text1[i - 1] == text2[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,      # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost  # substitution
            )
        prev, curr = curr, prev

    distance = prev[n]

    # Normalize by max length
    max_len = max(len(text1), len(text2))
    similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0

    # Compute character-level similarity breakdown
    if len(text1) > 0 and len(text2) > 0:
        matches = sum(1 for i in range(min(len(text1), len(text2))) if text1[i] == text2[i])
        match_ratio = matches / max(len(text1), len(text2))
    else:
        match_ratio = 0.0

    result = {
        "edit_distance": distance,
        "normalized_similarity": round(similarity, 6),
        "text1_length": len(text1),
        "text2_length": len(text2),
        "length_difference": abs(len(text1) - len(text2)),
        "character_match_ratio": round(match_ratio, 6),
        "max_possible_distance": max_len,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def doc_similarity_matrix(texts_json: str) -> str:
    """Compute a pairwise similarity matrix for multiple documents.

    Input: JSON array of strings or plain text with documents separated by '---'
    Output: Similarity matrix with hierarchical clustering visualization info.
    """
    # Parse input
    try:
        docs = json.loads(texts_json)
        if isinstance(docs, str):
            docs = [docs]
        if not isinstance(docs, list):
            docs = [str(docs)]
    except (json.JSONDecodeError, TypeError):
        # Try splitting by document separator
        docs = [d.strip() for d in texts_json.split('---') if d.strip()]
        if not docs:
            docs = [texts_json]

    if len(docs) < 2:
        return json.dumps({
            "error": "Need at least 2 documents for similarity matrix",
            "num_docs": len(docs),
        }, ensure_ascii=False, indent=2)

    # Tokenize all documents
    all_tokens = []
    for doc in docs:
        tokens = _tokenize_mixed(doc)
        tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)]
        all_tokens.append(tokens)

    # Compute IDF across all documents
    idf = _compute_idf(all_tokens)
    vectors = [_tfidf_vectorize(t, idf) for t in all_tokens]

    # Compute similarity matrix
    n = len(docs)
    matrix = [[0.0] * n for _ in range(n)]
    similarities = []
    for i in range(n):
        for j in range(n):
            sim = _cosine_sim(vectors[i], vectors[j])
            matrix[i][j] = round(sim, 6)
            if i < j:
                similarities.append({
                    "doc1": i,
                    "doc2": j,
                    "doc1_preview": docs[i][:50],
                    "doc2_preview": docs[j][:50],
                    "similarity": round(sim, 6),
                })

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Compute average similarity to identify clusters
    avg_similarities = []
    for i in range(n):
        others = [matrix[i][j] for j in range(n) if j != i]
        avg_similarities.append({
            "doc_index": i,
            "doc_preview": docs[i][:50],
            "avg_similarity": round(sum(others) / max(len(others), 1), 6),
        })
    avg_similarities.sort(key=lambda x: x["avg_similarity"], reverse=True)

    # Hierarchical clustering (simple agglomerative)
    clusters = [[i] for i in range(n)]
    cluster_history = []

    while len(clusters) > 1:
        # Find most similar pair of clusters
        best_i, best_j = 0, 0
        best_sim = -1.0
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Average link between clusters
                total_sim = 0.0
                count = 0
                for di in clusters[i]:
                    for dj in clusters[j]:
                        total_sim += matrix[di][dj]
                        count += 1
                avg_sim = total_sim / count if count > 0 else 0
                if avg_sim > best_sim:
                    best_sim = avg_sim
                    best_i, best_j = i, j

        # Merge clusters
        merged = clusters[best_i] + clusters[best_j]
        cluster_history.append({
            "merged": [clusters[best_i], clusters[best_j]],
            "similarity": round(best_sim, 6),
            "merged_indices": merged,
        })
        # Remove in reverse order
        clusters.pop(best_j)
        clusters.pop(best_i)
        clusters.append(merged)

    result = {
        "num_documents": n,
        "similarity_matrix": matrix,
        "top_similar_pairs": similarities[:10],
        "document_similarity_ranking": avg_similarities,
        "clustering_history": cluster_history,
        "final_cluster": clusters[0] if clusters else [],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ========================================================================
# MCP TOOLS — SUMMARY & CLASSIFICATION
# ========================================================================

@mcp.tool()
def text_summarizer(text: str, num_sentences: int = 3) -> str:
    """Generate an extractive summary using TextRank algorithm.

    Splits text into sentences, builds a TF-IDF similarity matrix between
    sentences, runs PageRank to rank sentence importance, and returns
    the top-K most important sentences in original order.
    """
    try:
        split_result = json.loads(sentence_splitter(text))
    except (json.JSONDecodeError, TypeError):
        return json.dumps({"error": "Failed to split text into sentences"},
                          ensure_ascii=False, indent=2)

    sentences = split_result["sentences"]

    if len(sentences) < 2:
        return json.dumps({
            "summary": text,
            "num_sentences": 1,
            "note": "Text has fewer than 2 sentences; returning original",
        }, ensure_ascii=False, indent=2)

    num_sentences = min(num_sentences, len(sentences))

    # Tokenize each sentence
    sent_tokens = []
    for sent in sentences:
        tokens = _tokenize_mixed(sent)
        tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)
                  and t not in _CHINESE_STOPWORDS and t.lower() not in _ENGLISH_STOPWORDS]
        sent_tokens.append(tokens)

    # Compute IDF across sentences
    idf = _compute_idf(sent_tokens)
    vectors = [_tfidf_vectorize(t, idf) for t in sent_tokens]

    # Build sentence similarity graph
    n = len(sentences)
    graph: Dict[int, Set[int]] = {i: set() for i in range(n)}
    similarity_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            sim = _cosine_sim(vectors[i], vectors[j])
            similarity_matrix[i][j] = sim
            similarity_matrix[j][i] = sim
            if sim > 0:
                graph[i].add(j)
                graph[j].add(i)

    # Add edges for sentences with any similarity
    for i in range(n):
        for j in range(n):
            if i != j and similarity_matrix[i][j] > 0.01:
                graph[i].add(j)

    if all(len(neighbors) == 0 for neighbors in graph.values()):
        # If no edges, create a fully connected graph with similarity weights
        for i in range(n):
            for j in range(n):
                if i != j:
                    graph[i].add(j)

    # Run PageRank
    scores = _page_rank(graph)

    # Rank sentences by score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Select top-K sentences
    top_indices = set(idx for idx, score in ranked[:num_sentences])

    # Return in original order
    summary_sentences = [sentences[i] for i in range(n) if i in top_indices]

    # Metadata about the summary
    compression_ratio = len(''.join(summary_sentences)) / max(len(text), 1)

    result = {
        "summary": ' '.join(summary_sentences),
        "num_original_sentences": len(sentences),
        "num_summary_sentences": len(summary_sentences),
        "compression_ratio": round(compression_ratio, 4),
        "sentence_scores": [{"index": idx, "score": round(scores[idx], 6), "text": sentences[idx]}
                            for idx, _ in ranked[:10]],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def text_classifier(train_data_json: str, test_text: str) -> str:
    """Train a TF-IDF + Naive Bayes classifier and predict on test text.

    Train data format: JSON list of [{"text": "...", "label": "..."}, ...]
    Uses Laplace smoothing for robust probability estimation.
    """
    try:
        train_data = json.loads(train_data_json)
        if not isinstance(train_data, list):
            return json.dumps({"error": "train_data must be a JSON list"},
                              ensure_ascii=False, indent=2)
    except (json.JSONDecodeError, TypeError):
        return json.dumps({"error": "Invalid JSON format for train_data"},
                          ensure_ascii=False, indent=2)

    if len(train_data) < 2:
        return json.dumps({"error": "Need at least 2 training examples"},
                          ensure_ascii=False, indent=2)

    # Extract labels and tokenize
    labels = []
    doc_tokens = []
    label_counts: Dict[str, int] = {}

    for item in train_data:
        if "text" not in item or "label" not in item:
            continue
        label = str(item["label"])
        tokens = _tokenize_mixed(str(item["text"]))
        tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)]
        doc_tokens.append(tokens)
        labels.append(label)
        label_counts[label] = label_counts.get(label, 0) + 1

    if len(set(labels)) < 2:
        return json.dumps({"error": "Need at least 2 different labels"},
                          ensure_ascii=False, indent=2)

    # Compute IDF across training documents
    idf = _compute_idf(doc_tokens)

    # Build vocabulary
    vocab: Set[str] = set()
    for tokens in doc_tokens:
        vocab.update(tokens)
    vocab_size = len(vocab)
    num_docs = len(doc_tokens)

    # Train Naive Bayes with Laplace smoothing
    # P(label) = count(label) / N
    prior_probs: Dict[str, float] = {}
    for label, count in label_counts.items():
        prior_probs[label] = count / num_docs

    # P(token|label) = (count(token, label) + 1) / (count(label) + |V|)
    token_label_counts: Dict[str, Dict[str, int]] = {}
    label_token_counts: Dict[str, int] = {}

    for i, tokens in enumerate(doc_tokens):
        label = labels[i]
        if label not in label_token_counts:
            label_token_counts[label] = 0
        seen_tokens: Set[str] = set()
        for token in tokens:
            if token not in seen_tokens:
                seen_tokens.add(token)
                if token not in token_label_counts:
                    token_label_counts[token] = {}
                token_label_counts[token][label] = token_label_counts[token].get(label, 0) + 1
                label_token_counts[label] = label_token_counts.get(label, 0) + 1

    # Conditional probabilities with Laplace smoothing
    cond_probs: Dict[str, Dict[str, float]] = {}
    for token in vocab:
        cond_probs[token] = {}
        for label in label_counts:
            count = token_label_counts.get(token, {}).get(label, 0)
            cond_probs[token][label] = math.log((count + 1) / (label_token_counts.get(label, 0) + vocab_size))

    # Classify test text
    test_tokens = _tokenize_mixed(test_text)
    test_tokens = [t.lower() for t in test_tokens if t.strip() and not _is_punctuation(t)]

    # Compute log probability for each class
    log_probs: Dict[str, float] = {}
    for label in label_counts:
        log_prob = math.log(prior_probs[label])
        for token in test_tokens:
            if token in cond_probs:
                log_prob += cond_probs[token][label]
            else:
                # Unknown token: Laplace smoothing
                log_prob += math.log(1 / (label_token_counts.get(label, 0) + vocab_size))
        log_probs[label] = log_prob

    # Convert to probabilities
    max_log = max(log_probs.values())
    exp_probs = {label: math.exp(lp - max_log) for label, lp in log_probs.items()}
    sum_exp = sum(exp_probs.values())
    probs = {label: round(prob / sum_exp, 6) for label, prob in exp_probs.items()}

    predicted_label = max(probs, key=probs.get)
    confidence = probs[predicted_label]

    result = {
        "predicted_label": predicted_label,
        "confidence": confidence,
        "probabilities": probs,
        "test_text_preview": test_text[:100],
        "training_data": {
            "num_examples": num_docs,
            "num_labels": len(label_counts),
            "labels": list(label_counts.keys()),
            "label_distribution": label_counts,
            "vocabulary_size": vocab_size,
        },
        "top_features_for_prediction": sorted(
            [(t, cond_probs[t][predicted_label]) for t in test_tokens if t in cond_probs],
            key=lambda x: x[1], reverse=True
        )[:10],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def kmeans_cluster(texts_json: str, k: int = 3, max_iter: int = 50) -> str:
    """Cluster documents using K-Means++ with TF-IDF vectorization.

    Input: JSON array of strings.
    Uses K-Means++ initialization for better centroid seeding,
    Lloyd's algorithm for iteration, and returns SSE for quality evaluation.
    """
    try:
        docs = json.loads(texts_json)
        if not isinstance(docs, list) or len(docs) < 2:
            return json.dumps({"error": "Need at least 2 documents"},
                              ensure_ascii=False, indent=2)
    except (json.JSONDecodeError, TypeError):
        return json.dumps({"error": "Invalid JSON input"}, ensure_ascii=False, indent=2)

    k = min(k, len(docs))

    # Tokenize and vectorize all documents
    all_tokens = []
    for doc in docs:
        tokens = _tokenize_mixed(doc)
        tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)]
        all_tokens.append(tokens)

    if all(len(t) == 0 for t in all_tokens):
        return json.dumps({"error": "All documents are empty after tokenization"},
                          ensure_ascii=False, indent=2)

    idf = _compute_idf(all_tokens)
    vectors = [_tfidf_vectorize(t, idf) for t in all_tokens]

    vocab = set()
    for vec in vectors:
        vocab.update(vec.keys())
    vocab_list = sorted(vocab)
    vocab_size = len(vocab_list)

    # Convert sparse vectors to dense (list of floats) for computation
    def _to_dense(vec):
        return [vec.get(w, 0.0) for w in vocab_list]

    dense_vectors = [_to_dense(v) for v in vectors]

    def _euclidean_dist(v1, v2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    # K-Means++ initialization
    n = len(dense_vectors)
    centroids = []
    first_idx = random.randint(0, n - 1)
    centroids.append(dense_vectors[first_idx])

    for _ in range(1, k):
        distances = []
        for vec in dense_vectors:
            min_dist = min(_euclidean_dist(vec, c) for c in centroids)
            distances.append(min_dist ** 2)
        total_dist = sum(distances)
        if total_dist <= 0:
            # Pick remaining centroids randomly
            remaining = [i for i in range(n) if dense_vectors[i] not in centroids]
            if remaining:
                idx = random.choice(remaining)
                centroids.append(dense_vectors[idx])
            else:
                centroids.append(dense_vectors[random.randint(0, n - 1)])
        else:
            # Weighted random selection
            r = random.random() * total_dist
            cumulative = 0
            chosen = 0
            for i, d in enumerate(distances):
                cumulative += d
                if cumulative >= r:
                    chosen = i
                    break
            centroids.append(dense_vectors[chosen])

    # Lloyd's iteration
    assignments = [0] * n
    sse_history = []

    for iteration in range(max_iter):
        # Assign each point to nearest centroid
        new_assignments = []
        for vec in dense_vectors:
            dists = [_euclidean_dist(vec, c) for c in centroids]
            new_assignments.append(dists.index(min(dists)))
        assignments = new_assignments

        # Update centroids
        new_centroids = []
        for j in range(k):
            cluster_points = [dense_vectors[i] for i in range(n) if assignments[i] == j]
            if cluster_points:
                mean_vec = [sum(dim) / len(cluster_points) for dim in zip(*cluster_points)]
                new_centroids.append(mean_vec)
            else:
                new_centroids.append(centroids[j])
        centroids = new_centroids

        # Compute SSE
        sse = 0.0
        for i, vec in enumerate(dense_vectors):
            sse += _euclidean_dist(vec, centroids[assignments[i]]) ** 2
        sse_history.append(round(sse, 4))

        # Check convergence (SSE change < 0.1%)
        if len(sse_history) >= 2:
            change = abs(sse_history[-1] - sse_history[-2]) / max(sse_history[-2], 1)
            if change < 0.001:
                break

    # Organize results
    clusters: Dict[int, Dict[str, Any]] = {}
    for j in range(k):
        cluster_indices = [i for i in range(n) if assignments[i] == j]
        cluster_docs = [docs[i] for i in cluster_indices]
        # Get top terms for cluster centroid
        centroid_vec = centroids[j]
        term_scores = [(vocab_list[t], centroid_vec[t]) for t in range(len(centroid_vec))]
        term_scores.sort(key=lambda x: x[1], reverse=True)
        top_terms = [t for t, s in term_scores[:10] if s > 0]

        clusters[str(j)] = {
            "size": len(cluster_docs),
            "documents": cluster_docs[:10],
            "top_terms": top_terms,
            "document_indices": cluster_indices[:20],
        }

    result = {
        "k": k,
        "num_documents": n,
        "clusters": clusters,
        "sse": sse_history[-1] if sse_history else 0,
        "sse_history": sse_history,
        "iterations": len(sse_history),
        "vocabulary_size": vocab_size,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def keyword_frequency(text: str, top_k: int = 30) -> str:
    """Analyze word frequency distribution including Zipf's law verification,
    high-frequency and low-frequency word analysis.
    """
    tokens = _tokenize_mixed(text)
    tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)
              and t not in _CHINESE_STOPWORDS and t.lower() not in _ENGLISH_STOPWORDS]

    if not tokens:
        return json.dumps({"error": "No tokens found"}, ensure_ascii=False, indent=2)

    freq = collections.Counter(tokens)
    total = len(tokens)
    unique = len(freq)
    sorted_freq = freq.most_common()

    # Zipf's law verification
    zipf_data = []
    for rank, (word, count) in enumerate(sorted_freq[:50], 1):
        # Zipf: frequency * rank ≈ constant
        zipf_constant = count * rank
        zipf_data.append({
            "rank": rank,
            "word": word,
            "count": count,
            "frequency": round(count / total, 6),
            "zipf_constant": zipf_constant,
        })

    # Check Zipf's law approximation
    if zipf_data:
        first_constant = zipf_data[0]["zipf_constant"]
        zipf_accuracy = sum(1 for d in zipf_data[:10]
                            if abs(d["zipf_constant"] - first_constant) / first_constant < 0.5)
        zipf_verified = zipf_accuracy >= 5
    else:
        zipf_verified = False

    # High-frequency analysis
    high_freq = sorted_freq[:max(10, min(30, len(sorted_freq) // 10))]
    # Low-frequency words (hapax legomena - words appearing once)
    hapax = [w for w, c in sorted_freq if c == 1]

    # Frequency distribution intervals
    intervals = {
        "1_time": len(hapax),
        "2_5_times": sum(1 for w, c in sorted_freq if 2 <= c <= 5),
        "6_10_times": sum(1 for w, c in sorted_freq if 6 <= c <= 10),
        "11_50_times": sum(1 for w, c in sorted_freq if 11 <= c <= 50),
        "51_plus_times": sum(1 for w, c in sorted_freq if c > 50),
    }

    result = {
        "total_tokens": total,
        "unique_tokens": unique,
        "type_token_ratio": round(unique / total, 4),
        "hapax_legomena_count": len(hapax),
        "hapax_ratio": round(len(hapax) / total, 4),
        "frequency_distribution": intervals,
        "top_words": [{"word": w, "count": c, "frequency": round(c / total, 6)}
                      for w, c in sorted_freq[:top_k]],
        "zipfs_law_verification": {
            "verified": zipf_verified,
            "description": "Zipf's law states that the frequency of a word is inversely proportional to its rank",
            "first_10_entries": zipf_data[:10],
        },
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def collocation_extractor(text: str, top_k: int = 20, min_freq: int = 2) -> str:
    """Discover collocations using PMI (Pointwise Mutual Information) and
    chi-square statistical tests for bigram collocations.
    """
    tokens = _tokenize_mixed(text)
    tokens = [t.lower() for t in tokens if t.strip() and not _is_punctuation(t)
              and t not in _CHINESE_STOPWORDS and t.lower() not in _ENGLISH_STOPWORDS]

    if len(tokens) < 5:
        return json.dumps({"error": "Insufficient tokens for collocation extraction"},
                          ensure_ascii=False, indent=2)

    n = len(tokens)
    # Count unigrams and bigrams
    unigram_counts: Dict[str, int] = {}
    bigram_counts: Dict[Tuple[str, str], int] = {}

    for i in range(n):
        unigram_counts[tokens[i]] = unigram_counts.get(tokens[i], 0) + 1
        if i < n - 1:
            bigram = (tokens[i], tokens[i + 1])
            bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1

    # Compute PMI and chi-square for each bigram
    collocations = []
    for bigram, count in bigram_counts.items():
        if count < min_freq:
            continue
        w1, w2 = bigram
        c1 = unigram_counts.get(w1, 0)
        c2 = unigram_counts.get(w2, 0)

        pmi_val = _pmi(count, c1, c2, n)

        # Contingency table for chi-square
        a = count  # w1 and w2 together
        b = c1 - count  # w1 without w2
        c = c2 - count  # w2 without w1
        d = n - c1 - c2 + count  # neither
        chi2 = _chi_square(a, max(b, 1), max(c, 1), max(d, 1))

        # t-score for significance
        if c1 > 0 and c2 > 0:
            t_score = (count / n - (c1 / n) * (c2 / n)) / math.sqrt((count / n) / n)
        else:
            t_score = 0

        collocations.append({
            "collocation": f"{w1} {w2}",
            "frequency": count,
            "expected_frequency": round(c1 * c2 / n, 2),
            "pmi": round(pmi_val, 4),
            "chi_square": round(chi2, 4),
            "t_score": round(t_score, 4),
        })

    # Sort by PMI (descending)
    collocations.sort(key=lambda x: (-x['pmi'], -x['frequency']))

    # Determine which measure is best
    top_by_pmi = sorted(collocations, key=lambda x: -x['pmi'])[:top_k]
    top_by_chi2 = sorted(collocations, key=lambda x: -x['chi_square'])[:top_k]
    top_by_freq = sorted(collocations, key=lambda x: -x['frequency'])[:top_k]

    # Merge and deduplicate
    top_combined: List[Dict] = []
    seen_collocs: Set[str] = set()
    for c in top_by_pmi:
        if c['collocation'] not in seen_collocs:
            top_combined.append(c)
            seen_collocs.add(c['collocation'])
    for c in top_by_chi2:
        if c['collocation'] not in seen_collocs:
            top_combined.append(c)
            seen_collocs.add(c['collocation'])
    for c in top_by_freq:
        if c['collocation'] not in seen_collocs:
            top_combined.append(c)
            seen_collocs.add(c['collocation'])

    result = {
        "total_collocations_found": len(collocations),
        "top_collocations": top_combined[:top_k],
        "pmi_ranked": top_by_pmi[:10],
        "chi_square_ranked": top_by_chi2[:10],
        "frequency_ranked": top_by_freq[:10],
        "statistics": {
            "total_tokens": n,
            "unique_unigrams": len(unigram_counts),
            "unique_bigrams": len(bigram_counts),
        },
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def text_generator(prompt: str, max_length: int = 50, ngram: int = 3, temperature: float = 1.0) -> str:
    """Generate text using an N-gram Markov chain model.

    Builds a transition probability matrix from the prompt text, then
    samples the next token using random walk with temperature control.
    Higher temperature = more random; lower = more deterministic.
    """
    tokens = _tokenize_mixed(prompt)
    tokens = [t for t in tokens if t.strip()]

    if len(tokens) < ngram + 2:
        return json.dumps({"error": f"Prompt too short. Need at least {ngram + 2} tokens."},
                          ensure_ascii=False, indent=2)

    # Build N-gram transition matrix
    # Key: n-gram tuple, Value: list of next tokens
    transitions: Dict[Tuple[str, ...], List[str]] = {}
    for i in range(len(tokens) - ngram):
        key = tuple(tokens[i:i + ngram])
        next_token = tokens[i + ngram]
        if key not in transitions:
            transitions[key] = []
        transitions[key].append(next_token)

    if not transitions:
        return json.dumps({"error": "Could not build transition matrix"},
                          ensure_ascii=False, indent=2)

    # Also collect unigram frequencies for smooth generation
    unigram_freq = collections.Counter(tokens)
    unigram_probs = {w: c / len(tokens) for w, c in unigram_freq.items()}
    unigram_list = list(unigram_probs.keys())
    unigram_weights = [unigram_probs[w] for w in unigram_list]

    # Generate text using random walk
    # Start with a random key that exists in transitions
    start_key = random.choice(list(transitions.keys()))
    generated = list(start_key)

    for _ in range(max_length):
        key = tuple(generated[-ngram:])

        if key in transitions and transitions[key]:
            candidates = transitions[key]
            if temperature != 1.0:
                # Apply temperature scaling
                counts = collections.Counter(candidates)
                total = len(candidates)
                weights = [math.log(c / total + 1e-8) / temperature for c in [counts[w] for w in set(candidates)]]
                # Convert to probabilities via softmax
                max_w = max(weights)
                exp_w = [math.exp(w - max_w) for w in weights]
                sum_w = sum(exp_w)
                if sum_w > 0:
                    probs = [w / sum_w for w in exp_w]
                    unique_candidates = list(set(candidates))
                    next_token = random.choices(unique_candidates, weights=probs, k=1)[0]
                else:
                    next_token = random.choice(candidates)
            else:
                next_token = random.choice(candidates)
        else:
            # Fallback: sample from unigram distribution
            if temperature != 1.0:
                weights = [math.log(w + 1e-8) / temperature for w in unigram_weights]
                max_w = max(weights)
                exp_w = [math.exp(w - max_w) for w in weights]
                sum_w = sum(exp_w)
                if sum_w > 0:
                    probs = [w / sum_w for w in exp_w]
                    next_token = random.choices(unigram_list, weights=probs, k=1)[0]
                else:
                    next_token = random.choice(unigram_list)
            else:
                next_token = random.choices(unigram_list, weights=unigram_weights, k=1)[0]

        generated.append(next_token)

    generated_text = ''.join(generated)

    result = {
        "generated_text": generated_text,
        "seed_prompt_preview": prompt[:100],
        "generated_tokens": len(generated),
        "model_info": {
            "ngram_order": ngram,
            "transition_states": len(transitions),
            "vocabulary_size": len(unigram_freq),
            "temperature": temperature,
        },
        "transition_examples": [{"state": ' '.join(k), "next_tokens": list(set(v))[:5]}
                                for k, v in list(transitions.items())[:5]],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def char_frequency_analyzer(text: str) -> str:
    """Analyze character frequency distribution including letter frequency,
    Chinese character frequency, distribution statistics, and entropy.
    """
    # Overall character frequency
    total_chars = len(text)
    if total_chars == 0:
        return json.dumps({"error": "Empty text"}, ensure_ascii=False, indent=2)

    char_freq = collections.Counter(text)
    unique_chars = len(char_freq)

    # Separate by category
    chinese_chars: Dict[str, int] = {}
    english_letters: Dict[str, int] = {}
    digits: Dict[str, int] = {}
    punctuation: Dict[str, int] = {}
    spaces = 0
    others: Dict[str, int] = {}

    for ch, count in char_freq.items():
        if _is_chinese_char(ch):
            chinese_chars[ch] = count
        elif ch.isalpha() and ch.isascii():
            english_letters[ch.lower()] = english_letters.get(ch.lower(), 0) + count
        elif ch.isdigit():
            digits[ch] = count
        elif ch.isspace():
            spaces += count
        elif _is_punctuation(ch):
            punctuation[ch] = count
        else:
            others[ch] = count

    # Shannon entropy
    entropy = 0.0
    for count in char_freq.values():
        p = count / total_chars
        entropy -= p * math.log2(p)

    # Max possible entropy (uniform distribution)
    max_entropy = math.log2(unique_chars) if unique_chars > 0 else 0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

    # Zipf for characters
    sorted_chars = char_freq.most_common(30)
    zipf_check = []
    for rank, (ch, count) in enumerate(sorted_chars[:20], 1):
        zipf_check.append({
            "rank": rank,
            "char": ch if not _is_punctuation(ch) and not ch.isspace() else repr(ch),
            "count": count,
            "frequency": round(count / total_chars, 6),
            "zipf_constant": count * rank,
        })

    # Chinese character statistics
    top_chinese = sorted(chinese_chars.items(), key=lambda x: -x[1])[:20]
    # English letter frequency
    top_english = sorted(english_letters.items(), key=lambda x: -x[1])[:26]

    result = {
        "total_characters": total_chars,
        "unique_characters": unique_chars,
        "entropy": {
            "shannon_entropy": round(entropy, 4),
            "max_entropy": round(max_entropy, 4),
            "normalized_entropy": round(normalized_entropy, 4),
            "bits_per_character": round(entropy, 4),
        },
        "character_distribution": {
            "chinese_chars": sum(chinese_chars.values()),
            "chinese_unique": len(chinese_chars),
            "english_letters": sum(english_letters.values()),
            "english_unique": len(english_letters),
            "digits": sum(digits.values()),
            "punctuation": sum(punctuation.values()),
            "spaces": spaces,
            "others": sum(others.values()),
        },
        "top_chinese_characters": [{"char": ch, "count": c, "frequency": round(c / total_chars, 6)}
                                    for ch, c in top_chinese],
        "english_letter_frequency": [{"letter": ch, "count": c, "frequency": round(c / max(sum(english_letters.values()), 1), 6)}
                                      for ch, c in top_english],
        "top_overall_characters": [{"char": ch if not ch.isspace() else repr(ch),
                                     "count": c,
                                     "frequency": round(c / total_chars, 6)}
                                    for ch, c in sorted_chars],
        "zipf_preliminary": zipf_check,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def document_stats(text: str) -> str:
    """Compute comprehensive document statistics: character/word/sentence/paragraph
    counts, average sentence length, type-token ratio (TTR), and more.
    """
    # Basic counts
    total_chars = len(text)
    total_chars_no_space = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    chinese_chars_count = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', text))

    # Paragraphs
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    num_paragraphs = len(paragraphs)

    # Sentences
    try:
        split_result = json.loads(sentence_splitter(text))
        sentences = split_result["sentences"]
    except (json.JSONDecodeError, TypeError):
        sentences = [text]
    num_sentences = len(sentences)

    # Words/tokens
    tokens = _tokenize_mixed(text)
    clean_tokens = [t for t in tokens if t.strip() and not _is_punctuation(t)]
    num_tokens = len(clean_tokens)
    unique_tokens = len(set(t.lower() for t in clean_tokens))

    # English words
    english_words = [t for t in clean_tokens if _is_english_word(t)]
    num_english_words = len(english_words)

    # Type-Token Ratio (TTR)
    ttr = unique_tokens / max(num_tokens, 1)

    # Mean TTR (moving average)
    if num_tokens >= 100:
        mean_ttr = 0.0
        chunks = 0
        for i in range(0, num_tokens - 99, 50):
            chunk = [t.lower() for t in clean_tokens[i:i + 100]]
            chunk_unique = len(set(chunk))
            mean_ttr += chunk_unique / 100
            chunks += 1
        mean_ttr = mean_ttr / max(chunks, 1)
    else:
        mean_ttr = ttr

    # Average sentence length
    avg_sentence_chars = total_chars / max(num_sentences, 1)
    avg_sentence_words = num_tokens / max(num_sentences, 1)
    avg_word_length = sum(len(t) for t in clean_tokens) / max(num_tokens, 1)
    avg_paragraph_chars = total_chars / max(num_paragraphs, 1)
    avg_paragraph_sentences = num_sentences / max(num_paragraphs, 1)

    # Longest sentence and word
    longest_sentence = max(sentences, key=len) if sentences else ""
    longest_word = max(clean_tokens, key=len) if clean_tokens else ""

    # Character distribution
    char_dist = collections.Counter(text)
    # Category counts
    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    whitespace = sum(1 for c in text if c.isspace())
    punct = sum(1 for c in text if _is_punctuation(c) and not c.isspace())

    # Readability estimate
    flesch_ease = None
    if num_sentences > 0 and num_english_words > 0:
        total_syllables = 0
        for w in english_words:
            w_lower = w.lower()
            vowels = len(re.findall(r'[aeiouy]+', w_lower))
            if w_lower.endswith('e') and vowels > 1:
                vowels -= 1
            total_syllables += max(1, vowels)

        avg_words_per_sent = num_english_words / max(num_sentences, 1)
        avg_syl_per_word = total_syllables / max(num_english_words, 1)
        flesch_ease = round(206.835 - 1.015 * avg_words_per_sent - 84.6 * avg_syl_per_word, 2)

    result = {
        "basic_stats": {
            "total_characters": total_chars,
            "characters_no_space": total_chars_no_space,
            "chinese_characters": chinese_chars_count,
            "english_words": num_english_words,
            "sentences": num_sentences,
            "paragraphs": num_paragraphs,
            "tokens": num_tokens,
            "unique_tokens": unique_tokens,
        },
        "averages": {
            "chars_per_sentence": round(avg_sentence_chars, 2),
            "words_per_sentence": round(avg_sentence_words, 2),
            "chars_per_paragraph": round(avg_paragraph_chars, 2),
            "sentences_per_paragraph": round(avg_paragraph_sentences, 2),
            "avg_word_length": round(avg_word_length, 2),
        },
        "lexical_richness": {
            "type_token_ratio": round(ttr, 4),
            "mean_segmental_ttr": round(mean_ttr, 4),
            "honore_statistic": round(100 * math.log(num_tokens) / max(1 - len([w for w in set(t.lower() for t in clean_tokens) if clean_tokens.count(w if _is_english_word(w) else w) == 1]) / max(unique_tokens, 1), 0.01), 2) if num_tokens > 0 else 0,
        },
        "extremes": {
            "longest_sentence": longest_sentence[:100],
            "longest_sentence_length": len(longest_sentence),
            "longest_word": longest_word,
            "longest_word_length": len(longest_word),
        },
        "character_composition": {
            "letters": letters,
            "digits": digits,
            "whitespace": whitespace,
            "punctuation": punct,
            "other": total_chars - letters - digits - whitespace - punct,
        },
    }

    if flesch_ease is not None:
        result["flesch_reading_ease"] = flesch_ease

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def stopword_manager(action: str = "list", language: str = "zh", words: str = "") -> str:
    """Manage built-in stop words: list, add, remove, or check stop words.

    Actions:
    - 'list': List stop words for the specified language
    - 'add': Add comma-separated words to stop word list
    - 'remove': Remove comma-separated words from stop word list
    - 'check': Check if given words are stop words
    - 'stats': Show stop word statistics
    """
    global _CHINESE_STOPWORDS, _ENGLISH_STOPWORDS

    # Work with mutable copies
    zh_stop = set(_CHINESE_STOPWORDS)
    en_stop = set(_ENGLISH_STOPWORDS)

    if language.lower() in ('zh', 'cn', 'chinese'):
        target_stop = zh_stop
        lang_name = "Chinese"
    elif language.lower() in ('en', 'eng', 'english'):
        target_stop = en_stop
        lang_name = "English"
    else:
        return json.dumps({"error": f"Unsupported language: {language}"},
                          ensure_ascii=False, indent=2)

    word_list = [w.strip() for w in words.split(',') if w.strip()] if words else []

    if action == "list":
        sorted_words = sorted(target_stop)
        result = {
            "language": lang_name,
            "total_stopwords": len(target_stop),
            "stopwords": sorted_words,
            "sample": sorted_words[:50],
        }

    elif action == "add":
        added = [w for w in word_list if w not in target_stop]
        target_stop.update(word_list)
        if language.lower() in ('zh', 'cn', 'chinese'):
            _CHINESE_STOPWORDS = target_stop
        else:
            _ENGLISH_STOPWORDS = target_stop
        result = {
            "language": lang_name,
            "action": "add",
            "words_added": len(added),
            "total_stopwords": len(target_stop),
            "added_words": added,
        }

    elif action == "remove":
        removed = [w for w in word_list if w in target_stop]
        target_stop -= set(word_list)
        if language.lower() in ('zh', 'cn', 'chinese'):
            _CHINESE_STOPWORDS = target_stop
        else:
            _ENGLISH_STOPWORDS = target_stop
        result = {
            "language": lang_name,
            "action": "remove",
            "words_removed": len(removed),
            "total_stopwords": len(target_stop),
            "removed_words": removed,
        }

    elif action == "check":
        check_results = []
        for w in word_list:
            check_results.append({
                "word": w,
                "is_stopword": w in target_stop,
            })
        result = {
            "language": lang_name,
            "checked_words": check_results,
            "total_checked": len(word_list),
            "stopwords_found": sum(1 for r in check_results if r["is_stopword"]),
        }

    elif action == "stats":
        result = {
            "language": lang_name,
            "total_stopwords": len(target_stop),
            "avg_word_length": round(sum(len(w) for w in target_stop) / max(len(target_stop), 1), 2),
            "one_char_words": sum(1 for w in target_stop if len(w) == 1),
            "two_char_words": sum(1 for w in target_stop if len(w) == 2),
            "three_plus_char_words": sum(1 for w in target_stop if len(w) >= 3),
        }

    else:
        result = {"error": f"Unknown action: {action}. Use: list, add, remove, check, stats"}

    return json.dumps(result, ensure_ascii=False, indent=2)


# ========================================================================
# MAIN ENTRY
# ========================================================================

if __name__ == "__main__":
    mcp.run()