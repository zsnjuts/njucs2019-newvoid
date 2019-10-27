# njucs2019-newvoid
> 南京大学计算机系2019迎新晚会集门票抽奖小助手

鉴于集门票抽奖需要进行的计算较为复杂，我写了一个小脚本来自动计算你和你的小伙伴当前手里的票能不能拼出你想要的数字。

## HTML使用方法

直接打开链接http://zsnju.cn/njucs2019-newvoid/，按照提示输入就可以啦

或者把[bin_permutation.html](./bin_permutation.html)和[bin_permutation.js](./bin_permutation.js)下载下来，按照提示使用就可以啦

## Python使用方法

把bin_permutation.py下载下来，在里面找到下面这段代码

```python
if __name__ == '__main__':
    permut = get_permut(['10011', '00011', '01011'], '101001')
```

把get_permut的第一个参数按照上面格式换成你们的二进制字符串就行了，比如你们有4个人分别是10011,00011,01011,01011（顺序无所谓），那就改成

```python
if __name__ == '__main__':
    permut = get_permut(['10011', '00011', '01011', '01011'], '101001')
```

其他的都不变，然后运行就可以啦

如果你们这几个数可以拼出想要的101001，就会输出相应的计算方式；如果不能的话，就会输出没有可用的组合。