"""定义分类器模型的抽象基类

"""
import abc


class Model(abc.ABC):
    """模型的抽象类

    """
    _model = None
    feature_order = None

    @abc.abstractmethod
    def predict(self, x):
        """输入一个特征向量预测

        """
        pass

    @abc.abstractmethod
    def pre_trade(self, x):
        """向量预处理

        """
        pass

    @abc.abstractmethod
    def pre_trade_batch(self, x):
        """全部数据预处理

        """
        pass

    @abc.abstractmethod
    def _train(self, dataset, target, **kwargs):
        """训练一组训练数据

        """
        pass

    def train(self, dataset, target, *, test_size=0.3, random_state=0, **kwargs):
        """训练一组数据

        Parameters:

            dataset (pandas.DataFrame): - 训练用的DataFrame
            target (str): - 标签数据所在的列 
            test_size (float): - 测试集比例
            random_state: - 随机状态


        """
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, precision_score
        y = dataset[target].values
        columns = list(dataset.columns)
        columns.remove(target)
        self.feature_order = columns
        X_matrix = dataset[columns].as_matrix()
        X_matrix = self.pre_trade_batch(X_matrix)
        X_train, X_test, y_train, y_test = train_test_split(
            X_matrix, y, test_size=test_size, random_state=random_state)
        model = self._train(X_train, y_train, **kwargs)
        predictions = model.predict(X_test)
        print(model.score(X_test, y_test))
        print(precision_score(y_test, predictions, average='macro'))
        print(classification_report(y_test, predictions))
        self._model = model
