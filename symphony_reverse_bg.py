import pandas as pd
import os
import time

#backgroundあったら引く
#symphonyの生データのx軸を反転させてラフに合わせる
#ラフに合わせるときのオフセットは経験則なので適宜変更すること
#grating = 150/mm　とする
center_wl = 1200
pixels = 512 #symphonyの横のピクセル数，ちなみに縦は1ピクセルです

def foldersave():
    print('iHR上の中心波長：', end='')
    try:
        center_wl = int(input())
    except:
        print('数字だけを正しく入力してください。最初に戻ります!!')
        return

    print('データが保存されているフォルダのパスを入力してください：')
    path = str(input().strip('"'))
    filename_list = []
    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if 'log' in filename:
                print(f"{filename}はログファイルとして認識されました。処理をスキップします")
                continue
            filename_list.append(filename)
    sorted(filename_list)
    path_list = [os.path.join(path, filename) for filename in filename_list]

    print('backgroundはありますか？　y or n：', end='')
    bg_judge = input()
    if bg_judge == 'y':
        print('backgroundファイルのパス：', end='')
        pass_bg = input().strip('"')
        df_bg = pd.read_csv(pass_bg, sep='\t', header=None)
    elif bg_judge != 'n':
        print('yまたはnを正しく入力してください。最初に戻ります!!')
        return


    for i, filepath in enumerate(path_list):
        df = pd.read_csv(filepath, sep='\t', header=None)

        # backgroundを引く処理
        if bg_judge == 'y':
            df[1] = df[1] - df_bg[1]

        #x軸を反転させる処理
        df_reverse = df.iloc[::-1]

        #x軸にラフな値を代入する処理
        list_wl = []
        # start_wl = center_wl - 319 #319は過去の結果からの概算結果
        start_wl = center_wl - 246  #246は過去の結果からの概算結果
        delta_wl = 509.5 / 511
        for j in range(pixels):
            list_wl.append(start_wl + delta_wl * j)
        df_reverse[0] = list_wl

        #保存
        df_reverse.to_csv(os.path.splitext(filepath)[0] + '_reversed.txt', index=False, header=False)
        print(i + 1, '番目のデータが保存されました')
    print(f"保存場所は　{path}　です")

def filesave():
    print('iHR上の中心波長：', end='')
    try:
        center_wl = int(input())
    except:
        print('数字だけを正しく入力してください。最初に戻ります!!')
        return

    print('データが保存されているファイルのパスを入力してください：')
    path = str(input().strip('"'))
    if (not os.path.exists(path)) or (not os.path.isfile(path)):
        print("ファイルが存在しません。最初に戻ります!!\n")
        return

    print('backgroundはありますか？　y or n：', end='')
    bg_judge = input()
    if bg_judge == 'y':
        print('backgroundファイルのパス：', end='')
        pass_bg = input().strip('"')
        df_bg = pd.read_csv(pass_bg, sep='\t', header=None)
    elif bg_judge != 'n':
        print('正しく入力してください。最初に戻ります!!')
        return


    df = pd.read_csv(path, sep='\t', header=None)

    # backgroundを引く処理
    if bg_judge == 'y':
        df[1] = df[1] - df_bg[1]

    #x軸を反転させる処理
    df_reverse = df.iloc[::-1]

    #x軸にラフな値を代入する処理
    list_wl = []
    # start_wl = center_wl - 319 #319は過去の結果からの概算結果
    start_wl = center_wl - 246  #246は過去の結果からの概算結果
    delta_wl = 509.5 / 511
    for j in range(pixels):
        list_wl.append(start_wl + delta_wl * j)
    df_reverse[0] = list_wl

    #保存
    df_reverse.to_csv(path[:-4] + '_reversed.txt', index=False, header=False)
    print('データが保存されました')
    print(f"場所は　{path[:-4]}_reversed.txt　です")

