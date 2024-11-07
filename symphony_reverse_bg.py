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
    path = str(input())
    pass_list = []
    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return
    for path_ in os.listdir:
        if os.path.isfile(path_):
            pass_list.append(path_)
    sorted(pass_list)
    pass_list = [path + '/' + i for i in pass_list]
    numberofdata = len(pass_list)

    print('backgroundはありますか？　y or n：', end='')
    bg_judge = input()
    if bg_judge == 'y':
        print('backgroundファイルのパス：', end='')
        pass_bg = input().strip('"')
        df_bg = pd.read_csv(pass_bg, sep='\t', header=None)
    elif bg_judge != 'n':
        print('正しく入力してください。最初に戻ります!!')
        return


    for i in range(numberofdata):
        df = pd.read_csv(pass_list[i], sep='\t', header=None)

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
        df_reverse.to_csv(pass_list[i][:-4] + '_reversed.txt', index=False, header=False)
        print(i + 1, '番目のデータが保存されました')
    print(f"場所は　{path}　です")

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

if __name__ =='__main__':
    while True:
        print("フォルダ内のファイルを一括で処理したい場合は「d」、一つのファイルだけを処理したい場合は「i」を入力してください")
        mode = input()
        if mode == 'd':
            foldersave()
        elif mode == 'i':
            filesave()
        else:
            print('正しく入力してください。最初に戻ります!!\n')
        time.sleep(1.5)