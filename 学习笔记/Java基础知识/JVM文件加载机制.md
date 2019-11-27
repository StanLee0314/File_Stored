# JVM

## 类加载（ClassLoading）

在JAVA代码中，类的加载，连接，初始化过程都是在持续运行期间完成的。

- 加载

	> 查找并加载类的二进制数据

- 连接

	- 验证

		> 确保被加载的类的正确性

	- 准备

		> 为类的静态变量分配内存，并将其初始化为默认值

	- 解析

		> 把类中的符号引用转换为直接引用

- 初始化

	> 为类的静态变量赋予正确的初始值

- 使用

	- Java程序对类的使用方式可分为两种

		- 主动使用

			- 创建类的实例

			- 访问某个类的或者接口的静态变量，或者对该静态变量赋值

			- 调用类的静态方法

			- 通过反射动态加载某个类（Class.forName("xxx.xx")）

			- 初始化一个类的子类

			- Java虚拟机启动时被表明为启动类的类

			- JDK6之前我们会使用java反射来实现动态方法调用，多数框架用反射的比较多，例如mybatis、spring等。在JDK7中，新增了java.lang.invoke.MethodHandle（方法句柄），称之为“现代化反射”。其实反射和java.lang.invoke.MethodHandle都是间接调用方法的途径，但java.lang.invoke.MethodHandle比反射更简洁，用反射功能会写一大堆冗余代码。

				- MethodHandle实例的解析结果REF_getStatic，REF_putStatic，REF_invokeStatic句柄对于的类没有初始化，则初始化。

			- ```java
				public static void main(String[] args) throws Throwable {
						MethodType methodType = MethodType.methodType(String.class,String.class);
						MethodHandle methodHandle = MethodHandles.lookup().findStatic(Test.class, "toString", methodType);
						String result = (String) methodHandle.invokeWithArguments("James");
						System.out.println(result);
						
					}
				```

				

		- 被动使用

			- 通过子类引用父类的静态字段，为子类的被动使用，不会导致子类初始化

				```java
				class Dfather{  
				    static int count = 1;  
				    static{  
				        System.out.println("Initialize class Dfather");  
				    }  
				}  
				  
				class Dson extends Dfather{  
				    static{  
				        System.out.println("Initialize class Dson");  
				    }  
				}  
				  
				public class Test4 {  
				    public static void main(String[] args) {  
				        int x = Dson.count;  
				    }  
				}
				```

			- 通过数组定义类引用类，为类的被动使用，不会触发此类的初始化

			```java
			
			class E{  
			    static{  
			        System.out.println("Initialize class E");  
			    }  
			}  
			  
			public class Test5 {  
			    public static void main(String[] args) {  
			        E[] e = new E[10];  
			    }  
			}
			```

		- 常量在编译阶段会存入调用方法所在的类的常量池中（这个例子存在F类的常量池中），本质上没有直接引用到定义常量的类，因此不会触发定义常量的类的初始化

		```JAVA
		class F{  
		    static final int count = 1;  
		    static{  
		        System.out.println("Initialize class F");  
		    }  
		}  
		  
		public class Test6 {  
		    public static void main(String[] args) {  
		        int x = F.count;  
		    }  
		}
		```

		

	- 所有的Java虚拟机实现必须在每个类或接口被Java程序‘’首次主动使用“时才会初始化他们

	- 被动使用不会初始化类，但是有可能会加载类（JVM规范里没有说明）

		

- 卸载

## 类的加载机制

### **JVM的类加载机制**主要有如下3种

- 全盘负责：所谓全盘负责，就是当一个类加载器负责加载某个Class时，该Class所依赖和引用其他Class也将由该类加载器负责载入，除非显示使用另外一个类加载器来载入。
- 双亲委派：所谓的双亲委派，则是先让父类加载器试图加载该Class，只有在父类加载器无法加载该类时才尝试从自己的类路径中加载该类。通俗的讲，就是某个特定的类加载器在接到加载类的请求时，首先将加载任务委托给父加载器，依次递归，如果父加载器可以完成类加载任务，就成功返回；只有父加载器无法完成此加载任务时，才自己去加载。
- 缓存机制。缓存机制将会保证所有加载过的Class都会被缓存，当程序中需要使用某个Class时，类加载器先从缓存区中搜寻该Class，只有当缓存区中不存在该Class对象时，系统才会读取该类对应的二进制数据，并将其转换成Class对象，存入缓冲区中。这就是为很么修改了Class后，必须重新启动JVM，程序所做的修改才会生效的原因。

