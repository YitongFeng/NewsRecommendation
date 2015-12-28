测试集以test开头，训练集以train开头。

1. stopword.txt为停用此表

2. test_body_tf.txt 为测试集新闻正文的词频统计 每一行为一条string 各个词与统计数字以空格分离 与
test_news_ids相对应

3. test_news_body.txt 为测试集新闻正文 每一行为一条新闻正文 与test_news_ids相对应

4. test_news_ids.txt 为测试集新闻id

5. test_news_title.txt 为测试集新闻标题 一行一个标题 与test_news_ids相对应

6. test_title_tf.txt 测试集新闻标题词频统计 每一行为一条string 各个词与统计数字以空格分离 与
test_news_ids相对应

7. test_user_ids 测试集用户id

8. train_body_tf.txt 训练集新闻正文的词频统计 每一行为一条string 各个词与统计数字以空格分离 与train_news_ids相对应

9. train_news_body.txt 训练集新闻正文 每一行为一条新闻正文 与train_news_ids相对应

10. train_news_ids.txt 训练集新闻id

11. train_news_title.txt 训练集新闻标题 一行一个标题 与train_news_ids相对应

12. train_title_tf.txt 训练集新闻标题词频统计 每一行为一条string 各个词与统计数字以空格分离 与train_news_ids相对应

13. train_user_ids 训练集用户id

14. words.txt 不论是测试集还是训练集 新闻标题还是新闻正文 所有出现过的词（已去停词 去重）