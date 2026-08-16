# LeetCode 热题 100：刷题前算法知识详解（Python 版）

> 适用题单：[LeetCode 热题 100](https://leetcode.cn/studyplan/top-100-liked/)  
> 核对日期：2026-08-16  
> 当前题单：100 题，17 个官方模块；简单 20 题、中等 68 题、困难 12 题。

这不是一份“100 份答案拼在一起”的题解，而是一份开始刷题前的算法课。目标是让你看到新题时，能够依次回答：

1. 这道题真正要求维护的状态是什么？
2. 哪个数据结构能让这个状态被快速查询或更新？
3. 指针为什么可以移动、元素为什么可以删除、状态为什么可以压缩？
4. 算法正确性依赖的**不变量**是什么？
5. 约束允许 `O(n²)`、`O(n log n)`，还是必须 `O(n)`？

本文已经逐题核对官方题目正文、约束、提示、Python 函数签名和标签；困难题还对照了力扣官方题解中的主要方法。正文会保留官方模块顺序，但也会指出跨模块联系：例如前缀和同时出现在数组和树上，快慢指针同时用于链表找环和“数组映射成链表”，单调结构同时解决窗口最大值、每日温度、柱状图和接雨水。

## 建议怎样使用这份资料

不要试图一口气背下全部模板。推荐四遍学习法：

1. **第一遍读概念**：读每节的“识别信号”和“核心不变量”，先不抄代码。
2. **第二遍手写模板**：关掉文档，手写哈希、滑窗、二分、DFS/BFS、回溯和 DP 骨架。
3. **第三遍开始做题**：简单题限时 20 分钟，中等题 35 分钟；卡住时只看本节的模型，不立刻看完整题解。
4. **第四遍复盘**：记录“第一反应、失败原因、正确不变量、边界用例、复杂度”，一周后盲写。

推荐知识顺序不是网页顺序，而是：

```text
Python 与复杂度
  → 哈希 / 数组 / 双指针
  → 滑动窗口 / 前缀和 / 二分
  → 链表 / 栈 / 队列 / 堆
  → 树 / 图 / 回溯
  → 贪心 / 一维 DP / 背包 / 二维 DP
  → 单调结构 / 设计题 / 12 道困难题
```

---

# 0. 开始前必须具备的基础

## 0.1 先从数据规模反推复杂度

这是经验范围，不是硬性定律，但足够用于筛掉明显不可行的方法：

| 最大规模 | 通常可尝试的复杂度 | 常见方法 |
|---:|---:|---|
| `n ≤ 10` | 指数级、阶乘级 | 回溯、状态枚举、N 皇后 |
| `n ≤ 20` | `O(2^n)` 左右 | 子集枚举、位掩码 |
| `n ≤ 10³` | `O(n²)` | 二维 DP、固定一项再双指针 |
| `n ≤ 10⁵` | `O(n log n)` 或 `O(n)` | 排序、堆、二分、哈希、滑窗 |
| `n ≤ 10⁶` | 通常接近 `O(n)` | 扫描、计数、前缀和 |

复杂度分析不要只数循环层数。两个典型反例：

- 单调栈虽然有 `for + while`，但每个元素只入栈、出栈各一次，总计 `O(n)`。
- 最长连续序列虽然有外层循环和向后扩展，但只从每条链的起点扩展，每个不同数字最多参与一次，总计平均 `O(n)`。

## 0.2 写算法前先写“不变量”

不变量是在循环或递归的每一步都成立的事实。它既帮助推导，也帮助排错。

例如：

- 两数之和：处理下标 `i` 前，字典里只有 `i` 左侧元素。
- 滑动窗口：进入下一轮外循环前，窗口满足规定的合法性。
- 单调队列：队列中的下标递增，对应值递减，队首仍在窗口内。
- 二分查找：答案始终在当前搜索区间中。
- 链表反转：`prev` 是已经反转好的前缀，`cur` 是尚未处理后缀的头。
- 树形 DP：递归返回值只表达“能向父节点提供什么”，全局答案可在节点处另外更新。

如果代码写乱了，先不要补 `if`。重新说清楚变量含义和不变量，通常会直接暴露错误。

## 0.3 Python 高频容器与代价

```python
from collections import Counter, defaultdict, deque
from functools import cache
from heapq import heappop, heappush, heapify
from bisect import bisect_left, bisect_right

seen = set()                 # 存在性、去重
index = {}                   # 值 -> 下标
freq = Counter()             # 值 -> 次数
groups = defaultdict(list)   # 键 -> 一组对象
queue = deque()              # O(1) 的两端操作
heap = []                    # heapq 是小根堆
```

需要形成肌肉记忆的 Python 坑：

- `list.pop(0)` 是 `O(n)`，队列用 `deque.popleft()`。
- `x in list` 是 `O(n)`；高频存在性查询用 `set`/`dict`。
- 下标可能为 `0`，不要用 `if pos.get(x)` 判断键存在，要用 `if x in pos`。
- 列表不可哈希；频次数组作为字典键时要转成 `tuple`。
- `[[0] * n] * m` 会让多行引用同一个列表；应写 `[[0] * n for _ in range(m)]`。
- 切片、`reversed` 后转列表、`matrix[::-1]` 都可能分配新空间；严格 `O(1)` 辅助空间题要避免。
- `nums = new_list` 只改变局部绑定；原地修改可用逐项赋值或 `nums[:] = new_list`，后者仍需额外空间。
- `heapq` 只能直接比较元组中的后续字段。若两个优先级相同而对象（如 `ListNode`）不可比较，加入唯一序号：`(priority, serial, node)`。
- Python 递归深度通常约为 1000。极深链表、退化树或大网格 DFS 可能需要改成迭代写法；不要把提高递归上限当作算法正确性的替代品。

## 0.4 统一的解题检查表

读题后按顺序问：

1. 返回的是值、下标、计数、所有方案，还是可行性？
2. 子数组/子串是否连续？子序列是否允许跳过元素？
3. 输入是否有序、非负、唯一、可修改？
4. 是否出现“最近”“第 K”“所有前驱”“动态加入”“最小可行区间”等信号？
5. 暴力解是什么？重复计算发生在哪里？
6. 能否用哈希加速查询、用排序制造单调性、用前缀量消掉区间枚举？
7. 边界：空、单元素、全相同、全负、有重复、答案在首尾、完全无解。
8. 写完后口头证明：每一步为什么不会丢掉答案？

---

# 1. 哈希：把“搜索历史”变成常数时间查询

## 1.1 识别信号

看到这些描述，先想到哈希：

- 某个值此前是否出现过；
- 找当前值的“另一半”；
- 统计频次；
- 按某种等价关系分组；
- 去重后寻找连接关系。

哈希表用空间换时间，让插入、查询、删除的平均复杂度降为 `O(1)`。它不负责排序，也不保证最坏情况 `O(1)`；面试和力扣分析通常采用平均复杂度。

## 1.2 扫描历史：查询后再插入

```python
seen = {}

for i, x in enumerate(nums):
    need = target - x
    if need in seen:
        return [seen[need], i]
    seen[x] = i
```

不变量是：处理 `i` 时，`seen` 只含此前元素。因此当前元素不可能被用两次。若先插入再查询，当 `target == 2 * x` 时可能错误地匹配自己。

## 1.3 规范化签名：把“等价”变成“键相等”

异位词顺序不同，但排序结果或字符频率相同。若字符仅为小写英文字母，可以用固定 26 位频次签名：

```python
groups = defaultdict(list)

for word in strs:
    count = [0] * 26
    for ch in word:
        count[ord(ch) - ord("a")] += 1
    groups[tuple(count)].append(word)
```

好的签名必须满足：同组对象一定同键，不同组对象不会误撞，并且键本身可哈希。

## 1.4 只从链起点扩展

最长连续序列先去重，再只从 `x - 1` 不存在的 `x` 开始：

```python
values = set(nums)
best = 0

for x in values:
    if x - 1 not in values:
        y = x
        while y in values:
            y += 1
        best = max(best, y - x)
```

如果从每个数都向后扩展，`[1,2,...,n]` 会退化为 `O(n²)`；只从链首扩展后，每个不同数字最多被一条链访问一次。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [1. 两数之和](https://leetcode.cn/problems/two-sum/) | 简单 | 补数到历史下标的映射；先查后存 | `O(n)` / `O(n)` |
| [49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/) | 中等 | 排序签名或 26 位频次签名 | 总字符数 `O(T)` / `O(T)` |
| [128. 最长连续序列](https://leetcode.cn/problems/longest-consecutive-sequence/) | 中等 | `set` 去重，只从链首扩展 | 平均 `O(n)` / `O(n)` |

---

# 2. 双指针：用单调性一次排除一批候选

双指针不是固定代码，而是一种证明方式：移动某个指针时，必须解释为什么被跳过的候选不可能更优。

## 2.1 同向读写指针：稳定压缩

```python
write = 0

for x in nums:
    if x != 0:
        nums[write] = x
        write += 1

while write < len(nums):
    nums[write] = 0
    write += 1
```

不变量：`nums[:write]` 始终是已扫描部分中应保留元素的最终相对顺序。

## 2.2 相向指针：移动短板

盛水容器面积为：

\[
A=(r-l)\min(h_l,h_r)
\]

若 `h_l ≤ h_r`，保留 `l` 而将 `r` 左移，只会让宽度变小，短板仍不可能超过 `h_l`，所以不会更优；可以永久淘汰左端点。另一侧对称。

```python
left, right = 0, len(height) - 1
best = 0

while left < right:
    best = max(best, (right - left) * min(height[left], height[right]))
    if height[left] <= height[right]:
        left += 1
    else:
        right -= 1
```

## 2.3 排序 + 固定一项 + 两数之和

三数之和先排序，固定 `nums[i]`，然后在右侧有序区间用相向指针：和小则左移，和大则右移。去重有两层：固定项去重，命中答案后的左右端点去重。

这里排序不是为了“看起来整齐”，而是制造一种可证明的单调性：移动端点后，和只会朝一个方向变化。

## 2.4 接雨水：先从前后缀理解，再压缩为双指针

位置 `i` 的水量是：

\[
w_i=\min(L_i,R_i)-h_i
\]

其中 `L_i`、`R_i` 是包含当前位置的左侧最高和右侧最高。先写两个数组可得 `O(n)` 时间、`O(n)` 空间；再观察只需要较小的一侧边界即可结算当前端点，于是压缩为空间 `O(1)`：

```python
left, right = 0, len(height) - 1
left_max = right_max = 0
water = 0

while left <= right:
    left_max = max(left_max, height[left])
    right_max = max(right_max, height[right])

    if left_max <= right_max:
        water += left_max - height[left]
        left += 1
    else:
        water += right_max - height[right]
        right -= 1
```

关键不是背 `if`，而是：若 `left_max ≤ right_max`，右侧已经存在足够高的屏障，左端的水位上限由 `left_max` 确定，未知的更右部分不再影响它。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [283. 移动零](https://leetcode.cn/problems/move-zeroes/) | 简单 | 同向读写指针、稳定压缩、原地修改 | `O(n)` / `O(1)` |
| [11. 盛最多水的容器](https://leetcode.cn/problems/container-with-most-water/) | 中等 | 相向指针，每次淘汰短板端 | `O(n)` / `O(1)` |
| [15. 三数之和](https://leetcode.cn/problems/3sum/) | 中等 | 排序 + 固定一项 + 相向双指针 + 去重 | `O(n²)` / 依排序实现 |
| [42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/) | 困难 | 前后缀最大值；进阶为双指针，也可单调栈 | `O(n)` / `O(1)` |

---

# 3. 滑动窗口：维护一个连续区间

## 3.1 什么时候能滑

窗口 `[left,right]` 高效的前提是：右端扩张、左端收缩时，合法性具有可单调维护的方向，左边界不必回退。每个元素最多进入和离开窗口各一次，所以通常是 `O(n)`。

特别注意：数组含负数时，窗口和不再随扩张单调增加、随收缩单调减少。因此“和为 K 的子数组”不能套普通滑窗，应想到前缀和。

## 3.2 最长合法窗口：记录最近位置

```python
last = {}
left = 0
best = 0

for right, ch in enumerate(s):
    if ch in last:
        left = max(left, last[ch] + 1)
    last[ch] = right
    best = max(best, right - left + 1)
```

必须取 `max`，因为该字符上次出现的位置可能早已落在当前窗口左边；左边界绝不能倒退。

## 3.3 固定长度窗口：增一、删一、判断

找所有异位词时，合法窗口长度固定为 `len(p)`：

```python
need = [0] * 26
window = [0] * 26

for ch in p:
    need[ord(ch) - 97] += 1

ans = []
m = len(p)

for right, ch in enumerate(s):
    window[ord(ch) - 97] += 1

    if right >= m:
        out = s[right - m]
        window[ord(out) - 97] -= 1

    if right >= m - 1 and window == need:
        ans.append(right - m + 1)
```

26 是常数，因此每次比较两个 26 位列表，整体仍可记为 `O(n)`。字符集很大时再维护“不匹配的字符种数”。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) | 中等 | 可变窗口；最近位置让左端跳跃 | `O(n)` / `O(字符集)` |
| [438. 找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) | 中等 | 长度固定的频次窗口 | `O(\|s\|+\|p\|)` / `O(1)` |

---

# 4. 子串应用：前缀和、单调队列、最小覆盖

官方“子串”模块中的三题其实对应三种完全不同的模型。

## 4.1 前缀和 + 频次哈希

定义 `P[0]=0`，`P[j]` 为前 `j` 个数之和，则区间 `[i,j)` 的和为 `P[j]-P[i]`。当前前缀为 `p` 时，和为 `k` 的起点数量等于此前前缀 `p-k` 的出现次数。

```python
prefix = 0
answer = 0
freq = {0: 1}

for x in nums:
    prefix += x
    answer += freq.get(prefix - k, 0)
    freq[prefix] = freq.get(prefix, 0) + 1
```

`{0:1}` 代表空前缀，使从下标 0 开始的合法子数组能被计数。必须先查询再记录当前前缀，否则 `k == 0` 时会把空区间计入。字典存的是次数，不是单纯存在性。

## 4.2 单调队列：删除永远不会再赢的候选

窗口最大值的双端队列保存**下标**，并满足：

1. 下标从队首到队尾递增；
2. 对应值从队首到队尾单调不增；
3. 队首仍在当前窗口内。

```python
q = deque()
answer = []

for i, x in enumerate(nums):
    while q and q[0] <= i - k:
        q.popleft()

    while q and nums[q[-1]] <= x:
        q.pop()

    q.append(i)

    if i >= k - 1:
        answer.append(nums[q[0]])
```

为什么旧队尾能永久删除？新元素不小于它，而且比它更晚过期；只要旧元素还在未来窗口，新元素也一定在，并且更优。每个下标最多进出一次，所以是 `O(n)`。

## 4.3 最小覆盖：扩张到有效，收缩到极限

```python
need = Counter(t)
window = defaultdict(int)
required = len(need)
formed = 0
left = 0
best_len = float("inf")
best_left = 0

for right, ch in enumerate(s):
    window[ch] += 1
    if ch in need and window[ch] == need[ch]:
        formed += 1

    while formed == required:
        if right - left + 1 < best_len:
            best_len = right - left + 1
            best_left = left

        out = s[left]
        if out in need and window[out] == need[out]:
            formed -= 1
        window[out] -= 1
        left += 1
```

`formed` 是“已经满足需求次数的字符种类数”，不是字符总数。`t="AABC"` 必须覆盖两个 `A`。更新 `formed` 的时机必须在计数刚好跨过阈值时，不能每次都增减。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/) | 中等 | 前缀和 + 此前前缀频次 | `O(n)` / `O(n)` |
| [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) | 困难 | 保存下标的单调递减队列 | `O(n)` / `O(k)` |
| [76. 最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/) | 困难 | 字符频次；扩张有效、收缩极限 | `O(\|s\|+\|t\|)` / `O(字符集)` |

---

# 5. 普通数组：状态、区间、置换、贡献分解、原地哈希

## 5.1 Kadane：把“必须以当前结尾”定义成状态

\[
dp_i=\max(nums_i, dp_{i-1}+nums_i)
\]

```python
ending = best = nums[0]

for x in nums[1:]:
    ending = max(x, ending + x)
    best = max(best, ending)
```

`ending` 是必须以当前位置结尾的最大非空子数组和，`best` 才是全局答案。不能用 0 初始化，否则全负数组会错误返回 0。

## 5.2 区间合并：排序后只看结果尾部

按左端点排序后，新区间只可能与当前结果中的最后一个区间发生重叠：

```python
intervals.sort(key=lambda p: p[0])
merged = []

for start, end in intervals:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)
```

闭区间 `[1,4]` 与 `[4,5]` 在端点相交，因此要合并。

## 5.3 三次翻转实现原地轮转

右移 `k` 位先做 `k %= n`，然后翻转全部、前 `k` 个、后 `n-k` 个：

```python
def reverse_part(a, left, right):
    while left < right:
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1
```

切片拼接更短，但需要 `O(n)` 新空间，不满足进阶要求。

## 5.4 前后缀贡献：除自身乘积

\[
answer_i=\left(\prod_{j<i}nums_j\right)\left(\prod_{j>i}nums_j\right)
\]

```python
n = len(nums)
answer = [1] * n

prefix = 1
for i in range(n):
    answer[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(n - 1, -1, -1):
    answer[i] *= suffix
    suffix *= nums[i]
```

不用除法，因此一个零、多个零都无需特判。题目允许不把输出数组计入辅助空间。

## 5.5 原地哈希：值 `x` 应住在下标 `x-1`

长度为 `n` 的数组中，最小缺失正数一定落在 `[1,n+1]`。于是只需把范围 `[1,n]` 内的值放回对应槽位：

```python
n = len(nums)
i = 0

while i < n:
    x = nums[i]
    if 1 <= x <= n and nums[x - 1] != x:
        target = x - 1
        nums[i], nums[target] = nums[target], nums[i]
    else:
        i += 1

for i, x in enumerate(nums):
    if x != i + 1:
        return i + 1
return n + 1
```

`nums[x-1] != x` 防止重复值导致死循环。虽然单个位置可能连续交换，但每次有效交换至少让一个值归位，总交换数 `O(n)`。另一种官方方法是把数组当作出现性位图，用正负号标记。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/) | 中等 | Kadane；局部结尾状态 + 全局最优 | `O(n)` / `O(1)` |
| [56. 合并区间](https://leetcode.cn/problems/merge-intervals/) | 中等 | 按左端排序 + 维护最后区间 | `O(n log n)` |
| [189. 轮转数组](https://leetcode.cn/problems/rotate-array/) | 中等 | `k %= n` + 三次翻转 | `O(n)` / `O(1)` |
| [238. 除了自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/) | 中等 | 输出数组存前缀积，变量滚动后缀积 | `O(n)` / `O(1)`（不计输出） |
| [41. 缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/) | 困难 | 答案范围压缩 + 原地哈希/置换 | `O(n)` / `O(1)` |

---

# 6. 矩阵：坐标、不变量与边界收缩

## 6.1 矩阵置零：先标记，后修改

若看到零就立即清空整行整列，新产生的零会污染后续判断。常数空间做法用首行、首列存标记，并额外保存它们最初是否含零：

```python
m, n = len(matrix), len(matrix[0])
first_row_zero = any(matrix[0][j] == 0 for j in range(n))
first_col_zero = any(matrix[i][0] == 0 for i in range(m))

for i in range(1, m):
    for j in range(1, n):
        if matrix[i][j] == 0:
            matrix[i][0] = 0
            matrix[0][j] = 0

for i in range(1, m):
    for j in range(1, n):
        if matrix[i][0] == 0 or matrix[0][j] == 0:
            matrix[i][j] = 0

if first_row_zero:
    for j in range(n):
        matrix[0][j] = 0
if first_col_zero:
    for i in range(m):
        matrix[i][0] = 0
```

## 6.2 螺旋遍历：维护四条闭边界

维护尚未访问区域 `top..bottom × left..right`。每走完上、右、下、左一条边就收缩对应边界。走下边和左边前必须再次检查边界，否则单行或单列中心会被重复访问。

## 6.3 旋转图像：把坐标映射拆成两步

顺时针 90° 的映射是 `(i,j) -> (j,n-1-i)`，可分解为：

1. 沿主对角线转置；
2. 每一行反转。

```python
n = len(matrix)

for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

for row in matrix:
    row.reverse()
```

## 6.4 行列有序矩阵：从右上角逐行/逐列淘汰

```python
row = 0
col = len(matrix[0]) - 1

while row < len(matrix) and col >= 0:
    x = matrix[row][col]
    if x == target:
        return True
    if x > target:
        col -= 1
    else:
        row += 1
return False
```

当前值太大就排除当前列，太小就排除当前行，每步永久淘汰一行或一列，总共 `O(m+n)`。这道题不能像“搜索二维矩阵 I”那样把矩阵视为全局有序的一维数组：它只保证每行和每列各自递增。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [73. 矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/) | 中等 | 延迟修改；首行首列作为标记区 | `O(mn)` / `O(1)` |
| [54. 螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/) | 中等 | 四边界逐层收缩 | `O(mn)` / 输出外 `O(1)` |
| [48. 旋转图像](https://leetcode.cn/problems/rotate-image/) | 中等 | 转置 + 每行反转 | `O(n²)` / `O(1)` |
| [240. 搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/) | 中等 | 右上角阶梯搜索 | `O(m+n)` / `O(1)` |

---

# 7. 链表：维护关系，而不是搬运数值

链表题的计算往往不复杂，真正难点是修改 `next` 后仍清楚：哪一段已经完成、下一段入口在哪里、谁是新头和当前尾、有没有丢失后缀。

## 7.1 三个通用工具

- `dummy` 哨兵：把删除头节点、头节点变化统一成普通节点后的操作。
- `prev / cur / nxt`：反转链表的三指针。
- 快慢指针：制造固定距离、找中点、判环、找环入口。

节点相交和环入口比较的是对象身份，不是节点值：应判断 `p is q`，不能判断 `p.val == q.val`。

## 7.2 反转链表的核心不变量

```python
def reverse(head):
    prev, cur = None, head

    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    return prev
```

每轮开始时：`prev` 是已反转前缀的头，`cur` 是未处理后缀的头。必须先保存 `nxt`，否则反向连接后会丢掉后缀。

## 7.3 快慢指针的三种数学模型

### 两链相交：交换起点抵消长度差

```python
p, q = headA, headB

while p is not q:
    p = p.next if p else headB
    q = q.next if q else headA

return p      # 相交节点，或共同的 None
```

两者分别走 `A→B` 和 `B→A`，走过的总长度相同，因此独有前缀长度差被抵消。

### 固定间距：删除倒数第 N 个

从哨兵开始，先让 `fast` 超前 `n` 步；之后同步移动，`fast` 到尾时 `slow` 位于待删除节点前驱。哨兵让删除原头节点无需特判。

### Floyd 判环与找入口

```python
def detect_cycle(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            p = head
            while p is not slow:
                p = p.next
                slow = slow.next
            return p

    return None
```

设入环前长度为 `μ`，环长为 `λ`，首次相遇点距入口为 `x`。相遇时快指针比慢指针多走整圈，能推出 `μ = kλ - x`。因此一个指针从头走、另一个从相遇点走，同速前进会在入口相遇。

## 7.4 合并与链表归并排序

```python
def merge(a, b):
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next

    tail.next = a or b
    return dummy.next
```

不变量：`dummy.next ... tail` 已有序，且恰好包含已经消费的节点。

链表不支持随机访问，却能 `O(1)` 断开和拼接，因此排序链表最适合归并排序：快慢指针找中点，真正断开，递归排序两半，再合并。自顶向下为 `O(n log n)` 时间、`O(log n)` 递归栈；严格常数辅助空间时学习自底向上归并。

合并 K 个升序链表的两个主方法：

- 两两分治：每层全部节点被合并一次，共 `log k` 层，`O(N log k)`。
- 最小堆：堆中保存每条链当前头，共最多 `k` 项，也是 `O(N log k)`。

Python 堆里值相同时不能继续比较 `ListNode`，应放 `(node.val, serial, node)`。

## 7.5 K 个一组翻转：统一使用半开区间

把每组定义为 `[group_head, group_next)`：先确认确有 `k` 个节点，不足时原样保留；反转时令 `prev = group_next`，旧组头反转后会自动连向后缀。

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next

        group_next = kth.next
        prev, cur = group_next, group_prev.next

        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        old_head = group_prev.next
        group_prev.next = kth
        group_prev = old_head
```

## 7.6 随机链表复制

直观法用 `old -> new` 哈希映射，两遍填 `next` 和 `random`，`O(n)` 空间。进阶穿插法：

1. 把副本插在原节点后：`A→A'→B→B'`；
2. `A'.random = A.random.next`；
3. 拆开两条链，并恢复原链。

最容易漏的是恢复原链和末尾 `None` 边界。

## 7.7 LRU：哈希表 + 双向链表

需求同时包含按键 `O(1)` 查询与按使用顺序 `O(1)` 淘汰，单一结构无法完成：

- 哈希表保存 `key -> node`；
- 双向链表头端为最近使用 MRU，尾端为最久未使用 LRU；
- 两个哨兵消除空表和单节点特判。

节点必须同时保存 `key` 和 `value`，否则从尾端淘汰节点后无法 `O(1)` 删除字典中的对应键。`get` 命中和 `put` 更新已有键都要把节点移到头端；容量超限时删除尾哨兵之前的节点。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [160. 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/) | 简单 | 双指针换头，比较节点身份 | `O(m+n)` / `O(1)` |
| [206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/) | 简单 | `prev-cur-nxt` | `O(n)` / `O(1)` |
| [234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/) | 简单 | 中点 + 反转后半 + 比较，可恢复 | `O(n)` / `O(1)` |
| [141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/) | 简单 | Floyd 快慢指针相遇 | `O(n)` / `O(1)` |
| [142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/) | 中等 | Floyd 相遇后定位入口 | `O(n)` / `O(1)` |
| [21. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/) | 简单 | `dummy + tail` | `O(m+n)` / `O(1)` |
| [2. 两数相加](https://leetcode.cn/problems/add-two-numbers/) | 中等 | 逐位相加，循环覆盖最终进位 | `O(max(m,n))` |
| [19. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/) | 中等 | 哨兵 + 固定间距双指针 | `O(n)` / `O(1)` |
| [24. 两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/) | 中等 | 每轮重连 `prev→b→a→next` | `O(n)` / `O(1)` |
| [25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/) | 困难 | 完整组预检 + 半开区间反转 | `O(n)` / `O(1)` |
| [138. 随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/) | 中等 | 映射；进阶为穿插副本 | `O(n)` / `O(n)` 或 `O(1)` |
| [148. 排序链表](https://leetcode.cn/problems/sort-list/) | 中等 | 链表归并排序 | `O(n log n)` |
| [23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/) | 困难 | 分治归并或最小堆 | `O(N log k)` |
| [146. LRU 缓存](https://leetcode.cn/problems/lru-cache/) | 中等 | 哈希 + 双向链表 + 双哨兵 | 每次平均 `O(1)` |

---

# 8. 二叉树：先写清楚递归函数返回什么

树题动手前先补全这句话：`dfs(node)` 对以 `node` 为根的子树，返回 ______。

常见返回契约：

1. 子树答案：高度、是否合法；
2. 能向父节点延伸的单臂状态：直径、最大路径和；
3. 某个节点：最近公共祖先、构造后的根；
4. 不返回，只按遍历顺序维护路径状态。

## 8.1 前、中、后序与层序

- 前序“根左右”：根先作决定；适合复制、展开、携带路径。
- 中序“左根右”：BST 会得到严格递增序列。
- 后序“左右根”：父依赖子树结果；适合高度、直径、树形 DP。
- 层序 BFS：适合按层输出、最短层数、右视图。

迭代中序模板：

```python
stack = []
cur = root

while cur or stack:
    while cur:
        stack.append(cur)
        cur = cur.left

    cur = stack.pop()
    # 访问 cur
    cur = cur.right
```

层序遍历必须在进入本层时冻结 `len(queue)`；本层新加入的节点只能在下一层处理。

## 8.2 BST 是全局范围约束

只检查直接孩子不够。正确方法是向下传递开区间：

```python
def valid(node, low, high):
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return (
        valid(node.left, low, node.val)
        and valid(node.right, node.val, high)
    )
```

重复值不合法，所以必须严格不等。另一方法是验证中序序列严格递增。第 K 小也来自同一性质：中序访问到第 `k` 个即可提前结束，不必保存整条序列。

## 8.3 直径与最大路径和：返回单臂，节点处拼双臂

直径中，`depth(node)` 返回能给父节点使用的最大单臂深度；当前节点处可用左右两臂更新全局直径。

最大路径和完全同构：

```python
best = float("-inf")

def gain(node):
    nonlocal best
    if not node:
        return 0

    left = max(0, gain(node.left))
    right = max(0, gain(node.right))

    best = max(best, node.val + left + right)
    return node.val + max(left, right)
```

返回给父亲时只能选一臂，否则路径分叉；更新全局时才能把左右两臂拼起来。负贡献直接舍弃，但全局答案必须初始化为负无穷，保证全负树仍选至少一个节点。

## 8.4 树上的前缀和

路径总和 III 与数组“和为 K 的子数组”是同一模型，只是线性前缀变成当前根到节点的递归路径：

```python
freq = defaultdict(int)
freq[0] = 1

def dfs(node, prefix):
    if not node:
        return 0

    prefix += node.val
    count = freq[prefix - targetSum]

    freq[prefix] += 1
    count += dfs(node.left, prefix)
    count += dfs(node.right, prefix)
    freq[prefix] -= 1

    return count
```

离开节点时必须撤销，因为 `freq` 只能代表当前祖先链；否则会把不同分支错误拼成路径。

## 8.5 最近公共祖先

```python
def dfs(node):
    if node is None or node is p or node is q:
        return node

    left = dfs(node.left)
    right = dfs(node.right)

    if left and right:
        return node
    return left or right
```

契约：返回当前子树中找到的 `p/q`，或已经确定的 LCA。左右分别非空时，当前节点首次汇合两者。

## 8.6 从前序与中序构造树

前序提供根的顺序，中序确定左右子树范围。用哈希把“值到中序下标”降为 `O(1)`，递归只传区间边界，不反复切片：

```python
pos = {value: i for i, value in enumerate(inorder)}
pre_i = 0

def build(lo, hi):
    nonlocal pre_i
    if lo > hi:
        return None

    value = preorder[pre_i]
    pre_i += 1
    mid = pos[value]

    root = TreeNode(value)
    root.left = build(lo, mid - 1)
    root.right = build(mid + 1, hi)
    return root
```

题目保证值互异。每层 `inorder.index()` 或切片都会让最坏复杂度退化为 `O(n²)`。

## 8.7 展开为链表

目标顺序是前序。可逆前序“右、左、根”处理，用 `prev` 指向前序中的后继：处理当前节点时设 `node.right = prev`、`node.left = None`。也可用常数空间迭代法，把左子树最右节点接到原右子树，再把整棵左子树移到右侧。

| 题目 | 难度 | 递归契约/核心模型 | 目标复杂度 |
|---|---|---|---|
| [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/) | 简单 | 中序递归或显式栈 | `O(n)` / `O(h)` |
| [104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | 简单 | 返回子树高度 | `O(n)` / `O(h)` |
| [226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/) | 简单 | 交换并返回已翻转子树根 | `O(n)` / `O(h)` |
| [101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/) | 简单 | `mirror(a,b)` 比较外侧与内侧 | `O(n)` / `O(h)` |
| [543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/) | 简单 | 返回单臂高度，双臂更新直径 | `O(n)` / `O(h)` |
| [102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | 中等 | BFS，冻结每层长度 | `O(n)` / `O(w)` |
| [108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) | 简单 | 中点为根，递归左右区间 | `O(n)` |
| [98. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/) | 中等 | 上下界或严格递增中序 | `O(n)` / `O(h)` |
| [230. 二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) | 中等 | 中序第 `k` 个，提前终止 | 最多 `O(n)` |
| [199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/) | 中等 | BFS 每层最后一个；或右优先 DFS | `O(n)` |
| [114. 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) | 中等 | 逆前序 `prev` 或原地前驱重连 | `O(n)` |
| [105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 中等 | 前序根指针 + 中序区间哈希 | `O(n)` / `O(n)` |
| [437. 路径总和 III](https://leetcode.cn/problems/path-sum-iii/) | 中等 | 当前祖先链的前缀和 + 回溯 | `O(n)` / `O(h)` |
| [236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) | 中等 | 左右各找到一个时当前为 LCA | `O(n)` / `O(h)` |
| [124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) | 困难 | 返回单臂增益，双臂更新全局 | `O(n)` / `O(h)` |

Python 递归深度是这一模块的现实风险。节点上限很大且树可能退化时，优先考虑显式栈、BFS 或父指针迭代方案。

---

# 9. 图论：先确定节点、边和访问状态

看到图题先问：什么是节点？何时相邻？有向还是无向？求连通块、最短步数、可达性还是判环？访问状态能否直接写回输入？

## 9.1 网格是隐式图

矩阵格子是节点，上下左右合法移动是边。岛屿数量扫描所有格子，每遇到一块尚未访问的陆地，答案加一并用 DFS/BFS 淹掉整个连通块。

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

stack = [(r, c)]
grid[r][c] = "0"

while stack:
    x, y = stack.pop()

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
            grid[nx][ny] = "0"       # 入栈时立即标记
            stack.append((nx, ny))
```

必须在入栈/入队时标记，而不是弹出时才标记，否则同一节点可能被多个邻居重复加入。大网格递归 DFS 可能超过 Python 递归深度，显式栈更稳妥。

## 9.2 多源 BFS：所有源点同时成为第 0 层

腐烂的橘子把所有初始腐烂点一起入队，相当于增加一个虚拟超级源。逐层扩散，每处理完一整层才增加一分钟。

```python
q = deque()
fresh = 0

for r in range(m):
    for c in range(n):
        if grid[r][c] == 2:
            q.append((r, c))
        elif grid[r][c] == 1:
            fresh += 1

minutes = 0

while q and fresh:
    for _ in range(len(q)):
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc))
    minutes += 1

return minutes if fresh == 0 else -1
```

初始没有新鲜橘子返回 0；队列耗尽仍有新鲜橘子返回 -1。

## 9.3 拓扑排序：反复删除入度为 0 的节点

课程关系 `[course, pre]` 表示边 `pre -> course`。Kahn 算法把所有入度 0 的课程入队，取出后删除其出边；最终处理节点数等于课程数则无环，否则剩余部分含环。

```python
graph = [[] for _ in range(numCourses)]
indegree = [0] * numCourses

for course, pre in prerequisites:
    graph[pre].append(course)
    indegree[course] += 1

q = deque(i for i, d in enumerate(indegree) if d == 0)
taken = 0

while q:
    u = q.popleft()
    taken += 1
    for v in graph[u]:
        indegree[v] -= 1
        if indegree[v] == 0:
            q.append(v)

return taken == numCourses
```

DFS 判有向环则用三色：0 未访问，1 在当前递归路径，2 已完成。遇到指向颜色 1 的边才是回边；一个布尔 `visited` 无法区分当前祖先与已完成节点。

## 9.4 Trie：边代表字符，节点代表前缀

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True
```

`end` 不可省：插入 `apple` 后，`startsWith("app")` 为真，但 `search("app")` 应为假。单次操作 `O(L)`，空间与所有不同前缀的总字符数同阶。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/) | 中等 | 网格连通块 DFS/BFS | `O(mn)` |
| [994. 腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) | 中等 | 所有腐烂点作为多源 BFS 第 0 层 | `O(mn)` |
| [207. 课程表](https://leetcode.cn/problems/course-schedule/) | 中等 | Kahn 拓扑或 DFS 三色判环 | `O(V+E)` |
| [208. 实现 Trie（前缀树）](https://leetcode.cn/problems/implement-trie-prefix-tree/) | 中等 | 字符边 + 结束标记 | 单次 `O(L)` |

---

# 10. 回溯：在决策树上选择、递归、撤销

通用骨架：

```python
ans = []
path = []

def dfs(state):
    if 完成答案:
        ans.append(path.copy())
        return

    for choice in 当前可选项:
        if choice 不合法:
            continue

        path.append(choice)
        更新状态
        dfs(next_state)
        恢复状态
        path.pop()
```

必须保存 `path.copy()`；直接保存 `path` 会让所有答案引用同一个随后不断变化的列表。

## 10.1 排列、组合、子集的状态差异

- 排列：顺序重要，通常维护 `used[i]`，每层可从所有未使用元素选择。
- 子集/组合：顺序不重要，用 `start` 让下一个下标只向右走，避免 `[1,2]` 与 `[2,1]` 重复。
- 元素可重复选：选 `i` 后递归仍传 `i`；每个元素只能选一次则传 `i+1`。

子集的每个递归节点都是一个答案，所以一进入 `dfs` 就记录；排列则只有深度达到 `n` 的叶子是答案。

组合总和候选都是正数。排序后若当前数已大于 `remain`，后面也必然更大，可以 `break`；正数还保证剩余值持续下降，递归必然终止。

## 10.2 只搜索合法前缀

括号生成不应先生成全部字符串再验证。维护已用左右括号数：

- `open_used < n` 才能放 `(`；
- `close_used < open_used` 才能放 `)`。

这样每个前缀都至少有希望扩展为合法答案。输出数是 Catalan 数

\[
C_n=\frac{1}{n+1}\binom{2n}{n}
\]

因此时间不可能小于输出规模。

## 10.3 网格回溯：临时标记后一定恢复

单词搜索的状态是当前位置、待匹配字符下标和当前路径已用格子。可把当前格子临时改成 `#`，递归结束再恢复；即使提前找到答案，也应先恢复再返回。

实用剪枝：

- 单词比格子总数长，直接失败；
- 棋盘字符总频次不足，直接失败；
- 从棋盘中更稀有的单词端点开始，可显著减少起点；
- 路径不能重复使用格子。

## 10.4 分割回文串：回溯 + 区间 DP

若每次切割都重新检查回文，会重复计算相同区间。先预处理：

```python
n = len(s)
pal = [[False] * n for _ in range(n)]

for i in range(n - 1, -1, -1):
    for j in range(i, n):
        pal[i][j] = (
            s[i] == s[j]
            and (j - i <= 1 or pal[i + 1][j - 1])
        )
```

然后 `dfs(start)` 枚举下一段终点，只在 `pal[start][end]` 为真时递归。字符串有 `n-1` 个潜在切口，最坏输出 `2^(n-1)` 个分割，指数复杂度是输出规模决定的。

## 10.5 N 皇后：把约束编码成集合

逐行放置已经消除同行冲突。位置 `(r,c)` 占用列 `c`、主对角线 `r-c`、副对角线 `r+c`，三个集合让冲突判断平均 `O(1)`：

```python
cols, diag1, diag2 = set(), set(), set()

def dfs(r):
    if r == n:
        ans.append(["".join(row) for row in board])
        return

    for c in range(n):
        d1, d2 = r - c, r + c
        if c in cols or d1 in diag1 or d2 in diag2:
            continue

        cols.add(c); diag1.add(d1); diag2.add(d2)
        board[r][c] = "Q"

        dfs(r + 1)

        board[r][c] = "."
        cols.remove(c); diag1.remove(d1); diag2.remove(d2)
```

进阶可用三个位掩码保存列和对角线。`x & -x` 取最低位的 1，`x & (x-1)` 删除最低位的 1。

## 10.6 怎样判断剪枝是否安全

- 可行性剪枝：括号前缀、皇后冲突。
- 单调性剪枝：排序后的组合总和，当前数过大则后面都过大。
- 必要条件剪枝：单词字符频次不足。

只有“后面也一定失败”才能 `break`；仅当前选项失败时只能 `continue`。枚举全部路径时不要随意加记忆化，同一数值状态可能对应不同 `path`；记忆化更适合可行性、最优值或方案数。

| 题目 | 难度 | 搜索状态/剪枝 | 复杂度要点 |
|---|---|---|---|
| [46. 全排列](https://leetcode.cn/problems/permutations/) | 中等 | `used[i]`，元素互异 | `O(n·n!)` |
| [78. 子集](https://leetcode.cn/problems/subsets/) | 中等 | `start` 只向右，每个节点记录 | `O(n·2^n)` |
| [17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/) | 中等 | 每一位选择一个映射字符 | 上界 `O(n·4^n)` |
| [39. 组合总和](https://leetcode.cn/problems/combination-sum/) | 中等 | 非递减下标、元素可复用、排序剪枝 | 输出敏感的指数级 |
| [22. 括号生成](https://leetcode.cn/problems/generate-parentheses/) | 中等 | `open<n`、`close<open` | `O(C_n·n)` |
| [79. 单词搜索](https://leetcode.cn/problems/word-search/) | 中等 | 格子临时标记、频次与起点剪枝 | 约 `O(mn·3^(L-1))` |
| [131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning/) | 中等 | 回文区间 DP + 切割回溯 | 最坏输出 `2^(n-1)` |
| [51. N 皇后](https://leetcode.cn/problems/n-queens/) | 困难 | 逐行、列与两类对角线 | 搜索上界约 `O(n!)` |

---

# 11. 二分查找：寻找单调谓词的分界线

二分不只用于“找一个数”，更一般地是在单调真假序列中找第一个真或最后一个假，例如第一个 `>= target`、第一个 `> target`、最小可行容量。

## 11.1 统一使用左闭右开边界模板

```python
def lower_bound(nums, target):
    """第一个 >= target 的位置；不存在时返回 len(nums)。"""
    lo, hi = 0, len(nums)

    # [0, lo) 全部 < target
    # [hi, n) 全部 >= target
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums, target):
    """第一个 > target 的位置。"""
    lo, hi = 0, len(nums)

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

查找目标值的首尾位置可用 `left = lower_bound(target)`、`right = upper_bound(target)-1`，最后仍要验证 `left < n and nums[left] == target`。

常见错误来自混用 `[lo,hi]` 与 `[lo,hi)`：若采用左闭右开，保留 `mid` 时写 `hi = mid`；若采用闭区间，写法和循环条件都必须成套改变。

## 11.2 二维矩阵的虚拟一维下标

若每行递增且下一行首元素大于上一行尾元素，矩阵按行摊平后全局有序。无需真的复制：虚拟下标 `p` 映射到 `matrix[p // n][p % n]`，在 `[0,m*n)` 二分，复杂度 `O(log(mn))`。

这与第 240 题不同：第 240 题只保证行、列分别有序，不保证行间首尾关系。

## 11.3 旋转数组：每次至少有一半有序

搜索目标时，元素互异保证 `nums[lo] <= nums[mid]` 与否能判断哪一半有序。先判断目标是否位于这段有序区间，再决定保留哪半。

寻找最小值可以只和右端比较：

```python
lo, hi = 0, len(nums) - 1

while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] > nums[hi]:
        lo = mid + 1
    else:
        hi = mid

return nums[lo]
```

`nums[mid] > nums[hi]` 说明中点仍在旋转前的大数段，最小值严格在右侧；否则中点可能就是最小值，所以必须保留 `mid`。

若允许重复，`nums[lo] == nums[mid] == nums[hi]` 时无法判断有序半边，最坏复杂度可能退化。本题恰好保证互异。

## 11.4 两个有序数组中位数

先掌握“第 K 小消除法”：比较两数组剩余部分各自第 `k//2` 个候选，较小一方的那一段都不可能是第 `k` 小，可以整段删除，并把 `k` 减去**实际删除数**。

边界有三类：一个数组耗尽；`k == 1`；某数组剩余不足 `k//2`。

更紧凑的解法是在较短数组上二分切分位置。选 `i`、`j` 使左半总数为 `(m+n+1)//2`，并满足：

\[
A_{i-1}\le B_j,\qquad B_{j-1}\le A_i
\]

使用 `-inf/+inf` 统一处理切分在数组边缘。时间 `O(log min(m,n))`、空间 `O(1)`。这里二分的不是一个数据值，而是“较短数组贡献多少个元素到左半边”。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/) | 简单 | `lower_bound` | `O(log n)` |
| [74. 搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/) | 中等 | 虚拟摊平后的边界二分 | `O(log(mn))` |
| [34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) | 中等 | `lower_bound + upper_bound` | `O(log n)` |
| [33. 搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/) | 中等 | 识别有序半边并保留目标所在侧 | `O(log n)` |
| [153. 寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) | 中等 | 中点与右端比较 | `O(log n)` |
| [4. 寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) | 困难 | 第 K 小消除；或切分位置二分 | `O(log(m+n))` 或 `O(log min(m,n))` |

---

# 12. 栈：最近进入的状态最先结束

## 12.1 识别信号

- 括号或嵌套表达式；
- 离开一层嵌套时恢复上一层现场；
- 最近的未完成任务先被完成；
- 对每个元素找左/右第一个更大或更小值。

## 12.2 匹配栈与最小栈

有效括号让栈只保存未匹配左括号；遇到右括号时栈不能为空且栈顶类型必须匹配，最后还必须检查栈为空。

最小栈让每个元素同时保存“压入它之后的当前最小值”：`(value, prefix_min)`。这样 `push/pop/top/getMin` 全部 `O(1)`。若使用独立辅助栈，遇到等于当前最小值的值也必须同步压入，否则重复最小值弹出后会丢失状态。

## 12.3 字符串解码：栈保存上一层现场

遇到 `[` 时保存外层已生成字符串和本层重复次数，清空当前层；遇到 `]` 时弹出现场并拼接。数字可能多位，所以要写 `num = num * 10 + int(ch)`。时间至少与最终解码结果长度成正比。

## 12.4 单调栈：保存尚未找到答案的候选

每日温度的栈保存下标，对应温度单调不升：

```python
answer = [0] * len(temperatures)
stack = []

for i, temp in enumerate(temperatures):
    while stack and temp > temperatures[stack[-1]]:
        j = stack.pop()
        answer[j] = i - j
    stack.append(i)
```

保存下标既能比较值，又能计算距离。

柱状图最大矩形固定柱 `i` 为高度时，最大宽度由左右第一个更矮柱决定。一遍单调递增栈中，当遇到更矮的右边界时弹出并结算：

```python
stack = []
answer = 0

for right, cur_height in enumerate(heights + [0]):
    while stack and heights[stack[-1]] > cur_height:
        height = heights[stack.pop()]
        left = stack[-1] if stack else -1
        width = right - left - 1
        answer = max(answer, height * width)
    stack.append(right)
```

末尾的 0 是哨兵，强制结算剩余柱子。弹出时，当前 `right` 是右侧第一个更矮位置；弹出后的栈顶是左侧第一个更矮位置。

`>` 与 `>=` 都可能写出正确方案，但必须与“相等高度由哪根柱负责完整宽度”的边界定义一致，不能随意替换。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/) | 简单 | 未匹配左括号栈 | `O(n)` / `O(n)` |
| [155. 最小栈](https://leetcode.cn/problems/min-stack/) | 中等 | 值与前缀最小值同步入栈 | 每次 `O(1)` |
| [394. 字符串解码](https://leetcode.cn/problems/decode-string/) | 中等 | 栈保存外层字符串和重复次数 | `O(输出长度)` |
| [739. 每日温度](https://leetcode.cn/problems/daily-temperatures/) | 中等 | 单调递减的未决下标栈 | `O(n)` / `O(n)` |
| [84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/) | 困难 | 单调递增栈 + 左右更矮边界 | `O(n)` / `O(n)` |

---

# 13. 堆与优先队列：只维护当前最重要的候选

Python `heapq` 是小根堆；大根堆通常存负数。

## 13.1 Top K：堆只是一个方向，先看题目复杂度要求

维护大小为 `k` 的小根堆可以保留当前最大的 `k` 个数，堆顶就是其中最小者，也就是最终第 `k` 大：时间 `O(n log k)`、空间 `O(k)`。

但是当前第 215 题明确要求实现 `O(n)` 算法，所以堆适合学习 Top K 思路，却**不满足当前题目的严格要求**。应使用快速选择的期望 `O(n)`，或利用本题有限值域做计数。

三向快速选择的分区不变量：

```text
[lo, lt)  < pivot
[lt, i)   = pivot
[i, gt]   未处理
(gt, hi]  > pivot
```

分区完成后只进入第 `n-k` 小目标所在的一段；若目标落在等于枢轴的区间就直接返回。随机枢轴期望 `O(n)`、最坏 `O(n²)`，原地空间 `O(1)`。

注意要找的是排序后第 `k` 个元素，不是第 `k` 个不同元素。

## 13.2 高频元素：计数后再选择

频率最大不超过 `n`，所以可用频率桶：`buckets[f]` 保存出现 `f` 次的元素，然后从高频桶向低频收集。时间和空间都是 `O(n)`，满足“优于 `O(n log n)`”。

另一方法是对不同元素维护大小为 `k` 的频率小根堆，复杂度 `O(u log k)`，`u` 为不同元素数。

## 13.3 数据流中位数：双堆维持一个动态切分

- `low` 保存较小一半，用负数模拟大根堆；
- `high` 保存较大一半，是小根堆；
- `max(low) <= min(high)`；
- `len(low)` 等于 `len(high)` 或恰好多一。

```python
class MedianFinder:
    def __init__(self):
        self.low = []
        self.high = []

    def addNum(self, num):
        heappush(self.low, -num)
        heappush(self.high, -heappop(self.low))

        if len(self.high) > len(self.low):
            heappush(self.low, -heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

先把数放进 `low`，再把其最大值送到 `high`，保证左右有序；最后按数量再平衡。插入 `O(log n)`，查询中位数 `O(1)`。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [215. 数组中的第 K 个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) | 中等 | 严格题意用快速选择或计数；堆仅作对照 | 期望 `O(n)` |
| [347. 前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/) | 中等 | 频率桶；或频率小根堆 | 桶 `O(n)` |
| [295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/) | 困难 | 左大根堆 + 右小根堆 | 插入 `O(log n)`，查询 `O(1)` |

---

# 14. 贪心：局部摘要足以代表所有历史方案

贪心不是“凭感觉选当前最好”，而是证明一个更强的状态可以支配较弱状态。常见证明包括：

- 领先论证：贪心方案每一步都不落后于其他方案；
- 交换论证：任意最优解的局部选择可换成贪心选择而不变差；
- 前缀不变量：扫描到当前位置时，一个变量精确概括此前全部方案。

任意硬币面额的零钱兑换就是反例：优先选最大硬币未必最优，所以需要 DP。

## 14.1 前缀最低价

股票题把卖出日固定为今天时，最佳买入一定是此前最低价。维护 `min_price` 与目前最大利润即可，`O(n)`/`O(1)`。

## 14.2 最远可达位置

跳跃游戏中，如果两个历史方案都能覆盖到当前位置，而一个能到得更远，它不会比另一个差，因此全部状态可压缩成 `farthest`。扫描到 `i > farthest` 时说明出现不可跨越的断层。

## 14.3 跳跃游戏 II 是隐式 BFS

```python
steps = 0
current_end = 0
next_end = 0

for i in range(len(nums) - 1):
    next_end = max(next_end, i + nums[i])

    if i == current_end:
        steps += 1
        current_end = next_end
```

`[0,current_end]` 是 `steps` 跳内的当前 BFS 层；扫描整层得到再跳一次的最远边界 `next_end`。必须扫描完整层后才增加步数。循环只到倒数第二个位置，否则到达终点后会多算一次。

## 14.4 最早合法切点

划分字母区间先求每个字符最后出现位置。扫描当前片段时，`end` 是已见所有字符最后位置的最大值；当 `i == end`，这些字符都不会再在右侧出现，这是最早可行切点。每次选最早切点，因此片段数量最多。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [121. 买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) | 简单 | 前缀最低价 + 当前卖出收益 | `O(n)` / `O(1)` |
| [55. 跳跃游戏](https://leetcode.cn/problems/jump-game/) | 中等 | 可达最远位置支配其他状态 | `O(n)` / `O(1)` |
| [45. 跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/) | 中等 | 隐式 BFS 的层边界 | `O(n)` / `O(1)` |
| [763. 划分字母区间](https://leetcode.cn/problems/partition-labels/) | 中等 | 最后出现位置 + 最早合法切点 | `O(n)` / `O(字符集)` |

---

# 15. 动态规划：定义状态，再研究最后一步

写 DP 前依次回答：

1. `dp` 的每个下标精确代表什么？
2. 达到当前状态的最后一次选择是什么？
3. 它依赖哪些更小状态？
4. 空问题、非法状态和初值是什么？
5. 依赖决定了怎样的遍历顺序？答案在哪个状态？

DP 本质上是在一个无环依赖图上计算。滚动数组只是覆盖已经不再需要的状态，必须先保证覆盖顺序不破坏依赖。

## 15.1 相邻线性状态

爬楼梯是 Fibonacci 型：最后一步来自 `i-1` 或 `i-2`。`dp[0]=1` 表示什么也不做是到达 0 阶的一种方式。

打家劫舍转移：

\[
dp_i=\max(dp_{i-1},dp_{i-2}+nums_i)
\]

两个候选分别是“不偷当前房”和“偷当前房”。只依赖前两项，所以可压缩为两个变量。

杨辉三角的内部项来自上一行左上和正上；边界恒为 1。它适合练习“二维关系不等于必须保存完整二维表”。

## 15.2 0/1 背包与完全背包：一维数组的方向就是使用次数

统一定义 `dp[s]` 为容量/总和为 `s` 时的可行性或最优值。

| 模型 | 单个物品可用次数 | 容量遍历 | 原因 |
|---|---:|---|---|
| 0/1 背包 | 至多一次 | 从大到小 | `dp[s-x]` 仍是本轮加入物品前的旧状态 |
| 完全背包 | 无限次 | 从小到大 | 本轮更新过的 `dp[s-x]` 可继续使用当前物品 |

分割等和子集是 0/1 背包：总和为奇数直接失败，否则判断能否凑出一半。

```python
target = sum(nums) // 2
dp = [False] * (target + 1)
dp[0] = True

for x in nums:
    for s in range(target, x - 1, -1):
        dp[s] = dp[s] or dp[s - x]
```

若误从小到大遍历，同一轮会反复使用 `x`，把 0/1 背包变成完全背包。

零钱兑换与完全平方数是完全背包最优化：`dp[s]` 为凑出 `s` 的最少个数，初始除 `dp[0]=0` 外均设为不可达的无穷大，转移 `dp[s] = min(dp[s], dp[s-item]+1)`，容量从小到大。

## 15.3 单词拆分：前缀可达性

定义 `dp[i]` 表示前缀 `s[:i]` 能否拆成字典词。枚举最后一个单词长度，若此前前缀可达且最后一段在字典中，则当前可达。

用集合做词查询，并用字典最大词长限制枚举范围。Python 切片会创建字符串，实际代价与切片长度有关，不应把所有切片成本一律当 `O(1)`。

## 15.4 最长递增子序列：状态 DP 与最优尾值摘要

`O(n²)` 状态是：`dp[i]` 为以 `nums[i]` 结尾的严格递增子序列最大长度。

进阶 `O(n log n)` 维护：

> `tails[length-1]` 是所有该长度递增子序列中最小的可能结尾值。

```python
tails = []

for x in nums:
    pos = bisect_left(tails, x)
    if pos == len(tails):
        tails.append(x)
    else:
        tails[pos] = x

return len(tails)
```

相同长度下结尾越小，未来越容易扩展，所以较大的结尾可淘汰。`tails` 通常并不是原数组中的某条完整 LIS，只是长度状态的最优摘要。严格递增用 `bisect_left`；最长非递减才用 `bisect_right`。

## 15.5 乘积最大子数组：最大和最小会因负数交换角色

```python
cur_max = cur_min = answer = nums[0]

for x in nums[1:]:
    old_max, old_min = cur_max, cur_min
    cur_max = max(x, old_max * x, old_min * x)
    cur_min = min(x, old_max * x, old_min * x)
    answer = max(answer, cur_max)
```

必须先保存旧值，不能让刚更新的最大值参与最小值计算。候选包含 `x` 本身，因此遇到 0 或此前乘积变差时会自动重启。

## 15.6 最长有效括号：三种视角

DP 定义 `dp[i]` 为**以 `i` 结尾**的最长有效长度。只有 `s[i] == ')'` 才可能非零：

- 若前一字符是 `(`：`dp[i] = dp[i-2] + 2`；
- 若前一字符是 `)`：先跨过 `dp[i-1]`，检查其前一位是否为可匹配的 `(`，匹配后还要接上更前面的有效段。

```python
left = i - dp[i - 1] - 1
if left >= 0 and s[left] == '(':
    dp[i] = dp[i - 1] + 2
    if left >= 1:
        dp[i] += dp[left - 1]
```

另两种重要方法：

- 下标栈：初始放 `-1`，栈底代表最后一个未匹配右括号位置；
- 正反两遍计数：正向清除右括号过多的前缀，反向清除左括号过多的后缀，`O(1)` 空间。

| 题目 | 难度 | 状态/模型 | 目标复杂度 |
|---|---|---|---|
| [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/) | 简单 | Fibonacci 型方案数 | `O(n)` / `O(1)` |
| [118. 杨辉三角](https://leetcode.cn/problems/pascals-triangle/) | 简单 | 上一行相邻两项转移 | 输出规模同阶 |
| [198. 打家劫舍](https://leetcode.cn/problems/house-robber/) | 中等 | 相邻互斥线性 DP | `O(n)` / `O(1)` |
| [279. 完全平方数](https://leetcode.cn/problems/perfect-squares/) | 中等 | 平方数作为无限硬币 | `O(n√n)` / `O(n)` |
| [322. 零钱兑换](https://leetcode.cn/problems/coin-change/) | 中等 | 完全背包最少物品数 | `O(amount·coins)` |
| [139. 单词拆分](https://leetcode.cn/problems/word-break/) | 中等 | 前缀可达性 + 字典集合 | 常见 `O(n·最大词长)`，另计切片 |
| [300. 最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/) | 中等 | 结尾 DP；进阶 `tails + 二分` | `O(n log n)` |
| [152. 乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/) | 中等 | 同时维护结尾最大与最小乘积 | `O(n)` / `O(1)` |
| [416. 分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/) | 中等 | 0/1 背包可达性 | `O(n·target)` / `O(target)` |
| [32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/) | 困难 | 结尾 DP、下标栈或双向计数 | `O(n)`；可做到 `O(1)` 空间 |

---

# 16. 多维动态规划：网格、区间与双前缀

## 16.1 网格 DP 的一维压缩

不同路径中，`dp[j]` 更新前代表上方，更新后的 `dp[j-1]` 代表左方，因此可写 `dp[j] += dp[j-1]`。

最小路径和同理：

```python
dp = [float("inf")] * n
dp[0] = 0

for i in range(m):
    for j in range(n):
        from_left = dp[j - 1] if j > 0 else float("inf")
        dp[j] = min(dp[j], from_left) + grid[i][j]
```

压缩后更要说清“更新前/更新后”的含义，否则遍历方向很容易写反。

## 16.2 子串与子序列必须分清

- 子串连续：常用区间 DP、中心扩展、滑窗或“以某位置结尾”。
- 子序列可跳过字符但保持顺序：常用两个前缀长度作为状态。

最长回文子串的区间状态：

\[
pal[l][r]=(s_l=s_r)\land pal[l+1][r-1]
\]

`left` 必须从大到小，保证内层区间已经计算。时间、空间均 `O(n²)`。更实用的中心扩展枚举奇偶中心，时间 `O(n²)`、空间 `O(1)`。

## 16.3 最长公共子序列

定义 `dp[i][j]` 为 `text1[:i]` 与 `text2[:j]` 的 LCS：

- 末尾相同：左上角加一；
- 末尾不同：取删除任一侧末尾后的最大值，即上方和左方最大。

一维压缩时，要用变量 `diagonal` 保存被覆盖前的左上角；`dp[j]` 更新前是上方，`dp[j-1]` 更新后是左方。

## 16.4 编辑距离

定义 `dp[i][j]` 为把 `word1[:i]` 变为 `word2[:j]` 的最少操作。末尾不同的三个来源：

- 删除 `word1` 末尾：`dp[i-1][j]`；
- 向 `word1` 插入目标末尾：`dp[i][j-1]`；
- 替换末尾：`dp[i-1][j-1]`。

空串边界不能漏：空串变成长度 `j` 需要 `j` 次插入；长度 `i` 变空串需要 `i` 次删除。

```python
dp = list(range(len(word2) + 1))

for i, ch1 in enumerate(word1, 1):
    diagonal = dp[0]
    dp[0] = i

    for j, ch2 in enumerate(word2, 1):
        old_up = dp[j]
        if ch1 == ch2:
            dp[j] = diagonal
        else:
            dp[j] = 1 + min(dp[j], dp[j - 1], diagonal)
        diagonal = old_up
```

| 题目 | 难度 | 状态/模型 | 目标复杂度 |
|---|---|---|---|
| [62. 不同路径](https://leetcode.cn/problems/unique-paths/) | 中等 | 网格计数，来自上与左 | `O(mn)` / `O(n)` |
| [64. 最小路径和](https://leetcode.cn/problems/minimum-path-sum/) | 中等 | 网格最小代价 | `O(mn)` / `O(n)` |
| [5. 最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/) | 中等 | 区间 DP 或中心扩展 | `O(n²)`；中心法 `O(1)` 空间 |
| [1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/) | 中等 | 双前缀 DP | `O(mn)` / `O(n)` |
| [72. 编辑距离](https://leetcode.cn/problems/edit-distance/) | 中等 | 双前缀最少操作 DP | `O(mn)` / `O(n)` |

---

# 17. 技巧：利用题目特殊约束把一般问题降维

## 17.1 异或抵消

`x ^ x = 0`、`x ^ 0 = x`，且异或满足交换律与结合律。因此其余元素恰好出现两次时，一遍异或会只留下唯一元素，`O(n)` 时间、`O(1)` 空间。

## 17.2 Boyer–Moore 多数投票

把不同元素两两抵消。出现次数超过一半的元素不可能被完全抵消：

```python
candidate = None
count = 0

for x in nums:
    if count == 0:
        candidate = x
    count += 1 if x == candidate else -1
```

`count` 是抵消后的净票数，不是真实频次。题目保证多数元素存在；若不保证，必须最后再验证候选。

## 17.3 荷兰国旗三向切分

维护：`[0,low)` 为 0，`[low,scan)` 为 1，`[scan,high]` 未处理，`(high,n)` 为 2。

```python
low = scan = 0
high = len(nums) - 1

while scan <= high:
    if nums[scan] == 0:
        nums[low], nums[scan] = nums[scan], nums[low]
        low += 1
        scan += 1
    elif nums[scan] == 2:
        nums[scan], nums[high] = nums[high], nums[scan]
        high -= 1
    else:
        scan += 1
```

把 2 换到右边后不能立刻增加 `scan`，因为换回来的元素仍然未知。

## 17.4 下一个排列：最右提升点 + 最小提升值 + 最小后缀

1. 从右向左找首个 `nums[i] < nums[i+1]`；
2. 从右侧找首个严格大于 `nums[i]` 的数并交换；
3. 反转后缀，使其从非递增变为升序。

为什么正确：字典序增幅要最小，首先改变的位置必须尽量靠右；该位置应换成右侧刚好更大的最小值；改变后，后缀必须排成最小的升序。找不到提升点说明原排列已最大，整体反转成最小排列。

## 17.5 数组映射成函数图：Floyd 找重复数

有 `n+1` 个位置，值都在 `[1,n]`，把边定义为 `i -> nums[i]`。从 0 不断沿边走必然进入环；重复值对应两个不同前驱指向同一节点，因此环入口就是重复数。

```python
slow = fast = 0

while True:
    slow = nums[slow]
    fast = nums[nums[fast]]
    if slow == fast:
        break

finder = 0
while finder != slow:
    finder = nums[finder]
    slow = nums[slow]

return finder
```

这不是普通“数组找重复”技巧，而是完全依赖题目特殊约束：值域能作为合法下标、只有一个不同的重复值、不能修改数组、要求常数空间。

备选方案是对值域 `[1,n]` 二分，统计 `<= mid` 的元素数；若数量大于 `mid`，根据抽屉原理重复值在左半。时间 `O(n log n)`、空间 `O(1)`。

| 题目 | 难度 | 核心模型 | 目标复杂度 |
|---|---|---|---|
| [136. 只出现一次的数字](https://leetcode.cn/problems/single-number/) | 简单 | 异或成对抵消 | `O(n)` / `O(1)` |
| [169. 多数元素](https://leetcode.cn/problems/majority-element/) | 简单 | Boyer–Moore 两两抵消 | `O(n)` / `O(1)` |
| [75. 颜色分类](https://leetcode.cn/problems/sort-colors/) | 中等 | 荷兰国旗三向切分 | `O(n)` / `O(1)` |
| [31. 下一个排列](https://leetcode.cn/problems/next-permutation/) | 中等 | 最右提升点 + 最小提升值 + 反转后缀 | `O(n)` / `O(1)` |
| [287. 寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/) | 中等 | 数组函数图的 Floyd 环入口 | `O(n)` / `O(1)` |

---

# 18. 12 道困难题不是 12 个孤立技巧

困难题的价值在于把基础模型推到边界。开始刷简单和中等前，不要求你能独立写出全部困难题，但应先知道它们考察的“关键跃迁”。

| 困难题 | 先掌握 | 真正的关键跃迁 | 主解法 |
|---|---|---|---|
| [42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/) | 前后缀最大值、双指针、单调栈 | 当前点只由两侧较矮屏障决定；可提前结算一侧 | 前后缀 `O(n)`；双指针 `O(1)` 空间；单调栈按横层结算 |
| [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) | 滑窗、`deque` | 新且更大的元素同时在值和过期时间上支配旧元素 | 单调队列 `O(n)`；堆懒删除；分块前后缀 |
| [76. 最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/) | Counter、可变窗口 | 合法性由带重复次数的多重集合决定；合法后要收缩到极限 | 频次窗口 `O(m+n)` |
| [41. 缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/) | 数组下标、抽屉原理 | 先证明答案只在 `[1,n+1]`，再把输入数组当哈希空间 | 符号标记或循环置换 `O(n)/O(1)` |
| [25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/) | 反转、哨兵 | 算法不难，难在组边界与重新连接的契约 | 完整组预检 + 半开区间反转 |
| [23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/) | 合并两链、堆、分治 | 让每个节点只经过 `log k` 层选择 | 分治归并或 K 路堆 `O(N log k)` |
| [124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) | 后序、树高 | 返回给父亲的单臂状态与节点处完整答案必须分离 | 树形 DP `O(n)` |
| [51. N 皇后](https://leetcode.cn/problems/n-queens/) | 回溯、集合 | 用列、`r-c`、`r+c` 把冲突检查压成 `O(1)` | 集合回溯；进阶位掩码 |
| [4. 寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) | 二分、归并、第 K 小 | 二分的是可排除数量或切分位置，不是直接找某个值 | 第 K 小消除；较短数组切分 |
| [84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/) | 栈、最近更小元素 | 柱子弹栈那一刻，左右最大延伸边界同时确定 | 单调递增栈 `O(n)` |
| [295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/) | 堆、动态平衡 | 动态维护“较小一半/较大一半”的有序切分 | 双堆：插入 `O(log n)`、查询 `O(1)` |
| [32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/) | 栈、结尾 DP | 不是判断整体合法，而是求每个结尾能向左连接多远 | 结尾 DP、下标栈、正反扫描 |

建议第一次学习困难题时按三层写法推进：

1. 先写朴素解并明确瓶颈；
2. 写一个容易证明的 `O(n)` 或 `O(n log n)` 版本，即使空间不是最优；
3. 最后再做空间压缩或常数优化。

例如接雨水先写左右最大数组，再推双指针；柱状图先分别求左右第一个更矮，再推一遍扫描；两个有序数组中位数先理解第 K 小消除，再挑战切分二分。这样学到的是推导过程，不是神秘模板。

---

# 19. 把 100 题压缩成少数可迁移模型

下面这些跨模块联系比网页标签更值得记忆：

| 同一模型 | 题目联系 | 迁移点 |
|---|---|---|
| 前缀和 + 频次 | 560 和为 K 的子数组 → 437 路径总和 III | 数组中历史前缀全部有效；树中只能保留当前祖先链，离开节点要撤销 |
| Floyd 环入口 | 142 环形链表 II → 287 寻找重复数 | 后者把 `i -> nums[i]` 看成函数图，数组约束保证环入口就是重复值 |
| 合并两个有序序列 | 21 合并两链 → 148 排序链表 → 23 合并 K 链 | 基础 merge 是分治归并和 K 路合并的底层积木 |
| 单调候选结构 | 239 窗口最大值、739 每日温度、84 柱状图、42 接雨水 | 删除一个候选前，必须证明新候选在值与有效期上支配它 |
| BFS 分层 | 102 层序、994 腐烂橘子、45 跳跃游戏 II | 显式队列和区间边界都在表示“相同步数可到达的一层” |
| 返回值与全局答案分离 | 543 直径 → 124 最大路径和 | 返回单臂给父亲，双臂只在当前节点更新完整答案 |
| 前后缀贡献 | 238 除自身乘积、42 接雨水、239 分块解法 | 把“除当前位置外的全局信息”拆为左贡献和右贡献 |
| 原地索引哈希 | 41 缺失正数、75 颜色分类 | 输入数组本身也是可用状态空间，但必须先证明可安全覆盖 |
| 边界二分 | 35 插入位置、34 首尾位置、153 旋转最小值、4 中位数 | 始终围绕单调谓词与答案区间写不变量，而不是背四套 `while` |
| “以当前位置结尾”DP | 53 最大子数组、152 最大乘积、32 有效括号 | 将全局区间问题转成一个可从左向右递推的局部结尾状态 |
| 决策树约束编码 | 22 括号、79 单词、51 皇后 | 越早把不可能前缀剪掉，搜索树越小；撤销必须精确对称 |

看到新题时，不要先问“它像第几题”，而要问：它是否存在同样的状态、单调性、支配关系或递归契约。

---

# 20. 实际刷题流程与复盘格式

## 20.1 每道题的五阶段

1. **复述题意**：用自己的话说明输入、输出、是否连续、是否原地、重复如何处理。
2. **写暴力解**：即使不编码，也要说明枚举对象与复杂度。
3. **寻找重复工作**：查询慢就想哈希；区间重复就想前缀；有序/单调就想双指针或二分；子问题重复就想 DP/记忆化。
4. **先写不变量再编码**：尤其是链表指针、窗口合法性、单调栈、二分区间、DP 状态。
5. **用反例检查**：空、一个元素、全相同、严格升/降、全负、重复最小值、答案在首尾、完全无解。

## 20.2 建议分六个阶段

| 阶段 | 模块 | 目标 |
|---|---|---|
| A | Python、复杂度、哈希、普通数组、矩阵 | 能独立写线性扫描、原地修改、前后缀 |
| B | 双指针、滑窗、前缀和、二分 | 能证明指针为何可移动，熟练处理开闭边界 |
| C | 链表、栈、队列、堆 | 能写哨兵、反转、单调结构、Top K 与双堆 |
| D | 二叉树、图、Trie、回溯 | 每题先写递归契约或图的节点/边/状态 |
| E | 贪心、一维 DP、背包、多维 DP | 能从“最后一步”推状态与遍历顺序 |
| F | 12 道困难题与二刷 | 从朴素法推导优化；一周后盲写关键模板 |

## 20.3 一题一页的复盘模板

```text
题号 / 日期：
我第一眼想到：
暴力解与复杂度：
被重复计算或缓慢查询的部分：
正确模型：
核心变量含义：
循环/递归不变量：
为什么不会漏答案：
时间 / 空间复杂度：
我写错的边界：
最小反例：
7 天后能否盲写：
```

“看懂题解”不等于“会做”。真正掌握的标准是：隔几天不看代码，仍能从约束、暴力瓶颈和不变量重新推导出主体结构。

---

# 21. 官方资料与本地核验说明

本教程以 [LeetCode 热题 100 当前学习计划](https://leetcode.cn/studyplan/top-100-liked/) 为题单来源。核对快照为 2026-08-16：100 题、17 模块、简单 20 / 中等 68 / 困难 12。

本地研究记录：

- [`research/official_plan.json`](research/official_plan.json)：官方题单顺序、编号、标题、难度、标签与链接。
- [`research/audit.json`](research/audit.json)：100 题详情覆盖、标题/编号一致性和 Python 签名完整性校验。
- [`research/extract_official_data.py`](research/extract_official_data.py)：可复核的数据提取与一致性检查脚本。

困难题主要对照的力扣官方题解：

- [42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/solutions/692342/jie-yu-shui-by-leetcode-solution-tuvc/)
- [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/solutions/543426/hua-dong-chuang-kou-zui-da-zhi-by-leetco-ki6m/)
- [76. 最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/solutions/257359/zui-xiao-fu-gai-zi-chuan-by-leetcode-solution/)
- [41. 缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/solutions/304743/que-shi-de-di-yi-ge-zheng-shu-by-leetcode-solution/)
- [25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/solutions/248591/k-ge-yi-zu-fan-zhuan-lian-biao-by-leetcode-solutio/)
- [23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/solutions/219756/he-bing-kge-pai-xu-lian-biao-by-leetcode-solutio-2/)
- [124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/solutions/297005/er-cha-shu-zhong-de-zui-da-lu-jing-he-by-leetcode-/)
- [51. N 皇后](https://leetcode.cn/problems/n-queens/solutions/398929/nhuang-hou-by-leetcode-solution/)
- [4. 寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/solutions/258842/xun-zhao-liang-ge-you-xu-shu-zu-de-zhong-wei-s-114/)
- [84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/solutions/266844/zhu-zhuang-tu-zhong-zui-da-de-ju-xing-by-leetcode-/)
- [295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/solutions/961062/shu-ju-liu-de-zhong-wei-shu-by-leetcode-ktkst/)
- [32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/solutions/314683/zui-chang-you-xiao-gua-hao-by-leetcode-solution/)

题目和要求可能随网站更新而调整。尤其要留意旧资料与当前题面差异：例如第 215 题当前明确要求 `O(n)`，所以经典的 `O(n log k)` 小根堆虽然是有价值的堆练习，却不是严格满足当前要求的最终答案。