> **这里说明一下双亲委派机制：**
>
> ​							根类加载器《------拓展类加载器《------系统类加载器《-------用户类加载器
>
> ```java
>   双亲委派机制，其工作原理的是，如果一个类加载器收到了类加载请求，它并不会自己先去加载，而是把这个请求委托给父类的加载器去执行，如果父类加载器还存在其父类加载器，则进一步向上委托，依次递归，请求最终将到达顶层的启动类加载器，如果父类加载器可以完成类加载任务，就成功返回，倘若父类加载器无法完成此加载任务，子加载器才会尝试自己去加载，这就是双亲委派模式，即每个儿子都很懒，每次有活就丢给父亲去干，直到父亲说这件事我也干不了时，儿子自己才想办法去完成。
>   
>   双亲委派机制的优势：采用双亲委派模式的是好处是Java类随着它的类加载器一起具备了一种带有优先级的层次关系，通过这种层级关可以避免类的重复加载，当父亲已经加载了该类时，就没有必要子ClassLoader再加载一次。其次是考虑到安全因素，java核心api中定义类型不会被随意替换，假设通过网络传递一个名为java.lang.Integer的类，通过双亲委托模式传递到启动类加载器，而启动类加载器在核心Java API发现这个名字的类，发现该类已被加载，并不会重新加载网络传递的过来的java.lang.Integer，而直接返回已加载过的Integer.class，这样便可以防止核心API库被随意篡改。
> ```

## 类是如何被加载的？

### 什么是类的加载机制？

> 将.class中的二进制数据读到内存，然后整理成类的元数据写到方法区；然后根据类的元数据结构在堆内存中创建类的实例对象；
>
>  
>
> 类的加载指的是将类的.class文件中的二进制数据读入到内存中，将其放在运行时数据区的方法区内，然后在堆区创建一个java.lang.Class对象（JVM规范并未说明Class对象位于哪里，HotSport虚拟机将其放在了方法区中），用来封装类在方法区内的类的数据结构。类的加载的最终产品是位于堆区中的Class对象，Class对象封装了类在方法区内的数据结构，并且向Java程序员提供了访问方法区内类的数据结构的接口。

### 类加载过程中做了什么？

> 在加载阶段，虚拟机需要完成以下三件事情：
>
> 1、通过一个类的全限定名来获取其定义的二进制字节流。
>
> 2、将这个字节流所代表的静态存储结构转化为方法区 类的运行时数据结构。
>
> 3、在Java方法区中生成一个代表这个类的java.lang.Class对象，作为对方法区中这些数据的访问入口。
>
> 加载阶段完成后，虚拟机外部的 二进制字节流就按照虚拟机所需的格式存储在方法区之中，而且在Java堆中也创建一个java.lang.Class类的对象，这样便可以通过该对象访问方法区中的这些数据

 

### 加载时机

> 并非是首次使用时加载，JVM允许类加载器预先加载类；
>
> 如果在加载的过程中，遇到了.class文件的缺失或者存在错误，类加载器只会在首次主动使用它们时才会报错，如果一直没有主动使用，则不会报错
>
> 也就是说编译完成后生成字节码文件，如果没有主动使用，那么据不会报错。

### 加载.Class文件的方式

- 从本地加载
- 通过网络下载.Class文件
- 从Zip，Jar等归档文件中加载.Class文件
- 从专有数据库中提取.Class文件
- 将Java源文件动态编译为.Class文件

```properties
-XX:+TraceClassLoading     用于追踪类的加载信息并打印
-XX:+TraceClassUnloading   用于追踪类的卸载信息并打印


-XX:+<option>	表示开启option选项
-XX:-<option>	表示关闭option选项
-XX:<option>=<value>	表示将option选项的值设置为value
```

