from functools import partial
from itertools import combinations
from operator import add, sub, and_, or_, invert
from typing import List


def get_permut_dfs(nums, cals):
    """递归地搜索所有合法后缀表达式，返回Iterable，nums为操作数，cals为二元运算符
    为了避免遍历所有解空间，使用了yield，这样get_permut在循环中找到解之后就可以直接退出
    若要找到所有解，只需要把所有的yield注释掉，把ans和return相关的注释取消，返回的ans列表就会包括所有可行解"""
    if len(nums) <= 1:
        yield (nums[0], )
        yield (nums[0], invert)
        # return [(nums[0], ), (nums[0], invert)]
    # ans = []
    for ln in range(1, len(nums)//2+1):  # 避免重复
        for comb in combinations(range(len(nums)), ln):
            mark = [False for _ in range(len(nums))]  # True的索引与False的索引分别属于两棵子树
            for c in comb:
                mark[c] = True
            nums1 = [nums[i] for i in range(len(nums)) if mark[i]]  # 子树1
            nums2 = [nums[i] for i in range(len(nums)) if not mark[i]]  # 子树2
            eqs1 = get_permut_dfs(nums1, cals)
            eqs2 = get_permut_dfs(nums2, cals)
            for eq1 in eqs1:
                for eq2 in eqs2:
                    for cal in cals:
                        yield eq1 + eq2 + (cal,)
                        yield eq1 + eq2 + (cal, invert)
                        yield eq2 + eq1 + (cal,)
                        yield eq2 + eq1 + (cal, invert)
                        # ans.append(eq1 + eq2 + (cal,))
                        # ans.append(eq1 + eq2 + (cal, invert))
                        # ans.append(eq2 + eq1 + (cal,))
                        # ans.append(eq2 + eq1 + (cal, invert))
    # return ans


def get_permut(binstrs: List[str], targetstr: str):
    """找到合法的后缀表达式，binstrs为现在有哪些二进制串，targetstr为想要拼成哪个二进制串"""
    target = int(targetstr, base=2)
    nums = list(map(partial(int, base=2), binstrs))  # 计算二进制串相应的值
    for equation in get_permut_dfs(nums, [add, sub, and_, or_]):
        stack = []
        for p in equation:
            if isinstance(p, int):
                stack.append(p)
            else:
                if len(stack) < 1:
                    break
                elif len(stack) < 2:
                    if p == invert:
                        stack[-1] = p(stack[-1])
                    else:
                        break
                else:
                    if p == invert:
                        stack[-1] = p(stack[-1])
                    else:
                        tmp = p(stack.pop(), stack.pop())
                        stack.append(tmp)
        else:
            if len(stack) == 1 and stack[-1] == target:
                return equation
    return tuple()  # 无解，返回空元组


def permut2str(permut):
    """将后缀表达式转为正常表达式"""
    calsign = {add: '+', sub: '-', and_: '&', or_: '|'}
    bin_stack, dec_stack = [], []  # 分别用二进制和十进制表示数字，执行完全一样的操作
    for p in permut:
        if isinstance(p, int):
            bin_stack.append(bin(p)[2:])
            dec_stack.append(str(p))
        else:
            if len(bin_stack) < 1:
                return ""
            elif len(bin_stack) < 2:
                if p == invert:
                    bin_stack[-1] = f"~({bin_stack[-1]})"
                    dec_stack[-1] = f"~({dec_stack[-1]})"
                else:
                    return ""
            else:
                if p == invert:
                    bin_stack[-1] = f"~({bin_stack[-1]})"
                    dec_stack[-1] = f"~({dec_stack[-1]})"
                else:
                    bin_stack.append("(" + bin_stack.pop() + calsign[p] + bin_stack.pop() + ")")
                    dec_stack.append("(" + dec_stack.pop() + calsign[p] + dec_stack.pop() + ")")
    if len(bin_stack) == 1:
        return bin_stack[-1], dec_stack[-1]
    else:
        return "", ""


if __name__ == '__main__':
    permut = get_permut(['10011', '00011', '01011', '01011'], '101001')
    if len(permut) == 0:  # 元组为空则没有可用组合
        print("没有可用的组合")
    else:
        print(f"后缀表达式为{permut}")
        bin_ans, dec_ans = permut2str(permut)
        print(f"结果为{bin_ans}，对应的十进制表示为{dec_ans}")