def scanfoldersave():
    print("ihr320分光器の中心波長を入力してください")
    try:
        center_wl = float(input())
    except Exception as e:
        print(e)
        print("数字を入力してください。最初に戻ります!!\n")
        return
    print("backgroundファイルのパスを入力してください")
    try:
        bg_path = str(input())
        if "\"" in bg_path:
            bg_path = bg_path.strip('"')
        bg_df = pd.read_csv(bg_path, sep='\t', comment='#', header=None)
    except Exception as e:
        print(e)
        print("backgroundファイルが存在しません。最初に戻ります!!\n")
        return
    print('データが保存されているフォルダのパスを入力してください：')
    folder_path = str(input())
    if "\"" in folder_path:
        folder_path = folder_path.strip('"')
    if (not os.path.exists(folder_path)) or (not os.path.isdir(folder_path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return
    folderdict = {}
    for foldername in os.listdir(folder_path):
        if not os.path.isdir(os.path.join(folder_path, foldername)):
            continue
        id = int(foldername.split('_')[0][3:])#_で分けて一番前 → さらに文字列posを飛ばす
        folderdict[id] = foldername

    folderdict = dict(sorted(folderdict.items(), key=lambda x: x[0]))

    for id, foldername in folderdict.items():
        for filename in os.listdir(os.path.join(folder_path, foldername)):
            if filename == '.DS_Store' or filename == 'log.txt' or "reversed.txt" in filename:
                continue
            filepath = os.path.join(folder_path, foldername, filename)
            try:
                df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
            except:
                print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
                continue
            df[1] = df[1] - bg_df[1]
            df_reverse = df.iloc[::-1]
                    #x軸にラフな値を代入する処理
            list_wl = []
            # start_wl = center_wl - 319 #319は過去の結果からの概算結果
            start_wl = center_wl - 246  #246は過去の結果からの概算結果
            delta_wl = 509.5 / 511
            for j in range(512):
                list_wl.append(start_wl + delta_wl * j)
            df_reverse[0] = list_wl
            savepath = os.path.join(folder_path+'_reverse', foldername, filename[:-4] + '_reversed.txt')
            if not os.path.exists(os.path.join(folder_path+'_reverse', foldername)):
                os.makedirs(os.path.join(folder_path+'_reverse', foldername))
            df_reverse.to_csv(savepath, index=False, header=False)
            print(f"{filepath}を処理．{savepath}に保存しました")

def everysave():
    print('iHR上の中心波長：', end='')
    try:
        center_wl = int(input())
    except:
        print('数字だけを正しく入力してください。最初に戻ります!!')
        return

    print('データが保存されているフォルダのパスを入力してください：')
    path = str(input().strip('"'))
    path_list = []
    Datapath_2_Bgpath_dict = {} # データのパスをキーとして対応するバックグランドのパスを値とする辞書

    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if 'log' in filename:
                print(f"{filename}はログファイルとして認識されました。処理をスキップします")
                continue
            if 'background' in filename:
                continue
            if not os.path.exists(os.path.join(path, "background_" + filename)):
                print(f"{filename}に対応するバックグラウンドファイルが存在しません。処理をスキップします")
                continue
            path_list.append(os.path.join(path, filename))
            Datapath_2_Bgpath_dict[os.path.join(path, filename)] = os.path.join(path, "background_" + filename)


    for i, filepath in enumerate(path_list):
        df = pd.read_csv(filepath, sep='\t', header=None)
        df_bg = pd.read_csv(Datapath_2_Bgpath_dict[filepath], sep='\t', header=None)

        # backgroundを引く処理
        df[1] = df[1] - df_bg[1]

        #x軸を反転させる処理
        df_reverse = df.iloc[::-1]

        #x軸にラフな値を代入する処理
        list_wl = []
        # start_wl = center_wl - 319 #319は過去の結果からの概算結果
        start_wl = center_wl - 246  #246は過去の結果からの概算結果
        delta_wl = 509.5 / 511
        for j in range(pixels):
            list_wl.append(start_wl + delta_wl * j)
        df_reverse[0] = list_wl

        #保存
        df_reverse.to_csv(os.path.splitext(filepath)[0] + '_reversed.txt', index=False, header=False)
        print(i + 1, '番目のデータが保存されました')
    print(f"保存場所は　{path}　です")

if __name__ =='__main__':
    while True:
        print("フォルダ内のファイルを一括で処理したい場合は「d」\n" \
        "一つのファイルだけを処理したい場合は「i」\n" \
        "ラインスキャン測定のデータを処理したい場合には「lsd」を入力してください\n" \
        "都度バックグラウンドを引きたい場合は「ev」を入力してください\n" \
        "終了したい場合は「q」を入力してください")
        mode = input()
        if mode == 'd':
            foldersave()
        elif mode == 'i':
            filesave()
        elif mode == 'lsd':
            scanfoldersave()
        elif mode == 'ev':
            everysave()
        elif mode == 'q':
            print('終了します。')
            break
        else:
            print('正しく入力してください。最初に戻ります!!\n')
        time.sleep(1.5)