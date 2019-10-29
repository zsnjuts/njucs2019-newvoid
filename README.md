# njucs2019-newvoid
> 南京大学计算机系2019迎新晚会集门票抽奖小助手

鉴于集门票抽奖需要进行的计算较为复杂，我写了一个小脚本来自动计算你和你的小伙伴当前手里的票能不能拼出你想要的数字。

## HTML使用方法

直接打开链接[http://zsnju.cn/njucs2019-newvoid/](http://zsnju.cn/njucs2019-newvoid/)，按照提示输入就可以啦

或者把[bin_permutation.html](./bin_permutation.html)和[bin_permutation.js](./bin_permutation.js)下载下来，按照提示使用就可以啦

## Python使用方法

把bin_permutation.py下载下来，在最下面找到下面这段代码

```python
if __name__ == '__main__':
    find_bin_permutation(['10011', '00011', '01011', '01011'])
```

把find_bin_permutation的参数按照上面格式换成你们的二进制字符串就行了，比如你们有4个人分别是10011,00011,01011,01011（顺序无所谓），那就改成

```python
if __name__ == '__main__':
    find_bin_permutation(['10011', '00011', '01011', '01011'])
```

其他的都不变，然后运行就可以啦

如果你们这几个数可以拼出想要的101001，就会输出相应的计算方式；如果不能的话，就会输出没有可用的组合。

## 算法接口解释

`get_postexpr`函数实现了经典问题24点求解的拓展问题：对于一个整数列表`nums`，有几个一元运算符`uny_ops`和几个二元运算符`bin_ops`，想要知道它们的组合能否计算出整数`target`，如果有的话给出对应的后缀表达式。需要的话也可以通过简单的修改得到所有的可行解。此函数中调用了`get_postexpr_dfs`函数。经过测试，这个算法效率还是比较高的。

使用`get_postexpr`函数，调用者可以自定义一元运算符和二元运算符，都可以计算出相应的后缀表达式。

结合`postexpr2str`函数就可以得到后缀表达式对应的正常表达式。

`find_bin_permutation`就是对上面两个算法接口的使用。