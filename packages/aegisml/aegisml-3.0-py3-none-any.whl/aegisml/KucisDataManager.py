'''
global variables:
root_path
meta_path
trainset
validset
testset

'''

def setQuantity(n, ratio):
    quantity = [math.floor(i*n) for i in ratio]
    remain = n - sum(quantity)
    quantity[0] += remain
    if sum(quantity) != n:
        raise Exception()
    else:
        return quantity

def download():
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.focus_force()
    path = fd.askdirectory()
    root.destroy()
    
    url = 'https://drive.google.com/u/0/uc?id=1-97yHevn9gdJ_9rLoDd_TT6HLcxkOXtn&export=download'
    filename = '/kucis_dataset.7z'
    gdown.download(url, path + filename, quiet=False)
            
def setPath(path):
    global root_path
    global meta_path
    root_path = path + 'kucis_dataset/'
    meta_path = root_path + 'metadata.csv'

def splitDataset(ratio, random_seed = 777):
    if len(ratio) != 3 or sum(ratio) != 1:
        raise Exception()

    global root_path
    global meta_path
    global trainset
    global validset
    global testset
    
    metadata = pd.read_csv(meta_path, encoding='latin1')
    random.seed(random_seed)
    total = len(metadata)
    train_list = list()
    valid_list = list()
    test_list  = list()
    malware_lists = list()
    
    for i in range(9):
        malware_lists.append(list(metadata[metadata.Class == i+1]['Id']))
        random.shuffle(malware_lists[i])
        
    for i, names in enumerate(malware_lists):
        q = setQuantity(len(names), ratio)
        train_list.append(malware_lists[i][:q[0]])
        valid_list.append(malware_lists[i][q[0]:q[0]+q[1]])
        test_list.append(malware_lists[i][q[0]+q[1]:q[0]+q[1]+q[2]])
    
    QTrain = [len(i) for i in train_list]
    QValid = [len(i) for i in valid_list]
    QTest = [len(i) for i in test_list]
    
    if sum(QTrain) + sum(QValid) + sum(QTest) != total:
        raise Exception()
    
    trainset = KucisDataset('train/', train_list, root_path)
    validset = KucisDataset('valid/', valid_list, root_path)
    testset = KucisDataset('test/', test_list, root_path)
    
    str0 = 'Total:{0}\n'.format(total)
    str1 = 'Proportions of Dataset:{0:5}, {1}, {2}\n'.format(ratio[0], ratio[1], ratio[2])
    str2 = 'Quantity of Trainset :{0:5}, {1}\n'.format(sum(QTrain), [len(i) for i in train_list])
    str3 = 'Quantity of Vaildset :{0:5}, {1}\n'.format(sum(QValid), [len(i) for i in valid_list])
    str4 = 'Quantity of Testset  :{0:5}, {1}'.format(sum(QTest), [len(i) for i in test_list])
    print(f'{str0}{str1}{str2}{str3}{str4}')
    
def makeImages(method):
    global trainset
    global validset
    global testset
    trainset.makeImages(method)
    validset.makeImages(method)
    testset.makeImages(method)
    
def showImage(method):
    if method == 'SO':
        mPath = 'Stream_Order/'
    elif method == 'IC':
        mPath = 'Incremental_Coordinate/'
    path = root_path + random.choice(['test/', 'train/', 'valid/']) + mPath
    os.listdir(path)
    image = np.load(path + random.choice(os.listdir(path)))
    plt.imshow(image, cmap='Greys', interpolation='nearest')
    plt.show()

class KucisDataset(Dataset):
    def __init__(self, dsType, malware_lists, path):
        self.dsType = dsType
        self.malware_lists = malware_lists
        self.path = path
        self.images = list()

    def __len__(self):
        return sum([len(i) for i in self.malware_lists])

    def __getitem__(self, idx): 
        return 0
    
    def makeImages(self, method, regulation=2.0, dim=1):
        if method == 'SO':
            self.Stream_Order()
        elif method == 'IC':
            self.Incremental_Coordinate(regulation, dim)
        
    def Stream_Order(self):
        j = ''.join
        s = np.save
        t = torch.tensor
        fl = math.floor
        q = math.sqrt
        dsPath = j([self.path, self.dsType, 'Stream_Order/'])
        lawPath = j([self.path, 'law_data/'])
        
        os.makedirs(dsPath, exist_ok=True)
        fnames = sum(self.malware_lists, [])
        for name in tqdm(fnames):
            with open(j([lawPath, name, '.bytes']), 'rb') as f:
                data = list(f.read())
            length = fl(q(len(data)))
            s(j([dsPath, name]), t(data[:length*length]).reshape(length, length).numpy().astype(dtype='uint8'))
        
    def Incremental_Coordinate(self, regulation, dim):
        j = ''.join
        s = np.save
        Fn = F.normalize
        dsPath = j([self.path, self.dsType, 'Incremental_Coordinate/'])
        lawPath = j([self.path, 'law_data/'])
        
        os.makedirs(dsPath, exist_ok=True)
        fnames = sum(self.malware_lists, [])
        for name in tqdm(fnames):
            with open(j([lawPath, name, '.bytes']), 'rb') as f:
                data = list(f.read())
                
            if len(data)%2:
                data = data[:-1]
            
            imgMap = [[0 for x in range(256)] for y in range(256)]
            
            dataIter = iter(data)
            nextd = dataIter.__next__
            for i in dataIter:
                imgMap[i][nextd()] += 1
            
            s(j([dsPath, name]), Fn(torch.FloatTensor(imgMap), p=regulation, dim=dim).numpy().astype(dtype='uint32'))
