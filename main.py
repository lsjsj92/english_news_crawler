
import cnn_crawler_handler

if __name__ == "__main__":
    crw = cnn_crawler_handler.CNNcrawler()
    search_list = []
    with open(crw.base_dir + '/data/search_list.txt', 'r') as f:
        for line in f:
            search_list.append(line.rstrip('\n'))
            print(search_list)
            # 최대 프로세스는 4개까지
            if len(search_list) == 4:
                crw.start(search_list)
                # 다 끝내고 초기화
                search_list = []
        # 4개가 안 되었을 때 진행. 하나도 없을 땐 진행 X
        if len(search_list) > 0 :
            crw.start(search_list)