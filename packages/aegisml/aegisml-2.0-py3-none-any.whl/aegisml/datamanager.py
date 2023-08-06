class KucisDataManager:
    def __setQuantity(self, n, ratio):
        quantity = [math.floor(i*n) for i in ratio]
        remain = n - sum(quantity)
        quantity[0] += remain
        if sum(quantity) != n:
            raise Exception()
        else:
            return quantity

    def setPath(self, path):
        self.path = path + 'kucis_dataset/'
        self.metadata_path = self.path + 'metadata.csv'
    
    def splitDataset(self, ratio, random_seed=777):
        if len(ratio) != 3 or sum(ratio) != 1:
            raise Exception()
        
        metadata = pd.read_csv(self.metadata_path,encoding='latin1')
        random.seed(random_seed)
        total = len(metadata)
        train_list = list()
        valid_list = list()
        test_list  = list()
        malware_lists   = list()
        
        for i in range(9):
            malware_lists.append(list(metadata[metadata.Class == i+1]['Id']))
            random.shuffle(malware_lists[i])
            
        for i, names in enumerate(malware_lists):
            q = self.__setQuantity(len(names), ratio)
            train_list.append(malware_lists[i][:q[0]])
            valid_list.append(malware_lists[i][q[0]:q[0]+q[1]])
            test_list.append(malware_lists[i][q[0]+q[1]:q[0]+q[1]+q[2]])
        
        QTrain = sum([len(i) for i in train_list])
        QValid = sum([len(i) for i in valid_list])
        QTest  = sum([len(i) for i in test_list])
        
        if QTrain + QValid + QTest != total:
            raise Exception()
        
        self.trainDS = KucisDataset('train/', train_list, self.path)
        self.validDS = KucisDataset('valid/', valid_list, self.path)
        self.testDS = KucisDataset('test/', test_list, self.path)
        
        str0 = 'Total:{0}\n'.format(total)
        str1 = 'Proportions of Dataset:{0:5}, {1}, {2}\n'.format(ratio[0], ratio[1], ratio[2])
        str2 = 'Quantity of Trainset :{0:5}, {1}\n'.format(QTrain, [len(i) for i in train_list])
        str3 = 'Quantity of Vaildset :{0:5}, {1}\n'.format(QValid, [len(i) for i in valid_list])
        str4 = 'Quantity of Testset  :{0:5}, {1}'.format(QTest   , [len(i) for i in test_list])
        print(f'{str0}{str1}{str2}{str3}{str4}')
        
    def makeImages(self, method):
        self.trainDS.makeImages(method)
        self.validDS.makeImages(method)
        self.testDS.makeImages(method)
        
    def showImage(self, method):
        if method == 'SO':
            mPath = 'Stream_Order/'
        elif method == 'IC':
            mPath = 'Incremental_Coordinate/'
        path = self.path + random.choice(['test/', 'train/', 'valid/']) + mPath
        os.listdir(path)
        image = np.load(path + random.choice(os.listdir(path)))
        plt.imshow(image, cmap='Greys', interpolation='nearest')
        plt.show()
