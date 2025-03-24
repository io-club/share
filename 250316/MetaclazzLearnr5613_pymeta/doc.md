# 使用元类配合 `exec` 在合适处简化代码

## 元类

Python 中几乎一切都是对象。类自身也是对象。

这带来了一些 Python 独有的特性。例如：

- Python 中的类变量对应 Java 中的静态属性。与静态属性不同，类变量是类这一对象自己的实例变量。
- Python 中类无需独立源码即可在程序运行中被动态地创建出来。

通过 `class` 关键字创建的类的类型，`type(cls)` 为 `type`。

Python 中有两个类似构造方法的方法。在实例生成前调用的是 `__new__(cls, *args, **kwargs) -> Self`，生成后调用的是 `__init__(self, *args, **kwargs) -> None`。前者创建实例，后者对已经创建的实例进行初始化。当 `MyClass(params)` 运行时，两者都会被调用。

`type` 中使用 `__new__` 创建新的类对象。在 `type` 外部，可以直接使用 `type(name, bases, dict, **kwds)` 动态创建新的类实例。


| 形参  | 含义           |
|-------|---------------|
| name  | 名            |
| bases | 所有基类     |
| dict  | 属性和方法定义 |

## `eval` 和 `exec`

使用元类还不止，想大量简化代码的一个方法是用 `eval` 和 `exec`。它们都可以以代码块作形参并执行它。其中 `eval` 返回代码块运行后的值。`exec` 运行代码。

使用元类可以创建类的模板。实际生成大量类对象的过程可以交给循环体中的 `exec`。

## 参考资料

> 1. [**Python 文档** - **标准库** - **内置函数** - **type**](https://docs.python.org/zh-cn/3.13/library/functions.html#type)
> 2. [**Python 文档** - **语言参考** - **数据模型** - **自定义类创建**](https://docs.python.org/zh-cn/3.13/reference/datamodel.html#customizing-class-creation)
> 3. [**Python 文档** - **标准库** - **抽象基类**](https://docs.python.org/zh-cn/3.13/library/abc.html#abc.ABCMeta)
