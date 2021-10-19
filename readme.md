<div align="center">
<h1>E5续订程序-腾讯云函数实现</h1>

[![GitHub issues](https://img.shields.io/github/issues/ICE99125/AutoAPI?color=red&style=for-the-badge)](https://github.com/ICE99125/AutoAPI/issues)  [![GitHub forks](https://img.shields.io/github/forks/ICE99125/AutoAPI?style=for-the-badge)](https://github.com/ICE99125/AutoAPI/network)  [![GitHub stars](https://img.shields.io/github/stars/ICE99125/AutoAPI?style=for-the-badge)](https://github.com/ICE99125/AutoAPI/stargazers)  [![Python](https://img.shields.io/badge/python-3.6%2B-orange?style=for-the-badge)](https://www.python.org/)
</div>

### 说明
这个脚本修改至 AutoApiSecret，但是原代码已经被 github 删除了，因此不再此链接
同样不保证能续定

### 步骤
1. 将执行方法改为 index.main，超时时间改为 900

   [![50VTvF.png](https://z3.ax1x.com/2021/10/19/50VTvF.png)](https://imgtu.com/i/50VTvF)

2. 获取 refresh_token

   可使用 rclone.exe 获取，具体参考[B站教程](https://www.bilibili.com/video/BV1mE411V74B?share_source=copy_web)

   也可以自己部署一个获取程序，使用腾讯云 serverless，可以方便以后获取，具体可以参考[E5_refresh_token](https://github.com/ICE99125/E5_refresh_token.git)

3. 填写环境变量，具体需要有

   |    变量名     |       描述       |
   | :-----------: | :--------------: |
   |   clien_id    |      应用ID      |
   | function_name | 云函数名称|
   | refresh_token | 获取到的刷新令牌 |
   |    secret     |     应用密钥     |
   | redirect_uri  |    重定向地址    |
   | region | 云函数所在地区代号，[详情](https://cloud.tencent.com/document/product/583/17238#:~:text=SecretId%3DAKID********EXAMPLE-,%E5%9C%B0%E5%9F%9F%E5%88%97%E8%A1%A8,-%E6%9C%AC%E4%BA%A7%E5%93%81%E6%89%80%E6%9C%89) |

4. 触发器可以选择每 30 分钟执行一次，两次执行的间隔不能超过 1 个小时，因为 refresh_token 能够换取 access_token 的有效时间仅 1 小时