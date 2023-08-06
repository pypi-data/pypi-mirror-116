# 携程 Apollo(阿波罗) 配置客户端

### 说明

这是一个携程 Apollo(阿波罗) 配置客户端。

### 链接

- [GitHub](https://github.com/ztj1993/py-apollo-client)
- [PyPI](https://pypi.org/project/py-apollo-client)

### 安装

```
pip install py-apollo-client
```

### 依赖

```
pip install requests
```

### 使用

环境变量获取客户端：

```
import os

from ApolloConfig import ApolloConfig

os.environ.setdefault('ENV_PREFIX_APOLLO', 'apollo')
os.environ.setdefault('APOLLO_URI', 'http://192.168.68.251:8080')
os.environ.setdefault('APOLLO_APPID', 'equipment-services')

client = ApolloConfig.env()
```

拉取配置：

```
print(client.pull())
```

获取配置(缓存)：

```
print(client.get('debug'))
```

获取配置：

```
print(client.get('debug', cache=False))
```

### 属性

属性|默认值|说明
---|---|---
uri|None|服务地址
appid|None|应用编号
ip|None|客户端地址，为 True 则自动获取
cluster|default|集群别名
namespace|application|空间别名
release|None|最后版本
last|0|最后获取配置时间戳
rate|5|速率限制，几秒内只请求一次接口
setting|{}|获取到的配置
