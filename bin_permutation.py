from functools import partial
from itertools import combinations
from operator import add, sub, and_, or_, invert
from typing import List, Iterable, Callable, Tuple, Dict, Iterator


def get_postexpr_dfs(nums: List[int],
                     uny_ops: Iterable[Callable[[int], int]], bin_ops: Iterable[Callable[[int, int], int]]) \
        -> Iterator[Tuple[int or Callable]]:
    """递归地搜索所有合法后缀表达式，返回Iterable，nums为操作数，uny_ops为一元运算符，bin_ops为二元运算符
    使用了yield，以避免内存开销过高，而且调用者找到解后停止后此函数就可以直接停止，从而避免遍历整个解空间"""
    if len(nums) <= 1:
        yield (nums[0], )
        for uop in uny_ops:
            yield (nums[0], uop)
    for ln in range(1, len(nums)//2+1):  # 避免重复
        for comb in combinations(range(len(nums)), ln):
            mark = [False for _ in range(len(nums))]  # True的索引与False的索引分别属于两棵子树
            for c in comb:
                mark[c] = True
            nums1 = [nums[i] for i in range(len(nums)) if mark[i]]  # 子树1
            nums2 = [nums[i] for i in range(len(nums)) if not mark[i]]  # 子树2
            eqs1 = get_postexpr_dfs(nums1, uny_ops, bin_ops)
            eqs2 = get_postexpr_dfs(nums2, uny_ops, bin_ops)
            for eq1 in eqs1:
                for eq2 in eqs2:
                    for bop in bin_ops:
                        yield eq1 + eq2 + (bop, )
                        yield eq2 + eq1 + (bop, )
                        for uop in uny_ops:
                            yield eq1 + eq2 + (bop, uop)
                            yield eq2 + eq1 + (bop, uop)


def get_postexpr(nums: List[int], target: int,
                 uny_ops: Iterable[Callable[[int], int]], bin_ops: Iterable[Callable[[int, int], int]]) \
        -> Tuple[int or Callable]:
    """寻找操作数nums与一元运算符uny_ops，二元运算符bin_ops所能构成的所有后缀表达式中结果为target的表达式
    通过调用get_postexpr_dfs遍历所能构成的所有后缀表达式，结果为target就直接返回
    如果想要得到所有可行解，把return的所有equation收集起来即可"""
    for equation in get_postexpr_dfs(nums, uny_ops, bin_ops):
        stack = []
        for p in equation:
            if isinstance(p, int):
                stack.append(p)
            else:
                if len(stack) < 1:
                    break
                elif len(stack) < 2:
                    if p in uny_ops:
                        stack[-1] = p(stack[-1])
                    else:
                        break
                else:
                    if p in uny_ops:
                        stack[-1] = p(stack[-1])
                    else:
                        tmp = p(stack.pop(), stack.pop())
                        stack.append(tmp)
        else:
            if len(stack) == 1 and stack[-1] == target:
                return equation
    return tuple()  # 无解，返回空元组


def postexpr2str(postexpr: Tuple[int or Callable],
                 uny_op_str: Dict[Callable[[int], int], str], bin_op_str: Dict[Callable[[int, int], int], str]) \
        -> Tuple[str, str]:
    """将后缀表达式转为正常表达式，uny_op_str与bin_op_str分别为一元运算符和二元运算符对应的字符串表示
    注意这里默认一元操作符都放在操作数前面"""
    bin_stack, dec_stack = [], []  # 分别用二进制和十进制表示数字，执行完全一样的操作
    for p in postexpr:
        if isinstance(p, int):
            bin_stack.append(bin(p)[2:])
            dec_stack.append(str(p))
        else:
            if len(bin_stack) < 1:
                return "", ""
            elif len(bin_stack) < 2:
                if p in uny_op_str:
                    bin_stack[-1] = f"{uny_op_str[p]}({bin_stack[-1]})"
                    dec_stack[-1] = f"{uny_op_str[p]}({dec_stack[-1]})"
                else:
                    return "", ""
            else:
                if p in uny_op_str:
                    bin_stack[-1] = f"{uny_op_str[p]}({bin_stack[-1]})"
                    dec_stack[-1] = f"{uny_op_str[p]}({dec_stack[-1]})"
                else:
                    bin_stack.append("(" + bin_stack.pop() + bin_op_str[p] + bin_stack.pop() + ")")
                    dec_stack.append("(" + dec_stack.pop() + bin_op_str[p] + dec_stack.pop() + ")")
    if len(bin_stack) == 1:
        return bin_stack[-1], dec_stack[-1]
    else:
        return "", ""


def find_bin_permutation(bin_strs: List[str], target_str: str = '101001'):
    """找到合法的后缀表达式，bin_strs为现在有哪些二进制串，target_str为想要拼成哪个二进制串，不填则默认为101001"""
    target = int(target_str, base=2)
    nums = list(map(partial(int, base=2), bin_strs))  # 计算二进制串相应的值
    # 可使用的二元运算符及其字符串表示
    bin_op_dict = {add: '+', sub: '-', and_: '&', or_: '|'}

    # 可使用的一元运算符及其字符串表示，按照取反后为负数寻找解
    uny_op_dict = {invert: '~'}  # 默认的取反运算符，取反后为负数
    postexpr = get_postexpr(nums, target, uny_op_dict.keys(), bin_op_dict.keys())
    print("-----取反为负时的结果-----")
    if len(postexpr) == 0:  # 元组为空则没有可用组合
        print("取反为负时，没有可用的组合")
    else:
        print(f"后缀表达式为{postexpr}")
        bin_ans, dec_ans = postexpr2str(postexpr, uny_op_dict, bin_op_dict)
        print(f"结果为{bin_ans}，对应的十进制表示为{dec_ans}")

    # 可使用的一元运算符及其字符串表示，按照取反后为正数寻找解
    invert_pos = (lambda x: ~(x | (-1 << x.bit_length())))  # 自定义的一元运算符，取反后仍然为正数，用^表示
    uny_op_dict_pos = {invert_pos: '^'}  # 可使用的一元运算符及其字符串表示
    postexpr = get_postexpr(nums, target, uny_op_dict_pos.keys(), bin_op_dict.keys())
    print("-----取反为正时的结果-----")
    if len(postexpr) == 0:  # 元组为空则没有可用组合
        print("取反为正时，没有可用的组合")
    else:
        print(f"后缀表达式为{postexpr}")
        bin_ans, dec_ans = postexpr2str(postexpr, uny_op_dict_pos, bin_op_dict)
        print(f"结果为{bin_ans}，对应的十进制表示为{dec_ans}")


if __name__ == '__main__':
    find_bin_permutation(['10011', '00011', '01011', '01011'])
