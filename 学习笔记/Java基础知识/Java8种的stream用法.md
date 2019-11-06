# <font size =4>Stream：</font>
1.stream本身并不存储数据，数据是存储在对应的collection里，或者在需要的时候才生成的；
2.stream不会修改数据源，总是返回新的stream；
3.stream的操作是懒执行(lazy)的：仅当最终的结果需要的时候才会执行，比如上面的例子中，结果仅需要前3个长度大于7的字符串，那么在找到前3个长度符合要求的字符串后，filter()将停止执行；

Stream 可以<font color =red>并行化</font>操作，迭代器只能命令式地、串行化操作。顾名思义，当使用串行方式去遍历时，每个 item 读完后再读下一个 item。而使用并行去遍历时，数据会被分成多个段，其中每一个都在不同的线程中处理，然后将结果一起输出

```java
        //创建
 Stream<Integer>  integerStream = Stream.of(2,3,4,5,3);
 System.out.println(integerStream.collect(Collectors.toSet()));
        //生成无限的流数据
 Stream<Double> randomInteger = Stream.generate(java.lang.Math::random).limit(10);
 randomInteger.collect(Collectors.toList()).forEach(System.out::println);
 Stream.iterate(1,item ->item +1).limit(10).forEach(System.out::println);
 integerStream.filter(item -> item > 3).forEach(System.out::println);
 ArrayList<String> list = (ArrayList<String>) Stream.of("a", "b", "hello").map(item-> item.toUpperCase())
                .collect(Collectors.toList());
        list.forEach(System.out::println);
 //peek方法生成一个包含原Stream的所有元素的新Stream，
 // 同时会提供一个消费函数（Consumer实例），新Stream每个元素被消费的时候都会执行给定的     消费函数，
 // 并且消费函数优先执行
 Stream.of(1, 2, 3, 4, 5)
                .peek(integer -> System.out.println("accept:" + integer))
                .forEach(System.out::println);

//直接引用stream函数
        FansStatisticsOutput result = new FansStatisticsOutput();
        result.setDetail(days.stream().collect(Collectors.toMap(
                Function.identity(),
                day -> new FansStatisticsDetailOutput())
        ));
//map
  EnumMap<BlogPostType, List<BlogPost>> postsPerType = posts.stream()
                .collect(Collectors.groupingBy(BlogPost::getType,
                () -> new EnumMap<>(BlogPostType.class), toList()));
         /*新增关注人数*/
            List<Member> newlyAddedDetail = data.stream().filter(it -> it.getConcernStatus() == ConcernEnum.CONCERN).collect(Collectors.toList());
         //3.每天新增人数详细信息
            Map<String, List<Member>> newlyAddedMap = newlyAddedDetail.stream().collect(Collectors.groupingBy(obj -> dateToDateStr(obj.getConcernTime())));
```

