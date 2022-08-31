import sys
import pandas as pd


url = sys.argv[1]
df = pd.read_csv(url)

print('Pre-processing file %s' % url)

for a in range(2, len(sys.argv)):
    match sys.argv[a]:
        case '-rcf': # remove correlated features 
            print('-> Searching for correlated features...')
            correlated_features = set()
            for i in range(2, len(df.columns)):
                if df.columns[i] not in correlated_features:
                    print('\t\t[%d de %d]' % (i, len(df.columns)))
                    tmp = df.columns.difference(correlated_features)
                    for j in range(2, len(tmp)):
                        print(df.columns[i] + " - " + tmp[j])
                        if df.columns[i] != tmp[j]:
                            input() 
                            if abs(df.iloc[:, i].corr(df.iloc[:, j])):
                                correlated_features.add(df.columns[i])
                                break
            print('\t->Removing correlated features...')
            print('\t->Removing %d of %d' % (len(correlated_features), len(df.columns)))
            df = df.drop(list(correlated_features), axis = 1)
            print('\t->Correlated features removed.')
                    
        case '-br': # base reduction
            print('-> Converting float64 to float32...')
            df.loc[:, df.dtypes == 'float64'] = df.loc[:, df.dtypes == 'float64'].apply(
                lambda x: x.astype('float32')
            )
            print('-> Bases converted.')
        case '-rc': # remove columns
            print('-> Removing columns manually...')
            a = a + 1
            cols = []
            while '-' in sys.argv[a]:
                cols.append(sys.argv[a])
                print('-> Converting float64 to float32...')
                a = a + 1
            df = df.drop(cols, axis=1)
            print('\t-> Columns removed.')
        case '-tc': # target column
            print('-> Transforming target column...')
            a = a + 1
            df[sys.argv[a]] = df[sys.argv[a]].replace(
                {
                    'tumoral': 1,
                    'normal': 0
                }
            )
            df[sys.argv[a]] = df[sys.argv[a]].astype('int8')
            print('-> Target column transformed...')
        case _:
            print('%s is not recognized.' % sys.argv[a])

print('Saving preprocessed data...')
df.to_csv('output.csv', encoding='utf-8')
print('Preprocessed data saved...')
print('END.')