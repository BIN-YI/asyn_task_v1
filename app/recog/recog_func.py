#任務的functions/modules，都放在這

#def example1():


def long_count_tasks(s, total):
    total = int(total)
    for i in range(total):
        if i % 10 == 0:
            #到時候就要求辨識那邊程式，用這個來更新狀態
            #我這邊只做結束訊息
            s.update_state(state='PROGRESS',
                              meta={'current': i, 'total': total, 'status': 'working'})
        time.sleep(1)
    #part 1
    # total數量可能是the number of parts in pipeline
    # current則是看目前所在區塊
    #s.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'working'})

    #part 2
    # s.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'working'})

    #...