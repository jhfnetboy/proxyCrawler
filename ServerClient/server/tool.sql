# 清除领取但未完成的任务，重新进入可分配状态,
# 必须在没有采集客户端运行的情况下,运行此sql

update item_url_task set ip = ' ', status = -1 where status = 0 and id<220;

update item_url_task set ip = ' ', status = -1 where ip = '192.168.11.115:1' and id < 220;	

update item_url_task set ip = ' ', status = -1 where ip = '192.168.11.115:1' and status = 0 and id < 220;

# 查重，根据eid，重复的只保留一条

#另外一种排重
ALTER IGNORE TABLE enterprise_raw ADD UNIQUE INDEX(eid);
