import queue
import threading
from functools import partial
from itertools import permutations, combinations_with_replacement, chain
from operator import add, sub, and_, or_, invert
from typing import List


def get_permut(binstrs: List[str], targetstr: str):
    """找到合法的后缀表达式，binstrs为现在有哪些二进制串，targetstr为想要拼成哪个二进制串"""
    target = int(targetstr, base=2)
    nums = list(map(partial(int, base=2), binstrs))  # 计算二进制串相应的值
    print(f"现有{nums}，正在寻找能够拼出{target}的方法...")
    cals = [add, sub, and_, or_, invert]  # 所有合法运算符
    result = queue.Queue(maxsize=1)  # 结果队列

    def solve(ivt_num):
        """寻找在使用取反操作符ivt_num次情况下的可行解"""
        print(f"线程{ivt_num}已开始运行...")
        for cal_comb in combinations_with_replacement(cals[0:4], len(nums)-1):
            for permut in permutations(chain(nums, cal_comb, [invert]*ivt_num)):
                stack = []
                flag = True
                for p in permut:
                    if isinstance(p, int):
                        stack.append(p)
                    else:
                        if len(stack) < 1:
                            flag = False
                            break
                        elif len(stack) < 2:
                            if p == invert:
                                stack[-1] = p(stack[-1])
                            else:
                                flag = False
                                break
                        else:
                            if p == invert:
                                stack[-1] = p(stack[-1])
                            else:
                                tmp = p(stack.pop(), stack.pop())
                                stack.append(tmp)
                if flag and len(stack) == 1 and stack[-1] == target:
                    result.put(permut)  # 找到解就放到结果队列中
                    print(f"线程{ivt_num}已找到解")
                    exit()
        print(f"线程{ivt_num}没有找到解")

    # 多线程遍历所有可能的后缀表达式，每个线程遍历一种取反次数
    solve_threads = []
    for ivt_num in range(len(nums)+1):  # 取反放在最外层循环，因为可能不需要这么多次取反就可以组合出来
        # 设置为daemon线程，这样主线程结束时子线程也会强制结束
        solve_threads.append(threading.Thread(target=solve, args=(ivt_num,), daemon=True))
        solve_threads[-1].start()

    # 主线程等待子线程，直到有子线程找到解或者所有子线程全部运行结束
    while result.empty() and any(tr.is_alive() for tr in solve_threads):
        pass
    if result.empty():
        return False
    else:
        return result.get()


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
        return ""


if __name__ == '__main__':
    permut = get_permut(['10011', '00011', '01011', '01011'], '101001')
    if permut is False:
        print("没有可用的组合")
    else:
        print(f"后缀表达式为{permut}")
        bin_ans, dec_ans = permut2str(permut)
        print(f"结果为{bin_ans}，对应的十进制表示为{dec_ans}")
