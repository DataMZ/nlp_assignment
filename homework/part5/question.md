#### some questions and answers 

##### 1. the reasons of overfitting and underfitting
###### (1) the reasons of overfitting

- 模型过于复杂
- 数据太简单
- 梯度/权重太大
- 参数太多
- 太少正则项

```
  解决：
   1. 调小模型复杂度
   2. 扩大数据集
   3. 增加数据复杂度
   4. 更多正则项
   5. dropout
   6. Batch Norm
   7. Pertub Label 
   8. noise
```

###### (2) the resons of underfitting

- 模型过于简单,无法满足样本复杂性
- 数据太复杂
- 梯度/权重太小
- 参数太少
- 太多正则项

```
  解决：
    1. 增加模型复杂度,以便适应数据特征。
    2. 减少数据
    3. 简化数据
    4. 减少正则化参数
```