## 类加载的方式-代码

> 类加载有三种方式：
>
> 1、命令行启动应用时候由JVM初始化加载
>
> 2、通过Class.forName()方法动态加载
>
> 3、通过ClassLoader.loadClass()方法动态加载
>
> **2和3的区别**
>
> Class.forName()：将类的.class文件加载到jvm中之后，还会对类进行解释，执行类中的static块；
>
> ClassLoader.loadClass()：只干一件事情，就是将.class文件加载到jvm中，不会执行static中的内容,只有在newInstance才会去执行static块。

## 类加载器（两种）

### Java虚拟机自带的加载器

- 根类加载器（BootstrapClassLoader)

	> 它用来加载 Java 的核心类，是用原生代码来实现的，并不继承自 java.lang.ClassLoader（负责加载$JAVA_HOME中jre/lib/rt.jar里所有的class，由C++实现，不是ClassLoader子类）。由于引导类加载器涉及到虚拟机本地实现细节，开发者无法直接获取到启动类加载器的引用，所以不允许直接通过引用进行操作。

- 扩展类加载器（ExtensionClassLoader）

	> 它负责加载JRE的扩展目录，lib/ext或者由java.ext.dirs系统属性指定的目录中的JAR包的类。由Java语言实现，父类加载器为null。

- 系统类加载器（SystemClassLoader)

	> 被称为系统（也称为应用）类加载器，它负责在JVM启动时加载来自Java命令的-classpath选项、java.class.path系统属性，或者CLASSPATH换将变量所指定的JAR包和类路径。程序可以通过ClassLoader的静态方法getSystemClassLoader()来获取系统类加载器。如果没有特别指定，则用户自定义的类加载器都以此类加载器作为父加载器。由Java语言实现，父类加载器为ExtClassLoader。

- 类加载器加载Class大致要经过如下8个步骤：

	> 1. 检测此Class是否载入过，即在缓冲区中是否有此Class，如果有直接进入第8步，否则进入第2步。
	> 2. 如果没有父类加载器，则要么Parent是根类加载器，要么本身就是根类加载器，则跳到第4步，如果父类加载器存在，则进入第3步。
	> 3. 请求使用父类加载器去载入目标类，如果载入成功则跳至第8步，否则接着执行第5步。
	> 4. 请求使用根类加载器去载入目标类，如果载入成功则跳至第8步，否则跳至第7步。
	> 5. 当前类加载器尝试寻找Class文件，如果找到则执行第6步，如果找不到则执行第7步。
	> 6. 从文件中载入Class，成功后跳至第8步。
	> 7. 抛出ClassNotFountException异常。
	> 8. 返回对应的java.lang.Class对象。

### 用户自定义类加载器

实现自定义类加载器的三步：

- 1.继承ClassLoader
- 2.重写findClass()方法
- 3.调用defineClass()方法

一个基本的自定义类加载器代码如下：

```java
public class CustomClassLoader extends ClassLoader {

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        try {
            byte[] result = getClassFromCustomPath(name);
            if (result == null) {
                throw new FileNotFoundException(name);
            } else {
                // defineClass方法将字节码转化为类
                return defineClass(name, result, 0, result.length);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        throw new ClassNotFoundException(name);
    }

    private byte[] getClassFromCustomPath(String name) {
        // 从自定义路径中加载指定类，返回类的字节码文件
        InputStream in = null;
        ByteArrayOutputStream out = null;
        String path = "/com/logic/" + name + ".class";
        try {
            in = new FileInputStream(path);
            out = new ByteArrayOutputStream();
            byte[] buffer = new byte[2048];
            int len = 0;
            while ((len = in.read(buffer)) != -1) {
                out.write(buffer, 0, len);
            }
            return out.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                in.close();
                out.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    public static void main(String[] args) {
        CustomClassLoader customClassLoader = new CustomClassLoader();
        try {
            Class<?> clazz = Class.forName("One", true, customClassLoader);
            Object obj = clazz.newInstance();
            // xx.xx.CustomClassLoader@610455d6
            System.out.println(obj.getClass().getClassLoader());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

